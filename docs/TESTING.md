# Teststand

Hardwarebestätigungen aus der Entwicklung am 27./28. Oktober 2026, macOS 27.0.1, Apple Silicon:

- DCP-7055: USB-Druck mit Text, Linien, Graustufen; tatsächlichen Ausdruck bestätigt.
- DCP-7055: wiederholte Scans, volle bedruckte Vorlage bis zur unteren Legende; Farbe 300/600 dpi, Grau 200/600 dpi. PNG-Pixel und DPI-Metadaten geprüft.
- QL-720NW und QL-700: separate USB-Warteschlangen, 62 × 40 mm auf 62-mm-Endlosrolle. Text, Rahmen, Orientierung und Schnitt bestätigt.
- Apple Pages: Ein manuell durchgeführter Druck wurde vom Nutzer am 28. Oktober 2026 als erfolgreich bestätigt.
- QL-Kopien: zwei Kopien im erzeugten Druckstrom geprüft; kein separater physischer Mehrkopientest.
- Scannerdecoder: 65 synthetische Integrationsprüfungen, JPEG-Decodertest und eigener Regressionstest der DCP-7055-Seitenende-Metadaten bestanden.
- brlaser: vier mitgelieferte Testgruppen bestanden.

Die öffentlichen Builds enthalten Bereinigungen von Pfaden/Metadaten gegenüber den ursprünglichen Testpaketen. Sie wurden erneut gebaut, entpackt und technisch geprüft; der komplette Hardwareablauf wurde mit diesen neu verpackten Dateien nicht wiederholt.

Vor breiter Verteilung auf einem zweiten Mac installieren und erneut testen: ein-/mehrseitiger Druck, passende Rolle, Scan und Druck nach Neustart sowie nach USB-Ab-/Anstecken. Kein Ersatz für unabhängiges Code- oder Sicherheitsreview.

## DCP-7055 mit Parallels Desktop 26.4 und Windows 11

Am 10. November 2026 auf einem zweiten Apple-Silicon-Mac mit macOS 27.0.1 und einem per USB angeschlossenen DCP-7055 geprüft. Parallels meldete bei der Einrichtung des ursprünglichen Profils in Windows „Failed to install printer, status = 16“. Mit einer neuen Warteschlange und demselben vollständigen Profil ohne Komma im PPD-Modellnamen erschien der Drucker automatisch in Windows. Das Aktualisieren der zuvor fehlgeschlagenen Warteschlange unter derselben Kennung genügte auf diesem System nicht.

Windows sendete einen einseitigen Textauftrag über das vollständige Profil. CUPS meldete ein ausgegebenes Blatt. Der Nutzer bestätigte anhand des aufgedruckten Testtexts, dass dieses Blatt lesbar im Ausgabefach lag. Die Druckerkomponente 6.2.8.3 enthält den geprüften Modellnamen und den ausführbaren ARM-Druckfilter. Der Paketbau prüft beide Eigenschaften im entpackten Installer.
