# Implementation Log: docxtpl

## 2026-09-23: Create the initial participant list template

- Goal: Create an editable Word template for the participant list.
- Implementation: Created the main DOCX template in Microsoft Word 365 with event placeholders, a participant table using docxtpl row tags, and a conditional notice.
- Observation: The document can be edited in Word 365. The first-page and subsequent-page headers have not yet been configured separately.
- Effort evidence: One new DOCX template; Word layout and template tags were prepared manually. No reliable implementation time was recorded.
- Verification: The template structure was reviewed in Word 365. Automated rendering and PDF output have not yet been verified.
- Issues encountered: None documented so far.
- Open points: Configure different header logos, include the company address from a reusable document component, and verify DOCX rendering.
- Affected files: events/document_templates/participant_list.docx

## 2026-09-24: Correct pagination settings in the DOCX template

- Goal: Verify and correct pagination behavior for the dynamic participant table and the multi-line notice block.
- Implementation:
  - Reviewed the table-row properties in Microsoft Word 365.
  - Disabled the repeated-header-row setting for the dynamic participant data row.
  - Kept the repeated-header-row setting enabled only for the static column-header row.
  - Enabled the paragraph setting that keeps lines of the visible notice block together on one page.
  - Excluded the docxtpl control paragraphs containing `{%p ... %}` from the pagination setting.
- Observation:
  - The dynamic participant row was initially configured as a repeated table header. After rendering, this caused the generated participant table to move to the next page unexpectedly.
  - The visible multi-line notice block could initially be split across two pages.
  - After correcting the Word settings, the participant table and the notice block showed the intended pagination behavior.
- Effort evidence:
  - One DOCX template was revised.
  - Two Word pagination settings were identified and corrected.
  - The corrections required manual rendering and visual verification.
- Issues encountered:
  - Repeated-header-row formatting was inherited by the template row that docxtpl duplicates for each participant.
  - Paragraph pagination settings must not be applied to docxtpl control paragraphs.
- Resolution or open point:
  - The template behavior was corrected in Microsoft Word 365.
  - The behavior still needs to be verified again after DOCX-to-PDF conversion.
- Affected files:
  - events/document_templates/participant_list.docx
  - docs/implementation-log.md

## 2026-09-24: Resolve font change during PDF conversion

- Goal: Check whether the rendered DOCX retains its typography after PDF conversion.
- Implementation: Generated a PDF through the locally operated Gotenberg service. Changed the main Word template font from Aptos to Arial and generated the PDF again.
- Observation: Text formatted with Aptos in Word appeared in a different font in the first PDF, visually resembling Times New Roman. After changing the template to Arial, the PDF appearance matched the expected layout more closely.
- Effort evidence: One DOCX template revision and two visual PDF checks. No implementation time was recorded.
- Possible cause: The converter may not have had Aptos available. The installed fonts and embedded PDF fonts have not yet been checked.
- Resolution: Arial is used as a practical template choice for this prototype. Installing additional fonts in the Gotenberg image is outside the current implementation scope.
- Open point: The actual font embedded or substituted in the PDF has not been identified.
- Affected files: events/document_templates/participant_list.docx, contact_legal_block.docx

## 2026-09-24: Explore template filters

- Goal: Determine whether formatting and custom presentation logic can be used inside the DOCX template.
- Implementation: Added a Jinja environment with a custom `initials` filter and a `django_date` adapter for Django's built-in date filter. Passed the environment to the docxtpl rendering call.
- Observation: The prototype can register filters for use in the Word template and they actually work.
- Effort evidence: One new Python module, one service change, and a revised DOCX template. No implementation time was recorded.
- Limitation: Reuse of an existing custom Django `templatetags` module has not yet been tested.
- Affected files: events/document_filters.py, events/services.py, events/document_templates/participant_list.docx

## 2026-09-24: Verify content in converted PDFs

- Goal: Check whether expected content remains available after DOCX-to-PDF conversion.
- Implementation: Generated PDFs for the reference events with Gotenberg and checked extracted PDF text.
- Observation: The tested participant content was present. The notice appeared for the event with 60 participants and was absent for the event with 25 participants.
- Effort evidence: Automated PDF text checks for two fixture events; no implementation time recorded.
- Limitation: Text extraction does not verify visual layout, fonts or page breaks.
- Affected files: events/test_document_generation.py, docs/implementation-log.md