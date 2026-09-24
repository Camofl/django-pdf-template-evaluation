import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.conf import settings
from django.utils import timezone
from mailmerge import MailMerge, MailMergeOptions

from events.models import Event
from events.services import build_participant_list_context

TEMPLATE_PATH = (
        Path(settings.BASE_DIR)
        / "events"
        / "document_templates"
        / "participant_list.docx"
)
OUTPUT_DIR = Path(settings.BASE_DIR) / "generated" / "mailmerge"


def format_datetime(value):
    return timezone.localtime(value).strftime("%d.%m.%Y %H:%M")


def render_preview(event_id):
    event = Event.objects.prefetch_related("participants").get(pk=event_id)
    context = build_participant_list_context(
        event,
        issued_on=timezone.localdate(),
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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"participant_list_event_{event_id}.docx"

    options = MailMergeOptions(merge_if_fields=True)

    with MailMerge(str(TEMPLATE_PATH), options=options) as document:
        document.merge_rows("participant_first_name", rows)
        document.merge(
            event_id=str(context["event"]["id"]),
            event_title=context["event"]["title"],
            event_start_at=format_datetime(context["event"]["start_at"]),
            event_end_at=format_datetime(context["event"]["end_at"]),
            event_responsible_person=context["event"]["responsible_person"],
            show_large_participant_notice=(
                "1" if context["show_large_participant_notice"] else "0"
            ),
        )
        document.write(str(output_path))

    return output_path


if __name__ == "__main__":
    print(render_preview(1))
    print(render_preview(2))
