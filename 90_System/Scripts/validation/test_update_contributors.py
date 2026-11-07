"""Test for update_contributors.py (offline, from a saved API answer)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "update_contributors.py"
API = [
    {"login": "ana", "type": "User", "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4", "html_url": "https://github.com/ana", "contributions": 9},
    {"login": "dependabot[bot]", "type": "Bot", "avatar_url": "https://avatars.githubusercontent.com/in/29110?v=4", "html_url": "https://github.com/apps/dependabot", "contributions": 3},
    {"login": "bo", "type": "User", "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4", "html_url": "https://github.com/bo", "contributions": 1},
]
README = "# T\n\n## Contributors\n\n<!-- contributors:start -->\nold\n<!-- contributors:end -->\n\n## License\n"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "api.json").write_text(json.dumps(API), encoding="utf-8")
    for name in ("README.md", "README.pt-BR.md"):
        (root / name).write_text(README, encoding="utf-8")
    (root / "NOTES.md").write_text("no markers\n", encoding="utf-8")
    args = [sys.executable, "-I", str(SCRIPT), "--root", str(root), "--from-json", str(root / "api.json")]
    subprocess.run(args, check=True, capture_output=True)
    text = (root / "README.md").read_text(encoding="utf-8")
    assert "old" not in text and "## License" in text, "only the block between the markers changes"
    assert 'src="https://avatars.githubusercontent.com/u/1?v=4&s=160"' in text and 'width="80"' in text, text
    assert "dependabot" not in text, "bots are left out"
    assert text.index("ana") < text.index('"bo"' if '"bo"' in text else "bo\""), "order follows the API (most contributions first)"
    assert 'alt="ana"' in text and 'href="https://github.com/bo"' in text, text
    assert (root / "README.pt-BR.md").read_text(encoding="utf-8") == text, "every README with markers is updated"
    first = text
    subprocess.run(args, check=True, capture_output=True)
    assert (root / "README.md").read_text(encoding="utf-8") == first, "a second run changes nothing"
print("ok: 7 checks")
