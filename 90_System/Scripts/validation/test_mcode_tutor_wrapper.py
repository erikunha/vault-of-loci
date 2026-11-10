"""Test for the agent wrapper: the reply the learner sees must survive the CLI.

The MiniMax CLI produces the reply and then either exits without printing it or keeps running
forever. The reply is on disk in both cases, so the wrapper reads it from the session. These tests
run the wrapper against a CLI that is faked, so the ways of losing the reply can be reproduced on
purpose.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

WRAPPER = Path(__file__).resolve().parents[2] / "Evals" / "mcode-tutor.sh"

# The reply the fake session holds, and the size in bytes the CLI reports when it chooses it.
ANSWER = "THE REAL ANSWER"
PREAMBLE = "WORKING PREAMBLE, not the answer"

FAKE_CLI = """#!/bin/bash
# A stand-in for the MiniMax CLI. MODE decides how the reply is left behind.
set -u
mode="$MODE"
bytes="$ANSWER_BYTES"
diag=""
prev=""
for arg in "$@"; do
  if [ "$prev" = "--diagnostics-dir" ]; then diag="$arg"; fi
  prev="$arg"
done
root="$HOME/.minimax/v2/sessions/2026/11/10"

make_session() {
  local sid="$1" with_message="$2"
  local dir="$root/probe-$RANDOM-$RANDOM"
  mkdir -p "$dir"
  printf '{"sessionId":"%s"}\\n' "$sid" > "$dir/manifest.json"
  if [ "$with_message" = "yes" ]; then
    python3 - "$dir/messages.jsonl" <<'PY'
import json, sys
path = sys.argv[1]
rows = [
    {"message_id": "msg-user", "message": {"role": "user", "content": [{"type": "text", "text": "prompt"}]}},
    {"message_id": "msg-a1", "message": {"role": "assistant", "content": [
        {"type": "thinking", "text": "hmm"}, {"type": "text", "text": "WORKING PREAMBLE, not the answer"}]}},
    {"message_id": "msg-a2", "message": {"role": "assistant", "content": [
        {"type": "thinking", "text": "hmm"}, {"type": "text", "text": "THE REAL ANSWER"}]}},
]
with open(path, "w", encoding="utf-8") as fh:
    for row in rows:
        fh.write(json.dumps(row) + "\\n")
PY
  fi
}

write_progress() {
  local sid="$1"
  printf '{"timestampMs":1,"kind":"execution_started","sessionId":"%s"}\\n' "$sid" > "$diag/progress.jsonl"
  printf '{"timestampMs":2,"kind":"answer_selected","messageId":"u-1","answerBytes":%s,"finishReason":"stop"}\\n' "$bytes" >> "$diag/progress.jsonl"
  printf '{"sessionId":"%s"}\\n' "$sid" > "$diag/execution.json"
}

case "$mode" in
  exit_after_reply)
    sid="probe-exit-$$"
    make_session "$sid" yes
    write_progress "$sid"
    exit 0
    ;;
  hang_after_reply)
    sid="probe-hang-$$"
    make_session "$sid" yes
    write_progress "$sid"
    sleep 300
    ;;
  no_messages)
    sid="probe-none-$$"
    make_session "$sid" no
    write_progress "$sid"
    exit 0
    ;;
  wrong_size)
    sid="probe-wrong-$$"
    make_session "$sid" yes
    write_progress "$sid"
    exit 0
    ;;
  no_event)
    sid="probe-noevent-$$"
    make_session "$sid" yes
    printf '{"timestampMs":1,"kind":"execution_started","sessionId":"%s"}\n' "$sid" > "$diag/progress.jsonl"
    printf '{"sessionId":"%s"}\n' "$sid" > "$diag/execution.json"
    echo "PARTIAL WORKING TEXT, the agent was still writing"
    exit 0
    ;;
  stdout_noise)
    sid="probe-noise-$$"
    make_session "$sid" yes
    write_progress "$sid"
    echo "STREAMED PROGRESS LINE FROM THE CLI"
    exit 0
    ;;
  crash)
    echo "mcode exec failed: simulated crash" >&2
    exit 3
    ;;
esac
"""


def run_wrapper(mode, tmp, answer_bytes=15):
    """Run the wrapper against the fake CLI. Returns (exit code, stdout, stderr, leaked dirs)."""
    home = Path(tmp) / "home"
    bin_dir = Path(tmp) / "bin"
    work = Path(tmp) / "work"
    for path in (home, bin_dir, work):
        path.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / "mcode"
    fake.write_text(FAKE_CLI, encoding="utf-8")
    fake.chmod(0o755)
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["TMPDIR"] = str(work)
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    env["MODE"] = mode
    env["ANSWER_BYTES"] = str(answer_bytes)
    env["MCODE_TUTOR_TIMEOUT"] = "20"
    env["MCODE_TUTOR_GRACE"] = "2"
    env["MCODE_TUTOR_POLL"] = "0.2"
    run = subprocess.run(["bash", str(WRAPPER)], input="prompt here", capture_output=True, text=True, env=env, timeout=60)
    leaked = sorted(p.name for p in work.iterdir() if p.is_dir())
    return run.returncode, run.stdout, run.stderr, leaked


with tempfile.TemporaryDirectory() as tmp:
    # The CLI writes the reply and exits without printing it. The reply is on disk, so it is
    # printed, and the run does not end as a failure.
    code, out, err, leaked = run_wrapper("exit_after_reply", tmp)
    assert code == 0, (code, err)
    assert out.strip() == ANSWER, out
    assert PREAMBLE not in out, out
    # The work directory is removed on exit, so the prompt and the diagnostics do not pile up.
    assert leaked == [], leaked

    # The CLI writes the reply and then keeps running. The reply is printed and the CLI is killed.
    code, out, err, leaked = run_wrapper("hang_after_reply", tmp)
    assert code == 0, (code, err)
    assert out.strip() == ANSWER, out
    assert PREAMBLE not in out, out
    assert leaked == [], leaked

    # The session has no messages file. The wrapper fails without a traceback on the error output.
    code, out, err, leaked = run_wrapper("no_messages", tmp)
    assert code == 1, (code, out)
    assert "Traceback" not in err, err
    assert out.strip() == "", out

    # The CLI crashes without a session. The error is passed on.
    code, out, err, leaked = run_wrapper("crash", tmp)
    assert code == 1, (code, out)
    assert "simulated crash" in err, err
    assert leaked == [], leaked

    # The CLI chose a reply that is not on disk yet, and the size it reports does not match any
    # message. The wrapper must not answer with an earlier message: the learner would read a
    # half-finished reply as the answer.
    code, out, err, leaked = run_wrapper("wrong_size", tmp, answer_bytes=99)
    assert code == 1, (code, out)
    assert PREAMBLE not in out, out
    assert out.strip() == "", out

    # The session holds messages and the CLI chose no answer. The wrapper must print nothing:
    # the last message on disk can be a half-finished text, and the run would score it.
    code, out, err, leaked = run_wrapper("no_event", tmp)
    assert code != 0, (code, out)
    assert out.strip() == "", out
    assert "PARTIAL WORKING TEXT" not in out, out
    assert leaked == [], leaked

    # The CLI prints a line of progress and the reply it chose is on disk. The reply the CLI
    # chose is the answer, and the line of progress is not.
    code, out, err, leaked = run_wrapper("stdout_noise", tmp)
    assert code == 0, (code, err)
    assert out.strip() == ANSWER, out
    assert "STREAMED PROGRESS" not in out, out
    assert leaked == [], leaked

print("mcode-tutor.sh: the reply survives the CLI in every way it can lose it")
