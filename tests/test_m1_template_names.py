"""Module 1. F1: form template names are typed by hand, so their spelling varies."""

from fieldreports.counting import form_indicator


def test_flaw_F1_template_names_match_in_any_capitalization_or_spacing():
    for name in ["Daily Report", "daily report", "DAILY REPORT - copy", "Daily  Report", "Safety checklist"]:
        assert form_indicator(name) is not None, name


def test_unrelated_templates_do_not_count():
    assert form_indicator("Punch List") is None
