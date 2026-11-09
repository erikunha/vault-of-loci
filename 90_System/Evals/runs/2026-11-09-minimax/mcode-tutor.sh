#!/bin/bash
# Runs MiniMax Code CLI on the prompt read from stdin and prints the final
# assistant message on stdout. The CLI can exit 70 when its runtime shutdown
# misses the deadline; the answer is still on disk, so read it from there.
set -u
work=$(mktemp -d "${TMPDIR:-/tmp}/mcode-tutor-XXXXXX")
diag="$work/diag"
mkdir -p "$diag"
trap 'rm -rf "$work"' EXIT
mcode exec --input - --output-format text --diagnostics-dir "$diag" >"$work/stdout.txt" 2>"$work/stderr.txt"
if [ -s "$work/stdout.txt" ]; then
  cat "$work/stdout.txt"
  exit 0
fi
if [ -s "$diag/failure-answer.txt" ]; then
  cat "$diag/failure-answer.txt"
  exit 0
fi
cat "$work/stderr.txt" >&2
exit 1
