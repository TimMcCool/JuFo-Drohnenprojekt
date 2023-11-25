# Findet Pixel, für deren RGB-Farbtripel die Bedingungen G/B > min_gr_gb_quot und G/R > min_gr_gb_quot gelten
# Verwendet zur Bestimmung des Grünanteils

from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen

# Parameter
path_luftbild = "C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Bilder/Eingabebilder/Bilder 22-10-22/Flugroute 1/YUN00005.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das ausgewertet werden soll
min_gr_gb_quot = 1.05

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
    pix = np.array(im) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Luftbild nicht farbig")
        exit()

    r, g, b = pix[:,:,0].flatten(), pix[:,:,1].flatten(), pix[:,:,2].flatten() #Erzeugen von eindimensionalen np Arrays mit den R, G, B Werten aller Pixel
    pixel_count = len(r)
    return r, g, b


def filter_pixels(im, min_gr_gb_quot, *, new_size=1080):
    """
    Filtert alle Pixel heraus, die im durch min_gr_gb_quot definierten Farbbereich liegen
    Diese Funktion kann auch von anderen Skripten importiert und ausgeführt werden

    Args:
        im (Image): Das Bild, für das alle Indices zurückgegeben werden sollen
        min_rg_gb_quot (float): Definiert das minimale Verhältnis von G/R und G/B für alle im Farbbereich liegenden Pixel
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll (standardmäßig 1080 Pixel)
    Returns:
        np.array: Indices aller Pixel, die im Farbbereich liegen
        np.array: Das Eingabebild als dreidimensionales numpy array
    """
    r, g, b = parse_image(im, new_size=new_size)
    # Ersetzen von 0 durch 1 in r und b, um Division durch 0 zu verhindern:
    r[r == 0] = 1
    b[b == 0] = 1
    # Erhöhen von g um c (c=3)
    g = np.array(g, dtype=np.uint32) #Ursprünglicher Datentyp von g ist uint8, der nur Werte im Bereich [0,255] erlaubt. Konvertieren zu uint32, um Addieren von 3 zu ermöglichen
    g += 3
    # Farbbereich ermitteln:
    index_farbbereich = np.intersect1d(
        np.where(g/r >= min_gr_gb_quot)[0],
        np.where(g/b >= min_gr_gb_quot)[0]
    )
    return index_farbbereich, pix

# Globale Variablen initialisieren
pix = None
pixel_count = None

# Farbbereiche filtern und Ergebnis ausgeben

if __name__ == "__main__":
    im = Image.open(path_luftbild)
    im.show()

    pixel_indices, pix = filter_pixels(im, min_gr_gb_quot)
    print("[Skript 2] Anteil Pixel im Farbbereich:", len(pixel_indices)*100 / pixel_count, "%")
    pix_marked = hilfsfunktionen.mark_area(pix, pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 2] Pixel im Farbbereich")
    plt.show()

'''# Markiertes Bild, markierte Farbwerte und Array mit Indices speichern

pixels = pix.reshape(pix.shape[0]*pix.shape[1], -1)
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript5_indices.json", "w") as f:
    json.dump([i.item() for i in pixel_indices], f)
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript5_colors.json", "w") as f:
    json.dump([[o.item() for o in i] for i in pixels[pixel_indices]], f)
im_marked = Image.fromarray(pix_marked)
im_marked.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript5_image.png")'''
