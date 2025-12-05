from classes_frontend import *
from abc import ABC, abstractmethod
import csv




# ============================
#       CLASSES PRODUITS
# ============================


class Produit(ABC):
    def __init__(self, id , nom, prix, image_path=None):
        self.id = id
        self.nom = nom
        self.prix = prix
        self.image_path = image_path  

    @abstractmethod
    def info(self):
        pass



class Alimentaire(Produit):
    pass

class Electronique(Produit):
    pass

class Humain(Produit):
    pass

class Autre(Produit):
    pass




class Boisson(Alimentaire):
    def __init__(self, id , nom, prix, volume, image_path=None):
        super().__init__(id, nom, prix, image_path)
        self.volume = volume    
        
    def info(self):
        return f" {self.id} - {self.nom} ({self.volume}L) - {self.prix}€\n"


class Food(Alimentaire):
    def __init__(self, id,  nom, prix, image_path=None):
        super().__init__(id, nom, prix, image_path)

    def info(self):
        return f" {self.id}  - {self.nom} - {self.prix}€\n"


class Vetement(Autre):
    def __init__(self, id,  nom, prix, taille, image_path=None):
        super().__init__(id , nom, prix, image_path)
        self.taille = taille

    def info(self):
        return f"{self.id} - {self.nom} - Taille {self.taille} - {self.prix}€\n"


class Tech(Electronique):
    def __init__(self,id, nom, prix, garantie, image_path=None):
        super().__init__(id, nom, prix, image_path)
        self.garantie = garantie

    def info(self):
        return f"{self.id} - {self.nom} - Garantie {self.garantie} ans - {self.prix}€\n"


class Developpeur(Humain):
    def __init__(self,id, nom, prix, niveau, image_path=None):
        super().__init__(id,nom, prix, image_path)
        self.niveau = niveau

    def info(self):
        return f"{self.id} - {self.nom} - Niveau {self.niveau} - {self.prix}€/jour - \n "


class TicketHackathon(Autre):
    def __init__(self,id, nom, prix, image_path=None):
        super().__init__(id,nom, prix, image_path)

    def info(self):
        return f"{self.id} - {self.nom} - {self.prix}€\n"



class Factory() :
    def create_Boisson(self, id, nom, volume, prix, image_path):
        # Conversion explicite pour éviter les erreurs de type
        return Boisson(id, nom, float(prix), float(volume), image_path)
    def create_Food(self, id, nom, prix, image_path):
        return Food(id, nom, float(prix), image_path)
    def create_Vetement(self, id, nom, prix, taille, image_path):
        return Vetement(id, nom, float(prix), taille, image_path)
    def create_Tech(self, id, nom, prix, garantie, image_path):
        return Tech(id, nom, float(prix), int(garantie), image_path) 
    def create_Developpeur(self, id, nom, prix, niveau, image_path):
        return Developpeur(id, nom, float(prix), niveau, image_path)
    def create_TicketHackathon(self, id, nom, prix, image_path):
        return TicketHackathon(id, nom, float(prix), image_path)



def fusion(liste_gauche, liste_droite, key):
    """
    Fusionne deux listes déjà triées (liste_gauche et liste_droite)
    en une seule liste triée, selon la clé 'key'.
    """
    resultat = []
    i = 0  # index pour liste_gauche
    j = 0  # index pour liste_droite

    # Tant qu'il reste des éléments dans les deux listes
    while i < len(liste_gauche) and j < len(liste_droite):
        if key(liste_gauche[i]) <= key(liste_droite[j]):
            resultat.append(liste_gauche[i])
            i += 1
        else:
            resultat.append(liste_droite[j])
            j += 1

    # Il peut rester des éléments dans l'une des deux listes
    while i < len(liste_gauche):
        resultat.append(liste_gauche[i])
        i += 1

    while j < len(liste_droite):
        resultat.append(liste_droite[j])
        j += 1

    return resultat
def merge_sort(liste, key):
    """
    Implémentation du tri par fusion.
    - liste : liste d'objets à trier
    - key   : fonction qui prend un élément et renvoie la clé de comparaison
    Retourne une nouvelle liste triée.
    """
    if len(liste) <= 1:
        return liste  # déjà triée

    milieu = len(liste) // 2
    gauche = merge_sort(liste[:milieu], key)
    droite = merge_sort(liste[milieu:], key)

    return fusion(gauche, droite, key)


# ============================
#       CLASSE INVENTAIRES
# ============================

class Inventaire(ABC):
    def __init__(self):
        self.liste = []

    @abstractmethod
    def ajouter_produit(self, produit):
        pass

    @abstractmethod
    def delete_produit(self, id_produit):
        pass

    # ================= AJOUT : méthodes de tri =================

    def trier_par_nom(self):
        """
        Trie l'inventaire par ordre alphabétique du nom du produit.
        """
        self.liste = merge_sort(self.liste, key=lambda p: str(p.nom).lower())

    def trier_par_prix(self):
        """
        Trie l'inventaire par ordre croissant du prix.
        """
        self.liste = merge_sort(self.liste, key=lambda p: float(p.prix))


class Inventaire_Produits(Inventaire) : 
    def __init__(self, panier):
        super().__init__()
        self.current_liste  = 0
        self.panier = panier

    def ajouter_produit(self, produit):
        self.liste.append(Produit_Fenetre(produit, 50 + len(self.liste) * 200  , 200, 100, 150, (220,220,220), self.panier))

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False

    def importer_liste(self, inventaire, force = False) : 
        if self.current_liste != inventaire or force: 
            self.current_liste = inventaire
            self.liste = []
            x, y = 0,0
            for p in inventaire.liste : 
                self.liste.append(Produit_Fenetre(p,x ,y , 100, 150, (220,220,220), self.panier))
                x += 200
                if x > 600 : 
                    x = 0
                    y+=300
            print("liste importe")

    def trier_par_nom_spe(self):
        """
        Trie l'inventaire par ordre alphabétique du nom du produit.
        """
        self.current_liste.trier_par_nom()
        self.importer_liste(self.current_liste, force = True)
        
    def trier_par_prix_spe(self):
        """
        Trie l'inventaire par ordre croissant du prix.
        """
        self.current_liste.trier_par_prix()
        self.importer_liste(self.current_liste, force = True)

class Inventaire_Panier(Inventaire) : 
    def __init__(self):
        super().__init__()
        self.prix_tot = 0

    def ajouter_produit(self, produit):
        self.liste.append(produit)
        self.prix_tot += produit.prix

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                self.prix_tot -= p.prix
                return True
        return False


class Inventaire_boisson(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_food(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_vetement(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_tech(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_developpeur(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_ticket(Inventaire):
    def __init__(self):
        super().__init__()

    def ajouter_produit(self, produit):
        self.liste.append(produit)

    def delete_produit(self, id_produit):
        for p in self.liste:
            if p.id == id_produit:
                self.liste.remove(p)
                return True
        return False


class Inventaire_totale(Inventaire):
    def __init__(self):
        super().__init__()
        self.inventaires = []  # on garde une référence vers tous les inventaires sources

    def ajouter_produit(self, produit):
        """
        Implémentation minimale pour respecter l'interface Inventaire.
        Ici, on peut ajouter un produit directement dans l'inventaire total.
        """
        self.liste.append(produit)

    def construire_depuis_inventaires(self, *inventaires):
        """
        Construit l'inventaire total en concaténant les listes
        de tous les inventaires passés en argument.
        """
        self.inventaires = list(inventaires)
        self.liste = []
        for inv in inventaires:
            self.liste.extend(inv.liste)

    def delete_produit(self, id_produit):
        """
        Supprime le produit d'id `id_produit` :
        - dans tous les inventaires sources
        - et dans l'inventaire total
        Retourne True si au moins un produit a été supprimé, False sinon.
        """
        supprime = False

        # 1) supprimer dans les inventaires d'origine
        for inv in self.inventaires:
            if isinstance(inv, Inventaire):  # par sécurité
                if inv.delete_produit(id_produit):
                    supprime = True

        # 2) mettre à jour la liste totale
        if supprime:
            self.liste = [p for p in self.liste if p.id != id_produit]

        return supprime


# ============================
#       CLASSE ORDER
# ============================

class Order:
    def __init__(self, statut, user, produits):
        self.statut = statut
        self.user = user
        self.produits = produits
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, payment_info):
        for observer in self.observers:
            observer.update(payment_info)

    def set_statut(self, new_statut):
        self.statut = new_statut
        payment_info = {
            "user": self.user,
            "amount": sum(p.prix for p in self.produits),
            "statut": new_statut
        }
        self.notify_observers(payment_info)


class Observer:
    def update(self, payment_info):
        raise NotImplementedError


class MessageObserver(Observer):
    def update(self, payment_info):
        print(f"[INFO] Notification envoyée :")
        print(f" - Utilisateur : {payment_info['user']}")
        print(f" - Montant : {payment_info['amount']}€")
        print(f" - Statut : {payment_info['statut']}")


# ============================
#       CLASSE UTILISATEUR
# ============================


class user(ABC) :
    def __init__(self, iduser, nom, prenom) :
        self.iduser = iduser
        self.nom = nom
        self.prenom = prenom
        self.inventaire=[]
    @abstractmethod
    def ajouter_produit_inventaire(self,produit) :
        pass
    @abstractmethod
    def supprimer_produit_inventaire(self,produit) :                 
        pass

class Admin(user) :
    def __init__(self, iduser, nom, prenom,filepath_client_csv,filepath_produit1_csv,filepath_produit2_csv,filepath_produit3_csv,filepath_produit4_csv,filepath_produit5_csv,filepath_produit6_csv) :
        super().__init__(iduser, nom, prenom)
        self.filepath_client_csv = filepath_client_csv
        self.filepath_produit1_csv = filepath_produit1_csv
        self.filepath_produit2_csv = filepath_produit2_csv
        self.filepath_produit3_csv = filepath_produit3_csv
        self.filepath_produit4_csv = filepath_produit4_csv
        self.filepath_produit5_csv = filepath_produit5_csv
        self.filepath_produit6_csv = filepath_produit6_csv

    def ajouter_produit_inventaire(self,produit) :
        self.inventaire.append(produit)
    def supprimer_produit_inventaire(self,idproduit) :
        for p in self.inventaire :
            if p.id == idproduit :
                self.inventaire.remove(p)
                return True
        return False
    def ajouter_produit_csv(self,produit,filepath) :
        with open (filepath,'a',newline='') as csvfile :
            fieldnames = ['id','nom','prix','image_path']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames,delimiter=';')
            writer.writerow({'id':produit.id,'nom':produit.nom,'prix':produit.prix,'image_path':produit.image_path})

    def supprimer_produit_csv(self,idproduit,filepath) :
        produits = []
        with open(filepath, 'r', newline='') as csvfile :
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader :
                if int(row['id']) != idproduit :
                    produits.append(row)
        with open(filepath, 'w', newline='') as csvfile :
            fieldnames = ['id','nom','prix','image_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for produit in produits :
                writer.writerow(produit)

    


    def supprimer_client_csv(self,idclient) :
        clients = []
        with open(self.filepath_client_csv, 'r', newline='') as csvfile :
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader :
                if int(row['iduser']) != idclient :
                    clients.append(row)
        with open(self.filepath_client_csv, 'w', newline='') as csvfile :
            fieldnames = ['iduser', 'nom', 'prenom']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for client in clients :
                writer.writerow(client)

class Client(user) :
    def __init__(self, iduser, nom, prenom,order,monnaie,filepath_csv,payment_strategy=None) :
        super().__init__(iduser, nom, prenom)
        self.order = order
        self.monnaie = monnaie
        self.filepath_csv = filepath_csv
        self.payment_strategy = payment_strategy
    def ajouter_produit_inventaire(self,produit) :
        self.inventaire.append(produit)

    
    def supprimer_produit_inventaire(self,idproduit) :
        for p in self.inventaire :
            if p.id == idproduit :
                self.inventaire.remove(p)
                return True
        return False

    def supprimer_produit_csv(self,idproduit,filepath) :
        produits = []
        with open(filepath, 'r', newline='') as csvfile :
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader :
                if int(row['id']) != idproduit :
                    produits.append(row)
        with open(filepath, 'w', newline='') as csvfile :
            fieldnames = ['id','nom','prix','image_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for produit in produits :
                writer.writerow(produit)

    def stockage_inventaire_csv(self) :
        with open (self.filepath_csv,'w',newline='') as csvfile :
            fieldnames = ['id','nom','prix','image_path']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames,delimiter=';')
            writer.writeheader()
            for p in self.inventaire :
                writer.writerow({'id':p.id,'nom':p.nom,'prix':p.prix,'image_path':p.image_path})


    def process_payment(self):
        if self.payment_strategy is None:
            print("Aucune méthode de paiement définie !")
        else:
            # Effectuer le paiement via la stratls
            pass




class PaymentStrategy(ABC):
    @abstractmethod
    def payer(self, client, order):
        pass

class PaypalStrategy(PaymentStrategy):
    def payer(self, client, order):
        amount = sum(p.prix for p in order.produits)
        if client.monnaie >= amount:
            client.monnaie -= amount
            order.set_statut("Payé via Paypal")
            print(f"[PayPal] Paiement de {amount}€ effectué pour {client.nom}.")
        else:
            order.set_statut("Échec paiement Paypal")
            print(f"[PayPal] Paiement échoué pour {client.nom} : fonds insuffisants.")

class CreditCardStrategy(PaymentStrategy):
    def payer(self, client, order):
        amount = sum(p.prix for p in order.produits)
        if client.monnaie >= amount:
            client.monnaie -= amount
            order.set_statut("Payé via Carte Bancaire")
            print(f"[CB] Paiement de {amount}€ effectué pour {client.nom}.")
        else:
            order.set_statut("Échec paiement CB")
            print(f"[CB] Paiement échoué pour {client.nom} : fonds insuffisants.")

class CryptoStrategy(PaymentStrategy):
    def payer(self, client, order):
        amount = sum(p.prix for p in order.produits)
        if client.monnaie >= amount:
            client.monnaie -= amount
            order.set_statut("Payé via Crypto")
            print(f"[Crypto] Paiement de {amount}€ effectué pour {client.nom}.")
        else:
            order.set_statut("Échec paiement Crypto")
            print(f"[Crypto] Paiement échoué pour {client.nom} : fonds insuffisants.")




