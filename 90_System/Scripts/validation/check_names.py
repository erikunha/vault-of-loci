"""Naming standard: no file or folder in the vault has a space in its name.

Exits 1 and lists offenders. To fix: python3 90_System/Scripts/normalize_names.py --write
"""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
SKIP = {".git", ".obsidian", ".venv", "node_modules", ".smart-env", ".trash", ".claude"}
bad = sorted(p.relative_to(VAULT) for p in VAULT.rglob("*")
             if " " in p.name and not SKIP.intersection(p.relative_to(VAULT).parts))
for b in bad:
    print("has a space:", b)
print("names off standard:", len(bad))
sys.exit(1 if bad else 0)
