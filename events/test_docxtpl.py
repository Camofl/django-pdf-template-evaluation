import os
import sys
import tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from docxtpl import DocxTemplate

from events.models import Event
from events.services import build_participant_list_context

TEMPLATE_DIR = PROJECT_ROOT / "events" / "document_templates"
OUTPUT_DIR = PROJECT_ROOT / "generated" / "docxtpl"

MAIN_TEMPLATE = TEMPLATE_DIR / "participant_list.docx"
COMPANY_TEMPLATE = TEMPLATE_DIR / "contact_legal_block.docx"


def render_preview(event_id: int) -> Path:
    event = Event.objects.prefetch_related("participants").get(pk=event_id)
    context = build_participant_list_context(
        event,
        issued_on=date.today(),
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"participant_list_event_{event_id}.docx"

    with tempfile.TemporaryDirectory() as temporary_directory:
        rendered_company_path = (
                Path(temporary_directory) / "rendered_company_block.docx"
        )

        company_template = DocxTemplate(COMPANY_TEMPLATE)
        company_template.render(
            {"company": context["company"]},
            autoescape=True,
        )
        company_template.save(rendered_company_path)

        main_template = DocxTemplate(MAIN_TEMPLATE)
        context["contact_legal_block"] = main_template.new_subdoc(
            str(rendered_company_path)
        )
        main_template.render(context, autoescape=True)
        main_template.save(output_path)

    return output_path


if __name__ == "__main__":
    for event_id in (1, 2):
        print(render_preview(event_id))
