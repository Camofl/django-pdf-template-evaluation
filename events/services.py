from dataclasses import dataclass
from datetime import date

from .models import Event
import base64
import logging
from pathlib import Path

import requests
from django.conf import settings
from django.utils import timezone

class DocumentGenerationError(Exception):
    """Raised when a document cannot be generated."""


@dataclass(frozen=True)
class GeneratedDocument:
    filename: str
    content: bytes
    content_type: str = "application/pdf"


def build_participant_list_context(
        event: Event,
        issued_on: date,
) -> dict:
    participants = [
        {
            "first_name": participant.first_name,
            "last_name": participant.last_name,
            "gender": participant.get_gender_display(),
            "age": participant.age_on(issued_on),
        }
        for participant in event.participants.all()
    ]

    return {
        "event": {
            "id": event.pk,
            "title": event.title,
            "start_at": event.start_at,
            "end_at": event.end_at,
            "responsible_person": event.responsible_person,
        },
        "participants": participants,
        "participant_count": len(participants),
        "show_large_participant_notice": len(participants) > 25,
        "issued_on": issued_on,
        "company": {
            "name": "Example Company Ltd.",
            "address": "Example Street 1, 01067 Dresden, Germany",
            "email": "contact@example.invalid",
            "phone": "+49 351 000000",
            "legal_notice": "This document was generated automatically.",
        },
    }


logger = logging.getLogger(__name__)


def _format_datetime(value):
    return timezone.localtime(value).strftime("%d.%m.%Y %H:%M")


def _build_carbone_data(event):
    context = build_participant_list_context(
        event,
        issued_on=timezone.localdate(),
    )

    event_data = context["event"].copy()
    event_data["start_at"] = _format_datetime(
        event_data["start_at"]
    )
    event_data["end_at"] = _format_datetime(
        event_data["end_at"]
    )

    return {
        "event": event_data,
        "participants": context["participants"],
        "participant_count": context["participant_count"],
    }


def generate_participant_list(event: Event) -> GeneratedDocument:
    template_path = (
            Path(settings.BASE_DIR)
            / "events"
            / "document_templates"
            / "participant_list.docx"
    )

    try:
        template_content = base64.b64encode(
            template_path.read_bytes()
        ).decode("ascii")
        data = _build_carbone_data(event)
    except (OSError, ValueError) as error:
        logger.exception(
            "Could not prepare Carbone input for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "The participant list could not be prepared."
        ) from error

    try:
        response = requests.post(
            f"{settings.CARBONE_URL.rstrip('/')}/render/template",
            params={"download": "true"},
            json={
                "template": template_content,
                "data": data,
                "convertTo": "pdf",
                "converter": "L",
            },
            timeout=(5, 120),
        )
        response.raise_for_status()
    except requests.RequestException as error:
        logger.exception(
            "Carbone rendering failed for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "PDF generation failed."
        ) from error

    if not response.content.startswith(b"%PDF-"):
        logger.error(
            "Carbone returned no PDF for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "The rendering service returned no PDF."
        )

    return GeneratedDocument(
        filename=f"participant_list_event_{event.pk}.pdf",
        content=response.content,
    )
