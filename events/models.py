from datetime import date

from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    responsible_person = models.CharField(max_length=255)

    class Meta:
        ordering = ["start_at", "id"]

    def __str__(self) -> str:
        return f"{self.title} ({self.pk})"


class Participant(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"
        DIVERSE = "D", "Diverse"

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    birth_date = models.DateField()

    class Meta:
        ordering = ["last_name", "first_name", "id"]

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    def age_on(self, reference_date: date) -> int:
        years = reference_date.year - self.birth_date.year
        birthday_not_reached = (
                                   reference_date.month,
                                   reference_date.day,
                               ) < (
                                   self.birth_date.month,
                                   self.birth_date.day,
                               )
        return years - int(birthday_not_reached)
