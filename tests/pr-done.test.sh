#!/usr/bin/env bash
# Tests for scripts/pr-done.sh. Run: bash tests/pr-done.test.sh
# Each test builds a throwaway remote and clone in a temp folder, and a stub `gh`
# that answers `gh pr view` with $FAKE_PR. Everything is removed on exit.
set -uo pipefail

SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/scripts/pr-done.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

export HOME="$TMP" GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com

mkdir -p "$TMP/bin"
cat >"$TMP/bin/gh" <<'EOF'
#!/usr/bin/env bash
echo "$*" >>"$GH_LOG"
[ -n "$FAKE_PR" ] || { echo "gh: no PR" >&2; exit 1; }
printf '%s\n' "$FAKE_PR"
EOF
chmod +x "$TMP/bin/gh"
export PATH="$TMP/bin:$PATH"

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
assert_exit_0() { [ "$code" -eq 0 ] || { fail "expected exit 0, got $code"; echo "$out"; }; }
assert_exit_nonzero() { [ "$code" -ne 0 ] || fail "expected a non-zero exit"; }
branch_exists() { git -C "$repo" show-ref --verify --quiet "refs/heads/$1"; }
assert_branch_gone() { branch_exists "$1" && fail "expected branch $1 to be deleted"; }
assert_branch_kept() { branch_exists "$1" || fail "expected branch $1 to be kept"; }
remember_main() { main_before=$(git -C "$repo" rev-parse main); }
assert_main_unchanged() {
  [ "$(git -C "$repo" rev-parse main)" = "$main_before" ] || fail "expected local main to be left as it was"
}
assert_main_up_to_date() {
  [ "$(git -C "$repo" rev-parse main)" = "$(git -C "$repo" rev-parse origin/main)" ] ||
    fail "expected local main to match origin/main"
}

# new_repo: a bare $remote and a clone $repo with one commit on main, and a
# pushed branch `feature/x` with one commit that is not on main yet.
new_repo() {
  local dir
  dir=$(mktemp -d "$TMP/case.XXXXXX")
  remote="$dir/remote.git"
  repo="$dir/repo"
  export GH_LOG="$dir/gh.log"
  git init -q --bare -b main "$remote"
  git clone -q "$remote" "$repo" 2>/dev/null
  git -C "$repo" commit -q --allow-empty -m init
  git -C "$repo" push -q origin main
  git -C "$repo" switch -q -c feature/x
  echo x >"$repo/x.txt"
  git -C "$repo" add x.txt
  git -C "$repo" commit -q -m "add x"
  git -C "$repo" push -q -u origin feature/x 2>/dev/null
}

# squash_merge_on_remote: lands feature/x on the remote's main as one squash
# commit, the way GitHub does, without touching $repo.
squash_merge_on_remote() {
  local other="$repo-merger"
  git clone -q "$remote" "$other" 2>/dev/null
  git -C "$other" merge -q --squash origin/feature/x >/dev/null
  git -C "$other" commit -q -m "add x (#7)"
  git -C "$other" push -q origin main
}

# fake_pr <state>: the PR for feature/x, with the head commit the remote has.
fake_pr() {
  export FAKE_PR
  FAKE_PR=$(printf '7\t%s\tfeature/x\t%s\tmain' "$1" "$(git -C "$remote" rev-parse feature/x)")
}

# run_script <dir> [args]: runs pr-done from <dir>; sets $out and $code.
run_script() {
  local dir=$1
  shift
  out=$(cd "$dir" && "$BASH" "$SCRIPT" "$@" 2>&1)
  code=$?
}

run_test() {
  current="$1"
  local before=$errors
  "$1"
  if [ "$errors" -eq "$before" ]; then passed=$((passed + 1)); else failed=$((failed + 1)); fi
}

test_open_pr_changes_nothing() {
  new_repo
  remember_main
  fake_pr OPEN
  run_script "$repo"
  assert_exit_nonzero
  assert_contains "not merged"
  assert_branch_kept feature/x
  assert_main_unchanged
  [ "$(git -C "$repo" branch --show-current)" = "feature/x" ] || fail "expected to stay on feature/x"
}

test_gh_failure_changes_nothing() {
  new_repo
  export FAKE_PR=""
  run_script "$repo"
  assert_exit_nonzero
  assert_contains "could not read the PR"
  assert_branch_kept feature/x
}

test_squash_merged_branch_checked_out_in_main_checkout() {
  new_repo
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  [ "$(git -C "$repo" branch --show-current)" = "main" ] || fail "expected to end on main"
  assert_main_up_to_date
  assert_branch_gone feature/x
  [ -f "$repo/x.txt" ] || fail "expected main to contain the merged change"
}

test_clean_worktree_is_removed_when_run_from_inside_it() {
  new_repo
  git -C "$repo" switch -q main
  git -C "$repo" worktree add -q "$repo-wt" feature/x
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo-wt"
  assert_exit_0
  [ -d "$repo-wt" ] && fail "expected the worktree to be removed"
  assert_branch_gone feature/x
  assert_main_up_to_date
}

test_dirty_worktree_is_kept() {
  new_repo
  git -C "$repo" switch -q main
  git -C "$repo" worktree add -q "$repo-wt" feature/x
  echo wip >"$repo-wt/wip.txt"
  remember_main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_nonzero
  assert_contains "uncommitted"
  [ -f "$repo-wt/wip.txt" ] || fail "expected the dirty worktree to be kept"
  assert_branch_kept feature/x
  assert_main_unchanged
}

test_local_commits_beyond_the_pr_keep_the_branch() {
  new_repo
  remember_main
  squash_merge_on_remote
  fake_pr MERGED
  git -C "$repo" commit -q --allow-empty -m "local only"
  run_script "$repo"
  assert_exit_nonzero
  assert_contains "not in PR #7"
  assert_branch_kept feature/x
  assert_main_unchanged
  [ "$(git -C "$repo" branch --show-current)" = "feature/x" ] || fail "expected to stay on feature/x"
}

test_local_commits_in_a_worktree_keep_the_worktree() {
  new_repo
  git -C "$repo" switch -q main
  git -C "$repo" worktree add -q "$repo-wt" feature/x
  git -C "$repo-wt" commit -q --allow-empty -m "local only"
  remember_main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_nonzero
  [ -d "$repo-wt" ] || fail "expected the worktree to be kept"
  assert_branch_kept feature/x
  assert_main_unchanged
}

test_local_branch_behind_the_pr_head_is_deleted() {
  new_repo
  local other="$repo-pusher"
  git clone -q "$remote" "$other" 2>/dev/null
  git -C "$other" switch -q feature/x
  git -C "$other" commit -q --allow-empty -m "pushed from elsewhere"
  git -C "$other" push -q origin feature/x
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  assert_branch_gone feature/x
  assert_main_up_to_date
}

test_missing_local_base_is_created() {
  new_repo
  git -C "$repo" switch -q -c feature/other main
  git -C "$repo" branch -q -D main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  assert_main_up_to_date
  assert_branch_gone feature/x
}

test_base_with_local_commits_is_left_as_is_and_the_rest_is_done() {
  new_repo
  git -C "$repo" switch -q main
  git -C "$repo" worktree add -q "$repo-wt" feature/x
  git -C "$repo" commit -q --allow-empty -m "local main commit"
  remember_main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  assert_contains "main not updated"
  assert_main_unchanged
  [ -d "$repo-wt" ] && fail "expected the worktree to be removed"
  assert_branch_gone feature/x
}

test_base_that_cannot_fast_forward_over_local_files_is_left_as_is() {
  new_repo
  git -C "$repo" switch -q main
  git -C "$repo" worktree add -q "$repo-wt" feature/x
  echo mine >"$repo/x.txt"
  remember_main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  assert_contains "main not updated"
  assert_main_unchanged
  [ "$(cat "$repo/x.txt")" = "mine" ] || fail "expected the local x.txt to be kept"
  assert_branch_gone feature/x
}

test_pr_from_a_branch_named_like_the_base_is_refused() {
  new_repo
  git -C "$repo" switch -q main
  remember_main
  export FAKE_PR
  FAKE_PR=$(printf '7\tMERGED\tmain\t%s\tmain' "$(git -C "$repo" rev-parse main)")
  run_script "$repo"
  assert_exit_nonzero
  assert_branch_kept main
  assert_main_unchanged
}

test_main_checkout_on_another_branch_still_updates_main() {
  new_repo
  git -C "$repo" switch -q -c feature/other main
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo"
  assert_exit_0
  [ "$(git -C "$repo" branch --show-current)" = "feature/other" ] || fail "expected to stay on feature/other"
  assert_main_up_to_date
  assert_branch_gone feature/x
}

test_pr_number_argument_is_passed_to_gh() {
  new_repo
  squash_merge_on_remote
  fake_pr MERGED
  run_script "$repo" 7
  assert_exit_0
  grep -q '^pr view 7 ' "$GH_LOG" || fail "expected gh to be asked about PR 7, got: $(cat "$GH_LOG")"
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  run_test "$t"
done

echo
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
