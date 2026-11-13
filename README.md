# EduLIS Manual Notification Repository (JSON)

This companion repository lets you add LIS opportunity notifications directly in `notifications.json`. You enter the metadata and source URL; GitHub Actions validates the JSON and publishes a website-ready copy at `docs/manual_notifications.json`.

## Add a notification

Edit the root `notifications.json` file. Add an object to the array:

```json
{
  "id": "LIS20261114-01",
  "post_name": "Assistant Librarian",
  "organization": "Example University",
  "category": "Regular Recruitment",
  "published": "2026-11-14",
  "last_date": "2026-12-15",
  "official_url": "https://example.edu/recruitment/notification.pdf"
}
```

Required fields:
- `post_name`: notification/job title
- `organization`: institution/organisation
- `category`: EduLIS category or role label
- `official_url`: public source/official notification URL

Recommended fields:
- `id`: unique stable identifier
- `published`: publication date, `YYYY-MM-DD`
- `last_date`: last date, `YYYY-MM-DD`; use an empty string if not applicable

You can include optional `vacancies` and `start_date` fields if known. Use valid JSON: double quotes, commas between objects, and square brackets around the full list.

## Publish
1. Create a public repository named `edulis-lis-notification-links` under `edulispoint`.
2. Upload this package, preserving folder structure.
3. Ensure GitHub Actions are enabled.
4. Run **Publish manual notifications** once from the Actions tab.
5. Subsequent edits to `notifications.json` automatically validate and publish the output.

Raw output URL:
`https://raw.githubusercontent.com/edulispoint/edulis-lis-notification-links/main/docs/manual_notifications.json`

## Important
This version does not scrape webpages or extract metadata from URLs. You enter the metadata in the JSON file; the website displays it and links the title to `official_url`. This avoids unreliable extraction and cross-origin restrictions. The workflow validates required fields, dates, URLs and duplicate IDs/URLs before publishing.

The output uses the same key names as the existing EduLIS feed: `post_name`, `organization`, `category`, `published`, `last_date`, `official_url`, with optional `id`, `vacancies`, and `start_date`.
