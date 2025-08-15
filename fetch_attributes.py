#!/usr/bin/env python3
"""
fetch_attributes.py
---------------------------------
Iterates through all pages of the Braze /custom_attributes endpoint,
following the link header (RFC-5988 style) until no rel="next" link
is present.  The result is written to stdout and/or to disk.

Requirements:
  pip install requests
  pip install dotenv

Environment variables required:
  BRAZE_API_KEY          – Your REST API key with users.track permission
  BRAZE_REST_API_HOST    – Host portion of your REST endpoint
                           e.g. rest.iad-01.braze.com
Optional:
  OUT_FILE               – Path to write the full JSON payload (defaults to None)
  CSV_FILE               – Path to write a CSV of attributes (defaults to None)
"""

import os
import sys
import json
import csv
import time
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def env(name: str) -> str:
    """Pull a required environment variable or exit with a helpful error."""
    value = os.getenv(name)
    if not value:
        sys.exit(f"Environment variable {name} is required.")
    return value


API_KEY: str = env("BRAZE_API_KEY")
REST_ENDPOINT: str = env("BRAZE_REST_ENDPOINT").rstrip("/")
CSV_FILE: Optional[str] = os.getenv("CSV_FILE")  # optional
OUT_FILE: Optional[str] = os.getenv("OUT_FILE")  # optional

# --- Configuration ----------------------------------------------------------

BASE_URL = f"{REST_ENDPOINT}/custom_attributes"
REQUEST_HEADERS = {
    # Using Bearer is recommended for new API keys.
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "braze-attribute-export/1.0",
}

# ---------------------------------------------------------------------------


def parse_next_link(link_header: str) -> Optional[str]:
    """
    Given a raw Link header return the URL whose rel is "next", or None.
    The header looks like:
       <https://…/custom_attributes?cursor=XYZ>; rel="prev",
       <https://…/custom_attributes?cursor=ABC>; rel="next"
    """
    if not link_header:
        return None

    # Split pairs by comma
    for pair in link_header.split(","):
        pair = pair.strip()
        if 'rel="next"' in pair:
            # Extract substring between < and >
            start = pair.find("<") + 1
            end = pair.find(">", start)
            if start > 0 and end > start:
                return pair[start:end]
    return None


def fetch_all_attributes() -> List[Dict]:
    """
    Page through /custom_attributes and return a list of all
    attribute definition objects.
    """
    next_url = BASE_URL  # first request has no cursor
    collected: List[Dict] = []
    page_count = 0

    while next_url:
        page_count += 1
        print(f"Requesting page {page_count}: {next_url}", file=sys.stderr)
        resp = requests.get(next_url, headers=REQUEST_HEADERS, timeout=30)
        resp.raise_for_status()

        payload = resp.json()
        # Adjust the key below if Braze returns a different top-level field name
        attributes = payload.get("attributes", [])
        collected.extend(attributes)

        # Inspect Link header for rel="next"
        next_url = parse_next_link(resp.headers.get("Link", ""))

        # Optional: respect Braze rate limits (100 req/minute default)
        time.sleep(0.7)  # ~85 requests/minute

    print(f"\nTotal attributes retrieved: {len(collected)}", file=sys.stderr)
    return collected
def write_attributes_to_csv(file_path: str, attributes: List[Dict]):
    """Write a list of attribute objects to a CSV file."""
    if not attributes:
        return

    # Dynamically determine headers from the first object's keys
    headers = list(attributes[0].keys())

    # Prepare data for CSV writing (stringify complex types)
    processed_attributes = []
    for attr in attributes:
        processed_row = {}
        for key, value in attr.items():
            if isinstance(value, (dict, list)):
                processed_row[key] = json.dumps(value)
            else:
                processed_row[key] = value
        processed_attributes.append(processed_row)

    with open(file_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(processed_attributes)




def main():
    all_attributes = fetch_all_attributes()

    # Output
    json_dump = json.dumps(all_attributes, indent=2)
    print(json_dump)

    if OUT_FILE:
        with open(OUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(json_dump)
    if CSV_FILE:
        write_attributes_to_csv(CSV_FILE, all_attributes)
        print(f"Attributes written to {CSV_FILE}", file=sys.stderr)
        print(f"Attributes written to {OUT_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()