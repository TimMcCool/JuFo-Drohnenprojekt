# Findet Pixel, die "nahe" an vorgegebenen Referenz-Farbtripeln liegen (Entfernung zweier Farbwerte durch euklidischen Abstand bestimmt)
# Verwendet zur Bestimmung von Grünanteil und Braunanteil

from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import hilfsfunktionen

# Parameter
path_luftbild = "/Bilder/Eingabebilder/Bilder x-x-x/Flugroute x/YUN000xx.jpg" #Hier ist der Dateipfad zum Luftbild anzugeben, das ausgewertet werden soll
farbe = "grün"

if farbe == "grün":
    max_distanz = 15 #Maximaler euklidischer Abstand zwischen einem der vorgegeben Farbwerte und dem Farbwert eines Pixels, der im Farbbereich liegen soll
    farbwerte_json_path = "/Programme/Skript 3 Referenzfarbtripel/gruentoene_alle_rgb.json"# Dateipfad der JSON-Datei, die die Referenzfarbtripel enthält
elif farbe == "braun":
    max_distanz = 14 #Maximaler euklidischer Abstand zwischen einem der vorgegeben Farbwerte und dem Farbwert eines Pixels, der im Farbbereich liegen solls
    farbwerte_json_path = "/Programme/Skript 3 Referenzfarbtripel/brauntoene_alle_rgb.json"
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

    #im = hilfsfunktionen.crop_luftbild_to_waermebild(im)
    im = hilfsfunktionen.scale_image(im, new_size)
    pix = np.array(im) #Image-Objekt in 3-dimensionales np Array umwandeln

    if pix.shape[2] == 4:
        pix = np.delete(pix, 3, axis=2)
    if pix.shape[2] < 3:
        print("Fehler: Luftbild nicht farbig")
        exit()

    pix_flattened = pix.reshape(pix.shape[0]*pix.shape[1], -1) #3D auf 2D Array reduzieren, in dem die Farbtripel aller Pixel aneinandergereiht sind
    pixel_count = len(pix_flattened)
    return pix_flattened

def filter_pixels(im, farbtoene, _max_distanz, *, new_size=200):
    """
    Filtert alle Pixel heraus, die den gegebenen Referenz-Farbtönen ähneln
    Diese Funktion kann auch von anderen Skripten importiert und ausgeführt werden

    Args:
        im (Image): Das Bild, für das alle Indices zurückgegeben werden sollen
        farbtoene (list): Die Liste mit den gegebenen RGB-Referenzfarbtripeln
        _max_distanz (float): Maximaler Abstand zwischen zwei "ähnlichen" Farbtripeln
        new_size (int): Gibt die Breite an, auf die das Bild vor der Auswertung skaliert werden soll (standardmäßig 1080 Pixel)
    Returns:
        np.array: Indices aller Pixel, die den Referenz-Farbtönen ähneln
        np.array: Das Eingabebild als dreidimensionales numpy array
    """
    def pixel_in_farbbereich(pixel_farbe):
        """
        Ermittelt, ob ein Farbtripel einem der Referenzfarbtöne ähnelt

        Args:
            pixel_farbe (tuple or list): Das zu überprüfende RGB-Farbtripel
        Returns:
            boolean: Gibt True zurück, wenn pixel_farbe zu einem Referenz-Farbton einen Abstand kleiner gleich max_distanz hat, sonst False
        """
        for farbton in farbtoene:
            if hilfsfunktionen.distance(pixel_farbe, farbton) <= max_distanz:
                return True
        return False

    global max_distanz
    global pix_flattened

    max_distanz = _max_distanz
    pix_flattened = parse_image(im, new_size=new_size)

    in_farbbereich = np.array(list(map(pixel_in_farbbereich, pix_flattened)))
    index_farbbereich = np.where(in_farbbereich == True)[0]
    return index_farbbereich, pix

# Definieren globaler Variablen

pix = None
pix_flattened = None
pixel_count = None

if __name__ == "__main__":

    # Bild einlesen

    im = Image.open(path_luftbild)


    # Liste der gegebenen Referenz-Farbtripel aus JSON Datei einlesen

    with open(farbwerte_json_path, "r") as f:
        farbtoene = json.loads(f.read())

    # Pixel, deren Farbe Referenz-Farbtripeln "ähnelt", bestimmen und Ergebnis ausgeben

    pixel_indices, pix = filter_pixels(im, farbtoene, max_distanz)
    print(f"[Skript 3] Anteil Pixel mit {farbe}en Farbtönen:", len(pixel_indices)*100 / pixel_count, "%")
    pix_marked = hilfsfunktionen.mark_area(pix, pixel_indices)
    imgplot = plt.imshow(pix_marked)
    plt.title(f"[Skript 3] Pixel mit {farbe}en Farbtönen")
    plt.show()
