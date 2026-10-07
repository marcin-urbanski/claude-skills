#!/usr/bin/env bash
# Skill frontmatter checks, run before uploading a skill to claude.ai or linking it into ~/.claude/skills.
# Fails when a skills/*/SKILL.md description has "<" or ">" (claude.ai rejects XML-like tags),
# is longer than 1024 characters (Claude Code's limit), or when its name differs from the folder.
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
failed=0
for f in "$root"/skills/*/SKILL.md; do
  rel=${f#"$root"/}
  folder=$(basename "$(dirname "$f")")
  description=$(awk '/^---$/ { n++; next } n == 1 && /^description:/ { sub(/^description:[[:space:]]*/, ""); print; exit }' "$f")
  name=$(awk '/^---$/ { n++; next } n == 1 && /^name:/ { sub(/^name:[[:space:]]*/, ""); gsub(/^["'"'"']|["'"'"']$/, ""); print; exit }' "$f")
  case "$description" in
    *'<'* | *'>'*)
      echo "FAIL: $rel: description contains < or >"
      failed=1
      ;;
  esac
  if [ "${#description}" -gt 1024 ]; then
    echo "FAIL: $rel: description is ${#description} characters, limit 1024"
    failed=1
  fi
  if [ "$name" != "$folder" ]; then
    echo "FAIL: $rel: name '$name' differs from folder '$folder'"
    failed=1
  fi
done
[ "$failed" -eq 0 ] && echo "all skill descriptions free of < and >, within 1024 characters, names match folders"
exit "$failed"
