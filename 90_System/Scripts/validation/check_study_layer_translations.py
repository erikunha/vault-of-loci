"""Every study layer translation has the same keys as study_layer.json.

A translation lives next to it as study_layer.<language>.json. To switch a vault to
another language, copy the translation over study_layer.json. Exits 1 on any file
that cannot be read or whose keys differ.

Usage: python3 -I 90_System/Scripts/validation/check_study_layer_translations.py [vault_root]
"""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
SPECS = ROOT / "90_System" / "Specs"


def problems(specs: Path) -> list[str]:
    base = specs / "study_layer.json"
    try:
        keys = set(json.loads(base.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        return [f"study_layer.json: {error}"]
    found = []
    for path in sorted(specs.glob("study_layer.*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            found.append(f"{path.name}: {error}")
            continue
        if not isinstance(data, dict) or set(data) != keys:
            found.append(f"{path.name}: keys differ from study_layer.json")
    return found


if __name__ == "__main__":
    found = problems(SPECS)
    for item in found:
        print(item)
    print("translation problems:", len(found))
    sys.exit(1 if found else 0)
