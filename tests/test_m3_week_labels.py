"""Module 3. F2: every item from one Monday-to-Sunday week gets the same week label."""

from datetime import date

from fieldreports.counting import week_label


def test_flaw_F2_a_week_that_spans_two_months_keeps_one_label():
    assert week_label(date(2026, 9, 30)) == week_label(date(2026, 10, 2))


def test_different_weeks_get_different_labels():
    assert week_label(date(2026, 10, 2)) != week_label(date(2026, 10, 5))
