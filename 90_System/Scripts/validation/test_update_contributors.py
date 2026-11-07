"""Test for update_contributors.py (offline: a saved API answer and a fake user lookup)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "update_contributors.py"
START = "<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->"
END = "<!-- ALL-CONTRIBUTORS-LIST:END -->"
API = [
    {"login": "ana", "type": "User", "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4", "html_url": "https://github.com/ana"},
    {"login": "dependabot[bot]", "type": "Bot", "avatar_url": "https://x/bot", "html_url": "https://github.com/apps/dependabot"},
    {"login": "bo", "type": "User", "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4", "html_url": "https://github.com/bo"},
]
USERS = {"ana": {"name": "Ana Lima", "blog": ""}, "bo": {"name": None, "blog": "https://bo.dev"}}
RC = {"projectName": "vault-of-loci", "projectOwner": "erikunha", "imageSize": 100, "contributorsPerLine": 7,
      "files": ["README.md", "README.pt-BR.md"],
      "contributors": [{"login": "cy", "name": "Cy", "avatar_url": "https://avatars.githubusercontent.com/u/3?v=4",
                        "profile": "https://github.com/cy", "contributions": ["content", "translation"]},
                       {"login": "ana", "name": "Ana Lima", "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
                        "profile": "https://github.com/ana", "contributions": ["doc"]}]}
README = f"# T\n\n## Contributors\n\n{START}\nold\n{END}\n\n## License\n"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "api.json").write_text(json.dumps(API), encoding="utf-8")
    (root / "users.json").write_text(json.dumps(USERS), encoding="utf-8")
    (root / ".all-contributorsrc").write_text(json.dumps(RC), encoding="utf-8")
    for name in ("README.md", "README.pt-BR.md"):
        (root / name).write_text(README, encoding="utf-8")
    args = [sys.executable, "-I", str(SCRIPT), "--root", str(root), "--from-json", str(root / "api.json"), "--users-json", str(root / "users.json")]
    subprocess.run(args, check=True, capture_output=True)
    rc = json.loads((root / ".all-contributorsrc").read_text(encoding="utf-8"))
    people = {c["login"]: c for c in rc["contributors"]}
    assert set(people) == {"cy", "ana", "bo"}, "bots left out, commit authors added, manual entries kept"
    assert people["ana"]["contributions"] == ["doc", "code"], "a commit author gains code, keeps the rest"
    assert people["bo"]["name"] == "bo" and people["bo"]["profile"] == "https://bo.dev", people["bo"]
    text = (root / "README.md").read_text(encoding="utf-8")
    assert "old" not in text and "## License" in text, "only the block changes"
    assert "<table>" in text and 'width="100px;"' in text and "s=200" in text, "table with sharp 100 px avatars"
    assert "<b>Ana Lima</b>" in text and 'title="Content">🖋' in text and 'title="Translation">🌍' in text, text
    assert text.index("Ana Lima") < text.index("<b>bo</b>"), "people with more kinds of contribution come first"
    assert (root / "README.pt-BR.md").read_text(encoding="utf-8") == text, "every listed README is updated"
    first = text
    subprocess.run(args, check=True, capture_output=True)
    assert (root / "README.md").read_text(encoding="utf-8") == first, "a second run changes nothing"
print("ok: 10 checks")
