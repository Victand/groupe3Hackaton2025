"""
GUIDE DE SURVIE HACKATHON - VERSION CORRIGÉE
================================================
Un système pour planifier vos trajets entre lieux de hackathon
en France, avec choix du mode de transport.

CORRECTIONS APPORTÉES :
1. Ajout de __hash__ et __eq__ pour LieuHackathon (nécessaire pour les sets)
2. Correction du heapq.heappop pour gérer les comparaisons de tuples
3. Meilleure gestion des erreurs dans calculer_itineraire
"""

# === IMPORTS ===
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum
import heapq
import folium
import webbrowser
from datetime import datetime
import math
import random as rd

# === TYPES DE HACKATHON ===
class TypeHackathon(Enum):
    """Différents types de lieux de hackathon"""
    INCUBATEUR = "Incubateur"
    BUSINESS = "Business"
    CAMPUS = "Campus"
    INNOVATION = "Innovation"
    TECH_HUB = "Tech Hub"
    TECH_PARK = "Tech Park"

# === POSITION GÉOGRAPHIQUE ===
@dataclass
class Position:
    """Une position sur la carte avec latitude et longitude"""
    latitude: float
    longitude: float
    
    def distance_vers(self, autre_position: 'Position') -> float:
        """Calcule la distance en km vers une autre position"""
        # Formule mathématique pour distance entre deux points sur la Terre
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(autre_position.latitude), math.radians(autre_position.longitude)
        
        diff_lat = lat2 - lat1
        diff_lon = lon2 - lon1
        
        a = math.sin(diff_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Rayon de la Terre = 6371 km

# === MODES DE TRANSPORT ===
class Transport(ABC):
    """Classe de base pour tous les types de transport"""
    
    @abstractmethod
    def calculer_temps(self, distance_km: float) -> float:
        """Calcule le temps de trajet en heures"""
        pass
    
    @abstractmethod
    def get_nom(self) -> str:
        """Retourne le nom du transport"""
        pass
    
    @abstractmethod
    def get_vitesse(self) -> float:
        """Retourne la vitesse moyenne en km/h"""
        pass
    
    @abstractmethod
    def get_couleur(self) -> str:
        """Retourne la couleur pour l'affichage sur la carte"""
        pass


class Train(Transport):
    """Transport par train (TGV)"""
    
    def __init__(self, vitesse: float = 200):
        self._vitesse = vitesse
    
    def calculer_temps(self, distance_km: float) -> float:
        return distance_km / self._vitesse
    
    def get_nom(self) -> str:
        return "train"
    
    def get_vitesse(self) -> float:
        return self._vitesse
    
    def get_couleur(self) -> str:
        return "blue"


class Voiture(Transport):
    """Transport par voiture"""
    
    def __init__(self, vitesse: float = 90):
        self._vitesse = vitesse
    
    def calculer_temps(self, distance_km: float) -> float:
        return distance_km / self._vitesse
    
    def get_nom(self) -> str:
        return "voiture"
    
    def get_vitesse(self) -> float:
        return self._vitesse
    
    def get_couleur(self) -> str:
        return "red"

# === CRÉATION DE TRANSPORTS (USINE) ===
class FabriqueTransport:
    """Crée les objets de transport selon le type demandé"""
    
    _transports = {
        "train": Train(),
        "voiture": Voiture()
    }
    
    @classmethod
    def creer(cls, type_transport: str) -> Transport:
        """Crée un transport selon le type"""
        transport = cls._transports.get(type_transport.lower())
        if not transport:
            raise ValueError(f"Transport inconnu : {type_transport}")
        return transport

# === LIEU DE HACKATHON ===
class LieuHackathon:
    """Un lieu où se déroule un hackathon"""
    
    def __init__(self, nom: str, ville: str, position: Position, 
                 type_lieu: TypeHackathon):
        self._nom = nom
        self._ville = ville
        self._position = position
        self._type = type_lieu
        self._connexions = []  # Liste des routes vers d'autres lieux
    
    # Getters pour protéger les données
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def ville(self) -> str:
        return self._ville
    
    @property
    def position(self) -> Position:
        return self._position
    
    @property
    def type_lieu(self) -> TypeHackathon:
        return self._type
    
    @property
    def connexions(self):
        return self._connexions.copy()  # Copie pour protéger les données
    
    def ajouter_route(self, route: 'Route'):
        """Ajoute une route vers un autre lieu"""
        self._connexions.append(route)
    
    def get_voisins(self) -> List[Tuple['LieuHackathon', 'Route']]:
        """Retourne tous les lieux accessibles depuis ce lieu"""
        return [(r.arrivee, r) for r in self._connexions]
    
    # CORRECTION 1 : Ajout de __hash__ et __eq__ pour pouvoir utiliser les lieux dans des sets
    def __hash__(self):
        """Hash basé sur le nom unique du lieu"""
        return hash(self._nom)
    
    def __eq__(self, other):
        """Égalité basée sur le nom du lieu"""
        if not isinstance(other, LieuHackathon):
            return False
        return self._nom == other._nom
    
    def __str__(self) -> str:
        return f"{self._nom} ({self._ville})"
    
    def __repr__(self) -> str:
        return f"LieuHackathon({self._nom})"

# === ROUTE ENTRE DEUX LIEUX ===
class Route:
    """Une route entre deux lieux avec un mode de transport"""
    
    def __init__(self, depart: LieuHackathon, arrivee: LieuHackathon,
                 transport: Transport, distance_km: float):
        self._depart = depart
        self._arrivee = arrivee
        self._transport = transport
        self._distance = distance_km
    
    @property
    def depart(self) -> LieuHackathon:
        return self._depart
    
    @property
    def arrivee(self) -> LieuHackathon:
        return self._arrivee
    
    @property
    def transport(self) -> Transport:
        return self._transport
    
    @property
    def distance_km(self) -> float:
        return self._distance
    
    def calculer_temps(self) -> float:
        """Calcule le temps de trajet en heures"""
        return self._transport.calculer_temps(self._distance) + rd.uniform(0,0.01)
    
    def get_type_transport(self) -> str:
        """Retourne le type de transport"""
        return self._transport.get_nom()

# === RÉSULTAT D'UN ITINÉRAIRE ===
@dataclass
class ItineraireResultat:
    """Stocke les détails d'un itinéraire calculé"""
    lieux: List[LieuHackathon]        # Liste des lieux visités
    routes: List[Route]               # Liste des routes empruntées
    temps_total: float                # Temps total en heures
    distance_totale: float            # Distance totale en km
    trouve: bool                      # True si un itinéraire a été trouvé
    
    @property
    def nb_etapes(self) -> int:
        return len(self.lieux)
    
    def get_resume(self) -> str:
        """Retourne un résumé simple de l'itinéraire"""
        if not self.trouve:
            return "❌ Aucun itinéraire trouvé"
        
        lignes = [
            f"✅ Itinéraire trouvé : {self.nb_etapes} étapes",
            f"📏 Distance totale : {self.distance_totale:.1f} km",
            f"⏱️  Temps total : {self.temps_total:.1f}h ({self.temps_total*60:.0f} min)"
        ]
        return "\n".join(lignes)

# === ALGORITHME DE RECHERCHE DE CHEMIN ===
class RechercheChemin(ABC):
    """Algorithme pour trouver le meilleur chemin"""
    
    @abstractmethod
    def trouver_chemin(self, depart: LieuHackathon,
                      arrivee: LieuHackathon,
                      mode_transport: Optional[str] = None) -> ItineraireResultat:
        pass


class Dijkstra(RechercheChemin):
    """Algorithme de Dijkstra pour trouver le chemin le plus rapide"""
    
    def trouver_chemin(self, depart: LieuHackathon,
                      arrivee: LieuHackathon,
                      mode_transport: Optional[str] = None) -> ItineraireResultat:
        """
        Trouve le chemin le plus rapide entre deux lieux
        Peut filtrer par mode de transport
        """
        
        # CORRECTION 2 : Ajout d'un compteur unique pour éviter les problèmes de comparaison
        compteur = 0
        
        # File de priorité : (temps_cumulé, compteur, lieu_actuel, chemin_lieux, chemin_routes)
        file = [(0, compteur, depart, [depart], [])]
        compteur += 1
        
        visites = set()
        
        while file:
            # CORRECTION 3 : Déballage avec le compteur
            temps_actuel, _, lieu_actuel, chemin_lieux, chemin_routes = heapq.heappop(file)
            
            if lieu_actuel in visites:
                continue
            
            visites.add(lieu_actuel)
            
            # Si on est arrivé à destination
            if lieu_actuel == arrivee:
                distance_totale = sum(r.distance_km for r in chemin_routes)
                return ItineraireResultat(
                    chemin_lieux,
                    chemin_routes,
                    temps_actuel,
                    distance_totale,
                    True
                )
            
            # Explorer les voisins
            for voisin, route in lieu_actuel.get_voisins():
                # Filtrer par mode de transport si demandé
                if mode_transport and route.get_type_transport() != mode_transport:
                    continue
                
                if voisin not in visites:
                    temps_trajet = route.calculer_temps()
                    nouveau_temps = temps_actuel + temps_trajet
                    
                    heapq.heappush(file, (
                        nouveau_temps,
                        compteur,  # Compteur unique pour éviter les comparaisons de lieux
                        voisin,
                        chemin_lieux + [voisin],
                        chemin_routes + [route]
                    ))
                    compteur += 1
        
        # Pas de chemin trouvé
        return ItineraireResultat([], [], float('inf'), 0, False)

# === RÉSEAU COMPLET ===
class ReseauHackathon:
    """Gère tous les lieux et connexions"""
    
    def __init__(self):
        self._lieux = {}  # Dictionnaire nom -> lieu
        self._algorithme = Dijkstra()
    
    def ajouter_lieu(self, lieu: LieuHackathon):
        """Ajoute un lieu au réseau"""
        self._lieux[lieu.nom] = lieu
    
    def ajouter_route_double_sens(self, nom1: str, nom2: str,
                                 type_transport: str, distance_km: float):
        """Ajoute une route dans les deux sens entre deux lieux"""
        lieu1 = self._lieux.get(nom1)
        lieu2 = self._lieux.get(nom2)
        
        if not lieu1 or not lieu2:
            raise ValueError(f"Lieu non trouvé : {nom1} ou {nom2}")
        
        transport = FabriqueTransport.creer(type_transport)
        
        # Route aller
        route1 = Route(lieu1, lieu2, transport, distance_km)
        lieu1.ajouter_route(route1)
        
        # Route retour
        route2 = Route(lieu2, lieu1, transport, distance_km)
        lieu2.ajouter_route(route2)
    
    def get_lieu(self, nom: str):
        """Retourne un lieu par son nom"""
        return self._lieux.get(nom)
    
    def get_tous_lieux(self):
        """Retourne tous les lieux"""
        return list(self._lieux.values())
    
    def rechercher_lieux(self, terme: str):
        """Recherche des lieux par nom ou ville"""
        terme = terme.lower()
        resultats = []
        
        for lieu in self._lieux.values():
            if terme in lieu.nom.lower() or terme in lieu.ville.lower():
                resultats.append(lieu)
        
        return resultats
    
    def calculer_itineraire(self, depart_nom: str, arrivee_nom: str,
                           mode_transport: Optional[str] = None) -> ItineraireResultat:
        """Calcule l'itinéraire entre deux lieux"""
        # CORRECTION 4 : Meilleure gestion des erreurs avec messages clairs
        depart = self.get_lieu(depart_nom)
        arrivee = self.get_lieu(arrivee_nom)
        
        if not depart:
            print(f"⚠️  ERREUR : Le lieu '{depart_nom}' n'existe pas dans le réseau")
            print(f"   Conseil : Utilisez l'option 1 pour voir tous les lieux disponibles")
            return ItineraireResultat([], [], float('inf'), 0, False)
        
        if not arrivee:
            print(f"⚠️  ERREUR : Le lieu '{arrivee_nom}' n'existe pas dans le réseau")
            print(f"   Conseil : Utilisez l'option 1 pour voir tous les lieux disponibles")
            return ItineraireResultat([], [], float('inf'), 0, False)
        
        if depart == arrivee:
            print(f"⚠️  ERREUR : Le départ et l'arrivée sont identiques")
            return ItineraireResultat([], [], float('inf'), 0, False)
        
        return self._algorithme.trouver_chemin(depart, arrivee, mode_transport)
    
    def generer_carte(self, itineraire: Optional[ItineraireResultat] = None):
        """Crée une carte interactive avec l'itinéraire"""
        # Carte centrée sur la France
        carte = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
        
        # Couleurs pour chaque type de hackathon
        couleurs_types = {
            TypeHackathon.INCUBATEUR: "red",
            TypeHackathon.BUSINESS: "blue",
            TypeHackathon.CAMPUS: "green",
            TypeHackathon.INNOVATION: "orange",
            TypeHackathon.TECH_HUB: "purple",
            TypeHackathon.TECH_PARK: "darkred"
        }
        
        # Ajouter tous les lieux
        lieux_itineraire = set(itineraire.lieux) if itineraire and itineraire.trouve else set()
        
        for lieu in self._lieux.values():
            couleur = couleurs_types.get(lieu.type_lieu, "gray")
            
            # Étoile pour les lieux de l'itinéraire
            if lieu in lieux_itineraire:
                icon = folium.Icon(color=couleur, icon="star")            
            else:
                icon = folium.Icon(color=couleur, icon="info-sign")
            
            # Texte popup détaillé
            popup_text = f"""
            <div style='font-family: Arial; font-size: 14px;'>
            <h4 style='color:{couleur};'><b>{lieu.nom}</b></h4>
            <hr style='margin: 5px 0;'>
            <p><b>📍 Ville:</b> {lieu.ville}</p>
            <p><b>🏷️ Type:</b> {lieu.type_lieu.value}</p>
            <p><b>🌐 Coordonnées:</b><br>
            {lieu.position.latitude:.4f}, {lieu.position.longitude:.4f}</p>
            </div>
            """
            
            folium.Marker(
                location=[lieu.position.latitude, lieu.position.longitude],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=lieu.nom,
                icon=icon
            ).add_to(carte)
        
        # Ajouter l'itinéraire s'il existe
        if itineraire and itineraire.trouve:
            for i, route in enumerate(itineraire.routes):
                couleur_ligne = route.transport.get_couleur()
                
                folium.PolyLine(
                    locations=[
                        [route.depart.position.latitude, route.depart.position.longitude],
                        [route.arrivee.position.latitude, route.arrivee.position.longitude]
                    ],
                    color=couleur_ligne,
                    weight=4,
                    opacity=0.7,
                    popup=(
                        f"<b>Étape {i+1}</b><br>"
                        f"{route.depart.nom} → {route.arrivee.nom}<br>"
                        f"🚦 {route.transport.get_nom().upper()}<br>"
                        f"📏 {route.distance_km:.0f} km<br>"
                        f"⏱️ {route.calculer_temps()*60:.0f} min"
                    )
                ).add_to(carte)
            
            # Ajouter un tableau détaillé de l'itinéraire
            details_html = '''
            <div style="position: fixed; 
                        top: 50px; left: 50px; width: 350px; height: auto; 
                        background-color: white; z-index:9999; font-size:14px;
                        border:2px solid grey; border-radius: 5px; padding: 15px;
                        box-shadow: 0 0 15px rgba(0,0,0,0.2);
                        font-family: Arial; overflow-y: auto; max-height: 80vh;">
            <h4 style="margin-top:0; color:#2c3e50;">🗺️ DÉTAILS DE L'ITINÉRAIRE</h4>
            <hr style="margin:10px 0;">
            '''
            
            # Ajouter chaque étape
            for i, lieu in enumerate(itineraire.lieux):
                if i == 0:
                    details_html += f'<p style="margin:8px 0;"><b>🚩 DÉPART</b><br>{lieu.nom}</p>'
                elif i == len(itineraire.lieux) - 1:
                    details_html += f'<p style="margin:8px 0;"><b>🏁 ARRIVÉE</b><br>{lieu.nom}</p>'
                else:
                    details_html += f'<p style="margin:8px 0;"><b>📍 Étape {i+1}</b><br>{lieu.nom}</p>'                
                # Ajouter les détails de la route si elle existe
                if i < len(itineraire.routes):
                    route = itineraire.routes[i]
                    transport_emoji = "🚄" if route.transport.get_nom() == "train" else "🚗"
                    
                    details_html += f'''
                    <div style="background-color:#f8f9fa; padding:8px; margin:5px 0; border-radius:4px; border-left: 4px solid {route.transport.get_couleur()};">
                        <p style="margin:2px 0;"><b>{transport_emoji} {route.transport.get_nom().upper()}</b></p>
                        <p style="margin:2px 0; font-size:12px;">📏 {route.distance_km:.0f} km</p>
                        <p style="margin:2px 0; font-size:12px;">⏱️ {route.calculer_temps()*60:.0f} min</p>
                        <p style="margin:2px 0; font-size:12px;">🏃 {route.transport.get_vitesse():.0f} km/h</p>
                    </div>
                    '''
            
            # Résumé total
            details_html += f'''
            <hr style="margin:10px 0;">
            <div style="background-color:#e8f4fd; padding:10px; border-radius:4px;">
                <p style="margin:4px 0;"><b>📊 RÉSUMÉ</b></p>
                <p style="margin:4px 0; font-size:13px;">📏 Distance totale: {itineraire.distance_totale:.0f} km</p>
                <p style="margin:4px 0; font-size:13px;">⏱️ Temps total: {itineraire.temps_total:.1f}h ({itineraire.temps_total*60:.0f} min)</p>
                <p style="margin:4px 0; font-size:13px;">📍 Nombre d'étapes: {itineraire.nb_etapes}</p>
            </div>
            </div>
            '''
            
            carte.get_root().html.add_child(folium.Element(details_html))
        
        # Légende générale
        legende_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 250px; height: auto; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; border-radius: 5px; padding: 15px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    font-family: Arial;">
        <h5 style="margin-top:0; color:#2c3e50;">🗺️ LÉGENDE</h5>
        <hr style="margin:10px 0;">
        
        <p style="margin:5px 0;"><b>📍 Types de hackathon :</b></p>
        <p style="margin:3px 0;"><span style="color:red;">⬤</span> Incubateur</p>
        <p style="margin:3px 0;"><span style="color:blue;">⬤</span> Business</p>
        <p style="margin:3px 0;"><span style="color:green;">⬤</span> Campus</p>
        <p style="margin:3px 0;"><span style="color:orange;">⬤</span> Innovation</p>
        <p style="margin:3px 0;"><span style="color:purple;">⬤</span> Tech Hub</p>
        <p style="margin:3px 0;"><span style="color:darkred;">⬤</span> Tech Park</p>
        
        <hr style="margin:10px 0;">
        
        <p style="margin:5px 0;"><b>🚦 Modes de transport :</b></p>
        <p style="margin:3px 0;">
            <span style="color:blue; font-weight:bold;">━━━━</span> Train TGV
        </p>
        <p style="margin:3px 0;">
            <span style="color:red; font-weight:bold;">━━━━</span> Voiture
        </p>
        
        <hr style="margin:10px 0;">
        
        <p style="margin:5px 0;"><b>⭐ Itinéraire :</b></p>
        <p style="margin:3px 0; font-size:12px;">
            Les lieux avec étoile font partie de l'itinéraire
        </p>
        </div>
        '''
        carte.get_root().html.add_child(folium.Element(legende_html))
        
        return carte

# === CRÉATION DU RÉSEAU FRANÇAIS ===
def creer_reseau_france() -> ReseauHackathon:
    """Crée le réseau complet des hackathons en France"""
    reseau = ReseauHackathon()
    
    # Liste des 20 lieux de hackathon
    lieux_data = [
        ("Station F Paris", "Paris", 48.8334, 2.3725, TypeHackathon.INCUBATEUR),
        ("La Défense", "Paris", 48.8920, 2.2380, TypeHackathon.BUSINESS),
        ("Palaiseau Tech", "Palaiseau", 48.7144, 2.2464, TypeHackathon.CAMPUS),
        ("Strasbourg Digital", "Strasbourg", 48.5734, 7.7521, TypeHackathon.INNOVATION),
        ("Nancy Hub", "Nancy", 48.6921, 6.1844, TypeHackathon.CAMPUS),
        ("Metz Tech Center", "Metz", 49.1193, 6.1757, TypeHackathon.INNOVATION),
        ("Lille EuraTech", "Lille", 50.6311, 3.0206, TypeHackathon.INCUBATEUR),
        ("Lens Innovation", "Lens", 50.4280, 2.8317, TypeHackathon.TECH_HUB),
        ("Rouen Digital", "Rouen", 49.4432, 1.0993, TypeHackathon.INNOVATION),
        ("Rennes French Tech", "Rennes", 48.1173, -1.6778, TypeHackathon.INCUBATEUR),
        ("Brest Tech", "Brest", 48.3905, -4.4860, TypeHackathon.CAMPUS),
        ("Nantes Tech Hub", "Nantes", 47.2184, -1.5536, TypeHackathon.INNOVATION),
        ("Bordeaux Technowest", "Bordeaux", 44.8378, -0.5792, TypeHackathon.TECH_PARK),
        ("Limoges Innovation", "Limoges", 45.8336, 1.2611, TypeHackathon.CAMPUS),
        ("Toulouse IoT Valley", "Toulouse", 43.6047, 1.4442, TypeHackathon.INNOVATION),
        ("Montpellier Tech", "Montpellier", 43.6108, 3.8767, TypeHackathon.CAMPUS),
        ("Lyon Tech La Doua", "Lyon", 45.7833, 4.8667, TypeHackathon.CAMPUS),
        ("Grenoble Minatec", "Grenoble", 45.1885, 5.7245, TypeHackathon.TECH_PARK),
        ("Marseille Innovation", "Marseille", 43.2965, 5.3698, TypeHackathon.INCUBATEUR),
        ("Nice Sophia Antipolis", "Nice", 43.7102, 7.2620, TypeHackathon.TECH_PARK),
    ]
    
    # Créer tous les lieux
    for nom, ville, lat, lon, type_lieu in lieux_data:
        lieu = LieuHackathon(nom, ville, Position(lat, lon), type_lieu)
        reseau.ajouter_lieu(lieu)
    
    # Routes en train
    routes_train = [
        ("Station F Paris", "Strasbourg Digital", 400),
        ("Station F Paris", "Lille EuraTech", 220),
        ("Station F Paris", "Nantes Tech Hub", 380),
        ("Station F Paris", "Bordeaux Technowest", 550),
        ("Station F Paris", "Lyon Tech La Doua", 450),
        ("Station F Paris", "Marseille Innovation", 750),
        ("Lyon Tech La Doua", "Marseille Innovation", 300),
        ("Lyon Tech La Doua", "Grenoble Minatec", 100),
        ("Lille EuraTech", "Strasbourg Digital", 480),
        ("Bordeaux Technowest", "Toulouse IoT Valley", 250),
        ("Nantes Tech Hub", "Rennes French Tech", 110),
        ("Strasbourg Digital", "Nancy Hub", 130),
        ("Nancy Hub", "Metz Tech Center", 50),
        ("Toulouse IoT Valley", "Montpellier Tech", 240),
        ("Marseille Innovation", "Nice Sophia Antipolis", 180),
        ("Rouen Digital", "Station F Paris", 130),
    ]
    
    for lieu1, lieu2, distance in routes_train:
        reseau.ajouter_route_double_sens(lieu1, lieu2, "train", distance)
    
    # Routes en voiture
    routes_voiture = [
        ("Station F Paris", "La Défense", 10),
        ("Station F Paris", "Palaiseau Tech", 30),
        ("La Défense", "Palaiseau Tech", 35),
        ("Lille EuraTech", "Lens Innovation", 35),
        ("Lens Innovation", "Rouen Digital", 180),
        ("Rennes French Tech", "Brest Tech", 245),
        ("Brest Tech", "Nantes Tech Hub", 310),
        ("Nantes Tech Hub", "Bordeaux Technowest", 350),
        ("Bordeaux Technowest", "Limoges Innovation", 220),
        ("Limoges Innovation", "Lyon Tech La Doua", 380),
        ("Lyon Tech La Doua", "Grenoble Minatec", 105),
        ("Strasbourg Digital", "Nancy Hub", 145),
        ("Nancy Hub", "Metz Tech Center", 55),
        ("Metz Tech Center", "Lille EuraTech", 310),
        ("Toulouse IoT Valley", "Montpellier Tech", 240),
        ("Montpellier Tech", "Marseille Innovation", 170),
        ("Marseille Innovation", "Nice Sophia Antipolis", 200),
        ("Grenoble Minatec", "Nice Sophia Antipolis", 320),
        ("Palaiseau Tech", "Rouen Digital", 145),
        ("Station F Paris", "Lyon Tech La Doua", 465),
    ]
    
    for lieu1, lieu2, distance in routes_voiture:
        reseau.ajouter_route_double_sens(lieu1, lieu2, "voiture", distance)
    
    return reseau

# === INTERFACE UTILISATEUR ===
def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*70)
    print("    🚀 GUIDE DE SURVIE HACKATHON - FRANCE 🚀")
    print("="*70)
    print("\n📋 MENU :")
    print("  1. 📍 Voir tous les lieux")
    print("  2. 🔍 Rechercher un lieu")
    print("  3. 🛣️  Calculer un itinéraire")
    print("  4. 🗺️  Générer la carte complète")
    print("  0. ❌ Quitter")
    print("\n" + "="*70)

def main():
    """Fonction principale du programme"""
    print("\n⚙️  Construction du réseau français de hackathons...")
    reseau = creer_reseau_france()
    print(f"✅ Réseau prêt : {len(reseau.get_tous_lieux())} lieux")
    
    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()
        
        if choix == "1":
            print("\n📍 LISTE DES LIEUX DE HACKATHON :")
            print("-" * 50)
            lieux = sorted(reseau.get_tous_lieux(), key=lambda l: l.nom)
            for i, lieu in enumerate(lieux, 1):
                print(f"{i:2}. {lieu.nom:30} | {lieu.ville:15} | {lieu.type_lieu.value}")
            input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        elif choix == "2":
            terme = input("\n🔍 Rechercher (nom ou ville) : ").strip()
            if terme:
                resultats = reseau.rechercher_lieux(terme)
                print(f"\n✅ {len(resultats)} résultat(s) trouvé(s) :")
                for lieu in resultats:
                    print(f"  • {lieu.nom} à {lieu.ville} ({lieu.type_lieu.value})")
            else:
                print("\n❌ Veuillez entrer un terme de recherche")
            input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        elif choix == "3":
            print("\n🛣️  CALCUL D'ITINÉRAIRE")
            print("-" * 30)
            
            # Demander départ et arrivée
            depart = input("🚩 Lieu de départ : ").strip()
            arrivee = input("🏁 Lieu d'arrivée : ").strip()
            
            # Demander le mode de transport
            print("\n🚆🚗 CHOIX DU TRANSPORT :")
            print("  1. Tous les modes (itinéraire le plus rapide)")
            print("  2. Train uniquement")
            print("  3. Voiture uniquement")
            
            mode_choix = input("  👉 Votre choix (1-3) : ").strip()
            
            mode = None
            if mode_choix == "2":
                mode = "train"
                print("  ✅ Mode : Train TGV (200 km/h)")
            elif mode_choix == "3":
                mode = "voiture"
                print("  ✅ Mode : Voiture (90 km/h)")
            else:
                print("  ✅ Mode : Mixte (itinéraire optimal)")
            
            # Calculer l'itinéraire
            print(f"\n⚙️  Calcul de l'itinéraire {depart} → {arrivee}...")
            resultat = reseau.calculer_itineraire(depart, arrivee, mode)
            
            if resultat.trouve:
                print(f"\n{resultat.get_resume()}")
                
                # Afficher les étapes
                print("\n" + "="*70)
                print("📍 ÉTAPES DE L'ITINÉRAIRE :")
                print("="*70)
                
                for i, lieu in enumerate(resultat.lieux):
                    if i == 0:
                        print(f"\n🚩 DÉPART : {lieu.nom}")
                    elif i == len(resultat.lieux) - 1:
                        print(f"\n🏁 ARRIVÉE : {lieu.nom}")
                    else:
                        print(f"\n📍 Étape {i} : {lieu.nom}")
                    
                    # Afficher la route si elle existe
                    if i < len(resultat.routes):
                        route = resultat.routes[i]
                        transport = route.transport.get_nom()
                        emoji = "🚄" if transport == "train" else "🚗"
                        
                        print(f"   ↓")
                        print(f"   {emoji} {transport.upper()} vers {resultat.lieux[i+1].nom}")
                        print(f"   📏 Distance : {route.distance_km:.0f} km")
                        print(f"   ⏱️  Temps : {route.calculer_temps()*60:.0f} min")
                        print(f"   🏃 Vitesse : {route.transport.get_vitesse():.0f} km/h")
                
                # Proposer la carte
                print("\n" + "="*70)
                carte_choix = input("🗺️  Générer la carte avec itinéraire ? (o/n) : ").strip().lower()
                
                if carte_choix == 'o':
                    print("\n⚙️  Création de la carte...")
                    carte = reseau.generer_carte(resultat)
                    nom_fichier = f'itineraire_{depart.replace(" ", "_")}_vers_{arrivee.replace(" ", "_")}.html'
                    carte.save(nom_fichier)
                    print(f"✅ Carte sauvegardée : {nom_fichier}")
                    
                    ouvrir = input("🌐 Ouvrir dans le navigateur ? (o/n) : ").strip().lower()
                    if ouvrir == 'o':
                        webbrowser.open(nom_fichier)
            else:
                print("\n❌ Aucun itinéraire trouvé !")
                if mode:
                    print(f"⚠️  Essayez sans restriction de mode de transport")
            
            input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        elif choix == "4":
            print("\n🗺️  GÉNÉRATION DE LA CARTE COMPLÈTE")
            carte = reseau.generer_carte()
            nom_fichier = f'carte_hackathons_france_{datetime.now().strftime("%H%M%S")}.html'
            carte.save(nom_fichier)
            print(f"✅ Carte sauvegardée : {nom_fichier}")
            
            ouvrir = input("🌐 Ouvrir dans le navigateur ? (o/n) : ").strip().lower()
            if ouvrir == 'o':
                webbrowser.open(nom_fichier)
            
            input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        elif choix == "0":
            print("\n👋 Merci d'avoir utilisé le Guide de Survie Hackathon !")
            print("   Bonne chance pour vos aventures de hackathon ! 🚀")
            break
        
        else:
            print("\n❌ Choix invalide. Veuillez choisir 0-4.")

# === DÉMARRAGE DU PROGRAMME ===
if __name__ == "__main__":
    main()