import pygame
import sys
from random import randint
import os


# ============================
#      CLASSE FENETRE
# ============================
class Fenetre:
    def __init__(self, x, y, largeur, hauteur, couleur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.boutons = []
        self.textes  = []  # Liste des textes à afficher

    def ajouter_bouton(self, bouton):
        self.boutons.append(bouton)

    def ajouter_texte(self, texte, x, y, couleur=(0, 0, 0), taille=30):
        """Ajouter un texte à la fenêtre (position relative à la fenêtre)"""
        self.textes.append({
            "texte": texte,
            "x": x,
            "y": y,
            "couleur": couleur,
            "taille": taille,
            "font": pygame.font.SysFont(None, taille)
        })

    def afficher(self, surface):
        # Dessiner le fond
        pygame.draw.rect(surface, self.couleur, (self.x, self.y, self.largeur, self.hauteur), border_radius = 10)
        # Dessiner les textes
        for t in self.textes:
            texte_surface = t["font"].render(t["texte"], True, t["couleur"])
            surface.blit(texte_surface, (self.x + t["x"], self.y + t["y"]))
        # Dessiner les boutons
        for bouton in self.boutons:
            bouton.afficher(surface)

    def get_path (name) : 
        return os.path.join(os.path.dirname(__file__), name)


# ============================
#       CLASSE BUTTON
# ============================
class Bouton:
    def __init__(self, fenetre, x, y, largeur, hauteur, couleur, texte=("",0), action=None, args = (), kwargs = {}):
        self.fenetre = fenetre
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.texte = texte[0]
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.font = pygame.font.SysFont(None, texte[1])
        fenetre.ajouter_bouton(self)

    def afficher(self, surface):
        abs_x = self.fenetre.x + self.x
        abs_y = self.fenetre.y + self.y
        pygame.draw.rect(surface, self.couleur, (abs_x, abs_y, self.largeur, self.hauteur), border_radius = 10)
        if self.texte:
            texte_surface = self.font.render(self.texte, True, (0, 0, 0))
            texte_rect = texte_surface.get_rect(center=(abs_x + self.largeur / 2, abs_y + self.hauteur / 2))
            surface.blit(texte_surface, texte_rect)

    def est_clique(self, souris_pos):
        abs_x = self.fenetre.x + self.x
        abs_y = self.fenetre.y + self.y
        if abs_x <= souris_pos[0] <= abs_x + self.largeur and abs_y <= souris_pos[1] <= abs_y + self.hauteur:
            if self.action:
                self.action(*self.args, **self.kwargs)
            
            return True
            
        return False


# ============================
#       CLASSE POPUP
# ============================
class PopUp(Fenetre):
    def __init__(self, texte, TAILLE_ECRAN, popups_liste, largeur=400, hauteur=200 ):
        # Centrer le popup à l'écran
        x = (TAILLE_ECRAN[0] - largeur) // 2 + 20 * len(popups_liste)
        y = (TAILLE_ECRAN[1] - hauteur) // 2 + 20 * len(popups_liste)
        super().__init__(x, y, largeur, hauteur, (220, 220, 220))
        self.popups_liste = popups_liste  # référence à la liste des popups
        # Ajouter le texte
        self.ajouter_texte(texte, 20, 40, couleur=(0,0,0), taille=28)
        # Ajouter le bouton fermer
        bouton_fermer = Bouton(self, largeur//2 - 50, hauteur - 70, 100, 40, (255,100,100), ("Fermer",30), action=self.fermer)
        self.ajouter_bouton(bouton_fermer)

    def fermer(self):
        if self in self.popups_liste:
            self.popups_liste.remove(self)


# ============================
#       CLASSE PRODUIT
# ============================
class Produit_Fenetre(Fenetre):
    def __init__(self, parent, x, y, largeur, hauteur, couleur, panier):
        super().__init__(x, y, largeur, hauteur, couleur)
        self.parent  =parent
        self.prix = parent.prix
        self.nom = parent.nom
        self.ajouter_texte(self.nom, 10, 10, couleur=(0,0,0), taille=25)
        self.panier = panier
        # Charger l'image
        
        if os.path.exists(parent.image_path):
            self.image = pygame.image.load(parent.image_path)
        else : 
            self.image = pygame.image.load('./images/flappy_bird.png')

        self.image = pygame.transform.scale(self.image, (largeur-40, hauteur-140))  # redimensionner pour s'adapter
        # Ajouter le prix
        self.ajouter_texte(f"Prix : {format(self.prix, '.2f')} €", 20, hauteur-80, couleur=(0,0,0), taille=25)
        # Bouton acheter
        bouton_acheter = Bouton(self, largeur//2 - 50, hauteur-50, 100, 40, (100,255,100), ("Acheter",30), action=self.acheter_produit, args= (panier,))
        

    def afficher(self, surface):
        super().afficher(surface)
        # Afficher l'image
        surface.blit(self.image, (self.x + 20, self.y + 30))
    
    def acheter_produit(self, panier):
        self.panier.ajouter_produit(self.parent)
        



class ProduitPanier(Fenetre):
    def __init__(self, parent, x, y,
                 largeur=180, hauteur=250, couleur=(230,230,230),
                 supprimer_action=None, panier =0):
        
        super().__init__(x, y, largeur, hauteur, couleur)
        
        self.nom = parent.nom
        self.prix = parent.prix

        #self.ajouter_texte(self.nom, 10, 10, couleur=(0,0,0), taille=25)
        self.ajouter_texte(f"Prix : {format(self.prix, '.2f')} €", 10, hauteur-70,couleur=(0,0,0), taille=22)
        self.ajouter_texte(self.nom, 10, 10, couleur=(0,0,0), taille=25)

        if os.path.exists(parent.image_path):
            self.image = pygame.image.load(parent.image_path)
        else : 
            self.image = pygame.image.load('./images/flappy_bird.png')
       
        self.image = pygame.transform.scale(self.image,
                                            (largeur - 20, hauteur - 120))

        bouton_supprimer = Bouton(
            self,
            largeur//2 - 50,
            hauteur - 45,
            100,
            40,
            (255,100,100),
            ("Supprimer",30),
            action=supprimer_action
        )


    def afficher(self, surface):
        super().afficher(surface)
        surface.blit(self.image, (self.x + 10, self.y + 40))


class Panier_fenetre(Fenetre):
    def __init__(self, x, y, largeur, hauteur, couleur=(200,200,200), user  = 0):
        super().__init__(x, y, largeur, hauteur, couleur)
        self.produits = []   # Liste des ProduitPanier
        self.total = 0
        self.user  = user
        Bouton(self,  largeur - 60, 10, 55,40, (255,100,100),("Payer",30), self.payer, args = (self.user,))

    def ajouter_produit(self, produit):
        """
        Ajoute un nouveau ProduitPanier dans le panier.
        """

        # Position verticale en fonction du nombre d'éléments
        index = len(self.produits)
        px = self.x + 10
        py = self.y + 50 + index * 260   # espacement entre produits

        # Action de suppression
        def supprimer_action(p=produit.nom):
            self.supprimer_produit(p)

        # Créer le produit à afficher dans le panier
        self.produits.append(ProduitPanier(produit, px, py,supprimer_action=lambda: self.supprimer_produit(produit.nom)))
        self.mettre_a_jour_total()

    def supprimer_produit(self, nom_du_produit):
        """
        Supprime le premier produit correspondant au nom.
        """

        for p in self.produits:
            if p.nom == nom_du_produit:
                self.produits.remove(p)
                break

        self.reorganiser_positions()
        self.mettre_a_jour_total()

    def reorganiser_positions(self):
        """
        Replace les produits proprement après une suppression.
        """

        for i, p in enumerate(self.produits):
            p.x = self.x + 10
            p.y = self.y + 10 + i * 260

    def mettre_a_jour_total(self):
        self.total = sum(p.prix for p in self.produits)

    def afficher(self, surface):
        super().afficher(surface)

        # Afficher les produits du panier
        for p in self.produits:
            p.afficher(surface)

        # Afficher le total du panier
        font = pygame.font.SysFont(None, 30)
        surface.blit(
            font.render(f"Total : {format(self.total, '.2f')} €", True, (0,0,0)),
            (self.x + 20, self.y +20 )
        )
    def payer(self, user) : 
        if user.monnaie > self.total : 
            user.monnaie -= self.total
            self.produits = []
            self.total = 0
            
        else : 
            print("pas assez d'argent")
        print(user.monnaie)

    


def get_path (name) : 
    return os.path.join(os.path.dirname(__file__), name)

