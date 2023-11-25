# Berechnet den Anteil grüner Wald (=Schnittmenge grüne Pixel / Skript 1 und mit Wald bewachsene Pixel / Skript 5) und Anteil grüner Wiese (= Schnittmenge grüner und nicht mit Wald bewachsener Pixel)

from PIL import Image
import skript1_hsv
import skript5_hsv
import numpy as np
import hilfsfunktionen
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das ausgewertet werden soll
path_waermebild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpeg" #Hier ist der Dateipfad zum Wärmebild anzugeben, das ausgewertet werden soll

def schnittmengen_bestimmen(im_luftbild, im_waermebild):
    """
    Wertet Eingebabeluftbild mit Skript 1 (Grünanteil) aus. Wertet das zugehörige Wärmebild mit Skript 5 aus (Waldanteil). Bestimmt anschließend die Schnittmengen der Auswertungsergebnisse, um Bereiche zu finden, die sowoihl grün als auch bewaldet sind.

    Args:
        im_luftbild (Image): Eingabeluftbild
        im_waermebild (Image): Zum Luftbild gehörendes Wärmebild
    Returns:
        schnittmenge_skript1_skript5 (np.array): Indices der Pixel, die sowohl grün als auch bewaldet sind
        schnittmenge_skript1_nicht_skript5 (np.array): Indices der Pixel, die sowohl grün als auch nicht bewaldet sind
        pixel_count (int): Anzahl an Pixeln, die das verarbeitete Luftbild und das verarbeitete Wärmebild vor der Auswertung haben (die Bilder werden vor der Auswertung bündig gemacht und haben somit dieselbe Auflösung, folglich auch dieselbe Pixelanzahl)
    """
    # Verarbeien beider Bilder

    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, 1080)
    im_waermebild = hilfsfunktionen.scale_image(im_waermebild, 1080)

    # Auswertung Luftbild mit Skript 1 -> Bestimmung grüne Pixel

    #grüner Farbbereich:
    gruene_h_bereiche = [(60,180),(180,300)]
    gruene_s_bereiche = [(10,100),(1,25)]
    gruene_v_bereiche = [(0,100),(0,20)]

    skript1_output, pix_luftbild = skript1_hsv.filter_pixels(im_luftbild, gruene_h_bereiche, gruene_s_bereiche, gruene_v_bereiche, new_size=1080)

    # Auswertung Wärmebild mit Skript 5 -> Bestimmung mit Wald bewachsener Pixel
    skript5_output, _ = skript5_hsv.filter_pixels(im_waermebild, new_size=1080)

    # Schnittmengen und Pixelanzahl bestimmen
    schnittmenge_skript1_skript5 = np.intersect1d(skript1_output, skript5_output) # Schnittmenge Grün und Wald
    schnittmenge_skript1_nicht_skript5 = np.setdiff1d(skript1_output, skript5_output) # Schnittmenge Grün und Nicht-Wald

    pixel_count = im_luftbild.size[0] * im_luftbild.size[1] # Gesamtpixelzahl des om Z. 17 - 19 zugeschnittenen und skalierten Luftbilds
    pix_luftbild_flattened = pix_luftbild.reshape((pixel_count, -1))

    farbtripel_gruener_wald = pix_luftbild_flattened[schnittmenge_skript1_skript5]
    farbtripel_gruene_wiese = pix_luftbild_flattened[schnittmenge_skript1_nicht_skript5]

    return schnittmenge_skript1_skript5, schnittmenge_skript1_nicht_skript5, pixel_count

if __name__ == "__main__":


    # Bilder einlesen

    im_luftbild = Image.open(path_luftbild)
    im_waermebild = Image.open(path_waermebild)

    # Bestimmen der Schnittmengen

    schnittmenge_skript1_skript5, schnittmenge_skript1_nicht_skript5, pixel_count = schnittmengen_bestimmen(im_luftbild, im_waermebild)

    # Bestimmen der Anteile

    im_luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(im_luftbild)
    im_luftbild = hilfsfunktionen.scale_image(im_luftbild, 1080)

    pix = np.array(im_luftbild) #Image-Objekt in 3-dimensionalen np Array umwandeln

    anteil_wald_gruen = len(schnittmenge_skript1_skript5)/pixel_count
    anteil_wiese_gruen = len(schnittmenge_skript1_nicht_skript5)/pixel_count

    print("Anteil grüner Wald:", round((anteil_wald_gruen*10000)/100), "%")
    print("Anteil grüne Wiese:", round((anteil_wiese_gruen*10000)/100), "%")

    # Visualisieren

    pix_gruener_wald = hilfsfunktionen.mark_area(pix, schnittmenge_skript1_skript5)
    pix_gruene_wiese = hilfsfunktionen.mark_area(pix, schnittmenge_skript1_nicht_skript5)

    imgplot = plt.imshow(pix_gruener_wald)
    plt.title("[Skript 7] Anteil grüner Wald")
    plt.show()

    imgplot = plt.imshow(pix_gruene_wiese)
    plt.title("[Skript 7] Anteil grüne Wiese")
    plt.show()
