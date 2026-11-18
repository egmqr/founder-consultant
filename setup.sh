#!/usr/bin/env bash
# Install the skill for Claude Code and Codex by linking this folder (a git pull then updates it).
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
PY=""; for c in python3 python; do "$c" -c "" 2>/dev/null && PY="$c" && break; done  # skips the Windows Store stub
[ -n "$PY" ] || { echo "Python 3 not found" >&2; exit 1; }
for dir in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$dir"; link="$dir/founder-consultant"; [ -e "$link" ] && continue
  if [ -n "${WINDIR:-}" ]; then MSYS_NO_PATHCONV=1 cmd /c mklink /J "$(cygpath -w "$link")" "$(cygpath -w "$REPO")" >/dev/null
  else ln -s "$REPO" "$link"; fi
  echo "linked $link"
done
"$PY" "$REPO/scripts/kb.py" selftest
