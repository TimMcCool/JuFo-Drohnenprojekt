# Wertet automatisch alle Eingabebilder mit allen Skripten aus und speichert die Ergebnisse in einer JSON-Datei. Gibt den Fortschritt in der Konsole aus

import skript1_hsv
import skript2_rgb
import skript3_rgb
import skript4_rgb
import skript5_hsv
import skript6_rgb
import skript7
import skript8
import hilfsfunktionen

import os
from copy import deepcopy
from PIL import Image
import json
import numpy as np

# Ordner und den Ordnern untergeordnete Unterordner, die nach Bildern durchsucht werden
ordner = ["Bilder 26-05-23", "Bilder 29-08-22", "Bilder 22-10-22", "Bilder 09-02-23", "Bilder 23-03-23", "Bilder 27-04-22", "Bilder 16-07-22", "Bilder 09-11-23", "Kalibrierungsbilder"]
unterordner = ["Flugroute 2","Flugroute 1"]

# Bereits ausgewertete Daten öffnen
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/all_outputs.json") as f:
    data = json.load(f)

# Parameter für Skript 3
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Skript 3 Referenzfarbtripel/gruentoene_alle_rgb.json") as f:
    skript3_farbwerte_gruen = json.load(f)
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Skript 3 Referenzfarbtripel/brauntoene_alle_rgb.json") as f:
    skript3_farbwerte_braun = json.load(f)

skript3_max_distanz_gruen = 15
skript3_max_distanz_braun = 14

for o in ordner:
    print("Ordner", o)
    if o in data:
        data_ordner = data[o]
    else:
        data_ordner = {}

    for u in unterordner:
        print("Unterordner", u)
        if u in data_ordner:
            data_unterordner = data_ordner[u]
        else:
            data_unterordner = {}
        files = os.listdir("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/"+o+"/"+u+"/")
        files = list(filter(lambda filename : ".jpg" in filename, files))

        for file in files:
            try:
                image_name = file.split(".")[0]
                if image_name in data_unterordner:
                    continue
                print("Gerade wird ausgewertet: Bild", image_name)

                im_luftbild = Image.open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/"+o+"/"+u+"/"+image_name+".jpg")
                try:
                    im_waermebild = Image.open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/"+o+"/"+u+"/"+image_name+".jpeg")
                    im_luftbild_cut = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild) #Luftbild ins Format der Wärmebilder bringen
                except FileNotFoundError:
                    im_waermebild = None #Kein Wärmebild verfügbar (dies ist bei einigen Datensätzen der Fall)

                image_data = {"grün_anteil" : {}, "baumbewuchs_anteil":{}, "braun_anteil":{}, "schnittmengen":{}, "temperature_data":{}, "anteil_wald_gruen":None, "anteil_wiese_gruen":None}

                if "26-05-23" in o or ("22-10-22" in o or "23-03-23" in o):
                    try:
                        skala_min = 5
                        skala_max = 44
                        # In diesem Datensatz ist der von der Farbskala abgedeckte Temp.Bereich bekannt, Auswertung mit Skript 7
                        temperatures_flattened, indices_gruen, indices_braun, indices_wald = skript8.get_temperature_data(im_waermebild, im_luftbild)

                        image_data["temperature_data"]["avg_temp_gruen"] = np.mean(temperatures_flattened[indices_gruen])
                        image_data["temperature_data"]["avg_temp_nicht_gruen"] = np.mean(np.delete(temperatures_flattened, indices_gruen))
                        image_data["temperature_data"]["avg_temp_braun"] = np.mean(temperatures_flattened[indices_braun])
                        image_data["temperature_data"]["avg_temp_nicht_braun"] = np.mean(np.delete(temperatures_flattened, indices_braun))
                        image_data["temperature_data"]["avg_temp_wald"] = np.mean(temperatures_flattened[indices_wald])
                        image_data["temperature_data"]["avg_temp_nicht_wald"] = np.mean(np.delete(temperatures_flattened, indices_wald))
                        image_data["temperature_data"]["avg_temp_all"] = np.mean(temperatures_flattened)

                        image_data["temperature_data"]["std_temp_gruen"] = np.std(temperatures_flattened[indices_gruen]) # std bedeutet STABW
                        image_data["temperature_data"]["std_temp_nicht_gruen"] = np.std(np.delete(temperatures_flattened, indices_gruen))
                        image_data["temperature_data"]["std_temp_braun"] = np.std(temperatures_flattened[indices_braun])
                        image_data["temperature_data"]["std_temp_nicht_braun"] = np.std(np.delete(temperatures_flattened, indices_braun))
                        image_data["temperature_data"]["std_temp_wald"] = np.std(temperatures_flattened[indices_wald])
                        image_data["temperature_data"]["std_temp_nicht_wald"] = np.std(np.delete(temperatures_flattened, indices_wald))
                        image_data["temperature_data"]["std_temp_all"] = np.std(temperatures_flattened)

                        image_data["temperature_data"]["temperaturbereiche"] = {}
                        image_data["temperature_data"]["temperaturbereiche"]["gruene_pixel"] = (min(temperatures_flattened[indices_gruen]), max(temperatures_flattened[indices_gruen]))
                        image_data["temperature_data"]["temperaturbereiche"]["braune_pixel"] = (min(temperatures_flattened[indices_braun]), max(temperatures_flattened[indices_braun]))
                        image_data["temperature_data"]["temperaturbereiche"]["wald_pixel"] = (min(temperatures_flattened[indices_wald]), max(temperatures_flattened[indices_wald]))
                        image_data["temperature_data"]["temperaturbereiche"]["alle_pixel"] = (min(temperatures_flattened), max(temperatures_flattened))
                    except Exception as e:
                        print("Failed to calc temperture data, error:", e)
                if not "26-05-23" in o:
                    # --- WALDANTEIL BESTIMMEN ---

                    if im_waermebild is None:
                        image_data["baumbewuchs_anteil"]["skript_4"] = None
                        image_data["baumbewuchs_anteil"]["skript_5"] = None
                        image_data["baumbewuchs_anteil"]["skript_6"] = None
                    else:

                        # Auswertung mit Skript 4

                        skript4_output, skript4_pix = skript4_rgb.filter_pixels(im_waermebild)
                        image_data["baumbewuchs_anteil"]["skript_4"] = len(skript4_output) / (skript4_pix.shape[0] * skript4_pix.shape[1])

                        # Auswertung mit Skript 5

                        if not ("22-10-22" in o or "23-03-23" in o):
                            skript5_output, skript5_pix = skript5_hsv.filter_pixels(im_waermebild)
                            image_data["baumbewuchs_anteil"]["skript_5"] = len(skript5_output) / (skript5_pix.shape[0] * skript5_pix.shape[1])
                        else:
                            image_data["baumbewuchs_anteil"]["skript_5"] = None

                        # Auswertung mit Skript 6

                        skript6_output, skript6_pix = skript6_rgb.filter_pixels(im_waermebild)
                        image_data["baumbewuchs_anteil"]["skript_6"] = len(skript6_output) / (skript6_pix.shape[0] * skript6_pix.shape[1])

                        # Auswertung mit Skript 7
                        schnittmenge_skript1_skript5, schnittmenge_skript1_nicht_skript5, pixel_count = skript7.schnittmengen_bestimmen(im_luftbild, im_waermebild)
                        image_data["anteil_wald_gruen"] = len(schnittmenge_skript1_skript5)/pixel_count
                        image_data["anteil_wiese_gruen"] = len(schnittmenge_skript1_nicht_skript5)/pixel_count

                data_unterordner[image_name] = image_data
                data_ordner[u] = data_unterordner
                data[o] = data_ordner

                with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/all_outputs.json", "w") as f:
                    json.dump(data, f, indent=4)

                if "skript_1" in image_data["grün_anteil"]:
                    continue

                # --- ANTEIL GRÜNER WALD BESTIMMEN ---

                # Auswertung mit Skript 1

                #grüner Farbbereich:
                h_bereiche = [(60,180),(180,300)]
                s_bereiche = [(10,100),(1,25)]
                v_bereiche = [(0,100),(0,20)]

                skript1_output, skript1_pix = skript1_hsv.filter_pixels(im_luftbild, h_bereiche, s_bereiche, v_bereiche)
                image_data["grün_anteil"]["skript_1"] = len(list(skript1_output)) / (skript1_pix.shape[0] * skript1_pix.shape[1])

                # Auswertung mit Skript 2

                # grüner Farbbereich:
                min_gr_gb_quot = 1.05

                skript2_output, skript2_pix = skript2_rgb.filter_pixels(im_luftbild, min_gr_gb_quot)
                image_data["grün_anteil"]["skript_2"] = len(skript2_output) / (skript2_pix.shape[0] * skript2_pix.shape[1])

                # Schnittmenge Skript 1 und Skript 2

                skript1_2_schnittmenge = np.intersect1d(skript1_output, skript2_output)
                image_data["grün_anteil"]["skript_1_2_schnittmenge"] = len(skript1_2_schnittmenge) / (skript1_pix.shape[0] * skript1_pix.shape[1])

                # Auswertung mit Skript 3

                skript3_output, skript3_pix = skript3_rgb.filter_pixels(im_luftbild, skript3_farbwerte_gruen, skript3_max_distanz_gruen)
                image_data["grün_anteil"]["skript_3"] = len(list(skript3_output)) / (skript3_pix.shape[0] * skript3_pix.shape[1])

                if im_waermebild is not None:
                    # Schnittmenge Skript 1 und Skript 5

                    skript1_output_cut, skript1_pix_cut = skript1_hsv.filter_pixels(im_luftbild_cut, h_bereiche, s_bereiche, v_bereiche)
                    skript1_4_schnittmenge = np.intersect1d(skript1_output_cut, skript4_output)
                    image_data["schnittmengen"]["baumbewuchs_grün_anteil_skript_1"] = len(skript1_4_schnittmenge) / len(skript4_output)
                else:
                    image_data["schnittmengen"]["baumbewuchs_grün_anteil_skript_1"] = None


                # --- ANTEIL BRAUNER WALD BESTIMMEN ---

                # Auswertung mit Skript 1

                #brauner Farbbereich
                h_bereiche = [(0,60),(300,360)]
                s_bereiche = [(8,100),(8,100)]
                v_bereiche = [(0,100),(0,100)]

                skript1_output_braun, skript1_pix = skript1_hsv.filter_pixels(im_luftbild, h_bereiche, s_bereiche, v_bereiche)
                image_data["braun_anteil"]["skript_1"] = len(list(skript1_output_braun)) / (skript1_pix.shape[0] * skript1_pix.shape[1])

                # Auswertung mit Skript 3

                skript3_output_braun, skript3_pix = skript3_rgb.filter_pixels(im_luftbild, skript3_farbwerte_braun, skript3_max_distanz_braun)
                image_data["braun_anteil"]["skript_3"] = len(list(skript3_output_braun)) / (skript3_pix.shape[0] * skript3_pix.shape[1])

                # Schnittmenge Skript 1 und Skript 5
                if im_waermebild is not None:
                    skript1_output_cut, skript1_pix_cut = skript1_hsv.filter_pixels(im_luftbild_cut, h_bereiche, s_bereiche, v_bereiche)
                    skript1_4_schnittmenge = np.intersect1d(skript1_output_cut, skript4_output)
                    image_data["schnittmengen"]["baumbewuchs_braun_anteil_skript_1"] = len(skript1_4_schnittmenge) / len(skript4_output)
                else:
                    image_data["schnittmengen"]["baumbewuchs_braun_anteil_skript_1"] = None

                # --- SPEICHERN ---

                data_unterordner[image_name] = image_data
                data_ordner[u] = data_unterordner
                data[o] = data_ordner

                with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/all_outputs.json", "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/"+o+"/"+u+"/", file, "Fehler", e)
