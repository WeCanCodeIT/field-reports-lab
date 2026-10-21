"""Module 6. F8: a project's report reads only that project's attachments."""

from datetime import date

from fieldreports.client import CrewbookClient
from fieldreports.report import build_report


def test_flaw_F8_attachments_from_another_project_are_never_counted(crewbook):
    api = crewbook({
        "projects": [{"id": 1, "name": "North Yard"}, {"id": 2, "name": "South Yard"}],
        "attachments": [
            {"id": 1, "project_id": 1, "folder_name": "Two Week Look Ahead", "file_name": "a.pdf", "date": "2026-10-05"},
            {"id": 2, "project_id": 2, "folder_name": "Two Week Look Ahead", "file_name": "b.pdf", "date": "2026-10-05"},
            {"id": 3, "project_id": 2, "folder_name": "Two Week Look Ahead", "file_name": "c.pdf", "date": "2026-10-06"},
        ],
    })
    report = build_report(CrewbookClient("key"), date(2026, 10, 14))
    totals = {row.project: row.count for row in report.rows}
    assert totals == {"North Yard": 1, "South Yard": 2}
    attachment_calls = [query for path, query in api.calls if path == "/attachments"]
    assert attachment_calls and all("project_id" in query for query in attachment_calls)
