# Legt ein Wärmebild auf verschiedene Arten auf das zugehörige Luftbild
import hilfsfunktionen
from PIL import Image
import numpy as np

def alpha_komposition(luftbild : Image, waermebild : Image, *, alpha=0.5):
    # Luftbild auf Wärmebild zuschneiden, Wärmebild skalieren
    luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(luftbild)
    luftbild = luftbild.resize((1440, 1080))
    waermebild = waermebild.resize((1440, 1080))

    # Bilder aufeinanderlegen
    waermebild_data = waermebild.getdata()
    luftbild_data = luftbild.getdata()
    newData = []
    for i in range(len(waermebild_data)):
        data = [round(
            waermebild_data[i][channel] * alpha + luftbild_data[i][channel] * (1-alpha)
            ) for channel in range(3)
        ]
        newData.append(tuple(data))
    waermebild_data.putdata(newData)
    return waermebild

def kanalbasiert(luftbild : Image, waermebild : Image):
    # Luftbild auf Wärmebild zuschneiden, Wärmebild skalieren
    luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(luftbild)
    luftbild = luftbild.resize((1440, 1080))
    waermebild = waermebild.resize((1440, 1080))

    # Bilder aufeinanderlegen
    waermebild_data = waermebild.getdata()
    luftbild_data = luftbild.getdata()
    newData = []
    for i in range(len(waermebild_data)):
        data = [waermebild_data[i][0], waermebild_data[i][1], luftbild_data[i][2]]
        newData.append(tuple(data))
    waermebild_data.putdata(newData)
    return waermebild

def difference_blending(luftbild : Image, waermebild : Image):
    # Luftbild auf Wärmebild zuschneiden, Wärmebild skalieren
    luftbild = hilfsfunktionen.crop_luftbild_to_waermebild(luftbild)
    luftbild = luftbild.resize((1440, 1080))
    waermebild = waermebild.resize((1440, 1080))

    # Bilder aufeinanderlegen
    waermebild_data = waermebild.getdata()
    luftbild_data = luftbild.getdata()
    newData = []
    for i in range(len(waermebild_data)):
        data = [abs(
            waermebild_data[i][channel] - luftbild_data[i][channel]
            ) for channel in range(3)
        ]
        newData.append(tuple(data))
    waermebild_data.putdata(newData)
    return waermebild

im_luftbild = Image.open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Luftbilder/Bilder 16-07-22/Flugroute 1/YUN00005.jpg")
im_waermebild = Image.open("C:/Users/timkr/OneDrive/Hector/2022-23/Kooperationsphase Projekt/Luftbilder/Bilder 16-07-22/Flugroute 1/YUN00005.jpeg")

im_luftbild.show()
im_waermebild.show()

verknuepft = difference_blending(im_luftbild, im_waermebild)
verknuepft.show()
