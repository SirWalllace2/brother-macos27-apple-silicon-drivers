# Teststand

Hardwarebestätigungen aus der Entwicklung am 27./28. Oktober 2026, macOS 27.0.1, Apple Silicon:

- DCP-7055: USB-Druck mit Text, Linien, Graustufen; tatsächlichen Ausdruck bestätigt.
- DCP-7055: wiederholte Scans, volle bedruckte Vorlage bis zur unteren Legende; Farbe 300/600 dpi, Grau 200/600 dpi. PNG-Pixel und DPI-Metadaten geprüft.
- QL-720NW und QL-700: separate USB-Warteschlangen, 62 × 40 mm auf 62-mm-Endlosrolle. Text, Rahmen, Orientierung und Schnitt bestätigt.
- QL-Kopien: zwei Kopien im erzeugten Druckstrom geprüft; kein separater physischer Mehrkopientest.
- Scannerdecoder: 65 synthetische Integrationsprüfungen, JPEG-Decodertest und eigener Regressionstest der DCP-7055-Seitenende-Metadaten bestanden.
- brlaser: vier mitgelieferte Testgruppen bestanden.

Die öffentlichen Builds enthalten Bereinigungen von Pfaden/Metadaten gegenüber den ursprünglichen Testpaketen. Sie wurden erneut gebaut, entpackt und technisch geprüft; der komplette Hardwareablauf wurde mit diesen neu verpackten Dateien nicht wiederholt.

Vor breiter Verteilung auf einem zweiten Mac installieren und erneut testen: ein-/mehrseitiger Druck, passende Rolle, Scan und Druck nach Neustart sowie nach USB-Ab-/Anstecken. Kein Ersatz für unabhängiges Code- oder Sicherheitsreview.
