"""Settings for talking to the Crewbook API."""

import os

API_BASE = "https://api.example.com/v1"
PAGE_SIZE = 2
API_KEY_VARIABLE = "CREWBOOK_API_KEY"


def get_api_key():
    key = os.environ.get(API_KEY_VARIABLE, "").strip()
    if not key:
        raise RuntimeError(f"Set the {API_KEY_VARIABLE} environment variable to your Crewbook API key.")
    return key
