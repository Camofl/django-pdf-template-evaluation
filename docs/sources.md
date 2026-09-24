# Quellen: docx-mailmerge2

Abrufdatum aller Onlinequellen: 24. September 2026. Die Quellen beschreiben verfügbare
Funktionen. Die Ergebnisse der lokalen Versuche stehen getrennt im
Implementierungsprotokoll und in den Evaluationsnotizen. Fehlgeschlagene `INCLUDETEXT`
-Versuche sind eigene Beobachtungen und dürfen nicht als dokumentierte generelle
Unmöglichkeit zitiert werden.

- Projekt docx-mailmerge2. o. J. *docx-mailmerge2: Project description*.
  PyPI. https://pypi.org/project/docx-mailmerge2/. Verwendete Abschnitte: Installation,
  echte MergeFields, `get_merge_fields()`, `merge()`, `merge_rows()` und Hinweise zur
  experimentellen Verarbeitung von Word-IF-Feldern. Die konkrete Paketversion für den
  Prototypen ist gesondert in `requirements.txt` festzuhalten.
- Microsoft. o. J. *Feldfunktionen: MergeField-Feld*. Microsoft
  Support. https://support.microsoft.com/en-gb/office/field-codes-mergefield-field-7a6d24a1-68a6-4b05-8359-1dc087daf4e6.
  Verwendeter Abschnitt: Bedeutung und Darstellung echter Word-MergeFields. Die
  englischsprachige Dokumentation wurde für den technischen Feldbegriff verwendet.
- Microsoft. o. J. *Field codes: IF field*. Microsoft
  Support. https://support.microsoft.com/en-us/office/field-codes-if-field-9f79e82f-e53b-4ff5-9d2c-ae3b22b7eb5e.
  Verwendeter Abschnitt: Vergleich und bedingte Textausgabe mit Word-Feldfunktionen. Die
  Formatabweichung des Prototyps ist ein eigener Testbefund, keine aus dieser Quelle
  abgeleitete allgemeine Eigenschaft.
- Microsoft. o. J. *Feldfunktionen: IncludeText-Feld*. Microsoft
  Support. https://support.microsoft.com/de-de/office/feldfunktionen-includetext-feld-1c34d6d6-0de3-4b5c-916a-2ff950fb629e.
  Verwendeter Abschnitt: Einbindung von Text und Grafiken aus einer weiteren Datei. Die
  Quelle belegt die Word-Feldfunktion, nicht deren erfolgreiche automatische
  Aktualisierung im Prototyp.

