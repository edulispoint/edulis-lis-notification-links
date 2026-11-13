#!/usr/bin/env python3
"""Validate root notifications.json and publish docs/manual_notifications.json."""
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "notifications.json"
TARGET = ROOT / "docs" / "manual_notifications.json"

REQUIRED = ("post_name", "organization", "category", "official_url")
ALLOWED = {
    "id", "post_name", "organization", "category", "published",
    "last_date", "official_url", "vacancies", "start_date"
}

def valid_date(value, field, index):
    if value in (None, ""):
        return ""
    if not isinstance(value, str):
        raise ValueError(f"Item {index}: {field} must be YYYY-MM-DD or empty")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Item {index}: invalid {field} {value!r}; use YYYY-MM-DD")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Item {index}: {field} must use YYYY-MM-DD")
    return value

def main():
    if not SOURCE.exists():
        raise SystemExit("notifications.json not found")
    try:
        records = json.loads(SOURCE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(records, list):
        raise SystemExit("notifications.json must contain a JSON array")

    ids, urls, clean_records = set(), set(), []
    for i, item in enumerate(records, 1):
        if not isinstance(item, dict):
            raise SystemExit(f"Item {i}: each notification must be a JSON object")
        missing = [field for field in REQUIRED if not str(item.get(field, "")).strip()]
        if missing:
            raise SystemExit(f"Item {i}: missing required field(s): {', '.join(missing)}")

        unknown = set(item) - ALLOWED
        if unknown:
            print(f"Warning: item {i} has unknown field(s), preserving them: {', '.join(sorted(unknown))}")

        url = str(item["official_url"]).strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise SystemExit(f"Item {i}: official_url must be a full http(s) URL")

        rid = str(item.get("id", "")).strip()
        if rid and rid in ids:
            raise SystemExit(f"Duplicate id at item {i}: {rid}")
        if rid:
            ids.add(rid)

        normalized_url = url.rstrip("/").lower()
        if normalized_url in urls:
            raise SystemExit(f"Duplicate official_url at item {i}: {url}")
        urls.add(normalized_url)

        output = dict(item)
        for field in ("id", "post_name", "organization", "category", "official_url"):
            output[field] = str(output[field]).strip()
        output["official_url"] = url
        output["published"] = valid_date(item.get("published", ""), "published", i)
        output["last_date"] = valid_date(item.get("last_date", ""), "last_date", i)
        for field in ("vacancies", "start_date"):
            output.setdefault(field, "")
        clean_records.append(output)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(clean_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated and published {len(clean_records)} manual notification(s) to docs/manual_notifications.json")

if __name__ == "__main__":
    main()
