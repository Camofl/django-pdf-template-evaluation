# Manual Test Protocol: docxtpl

| Date       | Test document         | Test criterion                                                                    | Result | Observation                                                                                  |
|------------|-----------------------|-----------------------------------------------------------------------------------|--------|----------------------------------------------------------------------------------------------|
| 2026-09-24 | Large Reference Event | The table column-header row repeats on subsequent pages.                          | Passed | The static column-header row was repeated correctly.                                         |
| 2026-09-24 | Large Reference Event | The participant table starts at the expected position and continues across pages. | Passed | The table no longer moved unexpectedly to the next page after the row setting was corrected. |
| 2026-09-24 | Large Reference Event | The conditional notice is displayed and not split across two pages.               | Passed | The visible notice paragraph used the Word pagination setting for keeping lines together.    |
| 2026-09-24 | Small Control Event   | The conditional notice is not displayed.                                          | Passed | The if condition works as intended.                                                          |
| 2026-09-24 | Large Reference Event | The large first-page logo and small subsequent-page logo are displayed correctly. | Passed | Verified in the rendered DOCX document.                                                      |
| 2026-09-24 | Large Reference Event | Page numbers are visible in the footer on every page.                             | Passed | Verified in the rendered DOCX document.                                                      |
| 2026-09-24 | Large Reference Event | The company and legal block appears in the footer.                                | Passed | Verified in the rendered DOCX document.                                                      |

## PDF conversion test: docxtpl and Gotenberg

- Date: 2026-09-24
- Input: DOCX documents rendered from the reference fixture
- Conversion: Locally operated Gotenberg service using LibreOffice
- Test documents: Large Reference Event and Small Control Event
- Verification method: Download through the Django admin and visual inspection of the
  resulting PDF

| Test criterion                                           | Large event | Small event    | Observation                                                                                 |
|----------------------------------------------------------|-------------|----------------|---------------------------------------------------------------------------------------------|
| PDF downloads from the admin change view and opens       | Passed      | Passed         | Record the actual result.                                                                   |
| All participant records are present                      | Passed      | Passed         | Check the first and last records as well as completeness.                                   |
| Notice appears only above 25 participants                | Passed      | Passed         | Expected: visible for 60, absent for 25.                                                    |
| Large first-page logo and small subsequent-page logo     | Passed      | Not applicable | Check each page in the PDF.                                                                 |
| Page number is present on every page                     | Passed      | To verify      | Check the first and final pages.                                                            |
| Table header repeats without repeating a participant row | Passed      | Not applicable | Inspect each page transition.                                                               |
| Multi-line notice remains on one page                    | Passed      | Not applicable | Inspect the notice near a page transition.                                                  |
| Company and legal block appears at the document end      | Passed      | Passed         | Check content and placement.                                                                |
| Typography matches the intended template appearance      | Passed      | Passed         | Aptos appeared visually different; Arial gave the intended appearance in the inspected PDF. |
| No other visible layout differences                      | Passed      | Passed         | Note spacing, page breaks and overflow.                                                     |

### Font observation

In the initial Word template, text was formatted with Aptos. After conversion, the PDF
typography appeared visibly different and resembled Times New Roman. Changing the
template font to Arial produced the intended visual appearance in the inspected PDF.

The actual PDF font and the cause of the substitution have not been technically
verified. Installing additional fonts in the converter was not part of this prototype
step.