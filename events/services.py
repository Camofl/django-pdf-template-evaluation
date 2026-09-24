import logging
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import requests
from django.conf import settings
from django.utils import timezone
from mailmerge import MailMerge, MailMergeOptions

from .models import Event


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


def generate_participant_list(event: Event) -> GeneratedDocument:
    context = build_participant_list_context(
        event,
        issued_on=timezone.localdate(),
    )

    template_path = (
            Path(settings.BASE_DIR)
            / "events"
            / "document_templates"
            / "participant_list.docx"
    )

    rows = [
        {
            "participant_first_name": participant["first_name"],
            "participant_last_name": participant["last_name"],
            "participant_gender": participant["gender"],
            "participant_age": str(participant["age"]),
        }
        for participant in context["participants"]
    ]

    try:
        with tempfile.TemporaryDirectory() as temporary_directory:
            docx_path = (
                    Path(temporary_directory) / "participant_list.docx"
            )

            options = MailMergeOptions(merge_if_fields=True)

            with MailMerge(str(template_path), options=options) as document:
                document.merge_rows(
                    "participant_first_name",
                    rows,
                )
                document.merge(
                    event_id=str(context["event"]["id"]),
                    event_title=context["event"]["title"],
                    event_start_at=_format_datetime(
                        context["event"]["start_at"]
                    ),
                    event_end_at=_format_datetime(
                        context["event"]["end_at"]
                    ),
                    event_responsible_person=(
                        context["event"]["responsible_person"]
                    ),
                    show_large_participant_notice=(
                        "1"
                        if context["show_large_participant_notice"]
                        else "0"
                    ),
                )
                document.write(str(docx_path))

            docx_content = docx_path.read_bytes()

    except Exception as error:
        logger.exception(
            "DOCX rendering failed for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "DOCX rendering failed."
        ) from error

    try:
        response = requests.post(
            (
                f"{settings.GOTENBERG_URL.rstrip('/')}"
                "/forms/libreoffice/convert"
            ),
            files={
                "files": (
                    "participant_list.docx",
                    docx_content,
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document",
                )
            },
            timeout=(5, 120),
        )
        response.raise_for_status()

    except requests.RequestException as error:
        logger.exception(
            "PDF conversion failed for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "PDF conversion failed."
        ) from error

    if not response.content.startswith(b"%PDF-"):
        logger.error(
            "Conversion returned no PDF for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "The conversion service returned no PDF."
        )

    return GeneratedDocument(
        filename=f"participant_list_event_{event.pk}.pdf",
        content=response.content,
    )
