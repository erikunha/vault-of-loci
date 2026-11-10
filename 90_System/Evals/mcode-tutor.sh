#!/bin/bash
# Runs MiniMax Code CLI on the prompt read from stdin and prints the final
# assistant message on stdout.
#
# The CLI has two ways of losing the answer on exit. Its runtime shutdown can
# miss the deadline and it exits 70 with nothing on stdout, and it can also
# keep running long after the reply is already produced, so the caller only
# sees a timeout and throws the answer away. In both cases the reply is on
# disk: the diagnostics directory holds the session id, and the session
# directory holds the messages.
#
# So: run the CLI in the background, watch the session for the answer, and
# print it as soon as it is there. The CLI is killed when the answer is found
# or when the deadline passes, whichever comes first.
#
# The reply is tied to the "answer_selected" event the CLI writes, and not to
# the last message on disk. The agent writes text while it works, so the last
# message can be a half-finished one. The event carries the size in bytes of
# the reply the CLI chose, which identifies it exactly. A session that holds
# messages and no event names no answer, and the wrapper prints nothing rather
# than print a message that nobody chose.
#
# The deadline comes from MCODE_TUTOR_TIMEOUT, in seconds. It defaults to 600.
# The runner sets it to its own timeout, so the reply is not cut inside the
# wrapper while the run records a timeout that was never in effect.
set -u
work=$(mktemp -d "${TMPDIR:-/tmp}/mcode-tutor-XXXXXX")
diag="$work/diag"
mkdir -p "$diag"
trap 'rm -rf "$work"' EXIT
cat > "$work/prompt.txt"
deadline=${MCODE_TUTOR_TIMEOUT:-600}
# Seconds to keep looking after the CLI is gone, so a reply that lands on disk
# just after the exit is not thrown away.
grace=${MCODE_TUTOR_GRACE:-10}
# Seconds between polls of the session.
poll=${MCODE_TUTOR_POLL:-2}

# The reply the CLI chose, read from the session it wrote.
#
# Exit codes: 0 the reply was printed, 1 there is no session yet, 2 the CLI
# chose an answer but the reply is not on disk yet, 3 the session holds
# messages and the CLI chose no answer.
read_reply() {
  python3 - "$diag" "$work/session_dir" <<'PY'
import json, sys
from pathlib import Path

diag = Path(sys.argv[1])
cache = Path(sys.argv[2])


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# The session id the CLI wrote when it started.
execution = load_json(diag / "execution.json")
session_id = execution.get("sessionId") or "" if isinstance(execution, dict) else ""
if not session_id:
    sys.exit(1)

# The session directory. It is resolved once and then cached, because scanning
# every manifest in the sessions tree takes close to a second.
session_dir = ""
if cache.exists():
    session_dir = cache.read_text(encoding="utf-8").strip()
if not session_dir:
    root = Path.home() / ".minimax" / "v2" / "sessions"
    for manifest in root.rglob("manifest.json"):
        try:
            if json.loads(manifest.read_text(encoding="utf-8")).get("sessionId") == session_id:
                session_dir = str(manifest.parent)
                break
        except (OSError, ValueError):
            continue
    if not session_dir:
        sys.exit(1)
    cache.write_text(session_dir, encoding="utf-8")

# The size in bytes of the reply the CLI chose.
answer_bytes = None
try:
    progress = (diag / "progress.jsonl").read_text(encoding="utf-8")
except OSError:
    progress = ""
for line in progress.splitlines():
    if '"answer_selected"' not in line:
        continue
    try:
        record = json.loads(line)
    except ValueError:
        continue
    if record.get("kind") == "answer_selected":
        answer_bytes = record.get("answerBytes")

# The assistant messages with text, in the order the session wrote them.
try:
    lines = (Path(session_dir) / "messages.jsonl").read_text(encoding="utf-8").splitlines()
except OSError:
    sys.exit(1)
texts = []
for line in lines:
    if not line.strip():
        continue
    try:
        record = json.loads(line)
    except ValueError:
        continue
    message = record.get("message") or {}
    if message.get("role") != "assistant":
        continue
    content = message.get("content")
    if not isinstance(content, list):
        continue
    text = "".join(part.get("text", "") for part in content if part.get("type") == "text")
    if text.strip():
        texts.append(text)

if answer_bytes is not None:
    chosen = [text for text in texts if len(text.encode("utf-8")) == answer_bytes]
    if chosen:
        print(chosen[-1])
        sys.exit(0)
    # The CLI chose a reply that is not on disk yet. Waiting is the right move:
    # answering with an earlier message would answer with the wrong text.
    sys.exit(2)
if texts:
    # The session holds messages and the CLI chose no answer. Answering with the last of
    # them would answer with a half-finished text, so nothing is printed.
    sys.exit(3)
sys.exit(1)
PY
}

mcode exec --input - --output-format text --diagnostics-dir "$diag" \
  < "$work/prompt.txt" >"$work/stdout.txt" 2>"$work/stderr.txt" &
pid=$!

answer=""
status=1
start=$SECONDS
exited_at=""
while [ $((SECONDS - start)) -lt "$deadline" ]; do
  # The reply the CLI chose is read before what the CLI printed, because the CLI can
  # print a line of progress before the answer, and the run would score that line.
  answer=$(read_reply)
  status=$?
  case $status in
    0) break ;;
    2) ;;  # the reply is chosen but not written yet, keep waiting
  esac

  if [ -s "$diag/failure-answer.txt" ]; then
    answer=$(cat "$diag/failure-answer.txt")
    break
  fi

  if ! kill -0 "$pid" 2>/dev/null; then
    if [ -z "$exited_at" ]; then
      exited_at=$SECONDS
    fi
    if [ $((SECONDS - exited_at)) -ge "$grace" ]; then
      # The CLI is gone and left no session of its own, so what it printed is the answer.
      # A session that holds messages is not this case: there the CLI chose no answer.
      if [ "$status" = "1" ] && [ -s "$work/stdout.txt" ]; then
        answer=$(cat "$work/stdout.txt")
      fi
      break
    fi
  fi
  sleep "$poll"
done

# The CLI is still running in the normal case. It already produced the answer,
# so it is not needed any more. It ignores SIGTERM, so it is killed outright,
# and there is no wait: the process can keep its own children alive for a
# while, and waiting for it would hold the answer back.
pkill -9 -P "$pid" 2>/dev/null
kill -9 "$pid" 2>/dev/null

if [ -n "$answer" ]; then
  printf '%s\n' "$answer"
  exit 0
fi
cat "$work/stderr.txt" >&2
exit 1
