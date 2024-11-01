import cv2
from pathlib import Path



global nbFiltres, selection, cheminImages, cheminCascades, cascadeVisages, cascadeBouches, flux


# Paramètres
decalageFront = 0.18     # proportion que prend le front dans un visage 
decalageHautBouche = -0.2 # proportion que prend le duvet dans une bouche 

# Filtres
nbFiltres = 6
selection = {
    ".!canvas" + str (numFlitre + 2): False
    for numFlitre in range (nbFiltres)
}

# Dossiers
cheminImages = str (Path (__file__).resolve ().parent) + "\\images\\"
cheminCascades = str (Path (__file__).resolve ().parent) + "\\cascades\\"

# Cascades
cascadeVisages = cv2.CascadeClassifier (cheminCascades + "haarcascade_frontalface_alt.xml")
cascadeBouches = cv2.CascadeClassifier (cheminCascades + "haarcascade_smile.xml")

# Flux caméra
flux = cv2.VideoCapture (0)
