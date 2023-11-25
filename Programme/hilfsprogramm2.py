# Speichert Farbwerte einer Farbskala für eine Wärmebildkamera in eine JSON Datei
# Farbskala muss wie folgt aufgebaut sein:
# Oben Farben für hohe Temperaturen, unten für niedrige Temperaturen

from PIL import Image
import hilfsfunktionen
import numpy as np
import json

# Anzahl zu extrahierender Farbskala-Abstufungen festlegen

num_farbwerte = 200

# Bild mit Farbskala einlesen

im = Image.open("/Programme/Farbskalen/drohne_waermebild_farbskala.png")
im = im.resize((round((num_farbwerte/im.size[1])*im.size[0]), num_farbwerte))
pix = np.array(im) #Image-Objekt in 3-dimensionalen np Array umwandeln

# Farbwerte extrahieren

colors = []
for row in pix:
    color = tuple(row[0]) #Ersten Pixel der Reihe nehmen
    color = [int(color[i]) for i in range(3)] #Werte des RGB-Farbtripels von np.uint32 zu int konvertieren und als RGB-Farbtripel speichern
    colors.append(color) #RGB-Farbtripel zur Liste hinzufügen
colors.reverse() # Gesammelte Farben umkehren, sodass die kalten Farben in der Liste vorne und die warmen Farben hinten sind

# Farbwerte in JSON Datei speichern

with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Farbskalen/drohne_waermebild_farbskala.json", "w") as f:
    json.dump(colors, f, indent = None)
