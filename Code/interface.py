from os import path
from PIL import Image, ImageTk
import tkinter

from constantes import *
from traitement import *
from video import *



# Stockage des filtres sélectionnés dans un dictionnaire

def selectionner (evenement):

    cible = str (evenement.widget)
    selection [cible] = not selection [cible]



def initialisation ():

    # Caméra en haut

    global fenetre, zoneCamera
    
    fenetre = tkinter.Tk ()
    tailleZoneFiltre = 1920 // nbFiltres
    zoneCamera = tkinter.Canvas (fenetre, background = 'black', height = 1040 - tailleZoneFiltre, width = 1920)
    zoneCamera.pack (side = tkinter.TOP)
    
    
    """
    Sélection des filtres en bas
    nom : ".!canvas[numFiltre + 2]"
    exemple pour le 1er filtre : ".!canvas2"
    """
    
    for numFiltre in range (nbFiltres):
        zoneFiltre = tkinter.Canvas (fenetre, background = 'yellow', height = tailleZoneFiltre, width = tailleZoneFiltre)
        zoneFiltre.focus_set ()
        zoneFiltre.bind ("<ButtonRelease>", selectionner)
        
        # Ouverture de la miniature
        capture = tkinter.PhotoImage (cheminImages + "miniature" + str (numFiltre) + ".jpg")
        zoneFiltre.create_image (0, 0, anchor = tkinter.NW, image = capture)
        
        zoneFiltre.pack (expand = True, fill = tkinter.BOTH, side = tkinter.LEFT)
    
    zoneCamera.focus_set ()
    
    
    fenetre.protocol ("WM_DELETE_WINDOW", terminaison)



def terminaison ():

    fenetre.destroy ()
    exit (1)



def bouclePrincipale ():
    
    initialisation ()
    
    
    # Réinitialisation de l'image en permanence
    
    while True:
    
        sequencage ()

        # Ouverture de l'image
        imagePil = Image.open (path.join (cheminImages, "sequence.jpg"))
        capture = ImageTk.PhotoImage (imagePil)
        camera = zoneCamera.create_image (650, 120, anchor = tkinter.NW, image = capture)
        zoneCamera.pack ()
        
        fenetre.update ()
        
        zoneCamera.delete (camera)



bouclePrincipale ()
