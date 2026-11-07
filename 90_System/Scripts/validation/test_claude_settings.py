"""The Claude Code settings keep their two guards: secrets are never read, and the learner's own
notes are never edited without asking.

Run: python3 -I 90_System/Scripts/validation/test_claude_settings.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
perms = settings["permissions"]
for rule in ("Read(**/.env)", "Read(**/.env.*)", "Read(./.obsidian/plugins/*/data.json)"):
    assert rule in perms["deny"], f"deny rule missing: {rule}"
LEARNER = ("10_Tracks", "20_Concepts", "50_Review")
for folder in LEARNER:
    assert f"Edit(/{folder}/**)" in perms.get("ask", []), f"ask rule missing for {folder}"
    assert not any(r.startswith(f"Edit(/{folder}") for r in perms.get("allow", [])), f"an allow rule must not open {folder}"
print("ok:", 3 + 2 * len(LEARNER), "checks")
