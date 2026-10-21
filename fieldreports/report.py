"""Builds the weekly report: one row per project, indicator and week."""

from dataclasses import dataclass, field
from datetime import timedelta

import requests

from fieldreports.counting import count_attachments, count_forms

LOOKBACK_DAYS = 14


@dataclass
class Row:
    project: str
    indicator: str
    week: str
    count: int


@dataclass
class Report:
    rows: list = field(default_factory=list)
    skipped: list = field(default_factory=list)


def build_report(client, today):
    report = Report()
    since = today - timedelta(days=LOOKBACK_DAYS)
    for project in client.projects():
        try:
            forms = client.forms(project["id"], since)
            attachments = client.attachments(project["id"], since)
        except requests.HTTPError:
            continue
        counts = count_forms(forms) + count_attachments(attachments)
        for (indicator, week), count in sorted(counts.items()):
            report.rows.append(Row(project["name"], indicator, week, count))
    return report
