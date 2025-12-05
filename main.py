
# importation des bibliotheques
import pygame
import sys
import os
from random import randint

# importation des modules

import classes_frontend
from classes_frontend import *
import boutique
from boutique import *


# --- Defnition des actions des boutons ---
fenetre_actuelle = "accueil"
popups = []


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

def creer_popup():
    popups.append(PopUp("Ceci est un popup !",TAILLE_ECRAN, popups))
    



# ============================
#       INITIALISATION
# ============================

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre principale
TAILLE_ECRAN = (900, 600)
screen = pygame.display.set_mode(TAILLE_ECRAN)
pygame.display.set_caption("Fenêtres avec texte et boutons")



# ----------------------------
# Fenetre menu
# ----------------------------
fenetre_accueil = Fenetre(50, 50, 700, 500, (180, 220, 255))

fenetre_accueil.ajouter_texte("Bienvenue au guide de survie du Hackaton !", 60, 20, couleur=(0, 0, 150), taille=40)
fenetre_accueil.ajouter_texte("Bienvenue sur Hackify, la plateforme tout-en-un dédiée aux passionnés d’innovation et de création !\nParticipez facilement aux hackathons partout en France, inscrivez-vous en quelques clics et accédez à une carte interactive pour découvrir les événements près de chez vous.\nAchetez vos produits consommables indispensables, trouvez et louez des développeurs pour renforcer votre équipe, et vivez pleinement l’expérience hackathon grâce à un écosystème complet, simple et efficace.\nRejoignez la communauté et lancez-vous dans votre prochaine aventure tech !", 300, 250, couleur=(0, 0, 150), taille=40)

Bouton(fenetre_accueil, 300, 100, 200, 50, (100, 255, 100), ("Boutique",30), action=ouvrir_boutique)
Bouton(fenetre_accueil, 30, 100, 200, 50, (255, 255, 100),("Map",30) , action = ouvrir_carte)
Bouton(fenetre_accueil, 250, 420, 200, 50, (255, 100, 100),("Quitter",30) , action=lambda: sys.exit())
Bouton(fenetre_accueil, 0, 0, 200, 50, (100,255,100), ("Ouvrir Popup",30), action=creer_popup)


# ----------------------------
# Fenetre boutique
# ----------------------------
fenetre_boutique = Fenetre(50, 50, 700, 500, (200, 200, 200))
fenetre_boutique.ajouter_texte("Vous êtes dans la Boutique", 150, 50, couleur=(0, 100, 0), taille=35)
bouton_menu = Bouton(fenetre_boutique, 300, 400, 100, 50, (100, 150, 255), ("Menu",30), action=ouvrir_menu)

Bouton(fenetre_boutique, 20, 100, 130, 50, (100, 150, 255), ("Boisson",30), produits_fenetre.importer_liste, args =(inv_boisson,))
Bouton(fenetre_boutique, 200, 100, 110, 50, (100, 150, 255), ("Inscription",30), produits_fenetre.importer_liste,args = (inv_ticket,))
Bouton(fenetre_boutique, 350, 100, 170, 50, (100, 150, 255), ("Configuration PC",30), produits_fenetre.importer_liste,args = (inv_tech,))
Bouton(fenetre_boutique, 550, 100, 130, 50, (100, 150, 255), ("Mercenariat",30), produits_fenetre.importer_liste,args = (inv_dev,))

Bouton(fenetre_boutique, 20, 320, 130, 50, (100, 150, 255), ("trie_prix",30), produits_fenetre.trier_par_prix_spe)
Bouton(fenetre_boutique, 20, 400, 130, 50, (100, 150, 255), ("trie_alpahabet",30), produits_fenetre.trier_par_nom_spe)

produits_fenetre.importer_liste(inv_boisson)

# ----------------------------
# Fenetre Map
# ----------------------------
fenetre_carte = Fenetre(50, 50, 700, 500, (200, 200, 200))
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
            
            for popup in popups[:]:
                for bouton in popup.boutons:
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

    for popup in popups:
        popup.afficher(screen)
    
    panier.afficher(screen)
    

    pygame.display.flip()

pygame.quit()
def delete (self) : 
    self.liste.remove(self)
    total.remove(self)
