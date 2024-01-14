# Dient zur Auswertung von Wärmebildern
# Vom Skript ermittelter Parameter: Waldanteil
# Funktionsweise: Findet im Wärmebild alle Pixel, die in einem bestimmten Farbbereich liegen
# Parameter: HSV-Farbbereich, Dateipfad zu einer JSON Datei mit den Farbwerten der Farbskala, Dateipfad des Eingabewärmebilds, Dateipfad des zugehörigen Luftbilds (zur Visualisierung des Ergebnisses im Luftbild)

from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen

#Parameter
path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das zum Wärmebild ehört (wird nicht ausgewertet, sondern nur zur Visualisierung genutzt)
path_waermebild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpeg" #Hier ist der Dateipfad zum Wärmebild anzugeben, das ausgewertet werden soll

# Farbbereich, der alle "kalten" Pixel abdeckt
h_bereiche = [(96, 240)]
s_bereiche = [(1,100)]
v_bereiche = [(1,100)]

# Breite, auf die Eingabebild standardmäßig skaliert werden soll
image_scalation = 1080

def parse_image(im, *, new_size):
    """
    Bild einlesen und verarbeiten

    Args:
        im (Image): Zu verarbeitendes Bild
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll
    """
    global pix
    global pixel_count

    #im = hilfsfunktionen.crop_luftbild_to_waermebild(im)
    im = hilfsfunktionen.scale_image(im, new_size)
    pix = np.array(im) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Wärmebild nicht farbig")
        exit()

    r, g, b = pix[:,:,0].flatten(), pix[:,:,1].flatten(), pix[:,:,2].flatten() #Erzeugen von eindimensionalen np Arrays mit den R, G, B Werten aller Pixel
    h, s, v = hilfsfunktionen.rgb_to_hsv(r, g, b)
    pixel_count = len(h)
    return h, s, v

def filter_pixels(im, *, new_size=image_scalation):
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

if __name__ == "__main__":
    im_waermebild = Image.open(path_waermebild)
    im_waermebild.show()

    pixel_indices, pix = filter_pixels(im_waermebild)
    print("[Skript 5] Anteil Pixel im Farbbereich:", len(pixel_indices)*100 / pixel_count, "%")
    pix_marked = hilfsfunktionen.mark_area(pix, pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 5] Wärmebild: Pixel in Farbbereich")
    plt.show()

    # Zugehöriges Luftbild einlesen und verarbeiten

    im_luftbild = Image.open(path_luftbild)
    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, image_scalation)
    im_luftbild.show()
    pix_luftbild = np.array(im_luftbild) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix_luftbild.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix_luftbild = np.delete(pix_luftbild, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Luftbild nicht farbig")
        exit()

    # Ergebnis in Luftbild visualisieren

    pix_marked = hilfsfunktionen.mark_area(pix_luftbild, pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 5] Luftbild: Pixel im Farbbereich")
    plt.show()


'''# Markiertes Bild, markierte Farbwerte und Array mit Indices speichern

pixels = pix.reshape(pix.shape[0]*pix.shape[1], -1)
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript1_indices.json", "w") as f:
    json.dump([i.item() for i in pixel_indices], f)
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript1_colors.json", "w") as f:
    json.dump([[o.item() for o in i] for i in pixels[pixel_indices]], f)
im_marked = Image.fromarray(pix_marked)
im_marked.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript1_image.png")'''
