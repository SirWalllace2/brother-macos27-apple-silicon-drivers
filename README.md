# Brother Legacy macOS

Experimentelle native Apple-Silicon-Treiber für ältere Brother-Drucker und eine eigenständige DCP-7055-Scan-App. **macOS 27, Apple Silicon, USB.** Kostenloses Community-Projekt, ohne Verbindung zu oder Unterstützung durch Brother.

## Vibe-Coding-Hinweis 🤖

Dieses Projekt wurde mit Unterstützung von **OpenAI Codex „vibegecodet“**. KI hat wesentliche Teile der Anpassungen, der Scan-App und der Installationspakete erstellt. Die Treiber bauen auf bestehenden freien Projekten auf; deren Urheber und Lizenzen sind in [UPSTREAM.md](UPSTREAM.md) genannt.

Die folgenden Hardwaretests wurden an echten Geräten durchgeführt und die Ergebnisse vom Nutzer bestätigt. Das ist **keine umfassende Qualitäts- oder Sicherheitsprüfung**. Experimentelle Software, ohne Gewährleistung; Nutzung auf eigene Verantwortung.

## Downloads

Installationspakete und vollständige Quellarchive: **[GitHub Releases](https://github.com/SirWalllace2/brother-legacy-macos/releases)**. Die Releases sind als Vorabversionen gekennzeichnet. Ein Download ersetzt keinen Test auf deinem Mac.

| Modell | Drucken | Scannen | Bestätigter Test |
|---|---|---|---|
| DCP-7055 | nativer CUPS-Treiber | eigene App, PNG, Farbe/Graustufen, 100–600 dpi wählbar | USB-Druck; Farbe 300/600 dpi, Grau 200/600 dpi |
| QL-700 | nativer CUPS-Treiber | entfällt | USB, 62-mm-Endlosrolle, Text/Rahmen, Schnitt |
| QL-720NW | nativer CUPS-Treiber | entfällt | USB, 62-mm-Endlosrolle, Text/Rahmen, Schnitt |

Getestetes System: macOS 27.0.1 auf Apple Silicon. **Kein Nachweis für Intel-Macs, Windows, ältere macOS-Versionen, andere Modelle oder Netzwerkbetrieb.** Andere Rollen und die Zwischenauflösungen sind auswählbar, aber nicht alle Kombinationen wurden am Gerät getestet.

## Installation

1. Passendes `.pkg` aus dem Release laden und installieren (Administratorrechte).
2. Drucker per USB anschließen und einschalten.
3. Systemeinstellungen → Drucker & Scanner → Drucker hinzufügen → Verwenden → Software auswählen. Passendes Modell mit **Apple Silicon** wählen. Vorhandene Warteschlangen werden nicht automatisch umgestellt.
4. Für DCP-7055-Scans **DCP-7055 Scan** im Programme-Ordner öffnen. Es ist eine eigene App und kein Plug-in für „Digitale Bilder“. Keine Anmeldung, kein Rosetta und kein Homebrew auf dem Zielgerät nötig.

Bei QL-Druckern müssen Dokument-/Papierformat und Rollentyp zur eingelegten Rolle passen. 62-mm-Endlosrolle: z. B. 62 × 40/100/150 mm, Rollentyp Endlosrolle. Für vorgestanzte Etiketten genaue Größe und Einzeletiketten wählen. Eigene Längen sind möglich. Automatischer Schnitt ist abschaltbar. Rollentyp und Dokumentformat werden nicht automatisch vom Sensor übernommen.

Pages und andere Programme können über den normalen macOS-Druckdialog drucken. Der vollständige macOS-PDF-Druckweg wurde getestet; ein manuell bedienter Pages-Test wurde nicht protokolliert.

## macOS-Sicherheitsmeldung

Die Programme sind lokal **ad-hoc signiert**, die Installer **nicht Developer-ID-signiert und nicht notarisiert**. macOS kann das Öffnen blockieren. Nur installieren, wenn du Herkunft und Risiko selbst beurteilt hast. Falls macOS eine gezielte Freigabe für diese Datei unter Systemeinstellungen → Datenschutz & Sicherheit anbietet, kannst du diese nach Prüfung selbst nutzen. **Gatekeeper, SIP oder andere globale Sicherheitsfunktionen nicht abschalten.** Firmenrichtlinien können die Installation verhindern. Alternativ aus dem Quellcode selbst bauen.

## Einschränkungen und Entfernen

DCP-Scanbereich ungefähr 210 × 291 mm; Ränder sind nicht randlos lesbar. Ausgabe PNG, kein PDF/OCR. Auf Hardware-/Übertragungsfehler achten. Dies sind klassische CUPS-Treiber; zukünftige macOS-Versionen können deren Schnittstellen entfernen.

Zum Entfernen zuerst nur die neu angelegten Warteschlangen in den Systemeinstellungen löschen. Danach die zugehörigen Dateien aus den in [docs/INSTALL.md](docs/INSTALL.md) genannten Pfaden entfernen. Gemeinsame Filter erst löschen, wenn keine Warteschlange sie mehr verwendet.

## Bauen und beitragen

Siehe [BUILD.md](BUILD.md), [UPSTREAM.md](UPSTREAM.md) und [docs/TESTING.md](docs/TESTING.md). Bei Issues: Mac-Modell, macOS-Version, Druckermodell, Anschluss, Papier/Rolle und genaue Fehlermeldung angeben. **Keine Seriennummern, privaten Dokumente oder vollständigen USB-Mitschnitte hochladen.**
