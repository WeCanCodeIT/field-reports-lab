"""Command line: python -m fieldreports --out report.csv [--today YYYY-MM-DD]"""

import argparse
from datetime import date

from fieldreports.client import CrewbookClient
from fieldreports.config import get_api_key
from fieldreports.export import write_csv
from fieldreports.report import build_report


def main():
    parser = argparse.ArgumentParser(description="Weekly field compliance report")
    parser.add_argument("--out", default="report.csv")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    report = build_report(CrewbookClient(get_api_key()), args.today)
    write_csv(report, args.out)
    print(f"wrote {len(report.rows)} rows to {args.out}")
    for name in report.skipped:
        print(f"skipped: {name}")
    return 2 if report.skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
