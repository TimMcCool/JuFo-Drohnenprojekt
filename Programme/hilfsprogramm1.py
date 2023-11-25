# Nutzt Skript 1, um Grüntöne / Brauntöne in festgelegten Luftbildern geeigneter Waldstücke (händisch ausgewählt) zu sammeln
# Aus den gesammelten Farbtripeln werden dann einige zufällig ausgewählt und in einer JSON-Datei gespeichert
# Die gespeicherten Farbtripel werden Skript 3 als Referenzfarbtripel gegeben

import json
import numpy as np
import random
from PIL import Image

import hilfsfunktionen
import skript1_hsv

farbe = "grün" # Ob grüne oder braune Farbtripel gesammelt werden sollen
output_path = "/Programme/Skript 3 Referenzfabrtripel/brauntoene_alle_rgb.json" # Der Pfad der Datei, in der die Ausgabe gespeichert werden soll

assert farbe == "grün" or farbe == "braun"

if farbe == "grün":

    # Grüner Farbbereich (an Rändern verkleinert):
    h_bereiche = [(75,180),(180,285)]
    s_bereiche = [(30,100),(12,16)]
    v_bereiche = [(0,100),(0,8)]

    collect_per_image = 11 # Anzahl an Farbwerten, die pro Bild gesammelt werden
    luftbilder_paths = [
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 16-07-22/Flugroute 2/YUN00006.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 16-07-22/Flugroute 2/YUN00001.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 16-07-22/Flugroute 2/YUN00008.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 29-08-22/Flugroute 2/YUN00001.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 29-08-22/Flugroute 2/YUN00003.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 29-08-22/Flugroute 2/YUN00007.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 27-04-22/Route 2 - 1. Versuch/YUN00001.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 27-04-22/Route 2 - 1. Versuch/YUN00002.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 27-04-22/Route 2 - 1. Versuch/YUN00003.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 27-04-22/Route 2 - 1. Versuch/YUN00004.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Rohdaten/Bilder 27-04-22/Route 2 - 1. Versuch/YUN00007.jpg",

    ]

elif farbe == "braun":

    # Brauner Farbbereich (an Rändern verkleinert):
    h_bereiche = [(0,45),(315,360)]
    s_bereiche = [(20,100),(20,100)]
    v_bereiche = [(25,100),(25,100)]

    collect_per_image = 12
    luftbilder_paths = [
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-02-23/Flugroute 1/YUN00015.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-11-23/Flugroute 1/YUN00003.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-11-23/Flugroute 1/YUN00006.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-11-23/Flugroute 2/2. Flug/YUN00003.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-02-23/Flugroute 1/YUN00016.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-02-23/Flugroute 1/YUN00017.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 09-02-23/Flugroute 2/YUN00008.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 29-08-22/Flugroute 2/YUN00001.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 29-08-22/Flugroute 2 niedriger/YUN00009.jpg",
        "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Rohdaten/Bilder 29-08-22/Flugroute 2 niedriger/YUN00010.jpg"
    ]

farbtoene = []

for path in luftbilder_paths:
    # Alle ausgewählten Bilder öffnen und Farben herausfiltern:
    im = Image.open(path)
    pixel_indices, pix = skript1_hsv.filter_pixels(im, h_bereiche, s_bereiche, v_bereiche)
    pixels = pix.reshape(pix.shape[0]*pix.shape[1], -1)
    # Gefilterte Farbwerte aus dem Bild extrahieren:
    farbwerte = list(pixels[pixel_indices])
    # Farbwerte mischen und einen Teil der Farbwerte in Liste (JSON-serializable) speichern:
    random.shuffle(farbwerte)
    for i in range(collect_per_image):
        farbwert = farbwerte.pop(0)
        farbtoene.append([int(i) for i in farbwert])

# Gesammelte Farbwerte in JSON-Datei speichern
with open(output_path, "w") as f:
    json.dump(farbtoene, f)
