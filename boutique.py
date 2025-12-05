import pandas as pd
import csv
from classes_boutiques import *



def create_boisson_from_csv(Inventaire_boisson, df):
    factory = Factory()
    for index, row in df.iterrows():
        product = factory.create_Boisson(
            row['id'], row['nom'], row['volume'], row['prix'], row['image_path']
        )
        Inventaire_boisson.ajouter_produit(product)

        
test2 = pd.read_csv("./dossiercsv/food.csv",sep=";")
def create_food_from_csv(Inventaire_food,test2):
    factory = Factory()
    
    for index, row in test2.iterrows():
        product = factory.create_Food(row['id'], row['nom'], row['prix'], row['image_path'])

        Inventaire_food.ajouter_produit(product)
    

test3 = pd.read_csv("./dossiercsv/vetement.csv",sep=";")
def create_vetement_from_csv(Inventaire_vetement,test3):
    factory = Factory()

    
    for index, row in test3.iterrows():
        product = factory.create_Vetement(row['id'], row['nom'], row['prix'], row['taille'], row['image_path'])

        Inventaire_vetement.ajouter_produit(product)
    


test4 = pd.read_csv("./dossiercsv/tech.csv",sep=";")
def create_tech_from_csv(Inventaire_tech,test4):
    factory = Factory()
    
    for index, row in test4.iterrows():
        product = factory.create_Tech(row['id'], row['nom'], row['prix'],row['garantie'], row['image_path'])

        Inventaire_tech.ajouter_produit(product)
    


test5 = pd.read_csv("./dossiercsv/developpeur.csv",sep=";")
def create_developpeur_from_csv(Inventaire_developpeur,test5):
    factory = Factory()
    
    for index, row in test5.iterrows():
        product = factory.create_Developpeur(row['id'], row['nom'], row['prix'], row['niveau'], row['image_path'])

        Inventaire_developpeur.ajouter_produit(product)
    
 
test6 = pd.read_csv("./dossiercsv/ticket.csv",sep=";")
def create_ticket_from_csv(Inventaire_ticket,test6):
    factory = Factory()
    
    for index, row in test6.iterrows():
        product = factory.create_TicketHackathon(row['id'], row['nom'], row['prix'], row['image_path'])

        Inventaire_ticket.ajouter_produit(product)
    
if True:
    

    print("=== Test Complet du Catalogue Hackathon ===")
    # Création inventaires
    inv_boisson = Inventaire_boisson()
    inv_food = Inventaire_food()
    inv_vetement = Inventaire_vetement()
    inv_tech = Inventaire_tech()
    inv_dev = Inventaire_developpeur()
    inv_ticket = Inventaire_ticket()

    # Chargement CSV
    create_boisson_from_csv(inv_boisson, pd.read_csv("./dossiercsv/boisson.csv", sep=";"))
    create_food_from_csv(inv_food, pd.read_csv("./dossiercsv/food.csv", sep=";"))
    create_vetement_from_csv(inv_vetement, pd.read_csv("./dossiercsv/vetement.csv", sep=";"))
    create_tech_from_csv(inv_tech, pd.read_csv("./dossiercsv/tech.csv", sep=";"))
    create_developpeur_from_csv(inv_dev, pd.read_csv("./dossiercsv/developpeur.csv", sep=";"))
    create_ticket_from_csv(inv_ticket, pd.read_csv("./dossiercsv/ticket.csv", sep=";"))

    
    # Vérifier le contenu des inventaires
    print("=== Contenu Inventaire Boissons ===")
    for p in inv_boisson.liste:
        print(p.info(), end="")

    # Inventaire total
    inv_total = Inventaire_totale()
    inv_total.construire_depuis_inventaires(inv_boisson, inv_food, inv_vetement, inv_tech, inv_dev, inv_ticket)

    # Tri par nom puis affichage total
    inv_total.trier_par_nom()
    print("\n=== INVENTAIRE TOTAL TRIE PAR NOM ===")
    for p in inv_total.liste:
        print(p.info(), end="")

    # Tri par prix puis affichage total
    inv_total.trier_par_prix()
    print("\n=== INVENTAIRE TOTAL TRIE PAR PRIX ===")
    for p in inv_total.liste:
        print(p.info(), end="")

    # Test Client et paiement avec stratégie
    order = Order(statut="En attente", user="Jean Dupont", produits=inv_boisson.liste[:2])
    client = Client(
        iduser=1,
        nom="Dupont",
        prenom="Jean",
        order=order,
        monnaie=10.0,  # Assez pour payer Coca + Pepsi = 2 + 2.5 = 4.5€
        payment_strategy=PaypalStrategy(),
        filepath_csv="./dossiercsv/client_inventaire.csv"
    )

    observer = MessageObserver()
    order.add_observer(observer)

    client.process_payment()

    # Vérification CSV
    with open(client.filepath_csv, "r") as f:
        print(f.read())

    # Vérification inventaire interne
    for p in client.inventaire:
        print(p.info(), end="")
