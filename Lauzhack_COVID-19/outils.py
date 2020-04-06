from PIL import Image, ImageTk
import random
from math import floor

def quartHeure(heure, minute=0):
    a = round(minute / 15)
    return heure * 4 + a

def heureJournée(minutes):
    h = minutes // 60
    m = minutes % 60
    return h, m

def dimensionner(fichierImage, largeur):
    image = Image.open(fichierImage)
    largeurPercent = (largeur/float(image.size[0]))
    hauteur = int((float(image.size[1])*float(largeurPercent)))
    imageFinale = image.resize((largeur,hauteur), Image.ANTIALIAS)
    tkIm = ImageTk.PhotoImage(imageFinale)
    return tkIm

def grille_vers_canvas(coord, afficherImage, tailleBatiment):
    x, y = coord
    if afficherImage == 2:
        xc = x*tailleBatiment/2-y*tailleBatiment/2
        yc = (x+y)*tailleBatiment/4
    else:
        xc = x * tailleBatiment
        yc = y * tailleBatiment
    return xc, yc


def canvas_vers_grille(coord, afficherImage, tailleBatiment):
    xc, yc = coord
    if afficherImage == 2:
        x = floor((xc + 2*yc) / tailleBatiment)
        y = floor((2*yc - xc) / tailleBatiment)
    else:
        x = floor(xc / tailleBatiment)
        y = floor(yc / tailleBatiment)
    return x, y


def déplacer_habitant(habitant, posBat, modeRapide, afficherImage, tailleBatiment):
    if modeRapide:
        if afficherImage == 2:
            habitant.position = [v + tailleBatiment / 2 for v in posBat]
        else:
            habitant.position = [v + random.randint(0, round(tailleBatiment / 2)) for v in posBat]
    else:
        if afficherImage == 2:
            for v in range(2):
                nouveau = habitant.position[v] + random.randint(-5, 5)
                d = abs(nouveau - (posBat[v] + tailleBatiment / 2))
                if d < tailleBatiment * 0.4:
                    habitant.position[v] = nouveau
        else:
            for v in range(2):
                nouveau = habitant.position[v] + random.randint(-5, 5)
                d = nouveau - posBat[v]
                if d < tailleBatiment * 0.9 and d > tailleBatiment * 0.1:
                    habitant.position[v] = nouveau
    return habitant.position