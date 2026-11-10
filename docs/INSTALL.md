# Installierte Dateien

## DCP-Paket

- `/Applications/DCP-7055 Scan.app`
- `/Library/Printers/brlaser/Filter/rastertobrlaser`
- `/Library/Printers/brlaser/Documentation/`
- `/Library/Printers/PPDs/Contents/Resources/Brother-DCP-7055-brlaser-arm64.ppd`

### DCP-7055 mit Parallels und Windows 11

Ab Druckerkomponente 6.2.8.3 lautet der Modellname **Brother DCP-7055 brlaser 6.2.8 Apple Silicon**. Bei aktivierter Freigabe der Mac-Drucker in Parallels erscheint dieser Name auch im Windows-Druckdialog.

Beim Update das Paket auf dem Mac installieren. Falls Windows einen früher eingerichteten DCP-7055 weiterhin übergeht, denselben USB-Drucker in den macOS-Druckereinstellungen zusätzlich hinzufügen. Vor dem Hinzufügen im Feld **Name** einen neuen Namen wie **Brother DCP-7055 Apple Silicon** eingeben und unter **Verwenden → Software auswählen** das oben genannte Modell wählen. Damit erhält die Warteschlange eine neue Kennung. Aus Windows eine Testseite drucken und die funktionierende Warteschlange bei Bedarf auf dem Mac als Standard auswählen.

## QL-Paket

- `/Library/Printers/QL720/Filter/rastertoql720` (gemeinsamer Filter für QL-700 und QL-720NW)
- `/Library/Printers/QL720/Documentation/`
- `/Library/Printers/PPDs/Contents/Resources/Brother-QL-700-Apple-Silicon.ppd`
- `/Library/Printers/PPDs/Contents/Resources/Brother-QL-720NW-Apple-Silicon.ppd`

Keine Installationsskripte, Autostarts oder eigenen Netzwerkdienste. Warteschlangen manuell anlegen. Die Paket-IDs bleiben zur Upgrade-Kompatibilität erhalten; es gibt keine Garantie für jede bestehende Konfiguration.
