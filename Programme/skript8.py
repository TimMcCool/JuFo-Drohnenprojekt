# Berechnet die Durchschnittstemperaturen grüner, brauner und bewaldeter Bereiche

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen
import skript1_hsv
import skript4_rgb
import hilfsprogramm3

# Parameter:
path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das ausgewertet werden soll
path_waermebild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpeg" #Hier ist der Dateipfad zum Wärmebild anzugeben, das ausgewertet werden soll

# Maximale und minimale Temperatur der Wärmebild-Farbskala festlegen
skala_min = 5
skala_max = 44

#Kameraeinstellung beim Flug vom 26.05.2023: Skala reicht von 5°C bis 44°C


def get_temperature_data(im_waermebild, im_luftbild):
    """
    Wertet Eingebabeluftbild mit Skript 1 (Grünanteil, Braunanteil) aus. Wertet zugehöriges Wärmebild mit Skript 4 aus (Waldanteil).
    Bestimmt anschließend die Temperatur an jedem Wärmebildpixel mit Hilfsprogramm 3.
    Gibt die Ergebnisse zurück. Die Berechnung der Durchschnittstemperaturen erfolgt außerhalb von dieser Funktion.

    Args:
        im_luftbild (Image): Eingabeluftbild
        im_waermebild (Image): Zum Luftbild gehörendes Wärmebild
    Returns:
        temperatures_flattened (np.array): 1D np array, indem die Temperaturen aller Wärmebildpixel aneinandergereiht sind
        indices_gruen (np.array): Indices aller grünen Pixel. Kann zum Filtern von temperatures_flattened auf Temperaturen grüner Pixel verwendet werden
        indices_braun (np.array): Indices aller braunen Pixel. Kann zum Filtern von temperatures_flattened auf Temperaturen brauner Pixel verwendet werden
        indices_wald (np.array): Indices aller bewaldeter Pixel. Kann zum Filtern von temperatures_flattened auf Temperaturen bewaldeter Pixel verwendet werden
    """
    im_waermebild = hilfsfunktionen.scale_image(im_waermebild, 160)
    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, 160)

    pix = np.array(im_waermebild) #Image-Objekt in 3-dimensionalen np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Bild nicht farbig")
        exit()

    # Mit Skript 1 grüne und braune Pixel bestimmen

    h_bereiche = [(60,180),(180,300)]
    s_bereiche = [(11,100),(2,25)]
    v_bereiche = [(0,100),(0,20)]
    indices_gruen, _ = skript1_hsv.filter_pixels(im_luftbild, h_bereiche, s_bereiche, v_bereiche, new_size=im_luftbild.size[0])

    h_bereiche = [(0,60),(300,360)]
    s_bereiche = [(8,100),(8,100)]
    v_bereiche = [(0,100),(0,100)]
    indices_braun, _ = skript1_hsv.filter_pixels(im_luftbild, h_bereiche, s_bereiche, v_bereiche, new_size=im_luftbild.size[0])

    # Mit Skript 4 bewaldete Pixel bestimmen
    indices_wald, _ = skript4_rgb.filter_pixels(im_waermebild)

    # Mit Hilfsprogramm 3 Temperaturen ausrechnen

    temperatures = hilfsprogramm3.calculate_all_values(pix, skala_min, skala_max) # 2D-Array mit Temperaturen jedes Pixels. Achse 1: x-Position des Pixels, Achse 2: y-Position des Pixels
    temperatures_flattened = temperatures.flatten() # In 1D-Array umwandeln

    return temperatures_flattened, indices_gruen, indices_braun, indices_wald

if __name__ == "__main__":

    # Bilder einlesen

    im_waermebild = Image.open(path_waermebild)
    im_luftbild = Image.open(path_luftbild)

    # Daten auswerten

    temperatures_flattened, indices_gruen, indices_braun, indices_wald = get_temperature_data(im_waermebild, im_luftbild)

    # Durchschnittstemperaturen und STABW der Temperaturen für grüne, braune und alle Pixel berechnen

    avg_temp_gruen = np.mean(temperatures_flattened[indices_gruen])
    avg_temp_nicht_gruen = np.mean(np.delete(temperatures_flattened, indices_gruen))
    avg_temp_braun = np.mean(temperatures_flattened[indices_braun])
    avg_temp_nicht_braun = np.mean(np.delete(temperatures_flattened, indices_braun))
    avg_temp_wald = np.mean(temperatures_flattened[indices_wald])
    avg_temp_nicht_wald = np.mean(np.delete(temperatures_flattened, indices_wald))
    avg_temp_all = np.mean(temperatures_flattened)

    std_temp_gruen = np.std(temperatures_flattened[indices_gruen]) # std bedeutet STABW
    std_temp_nicht_gruen = np.mean(np.delete(temperatures_flattened, indices_gruen))
    std_temp_braun = np.std(temperatures_flattened[indices_braun])
    std_temp_nicht_braun = np.mean(np.delete(temperatures_flattened, indices_braun))
    std_temp_wald = np.std(temperatures_flattened[indices_wald])
    std_temp_nicht_wald = np.mean(np.delete(temperatures_flattened, indices_wald))
    std_temp_all = np.std(temperatures_flattened)

    print("Durchschnittstemperatur grüner Pixel:", avg_temp_gruen)
    print("Durchschnittstemperatur nicht grüner Pixel:", avg_temp_nicht_gruen)
    print("Durchschnittstemperatur brauner Pixel:", avg_temp_braun)
    print("Durchschnittstemperatur nicht brauner Pixel:", avg_temp_nicht_braun)
    print("Durchschnittstemperatur bewaldeter Pixel:", avg_temp_wald)
    print("Durchschnittstemperatur nicht bewaldeter Pixel:", avg_temp_nicht_wald)
    print("Durchschnittstemperatur aller Pixel:", avg_temp_all)

    print("STABW Temperatur grüner Pixel:", std_temp_gruen)
    print("STABW Temperatur nicht grüner Pixel:", std_temp_nicht_gruen)
    print("STABW Temperatur brauner Pixel:", std_temp_braun)
    print("STABW Temperatur nicht brauner Pixel:", std_temp_nicht_braun)
    print("STABW Temperatur bewaldeter Pixel:", std_temp_wald)
    print("STABW Temperatur nicht bewaldeter Pixel:", std_temp_nicht_wald)
    print("STABW Temperatur aller Pixel:", std_temp_all)

    print("Temperaturbereich grüner Pixel:", min(temperatures_flattened[indices_gruen]), "bis", max(temperatures_flattened[indices_gruen]))
    print("Temperaturbereich brauner Pixel:", min(temperatures_flattened[indices_braun]), "bis", max(temperatures_flattened[indices_braun]))
    print("Temperaturbereich bewaldeter Pixel:", min(temperatures_flattened[indices_wald]), "bis", max(temperatures_flattened[indices_wald]))
    print("Temperaturbereich aller Pixel:", min(temperatures_flattened), "bis", max(temperatures_flattened))
