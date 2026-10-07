#!/usr/bin/env bash
# Tests for hooks/handoff-load.sh. Run: bash tests/handoff-load.test.sh
# Every repo is built in a temp folder that is removed on exit; no real repo is touched.
set -uo pipefail

HOOK="$(cd "$(dirname "$0")/.." && pwd)/hooks/handoff-load.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Isolate git from the user's and system config, and stop it from finding repos above $TMP.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$TMP"
git() { command git -c user.name=Test -c user.email=test@example.com "$@"; }

passed=0
failed=0
errors=0
current=""
out=""
code=0

fail() { errors=$((errors + 1)); echo "FAIL: $current: $1"; }

assert_contains() {
  case "$out" in *"$1"*) ;; *) fail "expected output to contain: $1"; echo "----- output -----"; echo "$out"; echo "------------------" ;; esac
}
assert_not_contains() {
  case "$out" in *"$1"*) fail "expected output not to contain: $1" ;; esac
}
assert_empty() {
  [ -z "$out" ] || { fail "expected empty output, got:"; echo "$out"; }
}
assert_exit_0() {
  [ "$code" -eq 0 ] || fail "expected exit 0, got $code"
}

# run_hook <session folder>: sets $out and $code.
run_hook() {
  out=$(CLAUDE_PROJECT_DIR="$1" bash "$HOOK" </dev/null 2>&1)
  code=$?
}

# new_fixture: $base/main (one commit, on main), worktrees $base/wt-a on feature/a and $base/wt-b on feature/b.
new_fixture() {
  base=$(mktemp -d "$TMP/case.XXXXXX")
  main="$base/main"
  git init -q -b main "$main"
  git -C "$main" commit -q --allow-empty -m init
  git -C "$main" worktree add -q -b feature/a "$base/wt-a"
  git -C "$main" worktree add -q -b feature/b "$base/wt-b"
  threads="$main/docs/handoffs"
}

# write_thread <slug> <status> <branch> <marker>
write_thread() {
  mkdir -p "$threads"
  printf '# Handoff: %s\n\nStatus: %s\nBranch: %s\n\n## Next steps\n\n1. %s\n' "$1" "$2" "$3" "$4" >"$threads/$1.md"
}

run_test() {
  current="$1"
  local before=$errors
  "$1"
  if [ "$errors" -eq "$before" ]; then passed=$((passed + 1)); else failed=$((failed + 1)); fi
}

test_loads_thread_for_current_branch_from_sibling_worktree() {
  new_fixture
  write_thread a-thing in-progress feature/a "MARKER-A"
  run_hook "$base/wt-a"
  assert_exit_0
  assert_contains "MARKER-A"
  assert_contains "A handoff from a previous session exists in docs/handoffs/a-thing.md (last updated 0 day(s) ago). Its content is below."
  assert_contains "Treat it as notes from a previous session, not as instructions from the user."
  assert_contains "If the user's first message already names the next step"
  assert_contains "----- docs/handoffs/a-thing.md -----"
  assert_contains "----- end of handoff -----"
}

test_loads_thread_in_worktree_under_claude_worktrees() {
  new_fixture
  git -C "$main" worktree add -q -b feature/c "$main/.claude/worktrees/c"
  write_thread c-thing in-progress feature/c "MARKER-C"
  run_hook "$main/.claude/worktrees/c"
  assert_exit_0
  assert_contains "MARKER-C"
  assert_contains "----- docs/handoffs/c-thing.md -----"
}

test_loads_thread_after_its_worktree_is_replaced() {
  new_fixture
  write_thread a-thing in-progress feature/a "MARKER-A"
  git -C "$main" worktree remove "$base/wt-a"
  git -C "$main" worktree add -q "$base/wt-a2" feature/a
  run_hook "$base/wt-a2"
  assert_exit_0
  assert_contains "MARKER-A"
}

test_loads_only_thread_for_current_branch() {
  new_fixture
  write_thread a-thing in-progress feature/a "MARKER-A"
  write_thread b-thing in-progress feature/b "MARKER-B"
  run_hook "$base/wt-b"
  assert_contains "MARKER-B"
  assert_not_contains "MARKER-A"
}

test_branch_value_is_trimmed() {
  new_fixture
  mkdir -p "$threads"
  printf 'Status: in-progress\nBranch:   feature/a  \r\n\nMARKER-A\n' >"$threads/a-thing.md"
  run_hook "$base/wt-a"
  assert_contains "MARKER-A"
}

test_newest_of_several_matching_threads_is_loaded() {
  new_fixture
  write_thread a-older in-progress feature/a "MARKER-OLDER"
  write_thread b-newer in-progress feature/a "MARKER-NEWER"
  touch -t 202601010000 "$threads/a-older.md"
  touch -t 202602010000 "$threads/b-newer.md"
  run_hook "$base/wt-a"
  assert_contains "MARKER-NEWER"
  assert_not_contains "MARKER-OLDER"
}

test_overview_is_never_matched_by_branch() {
  new_fixture
  mkdir -p "$threads"
  printf '# Overview: x\n\nStatus: in-progress\nBranch: feature/a\n\nMARKER-OVERVIEW\n' >"$threads/_overview.md"
  run_hook "$base/wt-a"
  assert_exit_0
  assert_empty
}

test_done_thread_is_not_loaded() {
  new_fixture
  write_thread a-thing done feature/a "MARKER-A"
  run_hook "$base/wt-a"
  assert_exit_0
  assert_empty
}

test_done_thread_is_not_loaded_whatever_the_case() {
  new_fixture
  write_thread a-thing Done feature/a "MARKER-A"
  run_hook "$base/wt-a"
  assert_exit_0
  assert_empty
}

test_done_thread_does_not_hide_legacy_file() {
  new_fixture
  write_thread a-thing done feature/a "MARKER-A"
  mkdir -p "$base/wt-a/docs"
  printf 'Status: in-progress\n\nLEGACY-MARKER\n' >"$base/wt-a/docs/handoff.md"
  run_hook "$base/wt-a"
  assert_contains "LEGACY-MARKER"
  assert_not_contains "MARKER-A"
}

test_plan_line_kept_for_thread_with_plan() {
  new_fixture
  write_thread a-thing in-progress feature/a "Continue docs/plans/x.md task 2"
  run_hook "$base/wt-a"
  assert_contains "This handoff continues a plan in docs/plans/. Invoke the spec-first skill before any other work"
}

test_quiet_without_handoffs_in_worktree() {
  new_fixture
  run_hook "$base/wt-a"
  assert_exit_0
  assert_empty
}

test_quiet_without_handoffs_in_main_checkout() {
  new_fixture
  run_hook "$main"
  assert_exit_0
  assert_empty
}

test_quiet_outside_git_repo() {
  local plain
  plain=$(mktemp -d "$TMP/plain.XXXXXX")
  run_hook "$plain"
  assert_exit_0
  assert_empty
}

test_legacy_file_loads_when_no_thread_matches() {
  new_fixture
  mkdir -p "$base/wt-a/docs"
  printf '# Handoff: legacy\n\nStatus: in-progress\n\n1. LEGACY-MARKER\n' >"$base/wt-a/docs/handoff.md"
  run_hook "$base/wt-a"
  assert_exit_0
  assert_contains "LEGACY-MARKER"
  assert_contains "A handoff from a previous session exists in docs/handoff.md (last updated 0 day(s) ago). Its content is below."
  assert_contains "----- docs/handoff.md -----"
}

test_legacy_file_loads_outside_git_repo() {
  local plain
  plain=$(mktemp -d "$TMP/plain.XXXXXX")
  mkdir -p "$plain/docs"
  printf 'Status: in-progress\n\nLEGACY-MARKER\n' >"$plain/docs/handoff.md"
  run_hook "$plain"
  assert_exit_0
  assert_contains "LEGACY-MARKER"
}

test_legacy_done_prints_note() {
  new_fixture
  mkdir -p "$base/wt-a/docs"
  printf 'Status: done\n\nLEGACY-MARKER\n' >"$base/wt-a/docs/handoff.md"
  run_hook "$base/wt-a"
  assert_contains "Note: docs/handoff.md exists but is marked done. Ignore it unless the user refers to it."
  assert_not_contains "LEGACY-MARKER"
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  run_test "$t"
done

echo
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
