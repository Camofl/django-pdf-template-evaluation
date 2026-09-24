# Implementierungsprotokoll: Carbone

Stand: 25. September 2026. Dieses Protokoll trennt durchgeführte Arbeitsschritte von offenen Messungen. Exakte Arbeitszeiten wurden nicht erfasst. Die kürzere gefühlte Umsetzungsdauer gegenüber früheren Prototypen darf wegen des bereits aufgebauten Projektwissens nicht allein Carbone zugeschrieben werden.

## 2026-09-25: Kostenlosen lokalen Dienst starten

- Ziel: Carbone ohne Cloud und ohne kostenpflichtige Funktionen lokal betreiben.
- Umsetzung: Das Docker-Image `carbone/carbone-ee:full-5.14.5` über `compose.yaml` nur auf `127.0.0.1:4000` erreichbar gemacht. Kein Lizenzschlüssel wurde konfiguriert.
- Beobachtung: `/status` meldete `success: true`, HTTP-Code 200 und Version 5.14.5. Das Image startet ohne Lizenz im Community-Modus.
- Aufwandsnachweis: Eine Compose-Datei und ein zusätzlich zu betreibender Dienst. Keine Zeitmessung.
- Offener Punkt: Ein unveränderlicher Image-Digest und Betrieb unter Last wurden nicht dokumentiert.
- Betroffene Datei: `compose.yaml`.

## 2026-09-25: Word-Vorlage und JSON-Daten erproben

- Ziel: Kundenbearbeitbare Word-Tags zunächst mit wenigen Veranstaltungswerten überprüfen.
- Umsetzung: Eine neue DOCX-Vorlage mit Carbone-Tags erstellt und über die lokale HTTP-API mit inline übergebener Vorlage und JSON-Daten gerendert. Das Preview später auf beide Veranstaltungen der gemeinsamen Fixture erweitert.
- Beobachtung: Einfache Variablen wurden in eine lesbare PDF eingesetzt. Für die große und kleine Veranstaltung konnten DOCX- und PDF-Vorschauen erzeugt werden.
- Aufwandsnachweis: Eine DOCX-Vorlage und ein Preview-Skript. Keine Zeitmessung.
- Betroffene Dateien: `events/document_templates/participant_list.docx`, `events/preview_carbone.py`, `requirements.txt`.

## 2026-09-25: Dynamische Tabelle und Bedingung prüfen

- Ziel: 60 beziehungsweise 25 Teilnehmer in derselben Dokumentstruktur ausgeben und den Hinweis nur bei mehr als 25 Teilnehmern zeigen.
- Umsetzung: Die Teilnehmerzeile mit Array-Tags wiederholt und den mehrzeiligen Hinweis mit einer Community-Bedingung in der Vorlage gesteuert.
- Beobachtung: Ein zunächst im Singular geschriebener Array-Name passte nicht zum JSON-Schlüssel `participants`. Nach Korrektur wurden die Teilnehmer eingefügt. Der bedingte Block funktionierte im lokalen Versuch.
- Aufwandsnachweis: Eine Korrektur am Datenpfad der Word-Tags und visuelle Prüfungen beider Testfälle. Keine Zeitmessung.
- Lösung: In der Vorlage `participants` verwendet. Die Bedingung bleibt in der Word-Vorlage, nicht in Python als vollständig eingesetzter Text.
- Betroffene Datei: `events/document_templates/participant_list.docx`.

## 2026-09-25: Layout und Formatter prüfen

- Ziel: Logo-Größen, Kopf- und Fußzeilen, Seitenzahlen, Tabellenkopf und ungetrennten Hinweisblock untersuchen. Zusätzlich Formatter als optionales Merkmal erproben.
- Umsetzung: Word-Layout in der Carbone-Vorlage gestaltet und die erzeugten PDFs manuell geprüft. Einen eingebauten Formatter direkt in einem Carbone-Tag ausprobiert.
- Beobachtung: Laut eigener Sichtprüfung funktionierten die geforderten Layoutmerkmale und die Formatierung im PDF. Der erprobte Formatter lieferte das erwartete Ergebnis.
- Aufwandsnachweis: Änderungen an einer Word-Vorlage und manuelle Prüfungen. Keine Zeitmessung.
- Einschränkung: Es liegen keine Screenshots, Seitenprotokolle oder pixelgenauen Bildvergleiche vor. Die Wiederverwendung eigener Django-Filter wurde nicht getestet.
- Betroffene Datei: `events/document_templates/participant_list.docx`.

## 2026-09-25: Teilvorlage abgrenzen

- Ziel: Einen separat bearbeitbaren Kontakt- und Rechtsblock aus einer zweiten Datei in das Dokument übernehmen.
- Umsetzung: Die verfügbaren Community-Funktionen hinsichtlich einer passenden Inklusion eingegrenzt. Keine kostenpflichtige Funktion und kein künstlicher Python-Workaround eingesetzt.
- Beobachtung: Eine automatische Einbindung eines zweiten kundenbearbeitbaren Dokuments wurde in diesem Prototyp nicht erreicht. Der entsprechende Kontakt- und Rechtsblock fehlt damit in der Ausgabe.
- Aufwandsnachweis: Funktionsprüfung und Dokumentation der Grenze. Keine Zeitmessung.
- Ergebnis: Als nicht erfüllte Anforderung ausgewiesen. Es wird keine generelle Unmöglichkeit sämtlicher denkbarer Word-Verknüpfungen behauptet.

## 2026-09-25: Django-Integration und Tests abschließen

- Ziel: Die PDF aus der Admin-Änderungsansicht herunterladen und die gleichen Testfälle wie bei den anderen Kandidaten prüfen.
- Umsetzung: Die Word-Vorlage im Service Base64-kodiert, zusammen mit den fachlichen JSON-Daten an `/render/template` gesendet und die PDF per `FileResponse` ausgeliefert. Gemockte Tests für Übergabe und Admin-Download sowie einen optionalen Live-Test mit `RUN_CARBONE_TESTS=1` ergänzt.
- Beobachtung: Der Admin-Download und die Tests funktionierten laut lokalem Testlauf. Der Live-Test prüft auslesbare PDFs, Teilnehmernamen beider Veranstaltungen, mehrseitige Ausgabe und das bedingte Erscheinen des Hinweises.
- Aufwandsnachweis: Änderungen an Settings, Service und Admin sowie eine Testdatei. Keine Zeitmessung.
- Einschränkung: Automatische Textextraktion prüft nicht die visuelle Position oder Größe von Logos und Seitenzahlen.
- Betroffene Dateien: `config/settings.py`, `events/services.py`, `events/admin.py`, `events/test_document_generation.py`, `requirements.txt`.
