"""The fake API behaves like the real one: token exchange, pages, filters and outages."""

import requests

from fieldreports.config import API_BASE


def _get(path, token="test-token", **params):
    return requests.get(f"{API_BASE}{path}", params=params, headers={"Authorization": f"Bearer {token}"})


def test_token_exchange_needs_an_api_key(crewbook):
    crewbook()
    assert requests.post(f"{API_BASE}/auth/token", json={}).status_code == 401
    assert requests.post(f"{API_BASE}/auth/token", json={"api_key": "anything"}).json() == {"token": "test-token"}


def test_requests_without_the_token_are_refused(crewbook):
    crewbook()
    assert _get("/projects", token="wrong").status_code == 401


def test_lists_come_back_in_pages(crewbook):
    crewbook()
    first = _get("/projects", per_page=2, page=1).json()
    second = _get("/projects", per_page=2, page=2).json()
    assert len(first["items"]) == 2 and first["next_page"] == 2
    assert len(second["items"]) == 1 and second["next_page"] is None


def test_forms_carry_template_name_status_and_date(crewbook):
    crewbook()
    forms = _get("/projects/101/forms", per_page=50).json()["items"]
    assert forms and {"template_name", "status", "date"} <= set(forms[0])
    assert {form["status"] for form in forms} == {"submitted", "draft"}


def test_users_and_folders_belong_to_one_project(crewbook):
    crewbook()
    for kind in ("users", "folders"):
        items = _get(f"/projects/102/{kind}", per_page=50).json()["items"]
        assert items and {item["project_id"] for item in items} == {102}


def test_since_filters_forms_and_attachments(crewbook):
    crewbook()
    forms = _get("/projects/102/forms", per_page=50, since="2026-09-29").json()["items"]
    assert all(form["date"] >= "2026-09-29" for form in forms)
    attachments = _get("/attachments", per_page=50, since="2026-10-10").json()["items"]
    assert attachments and all(item["date"] >= "2026-10-10" for item in attachments)


def test_attachments_filter_by_project_only_when_asked(crewbook):
    crewbook()
    everything = _get("/attachments", per_page=50).json()["items"]
    one = _get("/attachments", per_page=50, project_id=101).json()["items"]
    assert len({item["project_id"] for item in everything}) == 3
    assert {item["project_id"] for item in one} == {101}


def test_outages_can_be_simulated(crewbook):
    crewbook({"projects": [{"id": 1, "name": "A"}], "fail": {"/projects/1/forms": 500}})
    assert _get("/projects/1/forms").status_code == 500
