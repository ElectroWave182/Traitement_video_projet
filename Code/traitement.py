import cv2
from numpy import *

from constantes import *



def sepia (image, nuancier):

    # Initialisation

    copie = image.copy ()
    hauteur = image.shape [0]
    largeur = image.shape [1]
    
    
    # Traitement
    
    gray = cv2.cvtColor (copie, cv2.COLOR_BGR2GRAY)
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie [ligne] [colonne]
            nuance = gray [ligne] [colonne]
            
            for canal in range (3):
                pixel [canal] = nuance * nuancier [canal] // 255
                
                
    # Sortie
    
    return copie



# Ajuster un masque à l'échelle d'un visage...
# ... ou un fond à l'échelle d'un objet.

def ajuster (image, nouvHauteur, nouvLargeur):

    # Initialisation

    hauteur = image.shape [0]
    largeur = image.shape [1]
    profondeur = image.shape [2]

    ajustee = array ([[
            [0] * profondeur
            for _ in range (nouvLargeur)
        ]
        for _ in range (nouvHauteur)
    ])
    
    
    # Traitement
    
    for nouvLigne in range (nouvHauteur):
        for nouvColonne in range (nouvLargeur):
        
            # Coordonnées décimales
            pixel = ajustee [nouvLigne] [nouvColonne]
            ligne = nouvLigne * hauteur / (nouvHauteur + 1)
            colonne = nouvColonne * largeur / (nouvLargeur + 1)
            
            # Pixélisation par moyenne pondérée
            for canal in range (profondeur):
                pixel [canal] += image [int (ligne)] [int (colonne)] [canal] * (int (ligne) - ligne + 1) * (int (colonne) - colonne + 1)
                pixel [canal] += image [int (ligne)] [int (colonne) + 1] [canal] * (int (ligne) - ligne + 1) * (colonne - int (colonne))
                pixel [canal] += image [int (ligne) + 1] [int (colonne)] [canal] * (ligne - int (ligne)) * (int (colonne) - colonne + 1)
                pixel [canal] += image [int (ligne) + 1] [int (colonne) + 1] [canal] * (ligne - int (ligne)) * (colonne - int (colonne))
                
    
    # Sortie
    
    return ajustee



# Superposer un masque en format png sur un visage

def superposer (image, gauche, haut, diametre, masque, proportionDecalageHaut):

    # Initialisation

    copie = image.copy ()
    hauteur = masque.shape [0]
    largeur = masque.shape [1]
    
    coefAgrandissement = diametre / largeur
    nouvHauteur = int (coefAgrandissement * hauteur)
    nouvLargeur = int (coefAgrandissement * largeur)

    masqueAjuste = ajuster (masque, nouvHauteur, nouvLargeur)
    decalageGauche = gauche
    decalageHaut = haut + int (diametre * proportionDecalageHaut)
    canalTransparence = masqueAjuste.shape [2] == 4


    # Traitement
    
    for ligne in range (nouvHauteur):
        for colonne in range (nouvLargeur):
            pixelBase = copie [ligne + decalageHaut] [colonne + decalageGauche]
            pixelMasque = masqueAjuste [ligne] [colonne]
            
            # Ajout du canal de transparence
            if not canalTransparence:
                pixelMasque = array (list (pixelMasque) + [255])
            
            opacite = pixelMasque [3] / 255
            for canal in range (3):
                pixelBase [canal] = pixelBase [canal] * (1 - opacite)
                pixelBase [canal] += pixelMasque [canal] * opacite
                pixelBase [canal] = int (pixelBase [canal])
    
    
    # Sortie
    
    return copie



# Détecter approximativement une couleur dans le fond

def approximation (couleurA, couleurB):

    similaires = True
    
    for canal in range (3):
        similaires = similaires and abs (couleurA [canal] - couleurB [canal]) < 20
        
    return similaires


# Remplacer une couleur par un fond

def soustractionFond (image, nouvFond, couleurFond = array ([0, 255, 0])):

    # Initialisation

    copie = image.copy ()
    hauteur = image.shape [0]
    largeur = image.shape [1]
    canalTransparence = image.shape [2] == 4


    # Traitement

    nouvFondAjuste = ajuster (nouvFond, hauteur, largeur)
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixelBase = copie [ligne] [colonne]
            pixelFond = nouvFondAjuste [ligne] [colonne]
            
            # Ajout du canal de transparence
            if not canalTransparence:
                append (pixelBase, 255)
            
            # Fond monochrome détecté
            if approximation (pixelBase, couleurFond):
                for canal in range (4):
                    pixelBase [canal] = pixelFond [canal]
                    
    # Superposition sur le fond de base
    copie = superposer (image, 0, 0, largeur, copie, 0)
    
    
    # Sortie
    
    return copie



def filtrage (image):


    # Copie
    
    copie = image.copy ()


    # Choix des filtres

    for filtre in selection:
    
        if selection [filtre]:
            numFiltre = int (filtre.lstrip (".!canvas")) - 2
            
            match numFiltre:
            
                # Sépia
                case 0:
                    nuancier = (190, 255, 240) # (bleu, vert, rouge)
                    copie = sepia (copie, nuancier)
                
                # Anonymous
                case 1:
                    masque = cv2.imread (cheminImages + "anonymous.png", cv2.IMREAD_UNCHANGED)
                    coordonnees = cascadeVisages.detectMultiScale (copie, minNeighbors = 4, minSize = (15, 15), scaleFactor = 1.1)
                    for gauche, haut, diametre, _ in coordonnees:
                        copie = superposer (copie, gauche, haut, diametre, masque, decalageFront)
                    
                # Lunettes
                case 2:
                    masque = cv2.imread (cheminImages + "lunettes.png", cv2.IMREAD_UNCHANGED)
                    coordonnees = cascadeVisages.detectMultiScale (copie, minNeighbors = 4, minSize = (15, 15), scaleFactor = 1.1)
                    for gauche, haut, diametre, _ in coordonnees:
                        copie = superposer (copie, gauche, haut, diametre, masque, decalageFront)
                    
                # Moustache
                case 3:
                    masque = cv2.imread (cheminImages + "moustache.png", cv2.IMREAD_UNCHANGED)
                    coordonnees = cascadeBouches.detectMultiScale (copie, minNeighbors = 3, minSize = (3, 3), scaleFactor = 1.1)
                    for gauche, haut, diametre, _ in coordonnees:
                        copie = superposer (copie, gauche, haut, diametre, masque, decalageHautBouche)

                # Change un fond vert en plage
                case 4:
                    fond = cv2.imread (cheminImages + "plage.jpg")
                    copie = soustractionFond (copie, fond)
                    
                # Superpose des flocons qui bougent sur un fond vert
                case 5:
                    fondAnime = cv2.VideoCapture (cheminImages + "flocons.gif")
                    _, fond = fondAnime.read ()
                    copie = soustractionFond (copie, fond)
                    
                case other:
                    print ("Filtre n°", numFiltre, "à ajouter au traitement.")
                    exit (0)
    
    
    # Sortie
    
    return copie
