"""Writes the report as CSV for the dashboard import."""

import csv

HEADERS = ["project", "indicator", "week", "count"]


def write_csv(report, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        for row in report.rows:
            writer.writerow([row.project, row.week, row.indicator, row.count])
        for name in report.skipped:
            writer.writerow([name, "SKIPPED", "", ""])
