
# importation des bibliotheques
import pygame
import sys
import os
from random import randint

import subprocess
import os


def ouvrir_map() : 
    # Chemin du fichier Python à exécuter
    fichier_a_executer = "map_finale.py"

    # Ouvrir un nouveau terminal et exécuter le fichier Python
    subprocess.Popen(f'start cmd /k "python {os.path.abspath(fichier_a_executer)}"', shell=True)





popups = []
TAILLE_ECRAN = (1000, 600)


def get_path (name) : 
    return os.path.join(os.path.dirname(__file__), name)

def ouvrir_boutique():
    global fenetre_actuelle
    fenetre_actuelle = "boutique"

def ouvrir_menu():
    global fenetre_actuelle
    fenetre_actuelle = "accueil"

def ouvrir_carte() : 
    global fenetre_actuelle
    fenetre_actuelle = "carte"

def creer_popup(popus , texte = "ceci est un popup"):
    popups.append(PopUp(texte,TAILLE_ECRAN, popups))

    
# importation des modules
import classes_frontend
from classes_frontend import *
import boutique
from boutique import *
from map_finale import *


# --- Defnition des actions des boutons ---
fenetre_actuelle = "accueil"



    


# ============================
#       INITIALISATION
# ============================

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre principale

screen = pygame.display.set_mode(TAILLE_ECRAN)
pygame.display.set_caption("Fenêtres avec texte et boutons")

panier = Panier_fenetre(750, 0, 250, 600)
produits_fenetre = Inventaire_Produits(panier)


# ----------------------------
# Fenetre menu
# ----------------------------
fenetre_accueil = Fenetre(0, 0, 750, 600, (180, 220, 255))

fenetre_accueil.ajouter_texte("Bienvenue au guide de survie du Hackaton !", 60, 20, couleur=(0, 0, 150), taille=40)
fenetre_accueil.ajouter_texte("Bienvenue sur Hackifind, le guide de survie des Hackatons en France.", 60, 250, couleur=(0, 0, 150), taille=25)
fenetre_accueil.ajouter_texte("Ici vous pourrez retrouver une map pour vous diriger entre les différnts hackathons." , 30, 300, couleur=(0, 0, 150), taille=25)
fenetre_accueil.ajouter_texte("Vous avez accès à une boutique pour acheter vos billets pour ", 100, 350, couleur=(0, 0, 150), taille=25)
fenetre_accueil.ajouter_texte(" vos prochains hackatons et les objets indispensables pour les gagner.", 60, 375, couleur=(0, 0, 150), taille=25)

Bouton(fenetre_accueil, 300, 100, 200, 50, (100, 255, 100), ("Boutique",30), action=ouvrir_boutique)
Bouton(fenetre_accueil, 30, 100, 200, 50, (255, 255, 100),("Map",30) , action = ouvrir_map)
Bouton(fenetre_accueil, 300, 520, 200, 50, (255, 100, 100),("Quitter",30) , action=lambda: sys.exit())
Bouton(fenetre_accueil, 0, 0, 200, 50, (100,255,100), ("Ouvrir Popup",30), action=creer_popup, args = (popups,))


# ----------------------------
# Fenetre boutique
# ----------------------------
fenetre_boutique = Fenetre(0, 0, 750, 600, (200, 200, 200))
fenetre_boutique.ajouter_texte("Vous êtes dans la Boutique", 250, 10, couleur=(0, 100, 0), taille=35)

bouton_menu = Bouton(fenetre_boutique, 500, 40, 100, 50, (255,100,100), ("Menu",30), action=ouvrir_menu)

Bouton(fenetre_boutique, 20,  50, 100, 30, (100, 150, 255), ("Boisson",20), produits_fenetre.importer_liste, args =(inv_boisson,))
Bouton(fenetre_boutique, 130, 50, 80, 30, (100, 150, 255), ("Inscription",20), produits_fenetre.importer_liste,args = (inv_ticket,))
Bouton(fenetre_boutique, 220, 50, 140, 30, (100, 150, 255), ("Configuration PC",20), produits_fenetre.importer_liste,args = (inv_tech,))
Bouton(fenetre_boutique, 370, 50, 100, 30, (100, 150, 255), ("Mercenariat",20), produits_fenetre.importer_liste,args = (inv_dev,))

Bouton(fenetre_boutique, 700, 50, 50, 30, (100, 150, 255), ("prix",20), produits_fenetre.trier_par_prix_spe)
Bouton(fenetre_boutique, 640, 50, 50, 30, (100, 150, 255), ("alpa",20), produits_fenetre.trier_par_nom_spe)

produits_fenetre.importer_liste(inv_boisson)

# ----------------------------
# Fenetre Map
# ----------------------------
fenetre_carte = Fenetre(0, 0, 750, 600, (200, 200, 200))
fenetre_carte.ajouter_texte("Vous êtes dans la Map", 150, 50, couleur=(0, 100, 0), taille=35)
Bouton(fenetre_carte, 300, 400, 100, 50, (100, 150, 255), ("Menu",30), action=ouvrir_menu)



# ============================
#       BOUCLE PRINCIPALE
# ============================




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if len(popups) > 0 : 
                for popup in popups[:]:
                    for bouton in popup.boutons:
                        bouton.est_clique(event.pos)
            else : 
                if fenetre_actuelle == "accueil":
                    for bouton in fenetre_accueil.boutons:
                        bouton.est_clique(event.pos)

                elif fenetre_actuelle == "boutique":
                    for bouton in fenetre_boutique.boutons:
                        bouton.est_clique(event.pos)
                    for produit in produits_fenetre.liste : 
                        for bouton in produit.boutons : 
                            bouton.est_clique(event.pos)

                elif fenetre_actuelle == "carte":
                    for bouton in fenetre_carte.boutons:
                        bouton.est_clique(event.pos)
                
                
                
                for p in panier.produits : 
                    for bouton in p.boutons : 
                        bouton.est_clique(event.pos)
                for bouton in panier.boutons :
                    bouton.est_clique(event.pos)

            

    # Affichage
    screen.fill((255, 255, 255))

    if fenetre_actuelle == "accueil":
        fenetre_accueil.afficher(screen)
    elif fenetre_actuelle == "boutique":
        fenetre_boutique.afficher(screen)
        for produit in produits_fenetre.liste : 
            produit.afficher(screen)
    elif fenetre_actuelle == "carte" : 
        fenetre_carte.afficher(screen)
    panier.afficher(screen)
    for popup in popups:
        popup.afficher(screen)
    
    
    

    pygame.display.flip()

pygame.quit()
def delete (self) : 
    self.liste.remove(self)
    total.remove(self)
