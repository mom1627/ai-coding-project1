# KI-Kundenassistent – MVP und Geschäftsvalidierung

## Ziel
Ein kleiner, nachvollziehbarer KI-Assistent für deutsche Dienstleistungsbetriebe, der häufige Fragen beantwortet, unverbindliche Terminanfragen strukturiert erfasst und E-Mail-Antworten als Entwürfe vorbereitet. Keine automatischen verbindlichen Zusagen.

## Zielkunden
Zunächst eine Branche auswählen (z. B. Friseursalons oder Reinigungsdienste). Erst nach 5–10 Gesprächen mit echten Betrieben den Funktionsumfang festlegen.

## MVP (erste Version)
1. Konfigurierbare FAQ mit Öffnungszeiten, Leistungen und Preisen.
2. Antworten nur aus freigegebenen Geschäftsinformationen; bei Unsicherheit an Menschen übergeben.
3. Formular für Terminanfragen mit Name, Kontaktweg, Wunschtermin und Einwilligung.
4. Übersicht für den Betreiber; Antworten und Terminbestätigungen zunächst manuell freigeben.
5. Einfache Demo mit Beispieldaten, ohne echte Kundendaten.

## Nicht im MVP
- Vollautomatisches Buchen, Versenden oder Telefonieren
- Unkontrollierte Websuche oder beliebige Shell-Befehle
- Verarbeitung sensibler Daten
- Bezahlfunktionen vor dem ersten Kundentest

## Geschäftshypothese (zu testen, keine Umsatzgarantie)
Pilotpreis: 99–249 EUR einmalige Einrichtung und 29–79 EUR/Monat für Betreuung, jeweils abhängig von Aufwand und Betriebskosten. Preise durch Kundengespräche validieren.

## 14-Tage-Plan
- Tage 1–2: Branche und 20 potenzielle Kunden identifizieren; 5 Gespräche führen.
- Tage 3–5: Demo mit Fake-Daten, FAQ und Anfrageformular bauen.
- Tage 6–8: Tests, Datenschutz- und Sicherheitsprüfung, Demo verbessern.
- Tage 9–11: 10 gezielte persönliche Angebote an passende Betriebe; keine Spam-Massenmails.
- Tage 12–14: Pilotkunde gewinnen oder Angebot nach Rückmeldungen anpassen.

## Erfolgsmessung
Anzahl Gespräche, konkrete Probleme, Demo-Anfragen, Pilotzusagen, tatsächliche Zeitersparnis und Kosten je Anfrage.

## Technik
Repository: mom1627/ai-coding-project1
- Python für Logik und Tests
- Einfache mobile Weboberfläche für Demo
- Konfiguration statt hartcodierter Kundendaten
- Geheimnisse niemals ins öffentliche Repository committen
- Lokales iSH-Modell optional; ein iPhone darf nicht als dauerhaft verfügbarer Produktivserver vorausgesetzt werden

## Recht und Sicherheit
Vor Nutzung mit echten Kunden: DSGVO, Datenschutzhinweise, Auftragsverarbeitung und anwendbare KI-Transparenzpflichten prüfen. Keine medizinische oder rechtliche Beratung durch den Bot. Menschliche Freigabe für Nachrichten mit Außenwirkung.

## Nächste technische Aufgabe
Implementiere zunächst eine offline testbare FAQ-Antwortlogik mit Beispielgeschäft, klarer Fallback-Antwort und Unit-Tests. Anschließend Demo-Oberfläche ergänzen.
