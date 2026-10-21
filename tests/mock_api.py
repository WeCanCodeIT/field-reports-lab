"""An in-process fake of the Crewbook API, built on the `responses` library.

Nothing here opens a socket: `responses` answers requests inside the `requests` library itself.
A dataset is a dict with projects, users, folders, forms and attachments, plus an optional
`fail` map of path -> HTTP status for simulating outages.
"""

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import responses

from fieldreports.config import API_BASE

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
TOKEN = "test-token"


def load_fixtures():
    return {name: json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))
            for name in ("projects", "users", "folders", "forms", "attachments")}


def _page(items, query):
    per_page = int(query.get("per_page", ["50"])[0])
    page = int(query.get("page", ["1"])[0])
    start = (page - 1) * per_page
    chunk = items[start:start + per_page]
    next_page = page + 1 if start + per_page < len(items) else None
    return {"items": chunk, "next_page": next_page}


class MockCrewbook:
    def __init__(self, dataset):
        self.data = {key: dataset.get(key, []) for key in ("projects", "users", "folders", "forms", "attachments")}
        self.fail = dataset.get("fail", {})
        self.calls = []

    def install(self, rsps):
        rsps.add_callback(responses.POST, f"{API_BASE}/auth/token", callback=self._token)
        rsps.add_callback(responses.GET, re.compile(re.escape(API_BASE) + r"/.*"), callback=self._get)

    def _token(self, request):
        body = json.loads(request.body or "{}")
        if not body.get("api_key"):
            return (401, {}, json.dumps({"error": "missing api_key"}))
        return (200, {}, json.dumps({"token": TOKEN}))

    def _get(self, request):
        url = urlparse(request.url)
        path = url.path[len(urlparse(API_BASE).path):]
        query = parse_qs(url.query)
        self.calls.append((path, query))
        if request.headers.get("Authorization") != f"Bearer {TOKEN}":
            return (401, {}, json.dumps({"error": "bad token"}))
        if path in self.fail:
            return (self.fail[path], {}, json.dumps({"error": "server error"}))
        items = self._items(path, query)
        if items is None:
            return (404, {}, json.dumps({"error": "not found"}))
        return (200, {}, json.dumps(_page(items, query)))

    def _items(self, path, query):
        since = query.get("since", [None])[0]
        if path == "/projects":
            return self.data["projects"]
        match = re.fullmatch(r"/projects/(\d+)/(users|folders|forms)", path)
        if match:
            project_id, kind = int(match.group(1)), match.group(2)
            items = [item for item in self.data[kind] if item["project_id"] == project_id]
            return _since(items, since) if kind == "forms" else items
        if path == "/attachments":
            items = self.data["attachments"]
            if "project_id" in query:
                items = [item for item in items if item["project_id"] == int(query["project_id"][0])]
            return _since(items, since)
        return None


def _since(items, since):
    return [item for item in items if since is None or item["date"] >= since]
