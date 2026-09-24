from io import BytesIO

from django.contrib import admin, messages
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse

from .models import Event, Participant
from .services import DocumentGenerationError, generate_participant_list


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    change_form_template = "admin/events/event/change_form.html"

    list_display = (
        "id",
        "title",
        "start_at",
        "end_at",
        "responsible_person",
    )
    search_fields = (
        "title",
        "responsible_person",
    )
    ordering = (
        "start_at",
        "id",
    )

    def get_urls(self):
        custom_urls = [
            path(
                "<int:event_id>/generate-participant-list/",
                self.admin_site.admin_view(
                    self.generate_participant_list_view
                ),
                name="events_event_generate_participant_list",
            ),
        ]
        return custom_urls + super().get_urls()

    def generate_participant_list_view(
            self,
            request: HttpRequest,
            event_id: int,
    ) -> FileResponse:
        event = get_object_or_404(
            Event.objects.prefetch_related("participants"),
            pk=event_id,
        )

        try:
            document = generate_participant_list(event)
        except NotImplementedError:
            messages.info(
                request,
                "No PDF generation engine is implemented on the main branch.",
            )
            return redirect(
                reverse(
                    "admin:events_event_change",
                    args=[event.pk],
                )
            )
        except DocumentGenerationError:
            messages.error(
                request,
                "The participant list could not be generated.",
            )
            return redirect(
                reverse(
                    "admin:events_event_change",
                    args=[event.pk],
                )
            )

        pdf_buffer = BytesIO(document.content)
        pdf_buffer.seek(0)

        return FileResponse(
            pdf_buffer,
            content_type=document.content_type,
            as_attachment=True,
            filename=document.filename,
        )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "event",
        "gender",
        "birth_date",
    )
    list_filter = (
        "gender",
        "event",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    list_select_related = (
        "event",
    )
    ordering = (
        "last_name",
        "first_name",
        "id",
    )
