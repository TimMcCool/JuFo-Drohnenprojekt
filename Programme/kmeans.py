# Funktion zum Durchführen von kmeans Clustering

import math
import numpy as np
import random
import hilfsfunktionen

class Centroid:

    def __init__(self, center):
        self.center = np.array(center)
        self.objects = []
        self.object_ids = []

    def distance(self, obj2):
        # Berechnet den euklidischen Abstand vom Objekt obj2 zum Centroid
        return hilfsfunktionen.distance(self.center, obj2)

    def change_center(self):
        # Position des Centroids auf die Durchschnittsposition der dem Centroiden zugeordneten Objekte setzen
        self.center = np.average(np.array(self.objects), axis=0)
        self.objects = []
        self.object_ids = []

def kmeans(data, *, iterations, centroids):
    # Führt kmeans Clustering durch
    # Argumente:
    # - data: Liste mit Objekten, die in Cluster eingeteilt werden sollen. Die Objekte müssen eindimensionale np Arrays des Datentyps int oder float sein uznd alle die gleiche Länge haben
    # - k: Anzahl an Durchläufen
    # - centroids: Eine Liste mit Objekten der Klasse Centroid

    for step in range(iterations+1):
        i = 0
        for obj in data:
            # Für jedes Objekt den Abstand zu den Centroiden berechnen

            min_distance = float('inf')
            min_centroid = None

            for centroid in centroids:
                distance = centroid.distance(obj)
                if distance < min_distance:
                    min_distance = distance
                    min_centroid = centroid

            # Objekt dem Centroid zuordnen, zu dem es den kleinsten Abstand hat
            min_centroid.objects.append(obj)
            min_centroid.object_ids.append(i)
            i += 1

        if step == iterations:
            return centroids

        for centroid in centroids:
            # Position der Centroide aktualisieren
            centroid.change_center()
