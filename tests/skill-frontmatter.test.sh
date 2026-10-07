#!/usr/bin/env bash
# Skill descriptions are uploaded to claude.ai, which rejects XML-like tags.
# Fails when any skills/*/SKILL.md has "<" or ">" in its frontmatter description.
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
failed=0
for f in "$root"/skills/*/SKILL.md; do
  line=$(awk '/^---$/ { n++; next } n == 1 && /^description:/ { print; exit }' "$f")
  case "$line" in
    *'<'* | *'>'*)
      echo "FAIL: ${f#"$root"/}: description contains < or >"
      failed=1
      ;;
  esac
done
[ "$failed" -eq 0 ] && echo "all skill descriptions free of < and >"
exit "$failed"
