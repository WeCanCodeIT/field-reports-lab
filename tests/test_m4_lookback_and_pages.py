"""Module 4. F3: forms and attachments use the same 14-day look-back. F6: every page is read."""

from datetime import date

from fieldreports.client import CrewbookClient
from fieldreports.counting import week_label
from fieldreports.report import build_report

TODAY = date(2026, 10, 14)


def _counts(report):
    return {(row.indicator, row.week): row.count for row in report.rows}


def test_flaw_F3_forms_and_attachments_share_one_14_day_window(crewbook):
    crewbook({
        "projects": [{"id": 1, "name": "Test Site"}],
        "forms": [
            {"id": 1, "project_id": 1, "template_name": "Daily Report", "status": "submitted", "date": "2026-09-20"},
            {"id": 2, "project_id": 1, "template_name": "Daily Report", "status": "submitted", "date": "2026-10-05"},
        ],
        "attachments": [
            {"id": 1, "project_id": 1, "folder_name": "Toolbox Talks", "file_name": "a.pdf", "date": "2026-10-03"},
        ],
    })
    counts = _counts(build_report(CrewbookClient("key"), TODAY))
    assert ("Daily Report", week_label(date(2026, 9, 20))) not in counts
    assert counts[("Daily Report", week_label(date(2026, 10, 5)))] == 1
    assert counts[("Toolbox Talk", week_label(date(2026, 10, 3)))] == 1


def test_flaw_F6_every_page_of_forms_is_read(crewbook):
    days = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09"]
    crewbook({
        "projects": [{"id": 1, "name": "Test Site"}],
        "forms": [{"id": n, "project_id": 1, "template_name": "Daily Report", "status": "submitted", "date": day}
                  for n, day in enumerate(days)],
    })
    counts = _counts(build_report(CrewbookClient("key"), TODAY))
    assert counts[("Daily Report", week_label(date(2026, 10, 5)))] == 5


def test_drafts_never_count(crewbook):
    crewbook({
        "projects": [{"id": 1, "name": "Test Site"}],
        "forms": [{"id": 1, "project_id": 1, "template_name": "Daily Report", "status": "draft", "date": "2026-10-05"}],
    })
    assert build_report(CrewbookClient("key"), TODAY).rows == []
