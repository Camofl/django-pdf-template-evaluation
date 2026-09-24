# Evaluation: Carbone Community

Stand: 25. September 2026. Grundlage sind der gepushte Branch `prototype/carbone`, die gemeinsame Fixture mit 60 und 25 Teilnehmern sowie die berichteten lokalen Funktions- und Sichtprüfungen. Beobachtung und Einordnung bleiben getrennt. Die Bewertung bezieht sich ausschließlich auf den Betrieb ohne Lizenzschlüssel.

## Implementierungsaufwand

**Beobachtung:** Die ersten Variablen, die Wiederholung einer Teilnehmerzeile und der bedingte Hinweis ließen sich mit Tags in einer Word-Vorlage umsetzen. Für Django war ein HTTP-Aufruf an einen separaten Carbone-Container notwendig. Exakte Arbeitszeiten wurden nicht erhoben.

**Einordnung:** Die subjektiv zügige Umsetzung ist positiv, erlaubt aber keinen isolierten Geschwindigkeitsvergleich. Datenmodell, Fixture, Admin-Route, Gotenberg-Erfahrung und Word-Layoutkenntnisse lagen aus den vorherigen Prototypen bereits vor. Der Lerneffekt begünstigte den dritten Kandidaten.

## Fehleranfälligkeit

**Beobachtung:** Die Tabelle blieb zunächst leer, weil in der Vorlage `participant` statt des übergebenen JSON-Schlüssels `participants` verwendet wurde. Nach Korrektur funktionierte die Ausgabe.

**Einordnung:** Tags sind gut lesbar, aber die Referenz auf JSON-Felder muss exakt stimmen. Der Fehler war im isolierten Versuch leicht zu lokalisieren. Daraus folgt noch keine allgemeine Aussage über die Fehlerrate.

## Praktische Stabilität

**Beobachtung:** Der lokale Status-Endpunkt meldete Version 5.14.5 als verfügbar. PDF-Erzeugung und Admin-Download funktionierten. Der explizit aktivierte Live-Test bestand nach Angabe des Entwicklers. Belastungstests, Fehlerfallserien und drei dokumentierte Laufzeitmessungen fehlen.

**Einordnung:** Für den Referenzfall ist die Funktion nachgewiesen. Allgemeine Aussagen zu Verfügbarkeit und Leistung bleiben offen.

## Integration in Django

**Beobachtung:** `events/services.py` liest die DOCX-Vorlage, kodiert sie als Base64 und sendet sie mit dem aus der gemeinsamen Domäne abgeleiteten JSON an den lokalen Endpunkt `/render/template`. Die PDF wird aus der vorhandenen Admin-Änderungsansicht heruntergeladen.

**Einordnung:** Die Anbindung ist überschaubar. Ein separater selbst betriebener Dienst ist dennoch erforderlich. Die Vorlage wird bei jedem Download erneut übertragen. Kurzbeleg: Carbone, o. J.

## Bearbeitbarkeit der Vorlage

**Beobachtung:** Variablen, Tabellenzeilen, der bedingte Hinweis und ein eingebauter Formatter wurden als Tags in Word 365 bearbeitet. Der bedingte Block und seine Formatierung funktionierten laut Sichtprüfung.

**Einordnung:** Die Gestaltung verbleibt weitgehend im vom Kunden vertrauten Word-Dokument. Die Tags erfordern dennoch Kenntnisse der Carbone-Syntax. Eingebaute Formatter sind für die Bearbeitbarkeit ein zusätzlicher Vorteil, der im ursprünglichen Testkatalog nicht als eigenes Merkmal vorgesehen war. Eine automatische Übernahme vorhandener Django-Filter wurde nicht geprüft. Kurzbeleg: Carbone, o. J.

## Dynamische Tabelle und Seitenumbrüche

**Beobachtung:** Der Live-Test prüft Teilnehmernamen für 60 und 25 Datensätze sowie mehr als eine PDF-Seite für die große Veranstaltung. Die Wiederholung der Tabellenüberschrift und die Seitenumbrüche funktionierten laut manueller Sichtprüfung.

**Einordnung:** Die mehrseitige Tabellenanforderung ist für die Referenzdaten erfüllt. Der Live-Test allein belegt jedoch weder die Position jeder Kopfzeile noch die Qualität der Seitenumbrüche.

## Bedingte Logik

**Beobachtung:** Der Hinweis war bei 60 Teilnehmern sichtbar und bei 25 nicht. Die Bedingung befand sich in der Word-Vorlage. Der mehrzeilige Block blieb laut Sichtprüfung zusammen. Der Live-Test prüft den Hinweis zusätzlich im extrahierten PDF-Text.

**Einordnung:** Der Block ist im getesteten Szenario ohne Python-seitiges Einsetzen des vollständigen Hinweistextes kundenbearbeitbar. Die Community-Funktionen für bedingte Blöcke sind hierfür relevant. Kurzbeleg: Carbone, o. J.

## Header, Footer und Seitenzahlen

**Beobachtung:** Großes Logo auf der ersten und kleines Logo auf den folgenden Seiten sowie Seitenzahlen und Tabellenkopf funktionierten laut manueller PDF-Prüfung. Die verwendeten Logos sind statische Inhalte der Word-Vorlage.

**Einordnung:** Diese Layoutteile erfordern keine kostenpflichtige dynamische Bildfunktion. Die Prüfung ist visuell und nicht durch seitenweise Screenshots belegt.

## Template-Inklusion

**Beobachtung:** Die Einbindung eines zweiten, separat bearbeitbaren Kontakt- und Rechtsdokuments wurde im Community-Prototyp nicht umgesetzt. Der Kontakt- und Rechtsblock fehlt daher im erzeugten Dokument. Ein manuell kopierter Block wäre keine gleichwertige Inklusion.

**Einordnung:** Dies ist die einzige vom Entwickler als nicht erfüllt berichtete Dokumentanforderung. Die Aussage betrifft den getesteten kostenlosen Ansatz, nicht jede theoretisch denkbare Kombination von Word-Feldern und externen Werkzeugen.

## PDF-Konvertierung

**Beobachtung:** Das verwendete vollständige Carbone-Image erzeugte sowohl DOCX als auch PDF. Ein separater Gotenberg-Dienst wurde für diesen Kandidaten nicht benötigt. Die PDFs waren lesbar und erfüllten laut Sichtprüfung die geforderten Layoutmerkmale mit Ausnahme des fehlenden Kontaktblocks.

**Einordnung:** Ein Dienst weniger ist für den konkreten Aufbau vorteilhaft. Der technische Gesamtvergleich muss beachten, dass Carbone seine eigene LibreOffice-Umgebung verwendet, während die anderen beiden Kandidaten über Gotenberg konvertiert wurden. Mögliche Layout- und Laufzeitunterschiede können daher nicht allein dem Template-System zugeschrieben werden.

## Abweichungen von der Erwartung aus Phase 1

**Beobachtung:** Variablen, mehrseitige Tabelle, bedingter Block, Layout und ein zusätzlicher Formatter funktionierten im lokalen Versuch. Die separat bearbeitbare Inklusion blieb aus.

**Einordnung:** Die breite Funktionsabdeckung der kostenlosen Variante war im konkreten Fall höher als eine bloße Betrachtung einzelner Bibliotheksfunktionen erkennen ließe. Die fehlende Inklusion bleibt relevant für das Ziel wiederverwendbarer Kundenvorlagen.

## Vorläufiges Fazit

Carbone Community erfüllte im getesteten Teilnehmerlistenfall nahezu alle geforderten Ausgabe- und Layoutmerkmale. Ein zweiter, kundenbearbeitbarer Dokumentbaustein konnte nicht eingebunden werden. Das günstige Aufwandsempfinden wird als Beobachtung dokumentiert, aber wegen des Lerneffekts nicht als objektiver Vorsprung gegenüber den zuerst implementierten Kandidaten gewertet.
