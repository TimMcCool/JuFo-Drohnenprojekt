# Dient zur Auswertung von Wärmebildern
# Vom Skript ermittelter Parameter: Waldanteil
# Funktionsweise: Filtert alle "kalten" Pixel heraus. Für "kalte" Pixel gilt: (t - temp_min) / (temp_max - temp_min) < bias
# Parameter: bias, Dateipfad zu einer JSON Datei mit den Farbwerten der Farbskala, Dateipfad des Eingabewärmebilds, Dateipfad des zugehörigen Luftbilds (zur Visualisierung des Ergebnisses im Luftbild)

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen
import hilfsprogramm3

#Parameter
path_luftbild = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das zum Wärmebild ehört (wird nicht ausgewertet, sondern nur zur Visualisierung genutzt)
path_waermebild = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpeg" #Hier ist der Dateipfad zum Wärmebild anzugeben, das ausgewertet werden soll
path_farbskala_json = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Farbskalen/drohne_waermebild_farbskala.json" #Hier ist der Dateipfad zur JSON-Datei, die die Farbwerte der Farbskala enthält, anzugeben
bias = 0.42

# Breite, auf die Eingabebild standardmäßig skaliert werden soll
image_scalation = 160

# Maximale und minimale Temperatur der Wärmebild-Farbskala festlegen
# Die Temperaturen werden vor der Auswertung ohnehin normalisiert, daher kann für skala_min und skala_max jeder beliebige Wert genommen werden
skala_min = 0
skala_max = 1

def parse_image(im, *, new_size):
    """
    Bild einlesen und verarbeiten

    Args:
        im (Image): Zu verarbeitendes Bild
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll
    """
    global pix
    im = hilfsfunktionen.scale_image(im, new_size)
    pix = np.array(im) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Wärmebild nicht farbig")
        exit()
    return pix

def filter_pixels(im_waermebild, bias=bias, *, new_size=image_scalation):
    '''
    Gibt die Indices aller "kalten" Pixel des Bilds zurück. Für "kalte" Pixel gilt: (t - temp_min) / (temp_max - temp_min) < bias

    Args:
        im_waermebild (Image): Wärmebild, für das die Indices ermittelt werden sollen
        bias (float): Wert für den bias-Parameter
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll
    Returns:
        np.array: Die Indices aller "kalten" Pixel
        np.array: Das Eingabebild als dreidimensionales numpy array
    '''
    global pixel_count

    pix = parse_image(im_waermebild, new_size=new_size)
    temperatures = hilfsprogramm3.calculate_all_values(pix, skala_min, skala_max) # Temperaturen mit Hilfsprogramm 3 berechnen
    temperatures_flattened = temperatures.flatten() #2D-Array mit Temperaturen in 1D-Array umwandeln
    pixel_count = len(temperatures_flattened)

    temperatures_normalized = (temperatures_flattened-min(temperatures_flattened))/(max(temperatures_flattened)-min(temperatures_flattened)) # Temperaturen normalisieren bzw. in Bereich [0;1] bringen
    return np.where(temperatures_normalized < bias)[0], pix

# Initialisieren globaler Variablen

pix = None
pixel_count = None

# Farbskala aus JSON-Datei einlesen

with open(path_farbskala_json, "r") as f:
    colors = json.loads(f.read())

if __name__ == "__main__":

    # Wärmebild einlesen

    im_waermebild = Image.open(path_waermebild)


    # Pixel filtern und Ergebnis ausgeben und in Wärmebild visualisieren

    indices_bewaldet, pix = filter_pixels(im_waermebild, bias) #Findet die Indices aller Pixel, die im Temperaturbereich liegen
    print("[Skript 4] Anteil “kalter“ Pixel bzw. Waldanteil:", len(indices_bewaldet) *100 / pixel_count, "%")

    pix_bewaldet = hilfsfunktionen.mark_area(pix, indices_bewaldet)
    imgplot = plt.imshow(pix_bewaldet)
    plt.title("[Skript 4] 'Kalte' bzw. mit Wald bewachsene Pixel")
    plt.show()

    # Zugehöriges Luftbild einlesen und verarbeiten

    im_luftbild = Image.open(path_luftbild)
    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    print(im_luftbild.size)
    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, image_scalation)
    im_luftbild.show()
    pix_luftbild = np.array(im_luftbild) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix_luftbild.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte (Transparenz) gelöscht werden
        pix_luftbild = np.delete(pix_luftbild, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Luftbild nicht farbig")
        exit()

    # Ergebnis in Luftbild visualisieren

    pix_bewaldet = hilfsfunktionen.mark_area(pix_luftbild, indices_bewaldet)
    imgplot = plt.imshow(pix_bewaldet)
    plt.title("[Skript 4] In Luftbild visualisiert: 'Kalte' bzw. mit Wald bewachsene Pixel")
    plt.show()

'''# Markiertes LuftbBild und Array mit Indices speichern
im_marked = Image.fromarray(pix_bewaldet)
im_marked.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript4_image.png")
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript4_indices.json", "w") as f:
    json.dump([i.item() for i in indices_bewaldet], f)'''
