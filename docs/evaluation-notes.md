# Evaluation: docx-mailmerge2

Stand: 2026-09-24. Diese Bewertung bezieht sich auf die bislang berichteten lokalen
Versuche. Sie ist kein abschließender Vergleich mit docxtpl oder Carbone. Die
tatsächliche DOCX-Vorlage und die lokale Preview-Implementierung wurden bislang nicht
anhand eines gepushten Commits geprüft.

## Implementierungsaufwand

**Beobachtung:** Eine Vorlage mit neun echten Word-MergeFields wurde erstellt. Alle neun
Feldnamen konnten mit `get_merge_fields()` erkannt werden. Eine einfache Erzeugung mit
dynamischer Teilnehmerzeile funktionierte im lokalen Versuch.

**Einordnung:** Die anfängliche Datenübergabe ist überschaubar. Der Aufwand für das
manuelle Anlegen und Pflegen von Word-Feldfunktionen muss getrennt vom Python-Code
bewertet werden. Die Beobachtung des Nutzers deutet auf höheren Pflegeaufwand bei
komplexeren bedingten Blöcken hin. Es liegen keine erhobenen Implementierungszeiten vor.

## Fehleranfälligkeit

**Beobachtung:** Mehrere IF-Felder ermöglichten unterschiedliche Absatzformatierungen.
Eine innerhalb eines IF-Feldresultats rot und kursiv gestaltete Passage erschien im
erzeugten Ergebnis dagegen ohne diese unterschiedlichen Zeichenformatierungen.

**Einordnung:** Eine erfolgreiche Bedingungsprüfung allein belegt keine ausreichende
Formatierungstreue. Die Ursache wurde nicht weiter isoliert. Der Effekt wird als
beobachtete Einschränkung des getesteten Gesamtverfahrens dokumentiert, nicht als
allgemeine Aussage über sämtliche Word-Feldkonfigurationen.

## Praktische Stabilität

**Beobachtung:** Die einfache DOCX-Erzeugung funktionierte. Wiederholte Durchläufe,
Fehlerfälle und automatisierte PDF-Tests wurden für diesen Kandidaten noch nicht
dokumentiert.

**Einordnung:** Zur Stabilität des vollständigen Download-Ablaufs ist noch keine
belastbare Aussage möglich.

## Integration in Django

**Beobachtung:** Die bestehende Veranstaltungs- und Teilnehmerdatenbasis wurde für den
lokalen Preview-Versuch genutzt. Eine Anbindung der Dokumenterzeugung an den
Admin-Download ist für diesen Branch noch nicht nachgewiesen.

**Einordnung:** Die Integration kann erst nach Implementierung und Test der
Service-Schnittstelle bewertet werden.

## Bearbeitbarkeit der Vorlage

**Beobachtung:** Feste Felder und die Teilnehmerzeile konnten in Word 365 erstellt
werden. Größere IF-Feldresultate mussten als Feldinhalt gepflegt werden.
Unterschiedliche Zeichenformatierungen innerhalb eines Feldresultats gingen im
getesteten Ergebnis verloren.

**Einordnung:** Die Vorlage ist grundsätzlich in Word bearbeitbar. Bei komplexem,
bedingtem Inhalt ist die Bearbeitung aber weniger unmittelbar als bei normalem
Word-Text. Ein aus Python eingesetzter vollständiger Hinweistext würde das Kriterium
kundenbearbeitbarer Vorlagen nicht gleichwertig erfüllen.

## Dynamische Tabelle und Seitenumbrüche

**Beobachtung:** Die einfache Teilnehmerliste wurde lokal mit einer dynamischen
Tabellenzeile erstellt. Eine dokumentierte Prüfung sämtlicher Datenzeilen, des
wiederholten Tabellenkopfs und der Seitenumbrüche liegt für diesen Kandidaten noch nicht
vor.

**Einordnung:** Eine positive Bewertung mehrseitiger Tabellen wäre derzeit verfrüht.

## Bedingte Logik

**Beobachtung:** Die Word-IF-Bedingung funktionierte im lokalen Versuch. Getrennte
IF-Felder erlaubten verschiedene Absatzformatierungen. Die differenzierte Formatierung
innerhalb eines IF-Feldresultats wurde nicht erhalten.

**Einordnung:** Bedingte Textausgabe ist nachgewiesen. Ein frei formatierbarer,
mehrabsätziger Block mit durchgehend erhaltener Gestaltung ist bislang nicht
nachgewiesen. Der experimentelle Status der IF-Verarbeitung in der
Bibliotheksdokumentation sollte bei der Interpretation berücksichtigt werden. Kurzbeleg:
Projekt docx-mailmerge2, o. J.

## Header, Footer und Seitenzahlen

**Beobachtung:** Für diesen Branch liegt noch kein dokumentiertes Ergebnis zu
unterschiedlich gestalteten Kopfzeilen, fortlaufenden Seitenzahlen oder einem korrekt
gerenderten Kontaktblock im Footer vor.

**Einordnung:** Das Funktionieren von Word-Feldern im Dokumentkörper darf nicht
ungeprüft auf Kopf- und Fußbereiche übertragen werden.

## Template-Inklusion

**Beobachtung:** Die Einbindung einer zweiten DOCX-Datei über `INCLUDETEXT` gelang im
lokalen Versuch nicht. Weder ein aktualisierter Kontaktblock im Ergebnisdokument noch
dessen automatische Übernahme in die PDF wurden nachgewiesen.

**Einordnung:** Word stellt mit `INCLUDETEXT` grundsätzlich eine Feldfunktion für
externe Inhalte bereit. Aus dieser Word-Funktion folgt jedoch keine nachgewiesene,
robuste Teilvorlagen-Inklusion für die Kombination aus docx-mailmerge2 und
automatisierter Konvertierung. Direkt in der Hauptvorlage angelegte MergeFields wären
ein Workaround für den Inhalt, aber kein gleichwertiger Nachweis für
Wiederverwendbarkeit. Kurzbeleg: Microsoft, o. J.; Projekt docx-mailmerge2, o. J.

## PDF-Konvertierung

**Beobachtung:** Für den docx-mailmerge2-Branch wurde noch keine vollständige
automatische Konvertierung und kein PDF-Ergebnis berichtet.

**Einordnung:** Für einen fairen Vergleich soll später derselbe lokal betriebene
Gotenberg-Dienst wie bei docxtpl verwendet und eigenständig auf diesem Branch integriert
werden.

## Abweichungen von der Erwartung aus Phase 1

**Beobachtung:** Die einfache dynamische Tabelle gelang. Dagegen verursachten lange
bedingte Feldresultate Schwierigkeiten bei der visuellen Bearbeitung. Die erwartete
Inklusion eines zweiten Word-Bausteins konnte bislang nicht demonstriert werden.

**Einordnung:** Das Ergebnis spricht für die Eignung bei festen Feldern und
tabellarischen Daten. Die Vorlage stößt im getesteten Szenario bei komplexer
Bedingungsformatierung und modularen Bausteinen an praktische Grenzen. Diese
Einschätzung ist auf den bisherigen Prototypstand beschränkt.

## Vorläufiges Fazit

Die funktionierende einfache DOCX-Erzeugung ist ein positiver Befund. Für die
vorliegende Anforderung ist vor allem die fehlende nachgewiesene, automatisch
aktualisierte Teilvorlagen-Inklusion und die beobachtete Einschränkung bei intern
gemischter Formatierung bedingter Feldresultate relevant. Aussagen zur vollständigen
PDF-Teilnehmerliste, zur Stabilität und zur endgültigen Eignung bleiben bis zur
Service-Integration und zu vergleichbaren Tests offen.
