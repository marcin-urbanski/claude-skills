#!/usr/bin/env bash
# pr-done [PR]: clean up locally after a pull request is merged on GitHub.
# Removes the PR branch's worktree, brings the base branch up to date and
# deletes the local branch. Without an argument it uses the current branch's PR.
# It checks everything first and changes nothing when a check fails:
# the PR must be merged, the worktree clean, and the local branch must hold
# nothing beyond what was merged (so squash merges are safe to delete).
# A base branch that cannot be fast-forwarded is left as is, with a warning.
set -euo pipefail

die() { echo "pr-done: $*" >&2; exit 1; }

# worktree_of <branch>: path of the worktree that has <branch> checked out.
worktree_of() {
  git worktree list --porcelain |
    awk -v b="branch refs/heads/$1" '/^worktree /{w=substr($0,10)} $0==b{print w; exit}'
}

has_branch() { git rev-parse -q --verify "refs/heads/$1" >/dev/null; }

info=$(gh pr view ${1:+"$1"} --json number,state,headRefName,headRefOid,baseRefName \
  --jq '[.number, .state, .headRefName, .headRefOid, .baseRefName] | @tsv') ||
  die "could not read the PR from GitHub"
IFS=$'\t' read -r number state head head_oid base <<<"$info"
[ "$state" = MERGED ] || die "PR #$number is $state, not merged; nothing changed."
[ "$head" != "$base" ] || die "PR #$number merges $head into itself; clean up by hand."

main_wt=$(git worktree list --porcelain | awk '/^worktree /{print substr($0,10); exit}')
cd "$main_wt"
git fetch -q --prune origin
# GitHub keeps the PR head after deleting the branch; fetch it so the check below can see it.
git fetch -q origin "refs/pull/$number/head" 2>/dev/null || true

# Checks. Nothing has changed before this block ends.
wt=$(worktree_of "$head")
if [ -n "$wt" ] && [ -n "$(git -C "$wt" status --porcelain)" ]; then
  die "$wt has uncommitted changes; nothing changed."
fi

local_oid=$(git rev-parse -q --verify "refs/heads/$head" || true)
if [ -n "$local_oid" ] && [ "$local_oid" != "$head_oid" ] &&
  ! git merge-base --is-ancestor "$local_oid" "origin/$base" &&
  ! { git cat-file -e "$head_oid^{commit}" 2>/dev/null && git merge-base --is-ancestor "$local_oid" "$head_oid"; }; then
  die "$head has commits not in PR #$number; nothing changed."
fi

base_wt=$(worktree_of "$base")
if [ "$wt" = "$main_wt" ] && [ -n "$base_wt" ]; then
  die "$base is checked out in $base_wt, so $main_wt cannot switch to it; nothing changed."
fi

# Changes.
if [ "$wt" = "$main_wt" ]; then
  git switch -q "$base"
  base_wt=$main_wt
elif [ -n "$wt" ]; then
  git worktree remove "$wt"
  echo "Removed worktree $wt"
fi

if ! has_branch "$base"; then
  git branch -q "$base" "origin/$base"
  echo "Created $base at $(git rev-parse --short "origin/$base")"
elif ! git merge-base --is-ancestor "refs/heads/$base" "origin/$base"; then
  echo "pr-done: $base not updated: it has commits that origin/$base does not have" >&2
elif [ -z "$base_wt" ]; then
  git update-ref "refs/heads/$base" "origin/$base"
  echo "Updated $base to $(git rev-parse --short "origin/$base")"
elif git -C "$base_wt" merge -q --ff-only "origin/$base" 2>/dev/null; then
  echo "Updated $base to $(git rev-parse --short "origin/$base")"
else
  echo "pr-done: $base not updated: git could not fast-forward it in $base_wt (local changes in the way?)" >&2
fi

if [ -n "$local_oid" ]; then
  git branch -q -D "$head"
  echo "Deleted branch $head"
fi
git worktree prune
echo "PR #$number done. Main checkout: $main_wt"
