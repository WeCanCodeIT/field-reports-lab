"""Rules for what counts as evidence of each weekly indicator, and which week it lands in."""

import re
from collections import Counter
from datetime import date

FORM_INDICATORS = ["Daily Report", "Safety Checklist"]
FOLDER_INDICATORS = ["Two Week Look Ahead", "Toolbox Talk"]


def _normalize(name):
    return re.sub(r"[^a-z0-9]+", " ", name.casefold()).strip()


def form_indicator(template_name):
    for indicator in FORM_INDICATORS:
        if _normalize(indicator) in _normalize(template_name):
            return indicator
    return None


def folder_indicator(folder_name):
    for indicator in FOLDER_INDICATORS:
        if indicator.lower() in folder_name.lower():
            return indicator
    return None


def week_label(day):
    return f"{day:%b}-W{day.isocalendar().week:02d}"


def count_forms(forms):
    counts = Counter()
    for form in forms:
        if form["status"] != "submitted":
            continue
        indicator = form_indicator(form["template_name"])
        if indicator:
            counts[(indicator, week_label(date.fromisoformat(form["date"])))] += 1
    return counts


def count_attachments(attachments):
    counts = Counter()
    for attachment in attachments:
        indicator = folder_indicator(attachment["folder_name"])
        if indicator:
            counts[(indicator, week_label(date.fromisoformat(attachment["date"])))] += 1
    return counts
