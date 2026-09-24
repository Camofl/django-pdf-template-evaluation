# Manuelles Prüfprotokoll: Carbone Community

Stand: 25. September 2026. Die Ergebnisse „bestanden“ für Layout und Darstellung beruhen auf der vom Entwickler berichteten Sichtprüfung der generierten PDFs. Es liegen keine seitenweise abgelegten Screenshots oder Beispiel-PDFs vor. Automatische Textprüfungen sind separat ausgewiesen. Die Fixture enthält eine große Veranstaltung mit 60 und eine Kontrollveranstaltung mit 25 Teilnehmern.

## Sichtprüfung

| Datum | Testveranstaltung | Prüfkriterium | Ergebnis | Beobachtung |
|---|---|---|---|---|
| 2026-09-25 | Große Referenzveranstaltung | Großes Logo auf Seite 1, kleines Logo auf Folgeseiten | Bestanden laut Sichtprüfung | Statische Word-Bilder; keine dynamische Bildfunktion. |
| 2026-09-25 | Große Referenzveranstaltung | Seitenzahl in jeder Fußzeile | Bestanden laut Sichtprüfung | Word-Seitenfelder in der generierten PDF sichtbar. |
| 2026-09-25 | Große Referenzveranstaltung | Tabellenüberschrift auf Folgeseiten wiederholt | Bestanden laut Sichtprüfung | Mehrseitige Teilnehmerliste geprüft. |
| 2026-09-25 | Große Referenzveranstaltung | Hinweisblock bei mehr als 25 Teilnehmern sichtbar | Bestanden | Bedingung in der Word-Vorlage; durch PDF-Textprüfung ergänzt. |
| 2026-09-25 | Kontrollveranstaltung | Hinweisblock bei 25 Teilnehmern ausgeblendet | Bestanden | Durch PDF-Textprüfung ergänzt. |
| 2026-09-25 | Große Referenzveranstaltung | Mehrzeiligen Hinweisblock nicht über Seiten trennen | Bestanden laut Sichtprüfung | Kein unerwünschter Umbruch beobachtet. |
| 2026-09-25 | Beide Veranstaltungen | Vollständige Teilnehmerdaten | Bestanden für getestete Nachnamen | Die automatisierte PDF-Prüfung erfasste sämtliche Nachnamen. Weitere einzelne Feldwerte wurden nicht vollständig automatisiert abgeglichen. |
| 2026-09-25 | Große Referenzveranstaltung | Kontakt- und Rechtsblock aus zweiter Vorlage | Nicht bestanden | Keine dokumentierte Community-Inklusion im Prototyp; Block fehlt. |
| 2026-09-25 | Beide Veranstaltungen | Keine sichtbaren sonstigen Layoutfehler | Bestanden laut Sichtprüfung | Kein auffälliger Fehler berichtet; keine pixelgenaue Prüfung. |
| 2026-09-25 | Beide Veranstaltungen | Eingebauten Formatter in Word-Tag verwenden | Bestanden | Ein Formatter wurde zusätzlich zum Pflichtkatalog lokal erprobt. |

## Automatisierte Prüfungen

| Datum | Prüfschritt | Ergebnis | Grenze |
|---|---|---|---|
| 2026-09-25 | Vorlage und 60 Teilnehmer an lokalen Carbone-Endpunkt übergeben | Bestanden laut lokalem Testlauf | Gemockte HTTP-Antwort belegt noch keine PDF-Konvertierung. |
| 2026-09-25 | PDF-Header und Download-Dateiname der Admin-Aktion | Bestanden laut lokalem Testlauf | Verwendete Mock-Bytes sind keine vollständige PDF. |
| 2026-09-25 | Live-Test mit `RUN_CARBONE_TESTS=1` | Bestanden laut lokalem Testlauf | Liest echte PDFs mit pypdf, prüft Titel, Nachnamen, Mehrseitigkeit und Hinweisgrenze; keine visuelle Layoutprüfung. |

## Nachweisgrenze

Die Tests liegen in `events/test_document_generation.py`. Der Live-Test wird nur bei gesetztem `RUN_CARBONE_TESTS=1` ausgeführt. Für eine spätere, unabhängige Reproduktion sollten Beispiel-PDFs oder anonymisierte Screenshots, konkrete Geräteangaben sowie mindestens drei Messungen der Downloadzeit ergänzt werden. Solche Messwerte wurden bisher nicht berichtet.
