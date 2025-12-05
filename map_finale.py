"""
GUIDE DE SURVIE HACKATHON - VERSION POO AVANCÉE CORRIGÉE
=========================================================

Architecture orientée objet avec Design Patterns pour impressionner le jury :
- Pattern Strategy pour les algorithmes de routage
- Pattern Factory pour créer différents types de transport
- Pattern Observer pour les statistiques temps réel
- Héritage et polymorphisme pour les transports
- Encapsulation complète des données

CORRECTIONS APPORTÉES:
- Panneau de détails de l'itinéraire sur la carte
- Popup avec ville, type et coordonnées
- Correction des bugs (noms de variables, méthodes manquantes)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Protocol
from enum import Enum
import heapq
import folium
import webbrowser
from datetime import datetime
import math
import random as rd


# ============================================================================
# ENUMS ET TYPES
# ============================================================================

class TypeHackathon(Enum):
    """Catégories de lieux de hackathon"""
    INCUBATEUR = "Incubateur"
    BUSINESS = "Business"
    CAMPUS = "Campus"
    INNOVATION = "Innovation"
    TECH_HUB = "Tech Hub"
    TECH_PARK = "Tech Park"


# ============================================================================
# PATTERN STRATEGY : Stratégies de transport
# ============================================================================

class StrategieTransport(ABC):
    """Interface pour les stratégies de transport"""
    
    @abstractmethod
    def calculer_temps_trajet(self, distance_km: float) -> float:
        """Calcule le temps de trajet en heures"""
        pass
    
    @abstractmethod
    def get_nom(self) -> str:
        """Retourne le nom du transport"""
        pass
    
    @abstractmethod
    def get_vitesse(self) -> float:
        """Retourne la vitesse moyenne"""
        pass
    
    @abstractmethod
    def get_couleur_carte(self) -> str:
        """Retourne la couleur pour la visualisation"""
        pass


class TransportTrain(StrategieTransport):
    """Stratégie de transport par train (TGV)"""
    
    def __init__(self, vitesse: float = 200):
        self._vitesse = vitesse
    
    def calculer_temps_trajet(self, distance_km: float) -> float:
        return distance_km / self._vitesse
    
    def get_nom(self) -> str:
        return "train"
    
    def get_vitesse(self) -> float:
        return self._vitesse
    
    def get_couleur_carte(self) -> str:
        return "blue"


class TransportVoiture(StrategieTransport):
    """Stratégie de transport par voiture"""
    
    def __init__(self, vitesse: float = 90):
        self._vitesse = vitesse
    
    def calculer_temps_trajet(self, distance_km: float) -> float:
        return distance_km / self._vitesse
    
    def get_nom(self) -> str:
        return "voiture"
    
    def get_vitesse(self) -> float:
        return self._vitesse
    
    def get_couleur_carte(self) -> str:
        return "red"


# ============================================================================
# PATTERN FACTORY : Création de transports
# ============================================================================

class TransportFactory:
    """Factory pour créer des instances de transport"""
    
    _transports: Dict[str, StrategieTransport] = {
        "train": TransportTrain(),
        "voiture": TransportVoiture()
    }
    
    @classmethod
    def creer_transport(cls, type_transport: str) -> StrategieTransport:
        """Crée une instance de transport selon le type"""
        transport = cls._transports.get(type_transport.lower())
        if not transport:
            raise ValueError(f"Type de transport inconnu : {type_transport}")
        return transport
    
    @classmethod
    def get_types_disponibles(cls) -> List[str]:
        """Retourne la liste des types de transport disponibles"""
        return list(cls._transports.keys())


# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================

@dataclass
class Position:
    """Représente une position géographique"""
    latitude: float
    longitude: float
    
    def distance_vol_oiseau(self, autre: Position) -> float:
        """Calcule la distance à vol d'oiseau (approximation simple)"""
        # Formule de Haversine simplifiée
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(autre.latitude), math.radians(autre.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Rayon de la Terre en km


class LieuHackathon:
    """Représente un lieu de hackathon avec encapsulation complète"""
    
    def __init__(self, nom: str, ville: str, position: Position, 
                 categorie: TypeHackathon):
        self._nom = nom
        self._ville = ville
        self._position = position
        self._categorie = categorie
        self._connexions: List[Connexion] = []
    
    # Getters (encapsulation)
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
    def categorie(self) -> TypeHackathon:
        return self._categorie
    
    @property
    def connexions(self) -> List['Connexion']:
        return self._connexions.copy()  # Copie défensive
    
    def ajouter_connexion(self, connexion: 'Connexion'):
        """Ajoute une connexion à ce lieu"""
        self._connexions.append(connexion)
    
    def get_voisins(self) -> List[Tuple['LieuHackathon', 'Connexion']]:
        """Retourne les lieux voisins avec leurs connexions"""
        return [(c.destination, c) for c in self._connexions]
    
    def __str__(self) -> str:
        return f"{self._nom} ({self._ville})"
    
    def __repr__(self) -> str:
        return f"LieuHackathon({self._nom})"
    
    def __hash__(self):
        return hash(self._nom)
    
    def __eq__(self, other):
        if not isinstance(other, LieuHackathon):
            return False
        return self._nom == other._nom
    
    # Nécessaire pour heapq
    def __lt__(self, other):
        if not isinstance(other, LieuHackathon):
            return NotImplemented
        return self._nom < other._nom


class Connexion:
    """Représente une connexion entre deux lieux"""
    
    def __init__(self, origine: LieuHackathon, destination: LieuHackathon,
                 transport: StrategieTransport, distance_km: float):
        self._origine = origine
        self._destination = destination
        self._transport = transport
        self._distance_km = distance_km
    
    @property
    def origine(self) -> LieuHackathon:
        return self._origine
    
    @property
    def destination(self) -> LieuHackathon:
        return self._destination
    
    @property
    def transport(self) -> StrategieTransport:
        return self._transport
    
    @property
    def distance_km(self) -> float:
        return self._distance_km
    
    def calculer_temps_trajet(self) -> float:
        """Calcule le temps de trajet en heures"""
        return self._transport.calculer_temps_trajet(self._distance_km) + rd.uniform(0, 0.01)
    
    def __str__(self) -> str:
        return (f"{self._origine.nom} → {self._destination.nom} "
                f"({self._transport.get_nom()}, {self._distance_km}km)")


# ============================================================================
# RÉSULTAT D'ITINÉRAIRE
# ============================================================================

@dataclass
class ResultatItineraire:
    """Encapsule le résultat d'un calcul d'itinéraire"""
    lieux: List[LieuHackathon]
    connexions: List[Connexion]
    temps_total_heures: float
    distance_totale_km: float
    trouve: bool
    
    @property
    def nombre_etapes(self) -> int:
        return len(self.lieux)
    
    def get_resume(self) -> str:
        """Retourne un résumé lisible de l'itinéraire"""
        if not self.trouve:
            return "Aucun itinéraire trouvé"
        
        lignes = [
            f"Itinéraire trouvé : {self.nombre_etapes} étapes",
            f"Distance totale : {self.distance_totale_km:.1f} km",
            f"Temps total : {self.temps_total_heures:.2f}h ({self.temps_total_heures*60:.0f} min)"
        ]
        return "\n".join(lignes)


# ============================================================================
# PATTERN STRATEGY : Algorithmes de routage
# ============================================================================

class AlgorithmeRoutage(ABC):
    """Interface pour les algorithmes de routage"""
    
    @abstractmethod
    def calculer_itineraire(self, graphe: 'ReseauHackathon', 
                           depart: LieuHackathon,
                           arrivee: LieuHackathon,
                           point_intermediaire: Optional[LieuHackathon] = None
                           ) -> ResultatItineraire:
        """Calcule un itinéraire optimal"""
        pass


class DijkstraRoutage(AlgorithmeRoutage):
    """Implémentation de l'algorithme de Dijkstra"""
    
    def calculer_itineraire(self, graphe: 'ReseauHackathon',
                           depart: LieuHackathon,
                           arrivee: LieuHackathon,
                           point_intermediaire: Optional[LieuHackathon] = None
                           ) -> ResultatItineraire:
        """
        Calcule l'itinéraire optimal avec Dijkstra
        Complexité : O(E log V)
        """
        if point_intermediaire:
            # Deux Dijkstra OBLIGATOIRES : depart->inter + inter->arrivee
            # Ceci garantit que le chemin passe FORCÉMENT par le point intermédiaire
            result1 = self._dijkstra_simple(graphe, depart, point_intermediaire)
            if not result1.trouve:
                return ResultatItineraire([], [], float('inf'), 0, False)
            
            result2 = self._dijkstra_simple(graphe, point_intermediaire, arrivee)
            if not result2.trouve:
                return ResultatItineraire([], [], float('inf'), 0, False)
            
            # Fusion (éviter duplication du point intermédiaire)
            lieux_complets = result1.lieux + result2.lieux[1:]  # ← [1:] IMPORTANT !
            connexions_completes = result1.connexions + result2.connexions
            temps_total = result1.temps_total_heures + result2.temps_total_heures
            distance_totale = result1.distance_totale_km + result2.distance_totale_km
            
            return ResultatItineraire(
                lieux_complets,
                connexions_completes,
                temps_total,
                distance_totale,
                True
            )
        else:
            # Dijkstra normal : départ → arrivée (peut passer par n'importe quel point)
            return self._dijkstra_simple(graphe, depart, arrivee)
        
    def _dijkstra_simple(self, graphe: 'ReseauHackathon',
                        depart: LieuHackathon,
                        arrivee: LieuHackathon) -> ResultatItineraire:
        """Dijkstra simple entre deux lieux"""
        
        compteur = 0
        # Priority queue : (temps_cumule, compteur, lieu_actuel, chemin_lieux, chemin_connexions)
        pq = [(0, compteur, depart, [depart], [])]
        compteur += 1
        visites = set()
        
        while pq:
            temps_actuel, _, lieu_actuel, chemin_lieux, chemin_connexions = heapq.heappop(pq)
            
            if lieu_actuel in visites:
                continue
            
            visites.add(lieu_actuel)
            
            # Arrivée ?
            if lieu_actuel == arrivee:
                distance_totale = sum(c.distance_km for c in chemin_connexions)
                return ResultatItineraire(
                    chemin_lieux,
                    chemin_connexions,
                    temps_actuel,
                    distance_totale,
                    True
                )
            
            # Explorer les voisins
            for voisin, connexion in lieu_actuel.get_voisins():
                if voisin not in visites:
                    temps_trajet = connexion.calculer_temps_trajet()
                    nouveau_temps = temps_actuel + temps_trajet
                    
                    heapq.heappush(pq, (
                        nouveau_temps,
                        compteur,
                        voisin,
                        chemin_lieux + [voisin],
                        chemin_connexions + [connexion]
                    ))
                    compteur += 1
        
        # Pas de chemin trouvé
        return ResultatItineraire([], [], float('inf'), 0, False)


# ============================================================================
# PATTERN OBSERVER : Statistiques en temps réel
# ============================================================================

class StatistiquesReseau:
    """Observer qui collecte des statistiques sur le réseau"""
    
    def __init__(self):
        self._nb_lieux = 0
        self._nb_connexions_train = 0
        self._nb_connexions_voiture = 0
        self._distance_totale_train = 0.0
        self._distance_totale_voiture = 0.0
    
    def notifier_lieu_ajoute(self):
        """Notifié quand un lieu est ajouté"""
        self._nb_lieux += 1
    
    def notifier_connexion_ajoutee(self, type_transport: str, distance: float):
        """Notifié quand une connexion est ajoutée"""
        if type_transport == "train":
            self._nb_connexions_train += 1
            self._distance_totale_train += distance
        else:
            self._nb_connexions_voiture += 1
            self._distance_totale_voiture += distance
    
    def get_rapport(self) -> str:
        """Génère un rapport des statistiques"""
        total_connexions = self._nb_connexions_train + self._nb_connexions_voiture
        total_distance = self._distance_totale_train + self._distance_totale_voiture
        
        return f"""
╔═══════════════════════════════════════════╗
║     STATISTIQUES DU RÉSEAU HACKATHON      ║
╚═══════════════════════════════════════════╝

📍 Lieux total : {self._nb_lieux}
🔗 Connexions totales : {total_connexions}
   • 🚄 Train : {self._nb_connexions_train}
   • 🚗 Voiture : {self._nb_connexions_voiture}

📏 Distance totale : {total_distance:.0f} km
   • 🚄 Réseau train : {self._distance_totale_train:.0f} km
   • 🚗 Réseau voiture : {self._distance_totale_voiture:.0f} km
"""


# ============================================================================
# RÉSEAU DE HACKATHON (Classe principale)
# ============================================================================

class ReseauHackathon:
    """Gère tous les lieux et connexions avec Pattern Observer"""
    
    def __init__(self):
        self._lieux: Dict[str, LieuHackathon] = {}
        self._algorithme = DijkstraRoutage()
        self._stats = StatistiquesReseau()
    
    def ajouter_lieu(self, lieu: LieuHackathon):
        """Ajoute un lieu au réseau"""
        self._lieux[lieu.nom] = lieu
        self._stats.notifier_lieu_ajoute()
    
    def ajouter_connexion_bidirectionnelle(self, nom1: str, nom2: str,
                                          type_transport: str, distance_km: float):
        """Ajoute une connexion bidirectionnelle entre deux lieux"""
        lieu1 = self._lieux.get(nom1)
        lieu2 = self._lieux.get(nom2)
        
        if not lieu1 or not lieu2:
            raise ValueError(f"Lieu non trouvé : {nom1} ou {nom2}")
        
        transport = TransportFactory.creer_transport(type_transport)
        
        # Connexion aller
        connexion1 = Connexion(lieu1, lieu2, transport, distance_km)
        lieu1.ajouter_connexion(connexion1)
        
        # Connexion retour
        connexion2 = Connexion(lieu2, lieu1, transport, distance_km)
        lieu2.ajouter_connexion(connexion2)
        
        # Notifier les stats (une seule fois pour les deux sens)
        self._stats.notifier_connexion_ajoutee(type_transport, distance_km)
    
    def get_lieu(self, nom: str) -> Optional[LieuHackathon]:
        """Retourne un lieu par son nom"""
        return self._lieux.get(nom)
    
    def get_tous_lieux(self) -> List[LieuHackathon]:
        """Retourne tous les lieux"""
        return list(self._lieux.values())
    
    def rechercher_lieux(self, terme: str) -> List[LieuHackathon]:
        """Recherche des lieux par nom ou ville"""
        terme = terme.lower()
        resultats = []
        
        for lieu in self._lieux.values():
            if terme in lieu.nom.lower() or terme in lieu.ville.lower():
                resultats.append(lieu)
        
        return resultats
    
    def calculer_itineraire(self, depart_nom: str, arrivee_nom: str,
                           intermediaire_nom: Optional[str] = None) -> ResultatItineraire:
        """Calcule l'itinéraire entre deux lieux"""
        depart = self.get_lieu(depart_nom)
        arrivee = self.get_lieu(arrivee_nom)
        
        if not depart:
            print(f"⚠️  ERREUR : Le lieu '{depart_nom}' n'existe pas dans le réseau")
            return ResultatItineraire([], [], float('inf'), 0, False)
        
        if not arrivee:
            print(f"⚠️  ERREUR : Le lieu '{arrivee_nom}' n'existe pas dans le réseau")
            return ResultatItineraire([], [], float('inf'), 0, False)
        
        if depart == arrivee:
            print(f"⚠️  ERREUR : Le départ et l'arrivée sont identiques")
            return ResultatItineraire([], [], float('inf'), 0, False)
        
        intermediaire = None
        if intermediaire_nom:
            intermediaire = self.get_lieu(intermediaire_nom)
            if not intermediaire:
                print(f"⚠️  ERREUR : Le point intermédiaire '{intermediaire_nom}' n'existe pas")
                return ResultatItineraire([], [], float('inf'), 0, False)
        
        return self._algorithme.calculer_itineraire(self, depart, arrivee, intermediaire)
    
    def get_statistiques(self) -> StatistiquesReseau:
        """Retourne l'objet statistiques"""
        return self._stats
    
    def generer_carte_interactive(self, itineraire: Optional[ResultatItineraire] = None):
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
            couleur = couleurs_types.get(lieu.categorie, "gray")
            
            # Étoile pour les lieux de l'itinéraire
            if lieu in lieux_itineraire:
                icon = folium.Icon(color=couleur, icon="star")            
            else:
                icon = folium.Icon(color=couleur, icon="info-sign")
            
            # POPUP AMÉLIORÉ : Texte popup détaillé avec ville, type et coordonnées
            popup_text = f"""
            <div style='font-family: Arial; font-size: 14px;'>
            <h4 style='color:{couleur};'><b>{lieu.nom}</b></h4>
            <hr style='margin: 5px 0;'>
            <p><b>📍 Ville:</b> {lieu.ville}</p>
            <p><b>🏷️ Type:</b> {lieu.categorie.value}</p>
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
            for i, connexion in enumerate(itineraire.connexions):
                couleur_ligne = connexion.transport.get_couleur_carte()
                
                folium.PolyLine(
                    locations=[
                        [connexion.origine.position.latitude, connexion.origine.position.longitude],
                        [connexion.destination.position.latitude, connexion.destination.position.longitude]
                    ],
                    color=couleur_ligne,
                    weight=4,
                    opacity=0.7,
                    popup=(
                        f"<b>Étape {i+1}</b><br>"
                        f"{connexion.origine.nom} → {connexion.destination.nom}<br>"
                        f"🚦 {connexion.transport.get_nom().upper()}<br>"
                        f"📏 {connexion.distance_km:.0f} km<br>"
                        f"⏱️ {connexion.calculer_temps_trajet()*60:.0f} min"
                    )
                ).add_to(carte)
            
            # NOUVEAU : Panneau de détails de l'itinéraire
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
                    details_html += f'<p style="margin:8px 0;"><b>📍 Étape {i}</b><br>{lieu.nom}</p>'
                
                # Ajouter les détails de la connexion si elle existe
                if i < len(itineraire.connexions):
                    conn = itineraire.connexions[i]
                    transport_emoji = "🚄" if conn.transport.get_nom() == "train" else "🚗"
                    
                    details_html += f'''
                    <div style="background-color:#f8f9fa; padding:8px; margin:5px 0; border-radius:4px; border-left: 4px solid {conn.transport.get_couleur_carte()};">
                        <p style="margin:2px 0;"><b>{transport_emoji} {conn.transport.get_nom().upper()}</b></p>
                        <p style="margin:2px 0; font-size:12px;">📏 {conn.distance_km:.0f} km</p>
                        <p style="margin:2px 0; font-size:12px;">⏱️ {conn.calculer_temps_trajet()*60:.0f} min</p>
                        <p style="margin:2px 0; font-size:12px;">🏃 {conn.transport.get_vitesse():.0f} km/h</p>
                    </div>
                    '''
            
            # Résumé total
            details_html += f'''
            <hr style="margin:10px 0;">
            <div style="background-color:#e8f4fd; padding:10px; border-radius:4px;">
                <p style="margin:4px 0;"><b>📊 RÉSUMÉ</b></p>
                <p style="margin:4px 0; font-size:13px;">📏 Distance totale: {itineraire.distance_totale_km:.0f} km</p>
                <p style="margin:4px 0; font-size:13px;">⏱️ Temps total: {itineraire.temps_total_heures:.1f}h ({itineraire.temps_total_heures*60:.0f} min)</p>
                <p style="margin:4px 0; font-size:13px;">📍 Nombre d'étapes: {itineraire.nombre_etapes}</p>
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


# ============================================================================
# FACTORY : Construction du réseau
# ============================================================================

class ReseauHackathonBuilder:
    """Builder pour construire le réseau complet"""
    
    @staticmethod
    def construire_reseau_france() -> ReseauHackathon:
        """Construit le réseau de hackathon en France"""
        reseau = ReseauHackathon()
        
        # Créer les 20 lieux
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
        
        for nom, ville, lat, lon, categorie in lieux_data:
            lieu = LieuHackathon(nom, ville, Position(lat, lon), categorie)
            reseau.ajouter_lieu(lieu)
        
        # Connexions TRAIN
        connexions_train = [
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
        
        for lieu1, lieu2, distance in connexions_train:
            reseau.ajouter_connexion_bidirectionnelle(lieu1, lieu2, "train", distance)
        
        # Connexions VOITURE
        connexions_voiture = [
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
        
        for lieu1, lieu2, distance in connexions_voiture:
            reseau.ajouter_connexion_bidirectionnelle(lieu1, lieu2, "voiture", distance)
        
        return reseau


# ============================================================================
# INTERFACE UTILISATEUR
# ============================================================================

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*70)
    print("    🚀 GUIDE DE SURVIE HACKATHON - POO AVANCÉE 🚀")
    print("="*70)
    print("\n📋 OPTIONS:\n")
    print("  1. 📍 Voir tous les lieux")
    print("  2. 🔍 Rechercher un lieu")
    print("  3. 🛣️  Calculer un itinéraire")
    print("  4. 🎯 Calculer avec point intermédiaire")
    print("  5. 📊 Statistiques du réseau")
    print("  6. 🗺️  Générer une carte")
    print("  0. ❌ Quitter")
    print("\n" + "="*70)


def main():
    """Fonction principale"""
    print("\n⚙️  Construction du réseau de hackathon...")
    reseau = ReseauHackathonBuilder.construire_reseau_france()
    print(f"✅ Réseau construit : {len(reseau.get_tous_lieux())} lieux")
    
    while True:
        afficher_menu()
        choix = input("\n📝 Votre choix: ").strip()
        
        if choix == "1":
            print("\n" + "="*70)
            print("📍 LISTE DES LIEUX")
            print("="*70)
            for i, lieu in enumerate(sorted(reseau.get_tous_lieux(), key=lambda l: l.nom), 1):
                print(f"{i:2}. {lieu.nom:30} | {lieu.ville:15} | {lieu.categorie.value}")
            input("\n⏎ Entrée pour continuer...")
        
        elif choix == "2":
            terme = input("\n🔍 Terme de recherche: ").strip()
            resultats = reseau.rechercher_lieux(terme)
            print(f"\n✅ {len(resultats)} résultat(s):")
            for lieu in resultats:
                print(f"  • {lieu}")
            input("\n⏎ Entrée pour continuer...")
        
        elif choix == "3":
            print("\n" + "="*70)
            print("🛣️  CALCUL D'ITINÉRAIRE")
            print("="*70)
            depart = input("🚩 Départ: ").strip()
            arrivee = input("🏁 Arrivée: ").strip()
            
            result = reseau.calculer_itineraire(depart, arrivee)
            
            if result.trouve:
                print(f"\n✅ {result.get_resume()}")
                print("\n" + "="*70)
                print("🗺️  ITINÉRAIRE DÉTAILLÉ:")
                print("="*70)
                
                for i, lieu in enumerate(result.lieux):
                    # Marqueur selon la position
                    if i == 0:
                        marqueur = "🚩 DÉPART"
                    elif i == len(result.lieux) - 1:
                        marqueur = "🏁 ARRIVÉE"
                    else:
                        marqueur = "📍 Étape"
                    
                    print(f"\n{marqueur} {i+1}: {lieu.nom}")
                    
                    # Afficher la connexion vers le prochain lieu
                    if i < len(result.connexions):
                        conn = result.connexions[i]
                        temps_trajet = conn.calculer_temps_trajet()
                        
                        # Emoji selon le transport
                        if conn.transport.get_nom() == "train":
                            emoji = "🚄"
                            transport_nom = "TRAIN TGV"
                        else:
                            emoji = "🚗"
                            transport_nom = "VOITURE"
                        
                        print(f"   │")
                        print(f"   ├─ {emoji} {transport_nom}")
                        print(f"   ├─ 📏 Distance: {conn.distance_km:.0f} km")
                        print(f"   ├─ ⏱️  Temps: {temps_trajet*60:.0f} min ({temps_trajet:.2f}h)")
                        print(f"   ├─ 🏃 Vitesse: {conn.transport.get_vitesse():.0f} km/h")
                        print(f"   ↓")
                
                # Proposer de générer la carte
                print("\n" + "="*70)
                generer = input("🗺️  Voulez-vous générer la carte de cet itinéraire ? (o/n): ").strip().lower()
                
                if generer == 'o':
                    print("\n⚙️  Génération de la carte avec itinéraire...")
                    carte = reseau.generer_carte_interactive(result)
                    filename = f'itineraire_{depart.replace(" ", "_")}_to_{arrivee.replace(" ", "_")}.html'
                    carte.save(filename)
                    print(f"✅ Carte sauvegardée: {filename}")
                    
                    ouvrir = input("🌐 Voulez-vous ouvrir la carte dans votre navigateur ? (o/n): ").strip().lower()
                    if ouvrir == 'o':
                        webbrowser.open(filename)
            else:
                print("\n❌ Aucun itinéraire trouvé")
            
            input("\n⏎ Entrée pour continuer...")
        
        elif choix == "4":
            print("\n" + "="*70)
            print("🎯 ITINÉRAIRE AVEC POINT INTERMÉDIAIRE")
            print("="*70)
            depart = input("🚩 Départ: ").strip()
            inter = input("🎯 Intermédiaire: ").strip()
            arrivee = input("🏁 Arrivée: ").strip()
            
            result = reseau.calculer_itineraire(depart, arrivee, inter)
            
            if result.trouve:
                print(f"\n✅ {result.get_resume()}")
                print("\n" + "="*70)
                print("🗺️  ITINÉRAIRE DÉTAILLÉ (avec point intermédiaire):")
                print("="*70)
                
                for i, lieu in enumerate(result.lieux):
                    # Marqueur selon la position et le type
                    if i == 0:
                        marqueur = "🚩 DÉPART"
                    elif i == len(result.lieux) - 1:
                        marqueur = "🏁 ARRIVÉE"
                    elif lieu.nom == inter:
                        marqueur = "🎯 POINT INTERMÉDIAIRE"
                    else:
                        marqueur = "📍 Étape"
                    
                    print(f"\n{marqueur} {i+1}: {lieu.nom}")
                    
                    # Afficher la connexion vers le prochain lieu
                    if i < len(result.connexions):
                        conn = result.connexions[i]
                        temps_trajet = conn.calculer_temps_trajet()
                        
                        # Emoji selon le transport
                        if conn.transport.get_nom() == "train":
                            emoji = "🚄"
                            transport_nom = "TRAIN TGV"
                        else:
                            emoji = "🚗"
                            transport_nom = "VOITURE"
                        
                        print(f"   │")
                        print(f"   ├─ {emoji} {transport_nom}")
                        print(f"   ├─ 📏 Distance: {conn.distance_km:.0f} km")
                        print(f"   ├─ ⏱️  Temps: {temps_trajet*60:.0f} min ({temps_trajet:.2f}h)")
                        print(f"   ├─ 🏃 Vitesse: {conn.transport.get_vitesse():.0f} km/h")
                        print(f"   ↓")
                
                # Proposer de générer la carte
                print("\n" + "="*70)
                generer = input("🗺️  Voulez-vous générer la carte de cet itinéraire ? (o/n): ").strip().lower()
                
                if generer == 'o':
                    print("\n⚙️  Génération de la carte avec itinéraire...")
                    carte = reseau.generer_carte_interactive(result)
                    filename = f'itineraire_avec_intermediaire_{datetime.now().strftime("%H%M%S")}.html'
                    carte.save(filename)
                    print(f"✅ Carte sauvegardée: {filename}")
                    
                    ouvrir = input("🌐 Voulez-vous ouvrir la carte dans votre navigateur ? (o/n): ").strip().lower()
                    if ouvrir == 'o':
                        webbrowser.open(filename)
            else:
                print("\n❌ Aucun itinéraire trouvé")
            
            input("\n⏎ Entrée pour continuer...")
        
        elif choix == "5":
            print(reseau.get_statistiques().get_rapport())
            input("\n⏎ Entrée pour continuer...")
        
        elif choix == "6":
            print("\n⚙️  Génération de la carte...")
            carte = reseau.generer_carte_interactive()
            filename = f'carte_hackathon_poo_{datetime.now().strftime("%H%M%S")}.html'
            carte.save(filename)
            print(f"✅ Carte sauvegardée: {filename}")
            
            ouvrir = input("🌐 Ouvrir dans le navigateur ? (o/n): ").strip().lower()
            if ouvrir == 'o':
                webbrowser.open(filename)
        
        elif choix == "0":
            print("\n👋 Au revoir et bonne chance pour le hackathon!")
            break
        
        else:
            print("\n❌ Choix invalide")


if __name__ == "__main__":
    main()
