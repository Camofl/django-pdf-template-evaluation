from datetime import datetime

from django.template.defaultfilters import date as django_date_filter
from django.utils import timezone
from jinja2 import Environment


def django_date(value, format_string="D d M Y"):
    if isinstance(value, datetime) and timezone.is_aware(value):
        value = timezone.localtime(value)

    return django_date_filter(value, format_string)


def initials(value):
    return "".join(part[0].upper() for part in str(value).split() if part)


def build_document_environment():
    environment = Environment()
    environment.filters["django_date"] = django_date
    environment.filters["initials"] = initials
    return environment
