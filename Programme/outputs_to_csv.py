# Speichert die Outputs von Skript 1 bis 8 für einen Datensatz in eine CSV-Datei

import csv
import json
import statistics
import numpy as np

# Parameter - Datensatz, der ausgegeben werden soll
datensatz = "Bilder 09-11-23"
flugroute = "Flugroute 1"

with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/all_outputs.json") as f:
    data = json.load(f)

setdata = data[datensatz][flugroute]
rows = [] # Initialisieren
output_path = f'C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/{datensatz}_{flugroute}.csv'

# Erste Spalte
rows.append(["Bild"])
for i in setdata:
    rows.append([i + ".jpg"])
    if len(setdata[i]["baumbewuchs_anteil"]) > 0:
        if setdata[i]["baumbewuchs_anteil"]["skript_4"] is None:
            setdata[i]["baumbewuchs_anteil"] = {}

rows.append(["Mittelwert ueber alle Bilder"])
rows.append([""])

# Zweite Spalte
rows[0].append("Gruenanteil Skript 1")
for count, file in enumerate(setdata):
    if setdata[file]["grün_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["grün_anteil"]["skript_1"])
rows[count+2].append("")
rows[count+3].append("")

# 3. Spalte
rows[0].append("Gruenanteil Skript 2")
for count, file in enumerate(setdata):
    if setdata[file]["grün_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["grün_anteil"]["skript_2"])
rows[count+2].append("")
rows[count+3].append("")

# 4. Spalte
rows[0].append("Gruenanteil Skript 3")
for count, file in enumerate(setdata):
    if setdata[file]["grün_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["grün_anteil"]["skript_3"])
rows[count+2].append("")
rows[count+3].append("")

if flugroute == "Flugroute 1":
    # 6. Spalte
    values = []
    rows[0].append("Gruenanteil Mittelwert Skript 1 und 2")
    for count, file in enumerate(setdata):
        if setdata[file]["grün_anteil"] == {}:
            rows[count+1].append("-")
            continue
        mw = (
            setdata[file]["grün_anteil"]["skript_1"] +
            setdata[file]["grün_anteil"]["skript_2"]
        ) / 2
        rows[count+1].append(mw)
        values.append(mw)
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append("")

    # 7. Spalte
    values = []
    rows[0].append("Gruenanteil STABW Skript 1 und 2")
    for count, file in enumerate(setdata):
        if setdata[file]["grün_anteil"] == {}:
            rows[count+1].append("-")
            continue
        stabw = statistics.stdev(
            [setdata[file]["grün_anteil"]["skript_1"],
            setdata[file]["grün_anteil"]["skript_2"]]
        )
        rows[count+1].append(stabw)
        values.append(stabw)
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append("")
else:
    # 6. Spalte
    values = []
    rows[0].append("Gruenanteil Mittelwert Skript 1 bis 3")
    for count, file in enumerate(setdata):
        if setdata[file]["grün_anteil"] == {}:
            rows[count+1].append("-")
            continue
        mw = (
            setdata[file]["grün_anteil"]["skript_1"] +
            setdata[file]["grün_anteil"]["skript_2"] +
            setdata[file]["grün_anteil"]["skript_3"]
        ) / 3
        rows[count+1].append(mw)
        values.append(mw)
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append("")

    # 7. Spalte
    values = []
    rows[0].append("Gruenanteil STABW Skript 1 bis 3")
    for count, file in enumerate(setdata):
        if setdata[file]["grün_anteil"] == {}:
            rows[count+1].append("-")
            continue
        stabw = statistics.stdev(
            [setdata[file]["grün_anteil"]["skript_1"],
            setdata[file]["grün_anteil"]["skript_2"],
            setdata[file]["grün_anteil"]["skript_3"]]
        )
        rows[count+1].append(stabw)
        values.append(stabw)
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append("")

# 5. Spalte
rows[0].append("Gruenanteil Schnittmenge Skript 1 u. Skript 2")
for count, file in enumerate(setdata):
    if setdata[file]["grün_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["grün_anteil"]["skript_1_2_schnittmenge"])
rows[count+2].append("")
rows[count+3].append("")

rows[0].append("")
for count, file in enumerate(setdata):
    rows[count+1].append("")
rows[count+2].append("")
rows[count+3].append("")

# 8. Spalte
rows[0].append("Braunanteil Skript 1")
for count, file in enumerate(setdata):
    if setdata[file]["braun_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["braun_anteil"]["skript_1"])
rows[count+2].append("")
rows[count+3].append("")


# 9. Spalte
rows[0].append("Braunanteil Skript 3")
for count, file in enumerate(setdata):
    if setdata[file]["braun_anteil"] == {}:
        rows[count+1].append("-")
        continue
    rows[count+1].append(setdata[file]["braun_anteil"]["skript_3"])
rows[count+2].append("")
rows[count+3].append("")


# 10. Spalte
values = []
rows[0].append("Braunanteil Mittelwert Skript 1 und 3")
for count, file in enumerate(setdata):
    if setdata[file]["braun_anteil"] == {}:
        rows[count+1].append("-")
        continue
    mw = (
        setdata[file]["braun_anteil"]["skript_1"] +
        setdata[file]["braun_anteil"]["skript_3"]
    ) / 2
    rows[count+1].append(mw)
    values.append(mw)
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

# 11. Spalte
values = []
rows[0].append("Braunanteil STABW Skript 1 und 3")
for count, file in enumerate(setdata):
    if setdata[file]["braun_anteil"] == {}:
        rows[count+1].append("-")
        continue
    stabw = statistics.stdev(
        [setdata[file]["braun_anteil"]["skript_1"],
        setdata[file]["braun_anteil"]["skript_3"]]
    )
    rows[count+1].append(stabw)
    values.append(stabw)
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

rows[0].append("")
for count, file in enumerate(setdata):
    rows[count+1].append("")
rows[count+2].append("")
rows[count+3].append("")

# 12. Spalte
rows[0].append("Waldanteil Skript 4")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        continue
    rows[count+1].append(setdata[file]["baumbewuchs_anteil"]["skript_4"])
rows[count+2].append("")
rows[count+3].append("")

# 13. Spalte
rows[0].append("Waldanteil Skript 5")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        continue
    rows[count+1].append(setdata[file]["baumbewuchs_anteil"]["skript_5"])
rows[count+2].append("")
rows[count+3].append("")

# 14. Spalte
rows[0].append("Waldanteil Skript 6")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        continue
    rows[count+1].append(setdata[file]["baumbewuchs_anteil"]["skript_6"])
rows[count+2].append("")
rows[count+3].append("")

# 15. Spalte
values = []
rows[0].append("Waldanteil Mittelwert Skript 4 bis 6")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        values.append(0)
        continue
    if setdata[file]["baumbewuchs_anteil"]["skript_5"] is None:
        mw = (
            setdata[file]["baumbewuchs_anteil"]["skript_4"] +
            setdata[file]["baumbewuchs_anteil"]["skript_6"]
        ) / 2
    else:
        mw = (
            setdata[file]["baumbewuchs_anteil"]["skript_4"] +
            setdata[file]["baumbewuchs_anteil"]["skript_5"] +
            setdata[file]["baumbewuchs_anteil"]["skript_6"]
        ) / 3
    rows[count+1].append(mw)
    values.append(mw)
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

# 16. Spalte
values = []
rows[0].append("Waldanteil STABW Skript 4 bis 6")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        values.append(0)
        continue
    if setdata[file]["baumbewuchs_anteil"]["skript_5"] is None:
        stabw = statistics.stdev(
            [setdata[file]["baumbewuchs_anteil"]["skript_4"],
            setdata[file]["baumbewuchs_anteil"]["skript_6"]]
        )
    else:
        stabw = statistics.stdev(
            [setdata[file]["baumbewuchs_anteil"]["skript_4"],
            setdata[file]["baumbewuchs_anteil"]["skript_5"],
            setdata[file]["baumbewuchs_anteil"]["skript_6"]]
        )
    rows[count+1].append(stabw)
    values.append(stabw)
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

rows[0].append("")
for count, file in enumerate(setdata):
    rows[count+1].append("")
rows[count+2].append("")
rows[count+3].append("")

# 17. Spalte
values = []
rows[0].append("Anteil gruener Wald Skript 7")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        values.append(0)
        continue
    rows[count+1].append(setdata[file]["anteil_wald_gruen"])
    values.append(setdata[file]["anteil_wald_gruen"])
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

# 18. Spalte
values = []
rows[0].append("Anteil gruene Wiese Skript 7")
for count, file in enumerate(setdata):
    if len(setdata[file]["baumbewuchs_anteil"]) == 0:
        rows[count+1].append("")
        values.append(0)
        continue
    rows[count+1].append(setdata[file]["anteil_wiese_gruen"])
    values.append(setdata[file]["anteil_wiese_gruen"])
rows[count+2].append(sum(values)/len(values))
rows[count+3].append("")

if len(setdata[file]["temperature_data"]) > 0:

    # 19. Spalte
    rows[0].append("")
    for count, file in enumerate(setdata):
        rows[count+1].append("")
    rows[count+2].append("")
    rows[count+3].append("")

    # 20. Spalte
    rows[0].append("Bild")
    for count, file in enumerate(setdata):
        rows[count+1].append(file + ".jpg")
    rows[count+2].append("Durchschnitt Datensatz")
    rows[count+3].append("STABW Datensatz")

    # 21. Spalte
    values = []
    rows[0].append("Temperatur gruener Vegetation (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_gruen"])
        values.append(setdata[file]["temperature_data"]["avg_temp_gruen"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 22. Spalte
    values = []
    rows[0].append("Temperatur nicht gruener Vegetation (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_nicht_gruen"])
        values.append(setdata[file]["temperature_data"]["avg_temp_nicht_gruen"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 23. Spalte
    values = []
    rows[0].append("Temperatur brauner Vegetation (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_braun"])
        values.append(setdata[file]["temperature_data"]["avg_temp_braun"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 24. Spalte
    values = []
    rows[0].append("Temperatur nicht brauner Vegetation (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_nicht_braun"])
        values.append(setdata[file]["temperature_data"]["avg_temp_nicht_braun"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 25. Spalte
    values = []
    rows[0].append("Temperatur Wald (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_wald"])
        values.append(setdata[file]["temperature_data"]["avg_temp_wald"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 26. Spalte
    values = []
    rows[0].append("Temperatur Nicht Wald (Durchschnitt pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_nicht_wald"])
        values.append(setdata[file]["temperature_data"]["avg_temp_nicht_wald"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))


    # 27. Spalte
    values = []
    rows[0].append("Durchschnittstemperatur gesamtbild")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["avg_temp_all"])
        values.append(setdata[file]["temperature_data"]["avg_temp_all"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 21. Spalte
    values = []
    rows[0].append("STD Temperatur gruener Vegetation (STD pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_gruen"])
        values.append(setdata[file]["temperature_data"]["std_temp_gruen"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 22. Spalte
    values = []
    rows[0].append("STD Temperatur nicht gruener Vegetation (STD pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_nicht_gruen"])
        values.append(setdata[file]["temperature_data"]["std_temp_nicht_gruen"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 23. Spalte
    values = []
    rows[0].append("std Temperatur brauner Vegetation (std pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_braun"])
        values.append(setdata[file]["temperature_data"]["std_temp_braun"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 24. Spalte
    values = []
    rows[0].append("std nicht brauner Vegetation (std pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_nicht_braun"])
        values.append(setdata[file]["temperature_data"]["std_temp_nicht_braun"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 25. Spalte
    values = []
    rows[0].append("std temp Wald (std pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_wald"])
        values.append(setdata[file]["temperature_data"]["std_temp_wald"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    # 26. Spalte
    values = []
    rows[0].append("std Temperatur Nicht Wald (std pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_nicht_wald"])
        values.append(setdata[file]["temperature_data"]["std_temp_nicht_wald"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))


    # 27. Spalte
    values = []
    rows[0].append("STD Gesamtbild")
    for count, file in enumerate(setdata):
        rows[count+1].append(setdata[file]["temperature_data"]["std_temp_all"])
        values.append(setdata[file]["temperature_data"]["std_temp_all"])
    rows[count+2].append(sum(values)/len(values))
    rows[count+3].append(statistics.stdev(values))

    rows[0].append("Temperaturbereich Grün (pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(f'{setdata[file]["temperature_data"]["temperaturbereiche"]["gruene_pixel"][0]} °C bis {setdata[file]["temperature_data"]["temperaturbereiche"]["gruene_pixel"][1]} °C')
    rows[count+2].append("")
    rows[count+3].append("")

    rows[0].append("Temperaturbereich Braun (pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(f'{setdata[file]["temperature_data"]["temperaturbereiche"]["braune_pixel"][0]} °C bis {setdata[file]["temperature_data"]["temperaturbereiche"]["braune_pixel"][1]} °C')
    rows[count+2].append("")
    rows[count+3].append("")

    rows[0].append("Temperaturbereich Wald (pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(f'{setdata[file]["temperature_data"]["temperaturbereiche"]["wald_pixel"][0]} °C bis {setdata[file]["temperature_data"]["temperaturbereiche"]["wald_pixel"][1]} °C')
    rows[count+2].append("")
    rows[count+3].append("")

    rows[0].append("Temperaturbereich All (pro Bild)")
    for count, file in enumerate(setdata):
        rows[count+1].append(f'{setdata[file]["temperature_data"]["temperaturbereiche"]["alle_pixel"][0]} °C bis {setdata[file]["temperature_data"]["temperaturbereiche"]["alle_pixel"][1]} °C')
    rows[count+2].append("")
    rows[count+3].append("")

with open(output_path, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    for row in rows:
        writer.writerow(row)
