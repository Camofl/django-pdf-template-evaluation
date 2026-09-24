# Manuelles Prüfprotokoll: docx-mailmerge2

Stand: 24. September 2026. „Bestanden“ bezieht sich jeweils auf den genannten Prüfschritt. Automatisierte Tests und visuelle Beobachtungen werden getrennt ausgewiesen. Es wurden keine Screenshots oder Beispiel-PDFs als versionierte Nachweise angegeben.

## DOCX-Vorlage und Feldverarbeitung

| Datum | Prüfschritt | Ergebnis | Beobachtung |
|---|---|---|---|
| 2026-09-24 | Neun echte MergeFields erkennen | Bestanden | `get_merge_fields()` erkannte die Veranstaltungs- und Teilnehmerfelder. |
| 2026-09-24 | Dynamische Teilnehmerliste erzeugen | Bestanden | Das einfache Preview lieferte eine DOCX mit befüllter Teilnehmerzeile. Die Vollständigkeit wird zusätzlich automatisiert geprüft. |
| 2026-09-24 | IF-Bedingung in Word verwenden | Bestanden | Bedingte Ausgabe funktionierte im lokalen Versuch. |
| 2026-09-24 | Verschiedene Absatzformatierungen mit getrennten IF-Feldern | Bestanden | Die Absätze konnten unterschiedlich formatiert werden. |
| 2026-09-24 | Rote und kursive Zeichen innerhalb eines IF-Feldresultats erhalten | Nicht bestanden | Die Unterschiede gingen im erzeugten Ergebnis verloren. |
| 2026-09-24 | Separaten Kontaktblock mit `INCLUDETEXT` einbinden | Nicht nachgewiesen | Die automatische Inklusion gelang nicht. Die Fehlerursache wurde nicht isoliert. |

## PDF-Konvertierung und Sichtprüfung

| Datum | Prüfschritt | Ergebnis | Beobachtung und Grenze |
|---|---|---|---|
| 2026-09-24 | Preview-DOCX mit lokalem Gotenberg konvertieren | Bestanden | Eine lesbare PDF wurde im isolierten Konvertierungsversuch erzeugt. |
| 2026-09-24 | PDF im Django-Admin herunterladen | Bestanden | Der Download funktionierte für die getesteten Veranstaltungen. |
| 2026-09-24 | PDF-Layout mit erzeugter DOCX vergleichen | Bestanden als Sichtprüfung | Laut eigener Prüfung waren keine wahrnehmbaren Unterschiede erkennbar. Keine pixelgenaue Analyse. |
| 2026-09-24 | Großes Logo auf Seite 1 und kleines Logo auf Folgeseiten | Nicht einzeln protokolliert | Gesamteindruck DOCX und PDF war gleich. Die Logos wurden nicht mit seitenweisen Bemerkungen belegt. |
| 2026-09-24 | Seitenzahl auf jeder PDF-Seite | Nicht einzeln protokolliert | Die Fußzeile enthält Seitenangaben. Eine seitenweise Kontrolle wurde nicht berichtet. |
| 2026-09-24 | Tabellenkopf auf Folgeseiten wiederholt | Nicht einzeln protokolliert | Aus dem allgemeinen Layoutvergleich folgt kein eigenständiger Nachweis jedes Seitenübergangs. |
| 2026-09-24 | Mehrzeiligen Hinweis ohne Trennung anzeigen | Nicht einzeln protokolliert | Die Bedingung ist getestet, die Lage an einem Seitenübergang nicht gesondert dokumentiert. |
| 2026-09-24 | Kontakt- und Rechtsblock aus zweiter Datei im Footer | Nicht bestanden | Der Block wurde nach dem erfolglosen Inklusionsversuch entfernt. Der Footer enthält nur die Seitenangabe. |
| 2026-09-24 | Keine auffälligen sonstigen Layoutabweichungen zwischen DOCX und PDF | Bestanden als Sichtprüfung | Keine wahrnehmbaren Unterschiede berichtet. |

## Automatisierte Prüfungen

| Datum | Prüfschritt | Ergebnis | Grenze |
|---|---|---|---|
| 2026-09-24 | Gerenderte DOCX enthält Veranstaltungstitel und Teilnehmernachnamen | Bestanden laut lokalem Testlauf | Der HTTP-Aufruf an Gotenberg wird hierbei gemockt. |
| 2026-09-24 | Admin liefert PDF-Header und Download-Dateinamen | Bestanden laut lokalem Testlauf | Die verwendeten Mock-Bytes sind keine gültige PDF. |
| 2026-09-24 | Live-Test mit `RUN_GOTENBERG_TESTS=1` | Bestanden laut lokalem Testlauf | Prüft lesbare PDFs, Text für 60 und 25 Teilnehmer, mehrseitige große Ausgabe und bedingten Warntext. Prüft kein Layout. |

## Nachweisgrenze

Die Testdatei `events/test_document_generation.py` und die Word-Vorlage liegen im Branch. Der lokale Live-Test wurde vom Entwickler erfolgreich ausgeführt. Ein CI-Protokoll, konkrete Laufzeiten und abgelegte Beispiel-PDFs wurden nicht angegeben. Für eine vollständige visuelle Endabnahme sollten Logo, Seitenzahl, Tabellenkopf und Hinweisblock pro relevanter Seite mit konkreter Bemerkung erneut geprüft werden.
