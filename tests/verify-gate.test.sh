#!/usr/bin/env bash
# Tests for hooks/verify-gate.sh. Run: bash tests/verify-gate.test.sh
# Each test builds a temporary git repo whose checks.sh passes or fails on the content of a file named `state`.
# Repos, the hook's per-session state and the log of check runs live in a temp folder that is removed on exit.
set -uo pipefail

HOOK="$(cd "$(dirname "$0")/.." && pwd)/hooks/verify-gate.sh"
# An explicit template, because macOS mktemp ignores $TMPDIR, which the Claude Code sandbox points at the only
# writable temp folder. Stop if it fails: every git -C "" below would then act on this repo.
TMP=$(mktemp -d "${TMPDIR:-/tmp}/verify-gate-test.XXXXXX") || { echo "mktemp failed" >&2; exit 1; }
trap 'rm -rf "$TMP"' EXIT

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
assert_empty() {
  [ -z "$out" ] || { fail "expected empty output, got:"; echo "$out"; }
}
assert_exit_0() {
  [ "$code" -eq 0 ] || fail "expected exit 0, got $code"
}
assert_blocks() {
  [ "$(printf '%s' "$out" | jq -r '.decision // empty' 2>/dev/null)" = "block" ] || fail "expected decision block, got: $out"
}
assert_does_not_block() {
  [ "$(printf '%s' "$out" | jq -r '.decision // empty' 2>/dev/null)" != "block" ] || fail "expected no block, got: $out"
}
# assert_runs <n>: checks.sh ran n times in this test.
assert_runs() {
  local n=0
  [ -f "$log" ] && n=$(wc -l <"$log" | tr -d ' ')
  [ "$n" -eq "$1" ] || fail "expected checks.sh to run $1 time(s), ran $n"
}

# Starts with the cd line the verify-setup skill prescribes, so the tests fail if the hook runs the script
# from somewhere its own path does not lead back to the repo root.
CHECKS='#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo run >>"$GATE_TEST_LOG"
if grep -q red state; then echo "FAILED: state is red"; exit 1; fi
echo "all green"'

# new_repo: a repo at $repo whose main branch has checks.sh and a green state, plus a fresh $session and $log.
new_repo() {
  repo=$(mktemp -d "$TMP/repo.XXXXXX") || { echo "mktemp failed" >&2; exit 1; }
  session="test-$(basename "$repo")"
  log="$repo.log"
  git -C "$repo" init -q -b main
  git -C "$repo" config user.email t@example.com
  git -C "$repo" config user.name t
  mkdir -p "$repo/.claude/skills/verify"
  printf '%s\n' "$CHECKS" >"$repo/.claude/skills/verify/checks.sh"
  echo green >"$repo/state"
  git -C "$repo" add -A
  git -C "$repo" commit -q -m init
}

# run_hook <event> [stop_hook_active]: runs the hook for $session in $repo; sets $out and $code.
run_hook() {
  out=$(jq -n --arg s "$session" --arg c "$repo" --arg e "$1" --argjson a "${2:-false}" \
      '{session_id: $s, cwd: $c, hook_event_name: $e, stop_hook_active: $a}' |
    TMPDIR="$TMP" GATE_TEST_LOG="$log" "$BASH" "$HOOK" 2>&1)
  code=$?
}

test_session_start_records_without_running_checks() {
  new_repo
  run_hook SessionStart
  assert_exit_0
  assert_empty
  assert_runs 0
}

test_stop_without_changes_since_start_does_not_run_checks() {
  new_repo
  run_hook SessionStart
  run_hook Stop
  assert_exit_0
  assert_empty
  assert_runs 0
}

test_change_that_passes_is_quiet() {
  new_repo
  run_hook SessionStart
  echo "change" >"$repo/new-file.txt"
  run_hook Stop
  assert_exit_0
  assert_empty
  assert_runs 1
}

test_passing_tree_is_not_checked_twice() {
  new_repo
  run_hook SessionStart
  echo "change" >"$repo/new-file.txt"
  run_hook Stop
  run_hook Stop
  assert_runs 1
}

test_committed_change_is_checked() {
  new_repo
  run_hook SessionStart
  echo "change" >"$repo/new-file.txt"
  git -C "$repo" add -A && git -C "$repo" commit -q -m change
  run_hook Stop
  assert_runs 1
}

test_failing_checks_block_with_their_output() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  assert_exit_0
  assert_blocks
  assert_contains "checks.sh"
  assert_contains "FAILED: state is red"
}

test_second_failure_in_a_row_is_let_through_with_a_warning() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  run_hook Stop true
  assert_exit_0
  assert_does_not_block
  assert_contains "still fail"
}

test_session_start_mid_session_keeps_the_first_record() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook SessionStart
  run_hook Stop
  assert_blocks
}

test_another_hooks_block_does_not_use_up_the_gate() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop true
  assert_blocks
}

test_failure_after_a_let_through_blocks_again() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  run_hook Stop true
  run_hook Stop
  assert_blocks
}

test_files_written_by_passing_checks_do_not_rerun_them() {
  new_repo
  printf '%s\necho out >coverage.out\n' "$CHECKS" >"$repo/.claude/skills/verify/checks.sh"
  git -C "$repo" commit -q -am "checks write a file"
  run_hook SessionStart
  echo change >"$repo/new-file.txt"
  run_hook Stop
  run_hook Stop
  assert_runs 1
}

test_no_temp_copy_is_left_behind() {
  new_repo
  git -C "$repo" rm -q -r .claude
  git -C "$repo" commit -q -m "no checks"
  run_hook SessionStart
  echo change >"$repo/new-file.txt"
  run_hook Stop
  ! ls "$TMP"/claude-verify-gate-"$session".checks.sh >/dev/null 2>&1 || fail "temp copy of checks.sh left in TMPDIR"
}

test_fix_after_a_block_is_quiet() {
  new_repo
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  echo "green, fixed" >"$repo/state"
  run_hook Stop true
  assert_exit_0
  assert_empty
  assert_runs 2
}

test_branch_cannot_weaken_the_base_branch_checks() {
  new_repo
  git -C "$repo" switch -q -c feature
  printf '#!/usr/bin/env bash\necho run >>"$GATE_TEST_LOG"\nexit 0\n' >"$repo/.claude/skills/verify/checks.sh"
  git -C "$repo" commit -q -am "weaken checks"
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  assert_blocks
  assert_contains "FAILED: state is red"
}

test_checks_new_on_this_branch_run_from_the_working_tree() {
  new_repo
  git -C "$repo" rm -q -r .claude
  git -C "$repo" commit -q -m "no checks on main"
  git -C "$repo" switch -q -c feature
  mkdir -p "$repo/.claude/skills/verify"
  printf '%s\n' "$CHECKS" >"$repo/.claude/skills/verify/checks.sh"
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  assert_blocks
}

test_stop_without_a_recorded_start_runs_checks() {
  new_repo
  run_hook Stop
  assert_exit_0
  assert_runs 1
}

test_project_without_checks_is_quiet() {
  new_repo
  git -C "$repo" rm -q -r .claude
  git -C "$repo" commit -q -m "no checks"
  run_hook SessionStart
  echo red >"$repo/state"
  run_hook Stop
  assert_exit_0
  assert_empty
}

test_folder_outside_git_is_quiet() {
  new_repo
  repo=$(mktemp -d "$TMP/plain.XXXXXX")
  run_hook Stop
  assert_exit_0
  assert_empty
}

run_test() {
  current="$1"
  local before=$errors
  "$1"
  if [ "$errors" -eq "$before" ]; then passed=$((passed + 1)); else failed=$((failed + 1)); fi
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  run_test "$t"
done

echo
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
