# PST_Telescope

Système d’Aide à la Visée pour Télescope (Push-To)
Ce projet a été réalisé dans le cadre d’un PST. Il s'agit d’un système embarqué qui transforme un télescope manuel (type Dobson) en un dispositif interactif capable d’aider l’utilisateur à pointer précisément des objets célestes, sans motorisation. Le concept repose sur la méthode du Push-To : l’utilisateur bouge le télescope manuellement, guidé par un affichage directionnel et des calculs de position céleste en temps réel.

Objectif
Le but est de permettre à un observateur, débutant ou expérimenté, de localiser facilement des étoiles, planètes, galaxies ou nébuleuses visibles depuis sa position, à tout moment. Le système affiche en temps réel les corrections à apporter à l’orientation du télescope pour viser l’objet sélectionné.

Composants matériels
- Raspberry Pi : ordinateur principal
- Écran OLED : affichage des menus, coordonnées et flèches directionnelles
- Module GPS : localisation et synchronisation temporelle précises
- Encodeurs rotatifs : mesure des mouvements du télescope (azimut / altitude)
- Bouton poussoir : navigation dans l'interface
- Courroies / engrenages : transmission du mouvement
- Supports 3D imprimés : fixation des composants sur le télescope
- Télescope Dobson : base de l'ensemble


Fonctionnement global
Le programme fonctionne en multi-threading, avec des tâches parallèles pour :
la récupération des données GPS, la lecture des encodeurs, l'affichage, la navigation bouton, le calcul directionnel.



Étape 1 : Initialisation
Le GPS établit la position (latitude, longitude, altitude).

L'utilisateur calibre le système en visant l'étoile Polaris.

Le système ajuste l’orientation absolue du télescope.


Étape 2 : Navigation dans l’interface
Un unique bouton permet de tout gérer :
Appui court : naviguer dans les menus
Appui long : valider une option
Double clic : revenir en arrière

Menus :
Liste d’objets (étoiles, planètes, lune, ciel profond)
Recommandations selon le niveau (débutant, intermédiaire, expert)
Informations système (GPS, angles encodeurs)


Étape 3 : Pointage
Une fois un objet sélectionné :
Le système calcule ses coordonnées azimut/altitude en temps réel à l’aide de la bibliothèque ephem.
Il compare avec la position actuelle du télescope (via les encodeurs).
Il affiche sur l’écran des flèches de correction directionnelle.
Un message “OK” s’affiche quand la cible est atteinte avec une précision inférieure à 1°.
Deux modes sont disponibles :

- Mode Pointage : mise à jour des coordonnées toutes les 30 secondes

- Mode Suivi (Tracking) : mise à jour toutes les 10 secondes, pour compenser la rotation terrestre


Fonctions logicielles principales
Le projet est structuré autour de fonctions critiques :

- setup_encoders() : configuration des GPIO et des encodeurs
- calibrate_on_polaris() : synchronisation initiale sur l’étoile polaire
- update_gps_data() : gestion continue des données GPS
- angle_from_counter() : conversion des compteurs d’impulsions en angles réels
- calculate_direction() : calcul de la direction à suivre (haut/bas/gauche/droite)
- check_button() : gestion des appuis court/long/double-clics
- display_gps_wait() : affichage en attente de signal GPS
- update_visible_recommendations() : tri intelligent des objets visibles selon niveau
- get_object_coordinates() : calcul des coordonnées cibles


Le programme gère aussi : 
- des calibrations fines (horizon/zénith pour l’altitude
- double point pour l’azimut)
- la compensation du jeu mécanique
- la gestion des erreurs GPS ou matérielles


Base de données céleste
Le fichier celestial_database_extended.py contient une base de données enrichie d’objets célestes :

- Étoiles brillantes : Polaris, Sirius, Vega, Betelgeuse, etc.
- Objets du ciel profond (Messier, NGC...) : M31, M42, M45, M13...
- Recommandations par niveau (débutant, intermédiaire, expert) avec filtrage en temps réel selon la visibilité
- Chaque objet est décrit par son nom, type, coordonnées (RA, Dec), magnitude.



ATTENTION 
Pour pouvoir faire tout fonctionné correctement, il faut utiliser un environnement virtuel.
Exemple de script à utiliser : 

#!/bin/bash
# Script simple pour lancer fullv2.py au démarrage du Raspberry Pi
#script de lancement
cd /home/pi
source oled-env/bin/activate
python fullv2.py

Quelque chose comme ca mais le faire automatiquement avec eventuellement un script .sh qui le ferait tout seul.
