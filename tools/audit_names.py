"""Fails if any person in the fixtures is not on the allow-list, or any email is outside example.com.

Every name in this repo is made up. The allow-list keeps it that way, so no real person's name or
data slips in with a fixture.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = set((ROOT / "tools" / "allowed_names.txt").read_text(encoding="utf-8").split("\n")) - {""}
EMAIL = re.compile(r"[\w.+-]+@([\w-]+\.)+[\w-]+")


def problems():
    found = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        text = path.read_text(encoding="utf-8")
        for email in EMAIL.finditer(text):
            if not email.group(0).endswith("@example.com"):
                found.append(f"{path.name}: email outside example.com: {email.group(0)}")
        if path.name == "users.json":
            for user in json.loads(text):
                if user["name"] not in ALLOWED:
                    found.append(f"{path.name}: name not on the allow-list: {user['name']}")
    return found


if __name__ == "__main__":
    issues = problems()
    for issue in issues:
        print(issue)
    print("names audit: " + ("FAILED" if issues else "ok"))
    sys.exit(1 if issues else 0)
