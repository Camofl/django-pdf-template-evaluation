# Evaluation: docx-mailmerge2

Stand: 24. September 2026. Die Beobachtungen beziehen sich auf die gemeinsame Veranstaltungs-Fixture mit 60 und 25 Teilnehmern sowie die bisherige Word-Vorlage. Aussagen über Ursachen und Eignung sind als Interpretation gekennzeichnet.

## Implementierungsaufwand

**Beobachtung:** Neun echte MergeFields wurden in Word 365 erkannt. Die dynamische Teilnehmerzeile ließ sich mit `merge_rows()` füllen. Für IF-Felder und den Versuch einer Teilvorlage waren weitere Word-Feldfunktionen erforderlich. Exakte Arbeitszeiten liegen nicht vor.

**Einordnung:** Die einfache Datenersetzung war überschaubar. Der Aufwand für die manuelle Gestaltung komplexer Feldfunktionen wird durch reine Python-Codezeilen nicht angemessen abgebildet.

## Fehleranfälligkeit

**Beobachtung:** Bedingte Ausgabe und unterschiedliche Absatzformatierungen über mehrere IF-Felder funktionierten. Rote und kursive Passagen innerhalb eines einzelnen Feldresultats verloren ihre differenzierte Formatierung.

**Einordnung:** Die Bedingung selbst ist nicht mit der Gestaltungstreue eines komplexen Textblocks gleichzusetzen. Die technische Ursache des Formatverlusts wurde nicht isoliert.

## Praktische Stabilität

**Beobachtung:** Der lokale Admin-Download funktionierte. Gemockte Tests prüfen die Übergabe und Antwort. Ein explizit aktivierter Live-Test mit Gotenberg lief nach Angabe des Entwicklers erfolgreich. Wiederholte Belastungs- und Fehlerszenarien sowie drei dokumentierte Laufzeitmessungen liegen nicht vor.

**Einordnung:** Aussagen über allgemeine Zuverlässigkeit oder Performanz wären derzeit nicht belegt.

## Integration in Django

**Beobachtung:** `events/services.py` erzeugt eine DOCX aus dem gemeinsamen Kontext, übermittelt sie per HTTP an Gotenberg und gibt PDF-Bytes zurück. Die bestehende Admin-Änderungsansicht bietet den Download an.

**Einordnung:** Die Integration in den vorgesehenen Nutzungspfad ist gelungen. Der zusätzliche Konvertierungsdienst bleibt eine betriebliche Abhängigkeit.

## Bearbeitbarkeit der Vorlage

**Beobachtung:** MergeFields und die Teilnehmerzeile sind in Word 365 bearbeitbar. Größere bedingte Inhalte müssen in Feldresultaten gepflegt werden. Unterschiedlich formatierte Textteile innerhalb eines getesteten IF-Feldresultats blieben nicht erhalten.

**Einordnung:** Die einfache Vorlage ist gut zugänglich. Für komplexe, kundenbearbeitbare Textblöcke ist der getestete Ansatz weniger geeignet als die einfache Felderkennung vermuten lässt. Ein Python-seitig eingefügter Textblock wäre für dieses Kriterium nicht gleichwertig.

## Dynamische Tabelle und Seitenumbrüche

**Beobachtung:** Der DOCX-Test prüft alle Teilnehmernachnamen der großen Veranstaltung. Der Live-Test prüft die Namen in beiden PDFs und mehr als eine Seite für die große Veranstaltung. Nach Sichtprüfung entsprachen die PDFs den generierten DOCX-Dateien.

**Einordnung:** Dynamische, mehrseitige Ausgabe ist für die Testdaten nachgewiesen. Die genaue Tabellenkopf-Wiederholung und konkrete Seitenübergänge sind durch Textextraktion allein nicht bewiesen.

## Bedingte Logik

**Beobachtung:** Word-IF-Felder mit `merge_if_fields=True` funktionierten. Der PDF-Live-Test prüft, dass der Warntext bei 60 Teilnehmern erscheint und bei 25 Teilnehmern fehlt. Die unterschiedlich formatierten Zeichen innerhalb eines IF-Feldresultats wurden nicht erhalten.

**Einordnung:** Bedingte Textausgabe ist nachgewiesen, eine gleichwertige freie Formatierung eines größeren Blocks nicht. Die Verarbeitung von IF-Feldern ist laut Bibliotheksbeschreibung experimentell. Kurzbeleg: Projekt docx-mailmerge2, o. J.

## Header, Footer und Seitenzahlen

**Beobachtung:** Die Fußzeile der aktuellen Vorlage enthält die Seitenangabe. Der Kontakt- und Rechtsblock wurde nach dem gescheiterten Inklusionsversuch entfernt. Die PDFs erschienen nach Sichtprüfung wie die generierten DOCX-Dateien. Eine seitenweise dokumentierte Einzelprüfung aller Kopf- und Fußbereiche liegt nicht vor.

**Einordnung:** Seitenangaben sind im getesteten Layout vorhanden. Unterschiedliche Logos auf erster und folgenden Seiten sowie wiederholte Tabellenköpfe sollten im abschließenden visuellen Prüfkatalog seitenweise bestätigt werden.

## Template-Inklusion

**Beobachtung:** Der lokale Versuch, eine zweite DOCX über `INCLUDETEXT` einzubinden, war nicht erfolgreich. Eine funktionierende automatische Einbindung wurde nicht nachgewiesen. Aktuell enthält die Vorlage keinen Kontakt- und Rechtsblock.

**Einordnung:** Der Inhalt ließe sich gegebenenfalls als einzelne Felder in der Hauptvorlage nachbauen. Dies wäre jedoch kein gleichwertiger, separat bearbeitbarer Baustein und wurde deshalb bewusst nicht als Erfüllung des Inklusionskriteriums gewertet. Das Ergebnis des lokalen Versuchs belegt keine generelle Unmöglichkeit der Word-Feldfunktion. Kurzbeleg: Microsoft, o. J.

## PDF-Konvertierung

**Beobachtung:** Derselbe lokal betriebene Gotenberg-Konverter wie bei docxtpl wurde verwendet. Eine isolierte DOCX-Konvertierung, der Admin-Download und der explizit aktivierte Live-Test funktionierten. Für die getesteten PDFs wurden keine wahrnehmbaren Unterschiede zur jeweiligen DOCX berichtet.

**Einordnung:** Die Konvertierung war im konkreten Prototyp erfolgreich. Ohne systematische Font- und Laufzeitprüfung lassen sich daraus keine allgemeinen Aussagen zur Layouttreue oder Geschwindigkeit ableiten. Kurzbeleg: Gotenberg, o. J.

## Abweichungen von der Erwartung aus Phase 1

**Beobachtung:** Die dynamische Tabelle und die bedingte Ausgabe gelangen. Der frei gestaltbare bedingte Block und die automatische Inklusion einer zweiten Word-Vorlage konnten dagegen nicht gleichwertig demonstriert werden.

**Einordnung:** Der praktische Versuch differenziert zwischen funktionierender Datenersetzung und kundenbearbeitbarer Dokumentgestaltung.

## Vorläufiges Fazit

Für einfache Felder, Teilnehmerzeilen und den Admin-PDF-Download erwies sich der Ansatz als funktionsfähig. Die wesentlichen Einschränkungen liegen im getesteten Umgang mit komplex formatierten IF-Feldresultaten und in der nicht nachgewiesenen Teilvorlagen-Inklusion. Die endgültige Einordnung erfolgt erst nach dem Vergleich mit den anderen Kandidaten.
