# Evaluation: docxtpl

## Dynamic table and page breaks

### Objective observation

The participant table is rendered dynamically by duplicating a DOCX template row.

During the initial template configuration, the repeated-header-row setting was enabled
for both the static column-header row and the dynamic participant data row. The dynamic
row was therefore treated as a table header after rendering. This resulted in unexpected
pagination behavior in the generated document.

The issue was corrected by enabling the repeated-header-row setting only for the static
column-header row. The dynamic row containing the participant variables was excluded
from this setting.

### Interpretation

The result shows that docxtpl can generate multi-page participant tables with repeated
column headers. However, the correct behavior depends on precise Word table formatting.

The template author must distinguish between static table-header rows and rows that are
duplicated by docxtpl. Incorrect inheritance of Word table properties can cause layout
defects that are not evident from the Python code alone.

### Assessment

The dynamic table requirement is fulfilled after correcting the DOCX template.

The observed issue increases the template maintenance and review effort. It represents a
potential error source, especially when templates are edited by users without detailed
knowledge of Word table properties and docxtpl row generation.

## Multi-line notice block

### Objective observation

The visible multi-line notice text was initially split across two pages.

The issue was corrected in Microsoft Word 365 by applying the paragraph pagination
setting that keeps the lines of the visible notice paragraph together.

The docxtpl control paragraphs containing `{%p if ... %}` and `{%p endif %}` were
excluded from this setting.

### Interpretation

The requirement for a non-separated notice block can be fulfilled through Word paragraph
formatting. The solution is template-based and does not require additional Python logic.

### Assessment

The requirement is fulfilled in the rendered DOCX document.

The behavior depends on the correct configuration of Word paragraph settings. It must
therefore be checked visually for every relevant template revision and again after PDF
conversion.

## PDF conversion

### Objective observation

The DOCX template rendered successfully and the PDF was generated through the locally
operated Gotenberg service. Text set in Aptos in Microsoft Word 365 appeared with
visibly different typography in the PDF. Changing the template font to Arial improved
the visual agreement with the Word document.

### Interpretation

The conversion result depends not only on docxtpl and the Word template but also on the
font environment of the LibreOffice-based conversion service. A missing font is a
plausible cause of the observed substitution, but the specific cause has not been
verified.

### Assessment

PDF generation is functional for the tested documents. Typography and potentially
pagination remain environment-dependent. For this prototype, the template uses Arial
instead of extending the Gotenberg image with additional fonts.