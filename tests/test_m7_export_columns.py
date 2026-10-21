"""Module 7. F5: every value in the CSV sits under its own header."""

import csv

from fieldreports.export import write_csv
from fieldreports.report import Report, Row


def test_flaw_F5_each_value_sits_under_its_header(tmp_path):
    out = tmp_path / "report.csv"
    write_csv(Report(rows=[Row("North Yard", "Daily Report", "2026-W41", 5)], skipped=["South Yard"]), out)
    rows = list(csv.DictReader(out.open(encoding="utf-8")))
    assert rows[0] == {"project": "North Yard", "indicator": "Daily Report", "week": "2026-W41", "count": "5"}
    assert rows[1]["project"] == "South Yard" and rows[1]["indicator"] == "SKIPPED"
