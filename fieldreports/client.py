"""A small client for the Crewbook API: projects, project users, forms and attachments."""

import requests

from fieldreports.config import API_BASE, PAGE_SIZE


class CrewbookClient:
    def __init__(self, api_key, base=API_BASE):
        self.api_key = api_key
        self.base = base
        self.session = requests.Session()
        self._token = None

    def _auth_header(self):
        if self._token is None:
            response = self.session.post(f"{self.base}/auth/token", json={"api_key": self.api_key})
            response.raise_for_status()
            self._token = response.json()["token"]
        return {"Authorization": f"Bearer {self._token}"}

    def _get(self, path, params=None):
        response = self.session.get(f"{self.base}{path}", params=params, headers=self._auth_header())
        response.raise_for_status()
        return response.json()

    def _get_all(self, path, params=None):
        items, page = [], 1
        while page is not None:
            data = self._get(path, dict(params or {}, per_page=PAGE_SIZE, page=page))
            items.extend(data["items"])
            page = data.get("next_page")
        return items

    def projects(self):
        return self._get_all("/projects")

    def users(self, project_id):
        return self._get_all(f"/projects/{project_id}/users")

    def folders(self, project_id):
        return self._get_all(f"/projects/{project_id}/folders")

    def forms(self, project_id, since):
        return self._get_all(f"/projects/{project_id}/forms", {"since": since.isoformat()})

    def attachments(self, project_id, since):
        return self._get_all("/attachments", {"since": since.isoformat()})
