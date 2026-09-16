from dataclasses import dataclass
from datetime import date

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


def generate_participant_list(event: Event) -> GeneratedDocument:
    raise NotImplementedError(
        "No document generation engine is implemented on the main branch."
    )
