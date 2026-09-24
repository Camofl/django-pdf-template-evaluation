from dataclasses import dataclass
from datetime import date

from .document_filters import build_document_environment
from .models import Event
import logging
import tempfile
from io import BytesIO
from pathlib import Path

import requests
from django.conf import settings
from django.utils import timezone
from docxtpl import DocxTemplate

logger = logging.getLogger(__name__)

TEMPLATE_DIR = (
        Path(settings.BASE_DIR) / "events" / "document_templates"
)

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


def generate_participant_list(event: Event) -> GeneratedDocument:
    context = build_participant_list_context(
        event,
        issued_on=timezone.localdate(),
    )

    main_path = TEMPLATE_DIR / "participant_list.docx"
    company_path = TEMPLATE_DIR / "contact_legal_block.docx"

    try:
        with tempfile.TemporaryDirectory() as temporary_directory:
            rendered_company_path = (
                    Path(temporary_directory) / "rendered_company_block.docx"
            )

            company_template = DocxTemplate(str(company_path))
            company_template.render(
                {"company": context["company"]},
                autoescape=True,
            )
            company_template.save(str(rendered_company_path))

            main_template = DocxTemplate(str(main_path))
            context["contact_legal_block"] = main_template.new_subdoc(
                str(rendered_company_path)
            )
            main_template.render(
                context,
                jinja_env=build_document_environment(),
                autoescape=True,
            )
            docx_buffer = BytesIO()
            main_template.save(docx_buffer)
            docx_buffer.seek(0)

        response = requests.post(
            (
                f"{settings.GOTENBERG_URL.rstrip('/')}"
                "/forms/libreoffice/convert"
            ),
            files={
                "files": (
                    "participant_list.docx",
                    docx_buffer,
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
    except Exception as error:
        logger.exception(
            "DOCX rendering failed for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "DOCX rendering failed."
        ) from error

    pdf_content = response.content
    if not pdf_content.startswith(b"%PDF-"):
        logger.error(
            "Conversion returned no valid PDF for event %s",
            event.pk,
        )
        raise DocumentGenerationError(
            "The conversion service returned no valid PDF."
        )

    return GeneratedDocument(
        filename=f"participant_list_event_{event.pk}.pdf",
        content=pdf_content,
    )
