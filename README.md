# Django PDF Template Evaluation

This branch implements the Carbone Community prototype for the event participant list. The common domain model and fixture data originate from `main`. The other candidates remain isolated on `prototype/docxtpl` and `prototype/docx-mailmerge2`. This repository is a research prototype, not a production deployment.

## Scope

- Render a Word template with event data and a dynamic participant table.
- Generate PDFs for the 60-participant reference event and the 25-participant control event.
- Trigger downloads from the Django admin event change view.
- Use a locally operated Carbone container without a license key or Carbone Cloud.
- Evaluate conditional content, multi-page layout and built-in formatters.
- Record the missing inclusion of a separately editable company and legal document.

## Requirements

- Python compatible with the pinned Django version in `requirements.txt`.
- pip and Docker with Docker Compose.
- A local port 4000 that is available for the Carbone service.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata events
python manage.py createsuperuser
docker compose up -d
curl --fail-with-body http://127.0.0.1:4000/status
python manage.py runserver
```

Open the Django admin at `http://127.0.0.1:8000/admin/`, select an event and use the participant list PDF link in its change view. The local converter address defaults to `http://127.0.0.1:4000` and can be overridden with `CARBONE_URL`. The Docker port is bound to localhost in `compose.yaml`. Do not expose the conversion service to the public internet when processing customer documents.

## Preview and tests

Generate local DOCX and PDF previews for both fixture events:

```bash
python -m events.preview_carbone
```

The preview files are written under `generated/carbone/` and are ignored by Git. Use only non-sensitive fixture data for this prototype. Run the regular test suite without an external service:

```bash
python manage.py test
```

The Carbone integration test requires the running local service:

```bash
RUN_CARBONE_TESTS=1 python manage.py test
```

Without `RUN_CARBONE_TESTS=1`, the live test is skipped. The mocked tests check data transfer and response headers; only the live test checks the resulting PDFs. Visual checks remain necessary for logos, footer page numbers, table headers and page breaks.

## Architecture and limitations

`events/services.py` builds data from the shared models, formats event datetimes for JSON, loads the versioned DOCX template and posts it to the local Carbone `/render/template` endpoint. The service validates the PDF response and returns it through the existing Django admin route. The full Docker image includes its own LibreOffice conversion environment, so this branch does not depend on Gotenberg.

This branch does not implement inclusion of a second editable DOCX for the company and legal block. The block is therefore absent from the generated document. No paid Carbone feature or Python-side copy-and-paste substitute is counted as fulfillment. The tested conditional content, participant table and built-in formatters remain editable in the Word template.

See `docs/implementation-log.md`, `docs/evaluation-notes.md`, `docs/manual-test-protocol.md` and `docs/sources.md` for observations and source records. Exact development times and benchmark measurements were not recorded.
