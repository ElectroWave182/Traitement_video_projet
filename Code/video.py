from constantes import *
from traitement import *



def sequencage ():

    # Lecture
    succes, uneImage = flux.read ()
    if succes is False:
        print ("Vidéo non lue.")
        exit (0)
    
    # Traitement
    uneImage = filtrage (uneImage)
    
    # Sortie
    cv2.imwrite (cheminImages + "sequence.jpg", uneImage) 
