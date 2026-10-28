# Herkunft und Lizenzen

Die lokale Integration wurde mit OpenAI Codex erstellt. Die folgenden Projekte sind die wesentliche Vorarbeit anderer Autoren. Dieses Repository beansprucht nicht, ihre Treiber neu erfunden zu haben.

- [printer-driver-ptouch](https://github.com/philpem/printer-driver-ptouch), Commit `78ef24cc7217e9fe6595efc8479116241eb1c5f0`.
- [brlaser](https://github.com/Owl-Maintain/brlaser), Commit `edf2770c4573973d5b90ce57ec407e675348c196`.
- [brscan](https://github.com/dmikushin/brscan), Commit `51a719b7df0d31e3371868e0bb7ad0847dd2b89a`.

Lokale Änderungen: macOS-CUPS-Anbindung und QL-PPDs, native Scanner-App, macOS-Portierung des brscan-Backends, USB-Lesepuffer, QL-/DCP-Gerätezuordnung und DCP-7055-Seitenende. Vendor-Dateien können gegenüber den obigen Commits verändert sein; der mitgelieferte Quellcode ist für diese Builds maßgeblich.

Eigene Integration und App: GPL-2.0-or-later. Für Drittanbieterdateien gelten die jeweiligen Dateiköpfe und mitgelieferten Lizenztexte. brscan enthält neben GPL-Code auch LGPL- und Brother-Open-License-Bestandteile (einschließlich unveränderter Kalibrierungsdaten); siehe `vendor/brscan/Copying`, `copying.lib`, `copying.brother`. Diese zusätzlichen Texte sind keine pauschale Umlizenzierung. Keine unveränderten proprietären Linux-`.so`-Treiber werden ausgeliefert.

Die Scanner-App bündelt dynamische Bibliotheken: libusb 1.0.30, libusb-compat 0.1.9 und libjpeg-turbo 3.2.0. Lizenztexte und Homebrew-Baurezepte liegen in `licenses/`. Das Release enthält zusätzlich deren Original-Quellarchive. Alle dynamischen Bibliotheken können anhand des Build-Skripts ersetzt und die App anschließend neu ad-hoc signiert werden.
