"""PostToolUse hook (Edit|Write): formats only the edited .md with the vault formatter.
Reads the hook JSON on stdin. Never blocks: any error exits 0."""
import importlib.util
import json
import sys
from pathlib import Path

FORMATTER = Path(__file__).resolve().parents[2] / "90_System" / "Scripts" / "format_notes.py"
SKIP = {".claude", ".agents", "node_modules", ".obsidian"}

try:
    data = json.load(sys.stdin)
    target = Path(data.get("tool_input", {}).get("file_path", ""))
    if target.suffix == ".md" and target.is_file() and not SKIP.intersection(target.parts):
        spec = importlib.util.spec_from_file_location("fmt", FORMATTER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        text = target.read_text(encoding="utf-8")
        new = mod.format_text(text)
        if new != text:
            target.write_text(new, encoding="utf-8")
except Exception:  # noqa: BLE001, S110  (a formatting hook must never block an edit)
    pass
sys.exit(0)
