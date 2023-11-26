# Aufbau der Repository

- **Ordner: Programme**
  Enthält alle Skripte (skript1.py bis skript6.py) und Hilfsprogramme (hilfsprogramm1.py - hilfsprogramm3.py).
- **Ordner: Bilder**
  - **Unterordner: Kalibrierungsbilder**
    Enthält alle Bilder, die zum Kalibrieren der Skripte verwendet wurden.
  - **Unterordner: Eingabebilder**
    Enthält Bildern, die ausgewertet wurden. Die Bilder sind basierend auf Aufnahmedatum und Flugroute in weitere Unterordner eingeteilt.
    Die Bilder sind basierend auf der Position, an der sie aufgenommen wurden, benannt. Das Bild /Bilder/Eingabebilder/Bilder 29-08-22/Flugroute 1/YUN00001.jpg wurde beispielsweise auf Position 1 aufgenommen.
- **Ordner: Outputs**
  Enthält pro Aufnahmedatum und Flugroute eine csv-Datei. Die csv-Datei enthält die Auswertungsergebnisse für alle Bilder, die am jeweiligen Datum auf der jeweiligen Flugroute aufgenommen wurden, inklusive Mittelwerten und Standardabweichungen.
  Beispielsweise enthält die Datei Outputs/Bilder 16-07-22_Flugroute 1.csv die Bilder, die am 16.07.22 auf Flugroute 1 aufgenommen wurden.
