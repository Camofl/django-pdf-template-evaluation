# Django PDF Template Evaluation

## Purpose

This project provides a research prototype for evaluating different approaches
to PDF generation in a Django application.

The prototype compares the following approaches:

- Carbone
- docx-mailmerge2
- docxtpl

The project uses an event and participant domain model. A participant list can
be generated from the Django admin change view of an event.

## Scope

The `main` branch contains only the shared Django application structure:

- Event and participant domain model
- Django admin integration
- Shared document generation service contract
- Test fixture data
- Automated tests
- Documentation structure

The `main` branch does not contain a PDF generation engine.

The individual approaches are implemented on separate branches:

- `prototype/carbone`
- `prototype/docx-mailmerge2`
- `prototype/docxtpl`

## Prerequisites

- Python 3.12 or newer
- pip
- Git

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Load fixture data:

```bash
python manage.py loaddata events
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the Django admin interface:

```text
http://127.0.0.1:8000/admin/
```

## Tests

Run all automated tests:

```bash
python manage.py test
```

## Document Generation

The `main` branch defines a shared service interface in `events/services.py`.

The document generation function intentionally raises `NotImplementedError` on
the `main` branch. A concrete implementation is added only in the respective
prototype branch.