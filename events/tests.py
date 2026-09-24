from datetime import date, datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Event, Participant
from .services import build_participant_list_context


class ParticipantAgeTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(
            title="Age Calculation Event",
            start_at=datetime(
                2026,
                9,
                16,
                9,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            end_at=datetime(
                2026,
                9,
                16,
                17,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            responsible_person="Jane Example",
        )

    def test_age_on_returns_age_after_birthday(self) -> None:
        participant = Participant.objects.create(
            event=self.event,
            first_name="Anna",
            last_name="Example",
            gender=Participant.Gender.FEMALE,
            birth_date=date(2000, 3, 10),
        )

        age = participant.age_on(date(2026, 9, 16))

        self.assertEqual(age, 26)

    def test_age_on_subtracts_one_before_birthday(self) -> None:
        participant = Participant.objects.create(
            event=self.event,
            first_name="Ben",
            last_name="Example",
            gender=Participant.Gender.MALE,
            birth_date=date(2000, 10, 1),
        )

        age = participant.age_on(date(2026, 9, 16))

        self.assertEqual(age, 25)

    def test_age_on_returns_age_on_birthday(self) -> None:
        participant = Participant.objects.create(
            event=self.event,
            first_name="Chris",
            last_name="Example",
            gender=Participant.Gender.DIVERSE,
            birth_date=date(2000, 9, 16),
        )

        age = participant.age_on(date(2026, 9, 16))

        self.assertEqual(age, 26)

    def test_event_contains_created_participant(self) -> None:
        participant = Participant.objects.create(
            event=self.event,
            first_name="Dana",
            last_name="Example",
            gender=Participant.Gender.FEMALE,
            birth_date=date(1998, 1, 1),
        )

        participants = list(self.event.participants.all())

        self.assertEqual(participants, [participant])


class ParticipantListContextTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(
            title="Context Test Event",
            start_at=datetime(
                2026,
                10,
                1,
                9,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            end_at=datetime(
                2026,
                10,
                1,
                17,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            responsible_person="John Example",
        )

    def create_participants(self, amount: int) -> None:
        for index in range(amount):
            Participant.objects.create(
                event=self.event,
                first_name=f"First{index}",
                last_name=f"Last{index}",
                gender=Participant.Gender.DIVERSE,
                birth_date=date(2000, 1, 1),
            )

    def test_context_contains_event_metadata(self) -> None:
        context = build_participant_list_context(
            self.event,
            issued_on=date(2026, 9, 16),
        )

        self.assertEqual(context["event"]["id"], self.event.pk)
        self.assertEqual(context["event"]["title"], "Context Test Event")
        self.assertEqual(
            context["event"]["responsible_person"],
            "John Example",
        )

    def test_context_contains_calculated_participant_age(self) -> None:
        Participant.objects.create(
            event=self.event,
            first_name="Alice",
            last_name="Example",
            gender=Participant.Gender.FEMALE,
            birth_date=date(2000, 5, 10),
        )

        context = build_participant_list_context(
            self.event,
            issued_on=date(2026, 9, 16),
        )

        self.assertEqual(context["participant_count"], 1)
        self.assertEqual(context["participants"][0]["age"], 26)
        self.assertEqual(context["participants"][0]["gender"], "Female")

    def test_context_shows_notice_for_more_than_25_participants(self) -> None:
        self.create_participants(26)

        context = build_participant_list_context(
            self.event,
            issued_on=date(2026, 9, 16),
        )

        self.assertEqual(context["participant_count"], 26)
        self.assertTrue(context["show_large_participant_notice"])

    def test_context_hides_notice_for_exactly_25_participants(self) -> None:
        self.create_participants(25)

        context = build_participant_list_context(
            self.event,
            issued_on=date(2026, 9, 16),
        )

        self.assertEqual(context["participant_count"], 25)
        self.assertFalse(context["show_large_participant_notice"])

    def test_context_contains_company_contact_data(self) -> None:
        context = build_participant_list_context(
            self.event,
            issued_on=date(2026, 9, 16),
        )

        self.assertIn("company", context)
        self.assertIn("name", context["company"])
        self.assertIn("address", context["company"])
        self.assertIn("email", context["company"])
        self.assertIn("phone", context["company"])
        self.assertIn("legal_notice", context["company"])


class EventAdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.invalid",
            password="safe-test-password",
        )
        self.event = Event.objects.create(
            title="Admin Test Event",
            start_at=datetime(
                2026,
                10,
                1,
                9,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            end_at=datetime(
                2026,
                10,
                1,
                17,
                0,
                tzinfo=ZoneInfo("Europe/Berlin"),
            ),
            responsible_person="Admin Example",
        )
        self.change_url = reverse(
            "admin:events_event_change",
            args=[self.event.pk],
        )
        self.generate_url = reverse(
            "admin:events_event_generate_participant_list",
            args=[self.event.pk],
        )

    def test_change_view_requires_authentication(self) -> None:
        response = self.client.get(self.change_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_change_view_displays_pdf_generation_link(self) -> None:
        self.client.force_login(self.admin_user)

        response = self.client.get(self.change_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Generate participant list PDF")
        self.assertContains(response, self.generate_url)

    def test_generate_view_requires_authentication(self) -> None:
        response = self.client.get(self.generate_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
