"""PostToolUse hook (Edit|Write): formats only the edited .md with the vault formatter, then rebuilds the
reading index (INDEX.md and 90_System/index.json) with build_index.py.
Reads the hook JSON on stdin. Only notes inside this vault are touched, and the formatter's own
skip rules apply (config folders, third-party folders marked `.vendored`).
Never blocks: any error exits 0."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "90_System" / "Scripts"
FORMATTER = SCRIPTS / "format_notes.py"
INDEXER = SCRIPTS / "build_index.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


target, in_vault = None, False
try:
    data = json.load(sys.stdin)
    target = Path(data.get("tool_input", {}).get("file_path", "")).resolve()
    if target.suffix == ".md" and target.is_file() and ROOT in target.parents:
        mod = load("fmt", FORMATTER)
        if not mod.SKIP.intersection(target.relative_to(ROOT).parts) and not mod.is_vendored(target, ROOT):
            in_vault = True
            text = target.read_text(encoding="utf-8")
            new = mod.format_text(text)
            if new != text:
                target.write_text(new, encoding="utf-8")
except Exception:  # noqa: BLE001, S110  (a formatting hook must never block an edit)
    pass

try:
    if in_vault and target != ROOT / "INDEX.md":
        load("build_index", INDEXER).update(ROOT)
except Exception:  # noqa: BLE001, S110  (the index never blocks either: check_index.py reports a stale one)
    pass
sys.exit(0)
