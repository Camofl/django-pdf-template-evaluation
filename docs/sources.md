# Quellen: Carbone Community

Abrufdatum: 25. September 2026. Die Quellen belegen dokumentierte Funktionen und Schnittstellen. Beobachtungen aus dem lokalen Prototyp sind im Implementierungsprotokoll und im manuellen Prüfprotokoll ausgewiesen. „o. J.“ bezeichnet Seiten ohne eindeutig ausgewiesenes Veröffentlichungsjahr.

- Carbone. o. J. *Deploy with Docker*. Carbone-Dokumentation. https://carbone.io/documentation/developer/self-hosted-deployment/deploy-with-docker.html. Verwendete Abschnitte: Docker-Imagevarianten und vollständige Variante mit LibreOffice. Im Branch wurde `carbone/carbone-ee:full-5.14.5` verwendet.
- Carbone. o. J. *How to license Carbone On-Premise*. Carbone-Dokumentation. https://carbone.io/documentation/developer/on-premise-installation/licensing.html. Verwendeter Abschnitt: Betrieb mit Community-Funktionen ohne Lizenzschlüssel. Keine kostenpflichtigen Funktionen wurden absichtlich für die Umsetzung eingesetzt.
- Carbone. o. J. *Generate reports*. Carbone-Dokumentation. https://carbone.io/documentation/developer/http-api/generate-reports.html. Verwendete Abschnitte: Inline-Vorlage als Base64, JSON-Daten, direkte PDF-Antwort mit `download=true` und LibreOffice-Konvertierung.
- Carbone. o. J. *The basics*. Carbone-Dokumentation. https://carbone.io/documentation/design/substitutions/the-basics.html. Verwendeter Abschnitt: Einfache Daten-Tags in Office-Vorlagen.
- Carbone. o. J. *Loop over array*. Carbone-Dokumentation. https://carbone.io/documentation/design/repetitions/with-arrays.html. Verwendeter Abschnitt: Wiederholung einer Tabellenzeile mit Array-Tags.
- Carbone. o. J. *Conditional blocks*. Carbone-Dokumentation. https://carbone.io/documentation/design/conditions/conditional-blocks.html. Verwendeter Abschnitt: Community-Funktionen `showBegin` und `showEnd` für bedingte Vorlagenbereiche.
- Carbone. o. J. *How formatters work*. Carbone-Dokumentation. https://carbone.io/documentation/design/formatters/overview.html. Verwendeter Abschnitt: In Word-Tags verfügbare Community-Formatter. Die Integration eigener Django-Filter wurde nicht geprüft.
- Carbone. o. J. *Supported template files and features*. Carbone-Dokumentation. https://carbone.io/documentation/design/overview/template-feature.html. Verwendeter Abschnitt: Layout-Funktionen und Einstufung von Community-Merkmalen.
- Django Software Foundation. o. J. *Request and response objects*. Django-Dokumentation für Version 5.2. https://docs.djangoproject.com/en/5.2/ref/request-response/. Verwendeter Abschnitt: `FileResponse` für den Admin-Download.
- pypdf-Projekt. o. J. *Extract Text from a PDF*. pypdf-Dokumentation. https://pypdf.readthedocs.io/en/stable/user/extract-text.html. Verwendeter Abschnitt: Auslesen von Text aus erzeugten PDFs im Live-Test.
