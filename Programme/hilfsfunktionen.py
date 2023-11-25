# Funktionen, die in verschiedenen Skripten an mehreren Stellen benötigt werden und daher in eine Extra-.Datei ausgelagert wurden

from PIL import Image
import numpy as np
import math

def rgb_to_hsv(r,g,b):
    #r, g, b: numpy-Arrays, die jeweils die R, G, B Werte von len(r) Farbtripeln enthalten
    #Gibt die np-Arrays h, s, v zurück, die díe berechneten H, S, V Werte der RGB-Farbtripel enthalten
    #Quelle für die Umrechnungsformel RGB -> HSV: https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    max_value = np.maximum(r, np.maximum(g, b))
    min_value = np.minimum(r, np.minimum(g, b))
    dif = max_value-min_value

    h = np.zeros(r.shape)
    s = np.zeros(r.shape)
    v = np.zeros(r.shape)

    for i in range(len(r)):
        # h berechnen
        if max_value[i] == min_value[i]:
            pass #In diesem Fall ist h = 0. h auf 0 initialisiert
        elif max_value[i] == r[i]:
            h[i] = (60 * ((g[i]-b[i])/dif[i]) + 360) % 360
        elif max_value[i] == g[i]:
            h[i] = (60 * ((b[i]-r[i])/dif[i]) + 120) % 360
        elif max_value[i] == b[i]:
            h[i] = (60 * ((r[i]-g[i])/dif[i]) + 240) % 360

        # s berechnen
        if max_value[i] == 0:
            pass #s auf 0 initialisiert
        else:
            s[i] = (dif[i]/max_value[i])*100

        # v berechnen
        v[i] = max_value[i]*100

    return h, s, v

def scale_image(im: Image, new_width : int):
    # im: Bild, das skaliert werden soll
    # new_width: Breite des Ausgabebildes. Wenn die Höhe des Ausgabebilds größer ist als die Breite, wird stattdessen die Höhe skaliert
    # GIbt das skalierte Image-Objekt zurück
    if im.size[1] < im.size[0]:
        im = im.resize((new_width, round((new_width/im.size[0])*im.size[1])), resample=Image.BOX)
        return im
    else:
        return im.resize((round((new_width/im.size[1])*im.size[0]), new_width), resample=Image.BOX)

def scale_image_based_on_width(im: Image, new_width : int):
    # im: Bild, das skaliert werden soll
    # new_width: Breite des Ausgabebildes
    # GIbt das skalierte Image-Objekt zurück
    return im.resize((new_width, round((new_width/im.size[0])*im.size[1])), resample=Image.BOX)


def mark_area(pix, pixel_indices):
    # pix: Die Pixel eines Bildes als np array, flattened (zweidimensional)
    # pixel_indicies: Die Indices der Pixel, die weiß eingefärbt werden sollen
    # Gibt ein weiß eingefärbtes Bild als zweidimensionalen np array zurück
    pix = np.array(pix)
    pix_flattened = pix.reshape(pix.shape[0]*pix.shape[1], -1)
    print(pix_flattened)
    pix_flattened[pixel_indices] = np.array([255,255,255])
    return pix_flattened.reshape(pix.shape[0], pix.shape[1], 3)

def distance(obj1, obj2):
    # Berechnet die euklidische, ungewichtete Distanz zwischen zwei Skalaren oder Zahlen
    try:
        return math.sqrt(
            sum(
                [(obj2[i] - obj1[i]) ** 2 for i in range(len(obj1))]
            )
        )
    except TypeError:
        # Es handelt sich bei obj1 und obj2 um nicht skalare Objekte, also um Zahlen
        return abs(obj2 - obj1)

def crop_luftbild_to_waermebild(luftbild : Image):
    # Schneidet ein Luftbild auf die Größe eines Wärmebilds zu, indem an den Rändern des Luftbildes Pixel entfernt werden
    luftbild = luftbild.resize((1920, 1080))
    size = luftbild.size
    rand_linksrechts = 280
    rand_obenunten = 30
    return luftbild.crop((rand_linksrechts,rand_obenunten,size[0] - rand_linksrechts,size[1]-rand_obenunten))

def merge_luftbild_waermebild(luftbild : Image, waermebild : Image):
    # Legt ein Wärmebild mit 50%iger Transparenz auf das zugehörige Luftbild (Alpha-Komposition)
    luftbild = crop_luftbild_to_waermebild(luftbild)
    luftbild = luftbild.resize((1440, 1080)).convert("RGBA")
    waermebild = waermebild.resize((1440, 1080)).convert("RGBA")

    # Wärmebild transparent machen
    data = waermebild.getdata()
    newData = []
    for i in data:
        i = list(i)
        i[3] = 128
        newData.append(tuple(i))
    waermebild.putdata(newData)

    # Bilder übereinanderlegen
    img = Image.new("RGBA", luftbild.size)
    img.paste(waermebild, (0, 0))
    result = Image.alpha_composite(luftbild, img)
    return result
