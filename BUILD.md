# Aus Quellcode bauen

Für die begleitete Einrichtung mit einem lokalen KI-Agenten: [Agent-Prompt zum Kopieren](docs/AGENT-PROMPT.md). Er verlangt eine Prüfung vor Ausführung und eine eigene Freigabe vor der Systeminstallation.

Voraussetzungen: Apple Silicon, macOS 27, Xcode Command Line Tools (`xcode-select --install`) und Python 3. Zum Bauen zusätzlich Homebrew-Pakete `cmake`, `libusb-compat` und `jpeg-turbo` installieren. Auf Zielgeräten sind diese Pakete nicht nötig.

```sh
brew install cmake libusb-compat jpeg-turbo
python3 scripts/build.py
```

Das Skript schreibt nur nach `build/` und `dist/`, fragt keine Drucker ab, startet keine Scans und installiert nichts ins System. Es baut die öffentlichen Quellen, führt Decoder-/Metadaten-/JPEG- und brlaser-Tests aus und erzeugt zwei Installer. App und Filter werden lokal ad-hoc signiert. Ein Apple-Developer-Konto wird nicht benötigt.

Die veröffentlichten Builds wurden mit libusb 1.0.30, libusb-compat 0.1.9 und libjpeg-turbo 3.2.0 gebaut. Deren Lizenztexte und Homebrew-Rezepte stehen in `licenses/`; Original-Quellarchive sind als Release-Download enthalten. Homebrew kann zukünftig andere Versionen liefern: Dann ist eine erneute Kompatibilitätsprüfung erforderlich. Die macOS-SDK-Version kann ebenfalls das Ergebnis verändern; bytegleiche Builds werden nicht zugesichert.

Dynamische Bibliotheken lassen sich im App-Bundle unter `Contents/Resources/lib` durch eigene kompatible Builds ersetzen. Relative Abhängigkeiten mittels `install_name_tool` erhalten und zuerst die Bibliotheken, dann die App mit `codesign --force --sign -` neu signieren. Kein Hardened Runtime/Library Validation wird aktiviert.

Die gebündelten Vendor-Quellen sind mit lokalen macOS-Anpassungen versehen; Details und ursprüngliche Commits siehe UPSTREAM.md. Unveränderte Linux-Binärtreiber und aufgezeichnete Dokumente/USB-Mitschnitte gehören nicht zum Build.

Für ein iCloud-synchronisiertes Checkout kann ein lokaler Build-Ordner gewählt werden, damit Finder-/Cloud-Metadaten nicht in App-Bundles geraten:

```sh
BROTHER_BUILD_DIR=/private/tmp/brother-build python3 scripts/build.py
```
