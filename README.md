# Aufbau der Repository

- **Ordner: Programme**
  
  Enthält alle Skripte (skript1.py bis skript6.py) und Hilfsprogramme (hilfsprogramm1.py - hilfsprogramm3.py).
- **Ordner: Bilder**
  - **Unterordner: Kalibrierungsbilder**
    
    Enthält alle Bilder, die zum Kalibrieren der Skripte verwendet wurden.
  - **Unterordner: Eingabebilder**
    
    Enthält alle Bilder, die ausgewertet wurden. Die Bilder sind basierend auf Aufnahmedatum und Flugroute in weitere Unterordner eingeteilt.
    Die Bilder sind basierend auf der Position, an der sie aufgenommen wurden, benannt. Das Bild /Bilder/Eingabebilder/Bilder 29-08-22/Flugroute 1/YUN00001.jpg wurde beispielsweise auf Position 1 aufgenommen.
- **Ordner: Outputs**
  
  Enthält pro Aufnahmedatum und Flugroute eine csv-Datei. Die csv-Datei enthält die Auswertungsergebnisse für alle Bilder, die am jeweiligen Datum auf der jeweiligen Flugroute aufgenommen wurden, inklusive Mittelwerten und Standardabweichungen.
  
  Beispielsweise enthält die Datei Outputs/Bilder 16-07-22_Flugroute 1.csv die Bilder, die am 16.07.22 auf Flugroute 1 aufgenommen wurden.

Im **Wiki** der Repository befinden sich zusätzliche Inhalte, für die in der Langfassung kein Platz mehr war.

# Überblick über die Skripte und Hilfsprogramme

| **Skript** | **Dient zur Auswertung von**                                                                                                         | **Vom Skript ermittelte Parameter**                                                                                                                          | **Verwendetes Farbmodell** |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| Skript 1   | Luftbildern                                                                                                                          | Grünanteil, Braunanteil                                                                                                                                      | HSV                        |
| Skript 2   | Luftbildern                                                                                                                          | Grünanteil                                                                                                                                                   | RGB                        |
| Skript 3   | Luftbildern                                                                                                                          | Grünanteil, Braunanteil                                                                                                                                      | RGB                        |
| Skript 4   | Wärmebilder                                                                                                                          | Waldanteil                                                                                                                                                   | RGB                        |
| Skript 5   | Wärmebildern, bei denen der durch die Farbskala abgedeckte Temperaturbereich _nicht_ gegeben ist                                     | Waldanteil                                                                                                                                                   | HSV                        |
| Skript 6   | Wärmebilder                                                                                                                          | Waldanteil                                                                                                                                                   | RGB                        |
| Skript 7   | Luftbildern und Wärmebildern [[1]](https://d.docs.live.net/a01e1561cb638b07/Projekte/JuFo%2024/TimKrome_JuFo_Langfassung.docx#_ftn1) | Anteil grüne Wiese, Anteil grüner Wald                                                                                                                       | HSV                        |
| Skript 8   | Luftbildern und Wärmebildern, bei denen der durch die Farbskala abgedeckte Temperaturbereich gegeben ist                             | Durchschnittstemperatur [°C], STABW der Temperatur [°C] und min. / max. Temperatur von grüner / brauner Vegetation, die im Bild auftritt, und vom Gesamtbild | RGB und HSV                |

| **Hilfsprogramm**  | **Zweck**                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Hilfsprogramm 1    | Dient zum Speichern von RGB-Farbtripeln grüner und brauner Vegetation, die Skript 3 als Eingabeparameter gegeben werden können. |
| Hilfsprogramm 2    | Dient zum Speichern der Farben einer Farbskala in Abstufungen.                                                                  |
| Hilfsprogramm 3    | Dient zum Berechnen der exakten Temperaturen eines Wärmebilds.                                                                  |
| k-Means Clustering | Eine Implementierung von k-Means Clustering wurde in der Datei _kmeans.py_ erstellt. Skript 6 verwendet diese Implementierung.  |
