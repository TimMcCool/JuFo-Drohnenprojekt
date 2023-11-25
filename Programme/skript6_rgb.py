# Finden von Clustern ähnlicher Farben mit k-means Clustering bei Wärmebildern
# Ausgeben des "kältesten" Clusters

from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

import kmeans
import hilfsfunktionen

# Parameter
path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das zum Wärmebild ehört (wird nicht ausgewertet, sondern nur zur Visualisierung genutzt)
path_waermebild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpeg" #Hier ist der Dateipfad zum Wärmebild anzugeben, das ausgewertet werden soll

# Breite, auf die Eingabebild standardmäßig skaliert werden soll
image_scalation = 160

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
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Wärmebild nicht farbig")
        exit()

    pixels = pix.reshape(pix.shape[0]*pix.shape[1], -1) #In 2-dimensionalen np Array umwandeln
    pixel_count = len(pixels)
    return pixels

def filter_pixels(im, *, new_size=image_scalation):
    """
    Führt k-means clustering mit den Eingabebild durch (2 Cluster: einer für warme und einer für kalte Pixel, 5 Iterationen). Gibt die Indices aller Pixel, die sich im kälteren Cluster befinden, zurück.

    Args:
        im (Image): Das Wärmebild, auf das k-means angewendet werden soll
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll (standardmäßig 1080 Pixel)
    Returns:
        np.array: Indices aller Pixel, die sich im kälteren Cluster befinden
        np.array: Das Eingabebild als dreidimensionales numpy array
    """
    global pixels

    # Verarbeiten des Eingabebilds
    pixels = parse_image(im, new_size=new_size)

    # Durchführen von kmeans
    result = kmeans.kmeans(pixels, iterations=5, centroids=[
        kmeans.Centroid(random.choice(pixels)) for i in range(2)
    ])

    # Finden des "kältesten" Clusters
    # -> Cluster mit dem niedrigsten durchschnittlichen Rot-Farbwert finden
    coldest_cluster = min(result, key=lambda cluster : sum(color[0] for color in cluster.objects)/ len(cluster.objects)) #cluster.objects sind die Farbwerte des Clusters
    pixel_indices = coldest_cluster.object_ids # coldest_cluster.object_ids sind die Indices der Pixel im Cluster

    return pixel_indices, pix

# Definieren globaler Variablen
pixel_count = None
pix = None
pixels = None

if __name__ == "__main__":

    # Einlesen und des Wärmebilds
    im = Image.open(path_waermebild)

    # Finden der Pixel, die zum "kälteren" Clusters gehören, mit kmeans
    pixel_indices, pix = filter_pixels(im)

    # Ergebnis in Konsole ausgeben
    print("[Skript 6] Anteil Pixel im kältesten Cluster:", len(pixel_indices)*100 / pixel_count, "%")

    # Visualisieren des Ergebnisses in beiden Bildern
    pix_marked = hilfsfunktionen.mark_area(np.array(pix), pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 6] In Wärmebild visulisiert: Kältester Cluster")
    plt.show()

    im = Image.open(path_luftbild)
    im = hilfsfunktionen.crop_luftbild_to_waermebild(im)
    im = hilfsfunktionen.scale_image(im, image_scalation)
    pix_luftbild= np.array(im) #Image-Objekt in 3-dimensionalen np Array umwandeln

    if pix.shape[2] == 4:
        # Wenn das Bild Farbwerte im RGBA-Format hat, dann müssen die A-Werte (Transparenz) gelöscht werden
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        # Das Bild ist Schwarz-Weiß und daher nicht im RGB-Format
        print("Fehler: Luftbild nicht farbig")
        exit()

    pix_marked = hilfsfunktionen.mark_area(np.array(pix_luftbild), pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title("[Skript 6] In Luftbild visulisiert: Kältester Cluster")
    plt.show()

'''# Markiertes Bild und Array mit Indices speichern
im_marked = Image.fromarray(pix_marked)
im_marked.save("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript3_image.png")
with open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Programme/Outputs/skript3_indices.json", "w") as f:
    json.dump(pixel_indices, f)'''
