import base64
import os
import re
from io import BytesIO
from unittest import skipUnless
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from pypdf import PdfReader

from events.models import Event
from events.services import generate_participant_list


class DocumentGenerationTests(TestCase):
    fixtures = ["events"]

    @patch("events.services.requests.post")
    def test_carbone_receives_template_and_reference_data(self, mock_post):
        mock_post.return_value.content = b"%PDF-1.4\nmock response\n"

        event = Event.objects.get(pk=1)
        generate_participant_list(event)

        self.assertEqual(mock_post.call_count, 1)

        args, kwargs = mock_post.call_args
        payload = kwargs["json"]

        self.assertTrue(args[0].endswith("/render/template"))
        self.assertEqual(kwargs["params"], {"download": "true"})
        self.assertEqual(payload["convertTo"], "pdf")
        self.assertEqual(payload["converter"], "L")
        self.assertEqual(payload["data"]["event"]["title"], event.title)
        self.assertEqual(payload["data"]["participant_count"], 60)
        self.assertEqual(len(payload["data"]["participants"]), 60)

        template_bytes = base64.b64decode(
            payload["template"],
            validate=True,
        )
        self.assertTrue(template_bytes.startswith(b"PK"))

        submitted_last_names = {
            participant["last_name"]
            for participant in payload["data"]["participants"]
        }
        expected_last_names = {
            participant.last_name
            for participant in event.participants.all()
        }
        self.assertEqual(submitted_last_names, expected_last_names)

    @patch("events.services.requests.post")
    def test_admin_returns_pdf_download(self, mock_post):
        mock_post.return_value.content = b"%PDF-1.4\nmock response\n"

        admin_user = get_user_model().objects.create_superuser(
            username="carbone-test-admin",
            email="carbone-test@example.invalid",
            password="test-password",
        )
        self.client.force_login(admin_user)

        url = reverse(
            "admin:events_event_generate_participant_list",
            args=[1],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn(
            "attachment;",
            response["Content-Disposition"],
        )
        self.assertIn(
            "participant_list_event_1.pdf",
            response["Content-Disposition"],
        )
        self.assertTrue(
            b"".join(response.streaming_content).startswith(b"%PDF-")
        )

    @skipUnless(
        os.environ.get("RUN_CARBONE_TESTS") == "1",
        "Requires a running local Carbone service.",
    )
    def test_live_pdfs_contain_data_and_conditional_notice(self):
        notice_marker = "Lorem ipsum"

        for event_id, expected_count in ((1, 60), (2, 25)):
            with self.subTest(event_id=event_id):
                event = Event.objects.get(pk=event_id)
                result = generate_participant_list(event)

                self.assertEqual(result.content_type, "application/pdf")
                self.assertTrue(result.content.startswith(b"%PDF-"))

                reader = PdfReader(BytesIO(result.content))
                self.assertGreaterEqual(len(reader.pages), 1)

                if event_id == 1:
                    self.assertGreater(len(reader.pages), 1)

                pdf_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )
                normalized_text = re.sub(r"\s+", " ", pdf_text)

                self.assertIn(event.title, normalized_text)
                self.assertEqual(
                    event.participants.count(),
                    expected_count,
                )

                for participant in event.participants.all():
                    with self.subTest(
                            event_id=event_id,
                            participant_id=participant.pk,
                    ):
                        self.assertIn(
                            participant.last_name,
                            normalized_text,
                        )

                if event_id == 1:
                    self.assertIn(notice_marker, normalized_text)
                else:
                    self.assertNotIn(notice_marker, normalized_text)
