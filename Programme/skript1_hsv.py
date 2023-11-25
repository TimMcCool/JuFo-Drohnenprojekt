# Filter Pixel, bei denen das RGB-Farbtripel in einem von mehreren festgelegten Bereichen liegen
# Verwendet zur Bestimmung von Grünanteil und Braunanteil

from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen

# Parameter
path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das ausgewertet werden soll
farbe = "grün" #Auszuwertender Farbanteil ("grün" oder "braun")

if farbe == "grün":
    # Grüne Farbbereiche:
    h_bereiche = [(60,180),(180,300)]
    s_bereiche = [(10,100),(1,25)]
    v_bereiche = [(0,100),(0,20)]
elif farbe == "braun":
    # Braune Farbbereiche:
    h_bereiche = [(0,60),(300,360)]
    s_bereiche = [(8,100),(8,100)]
    v_bereiche = [(0,100),(0,100)]
assert farbe == "grün" or farbe == "braun"

def parse_image(im, *, new_size):
    """
    Bild einlesen und verarbeiten

    Args:
        im (Image): Zu verarbeitendes Bild
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll
    """
    global pix
    global pixel_count

    im = hilfsfunktionen.scale_image(im, new_size)
    pix = np.array(im) #Image-Objekt in 3-dimensionalen np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann werden die A-Werte (Transparenz) gelöscht
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß
        print("Fehler: Luftbild nicht farbig")
        exit()

    r, g, b = pix[:,:,0].flatten(), pix[:,:,1].flatten(), pix[:,:,2].flatten() #Erzeugen von eindimensionalen np Arrays mit den R, G, B Werten aller Pixel
    h, s, v = hilfsfunktionen.rgb_to_hsv(r, g, b) # Konvertieren nach HSV
    pixel_count = len(h) # Pixelanzahl speichern
    return h, s, v

def filter_pixels(im, h_bereiche, s_bereiche, v_bereiche, *, new_size=1080):
    """
    Filtert alle Pixel heraus, bei denen die HSV-Werte in einem der Farbbereiche liegen
    Diese Funktion kann auch von anderen Skripten importiert und ausgeführt werden

    Args:
        im (Image): Das Bild, für das alle Indices zurückgegeben werden sollen
        h_bereiche (list), s_bereiche (list) und v_bereiche (list): Definieren die zu filternden Farbbereiche
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll (standardmäßig 1080 Pixel)
    Returns:
        np.array: Indices aller Pixel, die in einem der Farbbereiche liegen liegen
        np.array: Das Eingabebild als dreidimensionales numpy array
    """

    h, s, v = parse_image(im, new_size=new_size)

    indices_aller_farbbereiche = []
    for bereich in range(len(h_bereiche)):
        index_hbereich = np.intersect1d(np.where(h >= h_bereiche[bereich][0])[0], np.where(h <= h_bereiche[bereich][1])[0])
        index_sbereich = np.intersect1d(np.where(s >= s_bereiche[bereich][0])[0], np.where(s <= s_bereiche[bereich][1])[0])
        index_vbereich = np.intersect1d(np.where(v >= v_bereiche[bereich][0])[0], np.where(v <= v_bereiche[bereich][1])[0])
        indices_aller_farbbereiche.append( np.intersect1d(np.intersect1d(index_hbereich, index_sbereich), index_vbereich) )

    return np.concatenate(indices_aller_farbbereiche), pix

# Globale Variablen initialisieren
pix = None
pixel_count = None

# Farbbereiche filtern und Ergebnis ausgeben

if __name__ == "__main__": # Die if-Abfrage sorgt dafür, dass dieser Programmteil nicht autom. ausgeführt wird, wenn das Skript von einem anderen Skript importiert wird
    im = Image.open(path_luftbild)
    im.show()

    pixel_indices, pix = filter_pixels(im, h_bereiche, s_bereiche, v_bereiche)
    print("[Skript 1] Anteil Pixel in den Farbbereichen:", len(pixel_indices)*100 / pixel_count, "%")
    pix_marked = hilfsfunktionen.mark_area(pix, pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 1] Pixel in den Farbbereichen")
    plt.show()
