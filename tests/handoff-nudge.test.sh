#!/usr/bin/env bash
# Tests for hooks/handoff-nudge.sh. Run: bash tests/handoff-nudge.test.sh
# Transcripts and the once-per-session marker live in a temp folder that is removed on exit.
set -uo pipefail

HOOK="$(cd "$(dirname "$0")/.." && pwd)/hooks/handoff-nudge.sh"
TMP=$(mktemp -d)
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
assert_not_contains() {
  case "$out" in *"$1"*) fail "expected output not to contain: $1" ;; esac
}
assert_empty() {
  [ -z "$out" ] || { fail "expected empty output, got:"; echo "$out"; }
}
assert_exit_0() {
  [ "$code" -eq 0 ] || fail "expected exit 0, got $code"
}

# new_session: a unique $session and a $transcript of 100 bytes.
new_session() {
  session="test-$(basename "$(mktemp -d "$TMP/session.XXXXXX")")"
  transcript="$TMP/$session.jsonl"
  head -c 100 /dev/zero | tr '\0' 'x' >"$transcript"
}

# run_hook <stop_hook_active>: runs the hook with a 10-byte limit; sets $out and $code.
run_hook() {
  out=$(jq -n --arg s "$session" --arg t "$transcript" --argjson a "$1" \
      '{session_id: $s, transcript_path: $t, stop_hook_active: $a}' |
    TMPDIR="$TMP" HANDOFF_NUDGE_BYTES=10 "$BASH" "$HOOK" 2>&1)
  code=$?
}

run_test() {
  current="$1"
  local before=$errors
  "$1"
  if [ "$errors" -eq "$before" ]; then passed=$((passed + 1)); else failed=$((failed + 1)); fi
}

test_long_session_asks_for_the_thread_handoff() {
  new_session
  run_hook false
  assert_exit_0
  [ "$(printf '%s' "$out" | jq -r '.decision')" = "block" ] || fail "expected decision block, got: $out"
  assert_contains "handoff skill"
  assert_contains "the handoff for this thread of work"
  assert_not_contains "docs/handoff.md"
}

test_second_stop_in_same_session_is_quiet() {
  new_session
  run_hook false
  run_hook false
  assert_exit_0
  assert_empty
}

test_stop_hook_active_is_quiet() {
  new_session
  run_hook true
  assert_exit_0
  assert_empty
}

test_short_transcript_is_quiet() {
  new_session
  printf 'x' >"$transcript"
  run_hook false
  assert_exit_0
  assert_empty
}

for t in $(declare -F | awk '{print $3}' | grep '^test_'); do
  run_test "$t"
done

echo
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
