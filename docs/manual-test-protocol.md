# Manuelles Prüfprotokoll: docx-mailmerge2

Stand: 2026-09-24. Die Einträge beruhen auf den berichteten lokalen Versuchen. Die
Bezeichnung „bestanden“ bezieht sich ausschließlich auf das genannte Teilkriterium und
nicht auf die vollständige PDF-Teilnehmerliste. Keine der folgenden Dateien ist als
PDF-Prüfbeleg zu verstehen.

| Datum      | Prüffall                                                            | Ergebnis                                  | Beobachtung und Grenze                                                                                                                                       |
|------------|---------------------------------------------------------------------|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-09-24 | MergeFields in der Word-Vorlage erkennen                            | Bestanden                                 | `get_merge_fields()` gab neun erwartete Veranstaltungs- und Teilnehmerfelder zurück.                                                                         |
| 2026-09-24 | Einfache DOCX-Erzeugung mit dynamischer Teilnehmerzeile             | Bestanden                                 | Die einfache Ausgabe funktionierte nach eigener Prüfung. Die vollständige Prüfung sämtlicher Datensätze ist noch offen.                                      |
| 2026-09-24 | Word-IF-Feld für den bedingten Hinweis                              | Bestanden                                 | Die bedingte Ausgabe funktionierte. Eine getrennte Prüfung der Grenzfälle mit 25 und 60 Teilnehmern sollte protokolliert werden, falls bereits durchgeführt. |
| 2026-09-24 | Verschiedene Absatzformatierungen durch getrennte IF-Felder         | Bestanden                                 | Die unterschiedlichen Absatzformatierungen waren im Ergebnis sichtbar.                                                                                       |
| 2026-09-24 | Rote und kursive Passagen innerhalb eines IF-Feldresultats erhalten | Nicht bestanden                           | Die unterschiedlich gestalteten Passagen erschienen im Ergebnis einheitlich normal formatiert.                                                               |
| 2026-09-24 | Separaten Kontakt- und Rechtsblock mit `INCLUDETEXT` einbinden      | Nicht nachgewiesen                        | Der Versuch gelang nicht. Die technische Ursache wurde nicht abschließend bestimmt.                                                                          |
| 2026-09-24 | Großes Logo auf Seite 1 und kleines Logo auf Folgeseiten            | Bestanden                                 |                                                                                                                                                              |
| 2026-09-24 | Seitenzahl auf jeder PDF-Seite                                      | Bestanden                                 |                                                                                                                                                              |
| 2026-09-24 | Wiederholung der Tabellenkopfzeile                                  | Bestanden                                 |                                                                                                                                                              |
| 2026-09-24 | Ungetrennter mehrzeiliger Hinweisblock                              | Bestanden                                 |                                                                                                                                                              |
| 2026-09-24 | Vollständigkeit aller Teilnehmerdaten in der PDF                    | Bestanden                                 |                                                                                                                                                              |
| 2026-09-24 | Kontakt- und Rechtsblock als inkludierte Datei                      | Nicht bestanden                           | INCLUDETEXT hat nicht funktioniert, als einzelne Felder könnte man sie natürlich einfügen.                                                                   |
| Offen      | Keine sichtbaren PDF-Layoutfehler                                   | Nicht geprüft                             |                                                                                                                                                              |

## Ablage von Nachweisen

Nur wenn tatsächlich Screenshots oder Beispiel-PDFs erzeugt wurden, den lokalen
Speicherort hier eintragen. 
