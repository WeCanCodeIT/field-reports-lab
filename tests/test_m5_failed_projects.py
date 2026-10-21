"""Module 5. F4: a project the API failed on is reported as skipped, never shown as zero."""

from datetime import date

from fieldreports.client import CrewbookClient
from fieldreports.report import build_report


def test_flaw_F4_a_failed_project_is_listed_as_skipped(crewbook):
    crewbook({
        "projects": [{"id": 1, "name": "North Yard"}, {"id": 2, "name": "South Yard"}],
        "forms": [{"id": 1, "project_id": 1, "template_name": "Daily Report", "status": "submitted", "date": "2026-10-05"}],
        "fail": {"/projects/2/forms": 500},
    })
    report = build_report(CrewbookClient("key"), date(2026, 10, 14))
    assert report.skipped == ["South Yard"]
    assert {row.project for row in report.rows} == {"North Yard"}
