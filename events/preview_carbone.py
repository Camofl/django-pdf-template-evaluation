import base64
import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import requests
from django.utils import timezone

from events.models import Event
from events.services import build_participant_list_context

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = (
        PROJECT_ROOT
        / "events"
        / "document_templates"
        / "participant_list.docx"
)
OUTPUT_DIR = PROJECT_ROOT / "generated" / "carbone"
CARBONE_URL = "http://127.0.0.1:4000/render/template"


def format_datetime(value):
    return timezone.localtime(value).strftime("%d.%m.%Y %H:%M")


def build_carbone_data(event):
    context = build_participant_list_context(
        event,
        issued_on=timezone.localdate(),
    )

    event_data = context["event"].copy()
    event_data["start_at"] = format_datetime(event_data["start_at"])
    event_data["end_at"] = format_datetime(event_data["end_at"])

    return {
        "event": event_data,
        "participants": context["participants"],
        "participant_count": context["participant_count"],
    }


def render_preview(event_id, output_format):
    event = Event.objects.prefetch_related("participants").get(pk=event_id)

    template_content = base64.b64encode(
        TEMPLATE_PATH.read_bytes()
    ).decode("ascii")

    payload = {
        "template": template_content,
        "data": build_carbone_data(event),
        "convertTo": output_format,
    }

    if output_format == "pdf":
        payload["converter"] = "L"

    response = requests.post(
        CARBONE_URL,
        params={"download": "true"},
        json=payload,
        timeout=(5, 120),
    )
    response.raise_for_status()

    expected_start = b"%PDF-" if output_format == "pdf" else b"PK"
    if not response.content.startswith(expected_start):
        raise RuntimeError(
            f"Carbone did not return a valid {output_format.upper()} file."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = (
            OUTPUT_DIR / f"participant_list_event_{event_id}.{output_format}"
    )
    output_path.write_bytes(response.content)
    return output_path


if __name__ == "__main__":
    for event_id in (1, 2):
        for output_format in ("docx", "pdf"):
            print(render_preview(event_id, output_format))
