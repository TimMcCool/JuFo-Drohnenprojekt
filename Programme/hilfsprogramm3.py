# Rechnet die Farben eines Wärmebildes in Temperaturen um
# Das Hilfsprogramm kann auch bei Grafiken (z.B. Satellitenbilder), die Indices farblich darstellen, zur exakten Bestimmung der Werte verwendet werden

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen

# Maximale und minimale Wert der Wärmebild-Farbskala festlegen
#Kameraeinstellung beim Flug vom 26.05.2023: Skala reicht von 5°C bis 44°C

skala_min = 5
skala_max = 44

path_waermebild = "/Bilder/Eingabebilder/Bilder 26-05-23/Flugroute 1/YUN00018.jpeg" # Pfad zum Wärmebild, dessen Temperaturen umgerechnet werden sollen
path_luftbild = "/Bilder/Eingabebilder/Bilder 26-05-23/Flugroute 1/YUN00018.jpg" # Pfad zum Luftbild, das zum Wärmebild gehört

# Variable für die einzulesende Farbskala initialisieren
farbskala = []

def color_to_value(color : tuple, skala_min, skala_max):
    """
    Berechnet den zu einer Wärmebild-Farbe gehörenden Temperaturwert

    Args:
        color (tuple or list): RGB-Farbtripel, für die der zugehörige Temperaturwert berechnet werden soll
        skala_min (float), skala_max (float): Der von der Farbskala abgedeckte Wertbereich
    Returns:
        float: Temperaturwert
    """

    # Bestimmen des Farbwerts der Farbskala, das der gegebenen Farbe am nächsten liegt:
    min_distance = float("inf")
    min_distance_index = 0
    for i in range(len(farbskala)):
        distance = hilfsfunktionen.distance(farbskala[i], color)
        if distance < min_distance:
            min_distance = distance
            min_distance_index = i
    # Berechnen und zurückgeben der Werte:
    return (min_distance_index / len(farbskala)) * (skala_max - skala_min) + skala_min

def calculate_all_values(pix, skala_min, skala_max, path_farbskala_json = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Farbskalen/drohne_waermebild_farbskala.json", *, round_one_digit=False):
    """
    Berechnet für alle Wärmebildpixel die Temperaturen

    Args:
        pix (np.array): Das Eingabewärmebild als 3D numpy array
        skala_min (float), skala_max (float): Der von der Farbskala abgedeckte Wertbereich
        path_farbskala_json (str): Pfad zur JSON Datei, die die Farbwerte der Farbskala enthält
        round_one_digit (boolean): gibt an, ob die Werten auf eine Nachkommastelle gerundet werden sollen (standardmäßig auf False gesetzt)
    """
    global farbskala
    with open(path_farbskala_json, "r") as f:
        farbskala = json.loads(f.read())

    temperatures = []
    for i in range(len(pix)):
        row = []
        for o in range(len(pix[i])):
            temp = color_to_value(pix[i][o], skala_min, skala_max)
            if round_one_digit:
                temp = round(temp*10)/10
            row.append(temp)
        temperatures.append(row)
    return np.array(temperatures)

if __name__ == "__main__":
    # Bild einlesen

    im_waermebild = Image.open(path_waermebild)
    im_waermebild = hilfsfunktionen.scale_image_based_on_width(im_waermebild, 160)
    pix = np.array(im_waermebild) #Image-Objekt in 3-dimensionalen np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Bild nicht farbig")
        exit()

    im_luftbild = Image.open(path_luftbild)

    # Werten ausrechnen

    temperatures = calculate_all_values(pix, skala_min, skala_max, round_one_digit=True, path_farbskala_json = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Farbskalen/drohne_waermebild_farbskala.json")

    # Luftbild auf Wärmebild zuschneiden
    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    im_luftbild = hilfsfunktionen.scale_image_based_on_width(im_luftbild, im_waermebild.size[0])

    # Werten auf Pixel des Wärmebilds schreiben

    im_waermebild = hilfsfunktionen.scale_image_based_on_width(im_waermebild, im_waermebild.size[0]*30)
    im_waermebild.show()
    draw = ImageDraw.Draw(im_waermebild)
    font = ImageFont.load_default()
    for i in range(len(temperatures)):
        for o in range(len(temperatures[i])):
            draw.text((o*30+3, i*30+3),str(temperatures[i][o]),(255,255,255),font=font)

    im_waermebild.show()
    im_waermebild.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/Hilfsprogramm3_waermebild.png")

    # Werte auf Pixel des zugeh. Luftbilds schreiben

    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, im_luftbild.size[0]*30)
    draw = ImageDraw.Draw(im_luftbild)
    font = ImageFont.load_default()
    for i in range(len(temperatures)):
        for o in range(len(temperatures[i])):
            draw.text((o*30+3, i*30+3),str((round(temperatures[i][o])*100)/100),(255,255,255),font=font)

    im_luftbild.show()
    im_luftbild.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/Hilfsprogramm3_luftbild.png")

    # Durchschnittstemperatur ausgeben
    print("Durchschnittswert:", np.average(temperatures))
