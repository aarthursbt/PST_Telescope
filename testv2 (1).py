#!/usr/bin/python3
# coding: utf-8

import os
import time
import signal
import board
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import gpsd
from threading import Thread
import ephem  
import math
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

# === Configuration OLED ===
WIDTH = 128
HEIGHT = 64
ADDRESS = 0x3C
i2c = board.I2C()
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=ADDRESS)

# === Variables globales ===
gps_latitude = "N/A"
gps_longitude = "N/A"
gps_altitude = 0.0  # Variable altitude GPS
gps_time = None     # Variable temps GPS
current_alt = 0.0
current_az = 0.0
target_alt = 0.0
target_az = 0.0
stop_threads = False
button_pressed = False
last_update_time = 0  # Variable globale et persistante
last_az = 0.0  # Pour suivre les changements d'encodeur
last_alt = 0.0  # Pour suivre les changements d'encodeur
DEBUG_MODE = True  # Activer les logs de débogage

# === États du système ===
MODE_GPS_WAIT = -1    # Attente fix GPS au démarrage
MODE_INSTRUCTION = 0  # Message initial
MODE_CALIBRATION = 1  # Calibration sur Polaris
MODE_MAIN_MENU = 2    # Menu principal (3 options)
MODE_CATEGORY = 3     # Sélection catégorie d'objets
MODE_SELECTION = 4    # Menu sélection d'objets
MODE_POINTING = 5     # Guidage vers objet sélectionné
MODE_SKY_MAP = 6      # Mode carte du ciel
MODE_TRACKING = 7     # Mode suivi avec chronomètre
MODE_LEVEL_SELECTION = 8  # Nouveau mode: sélection niveau difficulté
MODE_RECOMMENDATIONS = 9  # Mode recommandations par niveau
MODE_SYSTEM_INFO = 10  # Mode informations système

# Modes d'affichage de guidage
GUIDANCE_MODE_ARROWS_8WAY = 0   # Flèches 8 directions (défaut)
GUIDANCE_MODE_COMPASS = 1       # Système de boussole
GUIDANCE_MODE_RADAR = 2         # Système radar
current_guidance_mode = GUIDANCE_MODE_ARROWS_8WAY

current_mode = MODE_GPS_WAIT

# Options du menu principal
main_menu_options = ["Object List", "Recommendations", "System Info"]
selected_main_menu_index = 0

# Variables pour suivre la qualité GPS
gps_satellites = 0  # Nombre de satellites
gps_quality = 0     # Indicateur de qualité

selected_category_index = 0
selected_object_index = 0
button_press_time = 0
long_press_threshold = 1.5  # Temps en secondes pour appui long

# === Nouvelle structure pour les recommandations ===
niveaux_observation = ["Beginner", "Intermediate", "Expert"]  # Sous-catégories
selected_level_index = 0
visible_now = True  # Par défaut, montrer seulement les objets visibles

# Classification des objets célestes par niveau de difficulté
objets_par_niveau = {
    "Beginner": [
        {"nom": "Moon", "categorie": "Moon", "index": 0},  # Format: nom, catégorie parent, index dans catégorie
        {"nom": "Jupiter", "categorie": "Planets", "index": 3},
        {"nom": "Saturn", "categorie": "Planets", "index": 4},
        {"nom": "Mars", "categorie": "Planets", "index": 2},
        {"nom": "Venus", "categorie": "Planets", "index": 1},
        {"nom": "Betelgeuse", "categorie": "Stars", "index": 3},
        {"nom": "Sirius", "categorie": "Stars", "index": 1},
        {"nom": "M45 (Pleiades)", "categorie": "Deep Sky", "index": 2}
    ],
    
    "Intermediate": [
        {"nom": "Uranus", "categorie": "Planets", "index": 5},
        {"nom": "Neptune", "categorie": "Planets", "index": 6},
        {"nom": "M31 (Andromeda)", "categorie": "Deep Sky", "index": 0},
        {"nom": "M42 (Orion)", "categorie": "Deep Sky", "index": 1},
        {"nom": "Vega", "categorie": "Stars", "index": 2},
        {"nom": "Arcturus", "categorie": "Stars", "index": 5},
        {"nom": "Fomalhaut", "categorie": "Stars", "index": 13},
        {"nom": "M13", "categorie": "Deep Sky", "index": 3}
    ],
    
    "Expert": [
        {"nom": "M57 (Ring)", "categorie": "Deep Sky", "index": 5},
        {"nom": "M51 (Whirlpool)", "categorie": "Deep Sky", "index": 6},
        {"nom": "M101", "categorie": "Deep Sky", "index": 7},
        {"nom": "M81", "categorie": "Deep Sky", "index": 8},
        {"nom": "M82", "categorie": "Deep Sky", "index": 9},
        {"nom": "M8 (Lagoon)", "categorie": "Deep Sky", "index": 10},
        {"nom": "M20 (Trifid)", "categorie": "Deep Sky", "index": 11},
        {"nom": "Mercury", "categorie": "Planets", "index": 0}
    ]
}

recommended_objects = []  # Liste filtrée des objets recommandés actuellement visibles

# Catégories d'objets célestes
categories = ["Stars", "Planets", "Moon", "Deep Sky", "Sun"]

# Base de données enrichie d'objets célestes
celestial_database = {
    "Stars": [
        "Polaris", "Sirius", "Vega", "Betelgeuse", "Rigel", "Arcturus", 
        "Aldebaran", "Deneb", "Capella", "Antares", "Altair", "Spica",
        "Pollux", "Fomalhaut", "Regulus", "Castor", "Procyon"
    ],
    "Planets": [
        "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"
    ],
    "Moon": ["Moon"],
    "Sun": ["Sun"],
    "Deep Sky": [
        "M31 (Andromeda)", "M42 (Orion)", "M45 (Pleiades)", "M13", "M27", 
        "M57 (Ring)", "M51 (Whirlpool)", "M101", "M81", "M82", "M8 (Lagoon)",
        "M20 (Trifid)", "M16 (Eagle)", "M17 (Omega)"
    ]
}

categories = ["Stars", "Planets", "Moon", "Sun", "Deep Sky"]

# Dictionnaire pour stocker les données complètes d'objets
star_catalog = {
    "Polaris": "Polaris,f|M|A0,2:31:49.09,89:15:50.8,2.0",
    "Sirius": "Sirius,f|M|A0,6:45:08.92,-16:42:58.0,1.5",
    "Vega": "Vega,f|M|A0,18:36:56.34,38:47:01.3,0.0",
    "Betelgeuse": "Betelgeuse,f|M|A0,5:55:10.29,7:24:25.3,0.5",
    "Rigel": "Rigel,f|M|A0,5:14:32.3,-8:12:06,0.1",
    "Arcturus": "Arcturus,f|M|A0,14:15:39.67,19:10:56.7,0.0",
    "Aldebaran": "Aldebaran,f|M|A0,4:35:55.23,16:30:33.5,0.9",
    "Deneb": "Deneb,f|M|A0,20:41:25.91,45:16:49.2,1.3",
    "Capella": "Capella,f|M|A0,5:16:41.36,45:59:52.8,0.1",
    "Antares": "Antares,f|M|A0,16:29:24.46,-26:25:55.2,1.0",
    "Altair": "Altair,f|M|A0,19:50:47.00,8:52:06.0,0.8",
    "Spica": "Spica,f|M|A0,13:25:11.57,-11:09:40.8,1.0",
    "Pollux": "Pollux,f|M|A0,7:45:18.95,28:01:34.3,1.2",
    "Fomalhaut": "Fomalhaut,f|M|A0,22:57:39.05,-29:37:20.1,1.2",
    "Regulus": "Regulus,f|M|A0,10:08:22.31,11:58:02.0,1.4",
    "Castor": "Castor,f|M|A0,7:34:35.87,31:53:18.0,1.6",
    "Procyon": "Procyon,f|M|A0,7:39:18.12,5:13:30.0,0.4"
}

# Dictionnaire pour objets du ciel profond - format corrigé
dso_catalog = {
    "M31 (Andromeda)": "M31,f|G,0:42:44.3,+41:16:9,4.3",
    "M42 (Orion)": "M42,f|G,5:35:17.3,-5:23:28,4.0",
    "M45 (Pleiades)": "M45,f|G,3:47:0.0,+24:7:0,1.2",
    "M13": "M13,f|G,16:41:41.24,+36:27:35.5,5.9",
    "M27": "M27,f|G,19:59:36.3,+22:43:16,8.1",
    "M57 (Ring)": "M57,f|G,18:53:35.1,+33:1:45,9.0",
    "M51 (Whirlpool)": "M51,f|G,13:29:52.7,+47:11:43,8.4",
    "M101": "M101,f|G,14:3:12.6,+54:20:57,7.9",
    "M81": "M81,f|G,9:55:33.2,+69:3:55,6.9",
    "M82": "M82,f|G,9:55:52.2,+69:40:47,8.4",
    "M8 (Lagoon)": "M8,f|G,18:3:37.0,-24:23:12,6.0",
    "M20 (Trifid)": "M20,f|G,18:2:23.0,-23:1:48,6.3",
    "M16 (Eagle)": "M16,f|G,18:18:48.0,-13:47:0,6.0",
    "M17 (Omega)": "M17,f|G,18:20:26.0,-16:10:36,6.0"
}

# === Configuration encodeurs ===
az_encoder_pins = (22, 23) 
alt_encoder_pins = (17, 18)  
az_counter = 0
alt_counter = 0
az_last_state = None
alt_last_state = None

# Variables de calibration d'altitude
ALT_CALIB_HORIZON_COUNT = None  # Valeur encodeur à l'horizon (0°)
ALT_CALIB_ZENITH_COUNT = None   # Valeur encodeur au zénith (90°)
ALT_CALIBRATED = False          # Flag indiquant si calibré

# Variables de calibration azimut
AZ_CALIB_POINT1_COUNT = 0
AZ_CALIB_POINT1_VALUE = 0.0
AZ_CALIB_POINT2_COUNT = 0
AZ_CALIB_POINT2_VALUE = 0.0
AZ_CALIBRATED = False

IS_CALIBRATING = False  # Flag pour bloquer les autres affichages pendant la calibration
BACKLASH_COMPENSATION = 0.5  # Compensation de jeu mécanique en degrés

# Variables pour inverser les encodeurs si nécessaire
AZ_ENCODER_REVERSED = False  # Mettre à True si l'azimut va dans le mauvais sens
ALT_ENCODER_REVERSED = False # Mettre à True si l'altitude va dans le mauvais sens

# Résolution native des encodeurs
ENCODER_STEPS_PER_REVOLUTION = 2400  

# Rapports de transmission selon vos engrenages
AZIMUTH_GEAR_RATIO = 7.5    # Exactement 300/40 = 7.5
ALTITUDE_GEAR_RATIO = 8.0   # Exactement 320/40 = 8.0

last_az_counter = 0
last_alt_counter = 0

def setup_encoders():
    """Configuration des pins encodeurs"""
    global az_last_state, alt_last_state
    GPIO.setup(az_encoder_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(az_encoder_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(alt_encoder_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(alt_encoder_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Lire l'état initial
    az_last_state = (GPIO.input(az_encoder_pins[0]), GPIO.input(az_encoder_pins[1]))
    alt_last_state = (GPIO.input(alt_encoder_pins[0]), GPIO.input(alt_encoder_pins[1]))
    print("=== Configuration des encodeurs ===")
    print(f"Type: Encodeur incrémental 600 PPR")
    print(f"Résolution AZ: {360/(ENCODER_STEPS_PER_REVOLUTION*AZIMUTH_GEAR_RATIO):.4f}°/impulsion")
    print(f"Résolution ALT: {360/(ENCODER_STEPS_PER_REVOLUTION*ALTITUDE_GEAR_RATIO):.4f}°/impulsion")
    print(f"Tour complet AZ: {ENCODER_STEPS_PER_REVOLUTION*AZIMUTH_GEAR_RATIO:.0f} impulsions")
    print(f"Tour complet ALT: {ENCODER_STEPS_PER_REVOLUTION*ALTITUDE_GEAR_RATIO:.0f} impulsions")

def calibrate_azimuth_improved():
    """Calibration azimutale en deux points: Polaris et 180° opposé"""
    global az_counter, current_az, IS_CALIBRATING
    global AZ_CALIB_POINT1_COUNT, AZ_CALIB_POINT1_VALUE, AZ_CALIB_POINT2_COUNT, AZ_CALIB_POINT2_VALUE, AZ_CALIBRATED
    
    IS_CALIBRATING = True
    
    # ÉTAPE 1: Calibration sur Polaris
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    try:
        # Calculer position réelle de Polaris
        observer = create_observer()
        polaris = ephem.readdb(star_catalog["Polaris"])
        polaris.compute(observer)
        polaris_az = float(polaris.az) * 180 / math.pi
        polaris_alt = float(polaris.alt) * 180 / math.pi
        
        # Afficher instructions
        draw.text((0, 0), "AZIMUTH CALIBRATION", font=font, fill=255)
        draw.text((0, 15), "Point to POLARIS", font=font, fill=255)
        draw.text((0, 30), f"Az: {polaris_az:.1f}° Alt: {polaris_alt:.1f}°", font=font, fill=255)
        draw.text((0, 45), "Press button", font=font, fill=255)
        
        display.image(image)
        display.show()
        time.sleep(0.5)  # S'assurer de l'actualisation de l'affichage
        
        wait_for_button_press()
        
        # Enregistrer premier point
        AZ_CALIB_POINT1_COUNT = az_counter
        AZ_CALIB_POINT1_VALUE = polaris_az
        print(f"Polaris: {AZ_CALIB_POINT1_VALUE:.1f}° at count {AZ_CALIB_POINT1_COUNT}")
        
        # ÉTAPE 2: Tourner à l'opposé (180°)
        opposite_az = (polaris_az + 180) % 360
        
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvelle image
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "AZIMUTH CALIBRATION", font=font, fill=255)
        draw.text((0, 15), "Rotate telescope 180°", font=font, fill=255)
        draw.text((0, 30), f"Target: {opposite_az:.1f}°", font=font, fill=255)
        draw.text((0, 45), "Press when aligned", font=font, fill=255)
        
        display.image(image)
        display.show()
        time.sleep(0.5)  # S'assurer de l'actualisation de l'affichage
        
        wait_for_button_press()
        
        # Enregistrer deuxième point
        AZ_CALIB_POINT2_COUNT = az_counter
        AZ_CALIB_POINT2_VALUE = opposite_az
        
        # Vérifier que la rotation est suffisante
        encoder_diff = abs(AZ_CALIB_POINT2_COUNT - AZ_CALIB_POINT1_COUNT)
        expected_diff = ENCODER_STEPS_PER_REVOLUTION * AZIMUTH_GEAR_RATIO / 2  # Moitié d'un tour
        
        if encoder_diff < expected_diff * 0.4:  # Moins de 40% de la valeur attendue
            display.fill(0)
            image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvelle image
            draw = ImageDraw.Draw(image)
            draw.text((0, 20), "ROTATION TOO SMALL", font=font, fill=255)
            draw.text((0, 35), "Please rotate 180°", font=font, fill=255)
            display.image(image)
            display.show()
            time.sleep(2)
            AZ_CALIBRATED = False
            IS_CALIBRATING = False
            return False
            
        # Calibration réussie
        AZ_CALIBRATED = True
        
        # Message de confirmation
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvelle image
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "AZIMUTH CALIBRATED", font=font, fill=255)
        draw.text((0, 15), f"Polaris: {polaris_az:.1f}°", font=font, fill=255)
        draw.text((0, 30), f"Opposite: {opposite_az:.1f}°", font=font, fill=255)
        draw.text((0, 45), "Calibration complete!", font=font, fill=255)
        display.image(image)
        display.show()
        time.sleep(2)
        
    except Exception as e:
        print(f"Calibration error: {e}")
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvelle image
        draw = ImageDraw.Draw(image)
        draw.text((0, 20), "CALIBRATION ERROR", font=font, fill=255)
        draw.text((0, 35), str(e)[:20], font=font, fill=255)
        display.image(image)
        display.show()
        time.sleep(2)
        AZ_CALIBRATED = False
    
    IS_CALIBRATING = False
    return AZ_CALIBRATED

def calibrate_altitude():
    """Calibration à deux points pour l'altitude (horizon et zénith)"""
    global ALT_CALIB_HORIZON_COUNT, ALT_CALIB_ZENITH_COUNT, ALT_CALIBRATED
    global alt_counter, current_alt, IS_CALIBRATING
    
    IS_CALIBRATING = True

    # ÉTAPE 1: Calibration horizon (0°)
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    draw.text((0, 0), "ALTITUDE CALIBRATION", font=font, fill=255)
    draw.text((0, 15), "Point to HORIZON", font=font, fill=255)
    draw.text((0, 30), "Align at 0 degrees", font=font, fill=255)
    draw.text((0, 50), "Then press button", font=font, fill=255)
    
    display.image(image)
    display.show()
    
    # Attendre appui bouton
    wait_for_button_press()
    
    # Enregistrer valeur horizon
    ALT_CALIB_HORIZON_COUNT = alt_counter
    print(f"Horizon calibrated at {ALT_CALIB_HORIZON_COUNT} pulses")
    time.sleep(1)  # Debounce
    
    # ÉTAPE 2: Calibration zénith (90°)
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvel objet image
    draw = ImageDraw.Draw(image)
    
    draw.text((0, 0), "ALTITUDE CALIBRATION", font=font, fill=255)
    draw.text((0, 15), "Point to ZENITH", font=font, fill=255)
    draw.text((0, 30), "Vertical position (90°)", font=font, fill=255)
    draw.text((0, 50), "Then press button", font=font, fill=255)
    
    display.image(image)
    display.show()
    time.sleep(0.5)  # Courte pause pour s'assurer de la mise à jour de l'affichage
    
    # Attendre appui bouton - utiliser méthode améliorée
    print("Waiting for zenith button press...")
    wait_for_button_press()
    print("Button pressed for zenith!")
    
    # Enregistrer valeur zénith
    ALT_CALIB_ZENITH_COUNT = alt_counter
    print(f"Zenith calibrated at {ALT_CALIB_ZENITH_COUNT} pulses")
    
    # Vérifier valeurs valides
    if ALT_CALIB_ZENITH_COUNT == ALT_CALIB_HORIZON_COUNT:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvel objet image
        draw = ImageDraw.Draw(image)
        draw.text((0, 20), "CALIBRATION ERROR", font=font, fill=255)
        draw.text((0, 35), "Same values detected!", font=font, fill=255)
        display.image(image)
        display.show()
        time.sleep(2)
        ALT_CALIBRATED = False
        IS_CALIBRATING = False
        return False
    
    # Calibration réussie
    ALT_CALIBRATED = True
    
    # Afficher confirmation
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))  # Créer nouvel objet image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "CALIBRATION SUCCESS", font=font, fill=255)
    draw.text((0, 20), f"Horizon: {ALT_CALIB_HORIZON_COUNT}", font=font, fill=255)
    draw.text((0, 35), f"Zenith: {ALT_CALIB_ZENITH_COUNT}", font=font, fill=255)
    draw.text((0, 50), "Press to continue", font=font, fill=255)
    display.image(image)
    display.show()
    wait_for_button_press()  # Ajouter attente bouton ici
    
    IS_CALIBRATING = False
    return True

def wait_for_button_press():
    """Détection de bouton complètement corrigée"""
    print("Waiting for button press...")
    
    # D'abord s'assurer que le bouton n'est pas pressé - attendre s'il l'est
    while GPIO.input(button_pin) == GPIO.LOW:
        time.sleep(0.05)
        print(".", end="")
    
    # Puis attendre que le bouton soit pressé
    while GPIO.input(button_pin) == GPIO.HIGH:
        time.sleep(0.05)
    
    # Quand pressé, attendre un moment
    time.sleep(0.2)
    print("Button pressed!")
    
    # Attendre que le bouton soit relâché
    while GPIO.input(button_pin) == GPIO.LOW:
        time.sleep(0.05)
    
    # Debounce final
    time.sleep(0.3)
    print("Button released!")

def angle_from_counter(counter, is_altitude=False):
    """Convertit les compteurs en angles avec calibration et compensation du jeu mécanique"""
    if is_altitude:
        # Si calibré, utiliser la calibration à deux points avec compensation
        if ALT_CALIBRATED and ALT_CALIB_HORIZON_COUNT is not None and ALT_CALIB_ZENITH_COUNT is not None:
            # Détection de sens de rotation pour compensation du jeu mécanique
            global last_alt_counter
            direction = 0
            if counter > last_alt_counter:
                direction = 1  # Montée
            elif counter < last_alt_counter:
                direction = -1  # Descente
            last_alt_counter = counter
            
            # Protection contre division par zéro
            if ALT_CALIB_ZENITH_COUNT == ALT_CALIB_HORIZON_COUNT:
                return 45.0  # Valeur par défaut en cas d'erreur
            
            # Interpolation linéaire entre horizon (0°) et zénith (90°)
            range_counts = ALT_CALIB_ZENITH_COUNT - ALT_CALIB_HORIZON_COUNT
            
            # Formule: angle = 90 * (counter - horizon_count) / (zenith_count - horizon_count)
            raw_angle = 90.0 * (counter - ALT_CALIB_HORIZON_COUNT) / range_counts
            
            # Appliquer compensation de jeu mécanique
            if direction == -1:  # Si mouvement vers le bas
                adjusted_angle = raw_angle - BACKLASH_COMPENSATION
            else:
                adjusted_angle = raw_angle
            
            # Limiter entre 0° et 90°
            angle = max(0.0, min(90.0, adjusted_angle))
        else:
            # Méthode standard si pas calibré
            angle = counter * (360.0 / (ENCODER_STEPS_PER_REVOLUTION * ALTITUDE_GEAR_RATIO))
            angle = max(0.0, min(90.0, angle))
    else:
        # Pour l'azimut, pas de changement
        angle = counter * (360.0 / (ENCODER_STEPS_PER_REVOLUTION * AZIMUTH_GEAR_RATIO))
        angle = angle % 360.0
        
    return angle

# === Configuration GPIO bouton ===
button_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def create_observer():
    """Crée un objet observateur ephem avec la position actuelle"""
    observer = ephem.Observer()
    try:
        lat = float(gps_latitude)
        lon = float(gps_longitude)
        observer.lat = str(lat)
        observer.lon = str(lon)
        observer.elevation = gps_altitude
        
        if gps_time:
            observer.date = ephem.Date(gps_time)
        else:
            observer.date = ephem.now()
    except ValueError:
        observer.lat = '48.8566'  # Paris par défaut
        observer.lon = '2.3522'
        observer.elevation = 35
        observer.date = ephem.now()
    return observer

def is_object_visible(object_name, category):
    """Détermine si un objet est actuellement visible (altitude > 10°)"""
    try:
        observer = create_observer()  # Utilise fonction existante
        
        # Obtenir objet céleste
        celestial_object = None
        
        if category == "Planets":
            if object_name == "Mercury":
                celestial_object = ephem.Mercury()
            elif object_name == "Venus":
                celestial_object = ephem.Venus()
            elif object_name == "Mars":
                celestial_object = ephem.Mars()
            elif object_name == "Jupiter":
                celestial_object = ephem.Jupiter()
            elif object_name == "Saturn":
                celestial_object = ephem.Saturn()
            elif object_name == "Uranus":
                celestial_object = ephem.Uranus()
            elif object_name == "Neptune":
                celestial_object = ephem.Neptune()
        elif category == "Moon":
            celestial_object = ephem.Moon()
        elif category == "Sun":  # Ajouter ce bloc
            celestial_object = ephem.Sun()
        elif category == "Stars" and object_name in star_catalog:
            celestial_object = ephem.readdb(star_catalog[object_name])
        elif category == "Deep Sky" and object_name in dso_catalog:
            celestial_object = ephem.readdb(dso_catalog[object_name])
                
        if celestial_object:
            celestial_object.compute(observer)
            # Convertir de radians en degrés
            alt = float(celestial_object.alt) * 180 / math.pi
            
            # Considérer visible si au moins 10 degrés au-dessus de l'horizon
            return alt > 10
        return False
    except:
        # En cas d'erreur, considérer l'objet visible pour éviter blocage
        return True

def update_visible_recommendations():
    """Met à jour la liste des objets recommandés visibles"""
    global recommended_objects, selected_level_index, visible_now
    
    level = niveaux_observation[selected_level_index]
    all_objects = objets_par_niveau[level]
    
    if visible_now:
        # Filtrer pour ne garder que les objets actuellement visibles
        recommended_objects = [
            obj for obj in all_objects 
            if is_object_visible(obj["nom"], obj["categorie"])
        ]
        
        # Si aucun objet visible, prendre tous les objets sans filtrage
        if not recommended_objects:
            recommended_objects = all_objects
            print(f"No {level} objects currently visible, showing all objects")
    else:
        # Montrer tous les objets sans filtrage
        recommended_objects = all_objects

def check_button():
    """Gestion des appuis bouton avec détection appui court/long et double-clic"""
    global button_pressed, button_press_time, current_mode
    global selected_category_index, selected_object_index, last_update_time
    global selected_level_index, visible_now, recommended_objects, selected_main_menu_index
    global IS_CALIBRATING
    
    # Variables pour gérer le double-clic
    last_press_time = 0
    double_click_threshold = 0.5  # Temps max entre deux clics pour un double-clic (500ms)
    
    while not stop_threads:
        if GPIO.input(button_pin) == GPIO.LOW:  # Bouton pressé
            if button_press_time == 0:  # Début d'appui
                button_press_time = time.time()
            elif time.time() - button_press_time > long_press_threshold:
                # Appui long détecté
                if current_mode == MODE_GPS_WAIT:
                    # Appui long: continuer même sans GPS complet
                    current_mode = MODE_INSTRUCTION
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_MAIN_MENU:
                    # Sélectionner option menu principal
                    if selected_main_menu_index == 0:  # Object List
                        current_mode = MODE_CATEGORY
                        selected_category_index = 0
                    elif selected_main_menu_index == 1:  # Recommendations
                        current_mode = MODE_LEVEL_SELECTION  # Aller d'abord à sélection niveau
                        selected_level_index = 0
                    elif selected_main_menu_index == 2:  # System Info
                        current_mode = MODE_SYSTEM_INFO
                    
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_POINTING:
                    # Changer mode de guidage sur appui long
                    toggle_guidance_mode()
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_LEVEL_SELECTION:
                    # Sélectionner niveau et aller à liste objets recommandés
                    current_mode = MODE_RECOMMENDATIONS
                    update_visible_recommendations()
                    selected_object_index = 0
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_CATEGORY:
                    # Sélectionner catégorie et aller à sélection objet
                    current_mode = MODE_SELECTION
                    selected_object_index = 0
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_SELECTION:
                    # Sélectionner objet et aller au mode pointage
                    current_mode = MODE_POINTING
                    category = categories[selected_category_index]
                    object_name = celestial_database[category][selected_object_index]
                    get_object_coordinates(object_name, category)
                    last_update_time = time.time()  # Initialiser temps de mise à jour
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_INSTRUCTION:
                    # Aller au mode calibration
                    current_mode = MODE_CALIBRATION
                    button_press_time = 0
                    time.sleep(0.1)
                elif current_mode == MODE_CALIBRATION:
                    # Démarrer le processus de calibration lorsque le bouton est pressé
                    if not IS_CALIBRATING:
                        IS_CALIBRATING = True
                        print("Starting calibration process...")
                        calibrate_on_polaris()  # Cette fonction gère tout le processus
                        IS_CALIBRATING = False
                        current_mode = MODE_MAIN_MENU
                        button_press_time = 0
                        button_pressed = True
                        time.sleep(0.5)
                elif current_mode == MODE_SKY_MAP:
                    # Aller directement au mode suivi
                    current_mode = MODE_TRACKING
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_TRACKING:
                    # Retourner à sélection objet sur appui long
                    current_mode = MODE_SELECTION
                    button_press_time = 0
                    button_pressed = True
                    time.sleep(0.5)
                elif current_mode == MODE_RECOMMENDATIONS:
                    if len(recommended_objects) > 0:
                        # Sélectionner objet et aller au mode pointage
                        obj = recommended_objects[selected_object_index]
                        # Synchroniser avec catégories principales
                        selected_category_index = categories.index(obj["categorie"])
                        selected_object_index = obj["index"]
                        
                        # Aller au mode pointage
                        current_mode = MODE_POINTING
                        object_name = celestial_database[obj["categorie"]][obj["index"]]
                        get_object_coordinates(object_name, obj["categorie"])
                        last_update_time = time.time()
                        button_press_time = 0
                        button_pressed = True
                        time.sleep(0.5)
                    else:
                        print("No recommended objects available")
                        button_press_time = 0
                        time.sleep(0.5)
        else:
            # Bouton relâché
            if button_press_time > 0:
                press_duration = time.time() - button_press_time
                current_time = time.time()
                button_press_time = 0
                
                # Si c'était un appui court
                if press_duration < long_press_threshold:
                    # Vérifier si c'est un double-clic
                    if current_time - last_press_time < double_click_threshold:
                        if current_mode == MODE_SELECTION:
                            # Double-clic en mode sélection: retourner au mode catégorie
                            print("Double-click detected: return to categories menu")
                            current_mode = MODE_CATEGORY
                            button_pressed = True
                            last_press_time = 0  # Reset pour éviter triple clics
                        elif current_mode == MODE_POINTING:
                            # Double-clic en mode pointage: retourner au mode sélection
                            print("Double-click detected: return to selection menu")
                            current_mode = MODE_SELECTION
                            button_pressed = True
                            last_press_time = 0
                        elif current_mode == MODE_RECOMMENDATIONS:
                            # Double-clic en mode recommandations: retourner à sélection niveau
                            current_mode = MODE_LEVEL_SELECTION
                            button_pressed = True
                            last_press_time = 0
                        elif current_mode == MODE_LEVEL_SELECTION:
                            # Double-clic en mode niveau: retourner au menu principal
                            current_mode = MODE_MAIN_MENU
                            button_pressed = True
                            last_press_time = 0
                        elif current_mode == MODE_CATEGORY:
                            # Double-clic en mode catégorie: retourner au menu principal
                            current_mode = MODE_MAIN_MENU
                            button_pressed = True
                            last_press_time = 0
                        elif current_mode == MODE_SYSTEM_INFO:
                            # Double-clic en mode système: retourner au menu principal
                            current_mode = MODE_MAIN_MENU
                            button_pressed = True
                            last_press_time = 0
                    else:
                        last_press_time = current_time  # Se souvenir du temps de clic
                        
                        if current_mode == MODE_GPS_WAIT:
                            # Appui court: ignorer GPS et continuer
                            current_mode = MODE_INSTRUCTION
                            button_pressed = True
                        elif current_mode == MODE_MAIN_MENU:
                            # Naviguer menu principal
                            selected_main_menu_index = (selected_main_menu_index + 1) % len(main_menu_options)
                            button_pressed = True
                        elif current_mode == MODE_CATEGORY:
                            # Naviguer catégories
                            selected_category_index = (selected_category_index + 1) % len(categories)
                            button_pressed = True
                        elif current_mode == MODE_SELECTION:
                            # Naviguer objets dans catégorie sélectionnée
                            category = categories[selected_category_index]
                            selected_object_index = (selected_object_index + 1) % len(celestial_database[category])
                            button_pressed = True
                        elif current_mode == MODE_POINTING:
                            # Aller directement au mode suivi astrophoto
                            current_mode = MODE_TRACKING
                            button_pressed = True
                        elif current_mode == MODE_SKY_MAP or current_mode == MODE_TRACKING:
                            # Retourner au mode pointage sur appui court
                            current_mode = MODE_POINTING
                            button_pressed = True
                        elif current_mode == MODE_LEVEL_SELECTION:
                            # Naviguer entre niveaux de difficulté
                            selected_level_index = (selected_level_index + 1) % len(niveaux_observation)
                            button_pressed = True
                        elif current_mode == MODE_RECOMMENDATIONS:
                            # Naviguer entre objets recommandés de niveau sélectionné
                            if len(recommended_objects) > 0:
                                selected_object_index = (selected_object_index + 1) % len(recommended_objects)
                            button_pressed = True
        
        time.sleep(0.1)

def set_target(alt, az):
    """Définir coordonnées cibles pour le pointage"""
    global target_alt, target_az
    target_alt = alt
    target_az = az
    print(f"Target set: Alt={alt:.1f}^, Az={az:.1f}^")

def display_gps_wait():
    """Afficher écran d'attente GPS avec indicateur de qualité"""
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    draw.text((0, 0), "GPS WAITING...", font=font, fill=255)
    
    # Afficher statut GPS
    if gps_latitude == "NO FIX":
        draw.text((0, 15), "Searching satellites", font=font, fill=255)
        # Points animés
        dots = "." * (int(time.time() * 2) % 4)
        draw.text((0, 25), f"Please wait{dots}", font=font, fill=255)
    elif gps_latitude == "ERR":
        draw.text((0, 15), "GPS Error!", font=font, fill=255)
    else:
        draw.text((0, 15), f"Position: {gps_latitude[:7]}", font=font, fill=255)
        draw.text((0, 25), f"Satellites: {gps_satellites}", font=font, fill=255)
        if gps_quality >= 2:  # Bonne qualité GPS
            draw.text((0, 35), "GPS Signal OK", font=font, fill=255)
        else:
            draw.text((0, 35), "Weak signal...", font=font, fill=255)
    
    display.image(image)
    display.show()

def update_gps_data():
    """Mettre à jour les données GPS en continu"""
    global gps_latitude, gps_longitude, gps_altitude, gps_time
    global gps_satellites, gps_quality  # Nouvelles variables
    
    try:
        gpsd.connect()
        while not stop_threads:
            try:
                packet = gpsd.get_current()
                if packet.mode >= 2:
                    # S'assurer que les coordonnées sont toujours des chaînes
                    try:
                        gps_latitude = f"{float(packet.lat):.6f}"
                        gps_longitude = f"{float(packet.lon):.6f}"
                    except (TypeError, ValueError):
                        gps_latitude = "ERR"
                        gps_longitude = "ERR"
                        print(f"GPS format error: lat={packet.lat}, lon={packet.lon}")
                    
                    # Obtenir informations satellites
                    if hasattr(packet, 'sats'):
                        try:
                            # Vérifier si sats est un entier ou une liste
                            if isinstance(packet.sats, int):
                                gps_satellites = packet.sats  # Nombre direct
                            elif hasattr(packet.sats, '__len__'):
                                gps_satellites = len(packet.sats)  # Collection (liste, tuple)
                            else:
                                # Convertir en chaîne et compter virgules+1 comme estimation
                                sats_str = str(packet.sats)
                                if ',' in sats_str:
                                    gps_satellites = sats_str.count(',') + 1
                                else:
                                    gps_satellites = 1  # Au moins 1 si quelque chose est présent
                        except Exception as e:
                            gps_satellites = 0
                            print(f"Error counting satellites: {e}")
                    else:
                        gps_satellites = 0
                        
                    # Évaluer qualité de fix (1=basique, 2=bon)
                    gps_quality = packet.mode
                    
                    # Obtenir altitude si disponible (mode 3D)
                    if packet.mode >= 3:
                        try:
                            gps_altitude = float(packet.alt)
                        except (TypeError, ValueError):
                            gps_altitude = 0.0
                    else:
                        gps_altitude = 0.0
                    
                    # Obtenir temps GPS précis
                    if hasattr(packet, 'time'):
                        gps_time = packet.time
                    else:
                        gps_time = datetime.datetime.now()
                else:
                    gps_latitude = "NO FIX"
                    gps_longitude = "NO FIX"
                    gps_satellites = 0
                    gps_quality = 0
            except Exception as e:
                gps_latitude = "ERR"
                gps_longitude = "ERR"
                print(f"Specific GPS error: {e}")
            time.sleep(1)
    except Exception as e:
        print(f"GPS error: {e}")
        gps_latitude = "ERR"
        gps_longitude = "ERR"

def update_angles():
    """Mettre à jour les angles depuis les encodeurs"""
    global current_alt, current_az, az_counter, alt_counter
    global az_last_state, alt_last_state, last_az, last_alt
    
    # Table de décodage pour l'encodeur (Gray code)
    encoder_states = {
        (0, 0, 0, 1): 1,   # Rotation horaire
        (0, 0, 1, 0): -1,  # Rotation anti-horaire
        (0, 1, 0, 0): -1,
        (0, 1, 1, 1): 1,
        (1, 0, 0, 0): 1,
        (1, 0, 1, 1): -1,
        (1, 1, 0, 1): -1,
        (1, 1, 1, 0): 1,
    }
    
    while not stop_threads:
        try:
            # Lecture de l'état actuel des encodeurs
            az_a = GPIO.input(az_encoder_pins[0])
            az_b = GPIO.input(az_encoder_pins[1])
            alt_a = GPIO.input(alt_encoder_pins[0])
            alt_b = GPIO.input(alt_encoder_pins[1])
            
            # États actuels
            az_state = (az_a, az_b)
            alt_state = (alt_a, alt_b)
            
            # Traiter azimut
            if az_state != az_last_state:
                direction = encoder_states.get((az_last_state[0], az_last_state[1], az_state[0], az_state[1]), 0)
                if direction != 0:
                    # Inverser si nécessaire
                    if AZ_ENCODER_REVERSED:
                        direction = -direction
                    az_counter += direction
                az_last_state = az_state
            
            # Traiter altitude
            if alt_state != alt_last_state:
                direction = encoder_states.get((alt_last_state[0], alt_last_state[1], alt_state[0], alt_state[1]), 0)
                if direction != 0:
                    # Inverser si nécessaire
                    if ALT_ENCODER_REVERSED:
                        direction = -direction
                    alt_counter += direction
                alt_last_state = alt_state
                
            # Calculer les angles actuels directement depuis les compteurs
            current_az = angle_from_counter(az_counter, is_altitude=False)
            current_alt = angle_from_counter(alt_counter, is_altitude=True)
            
            # Debug pour mouvements significatifs seulement
            if DEBUG_MODE and (abs(current_az - last_az) > 0.1 or abs(current_alt - last_alt) > 0.1):
                print(f"Position: Az={current_az:.1f}°, Alt={current_alt:.1f}°")
                last_az = current_az
                last_alt = current_alt
                
        except Exception as e:
            print(f"Erreur encodeur: {e}")
        
        time.sleep(0.001)  # 1ms

def calculate_direction():
    """Calculer la direction de pointage vers la cible"""
    delta_alt = target_alt - current_alt
    delta_az = target_az - current_az
    
    # Pour les cibles au-delà de 90°, adapter la stratégie de pointage
    if target_alt > 90:
        # Si la cible est de l'autre côté du zénith, ajuster l'azimut et l'altitude
        delta_alt = 180 - target_alt - current_alt
        delta_az = (target_az + 180) % 360 - current_az
    
    # Gérer la rotation 360° en azimut
    if abs(delta_az) > 180:
        delta_az = delta_az - 360 if delta_az > 0 else delta_az + 360
    
    # Seuil d'alignement (1 degré)
    if abs(delta_alt) < 1 and abs(delta_az) < 1:
        return "OK"
    
    # Calculer l'angle pour déterminer la direction
    angle = math.degrees(math.atan2(delta_alt, delta_az))
    
    # Convertir l'angle en direction 8 voies
    if 67.5 <= angle < 112.5:
        return "UP"
    elif 22.5 <= angle < 67.5:
        return "UP_RIGHT"
    elif -22.5 <= angle < 22.5:
        return "RIGHT"
    elif -67.5 <= angle < -22.5:
        return "DOWN_RIGHT"
    elif -112.5 <= angle < -67.5:
        return "DOWN"
    elif -157.5 <= angle < -112.5:
        return "DOWN_LEFT"
    elif 157.5 <= angle or angle < -157.5:
        return "LEFT"
    else:  # 112.5 <= angle < 157.5
        return "UP_LEFT"

def draw_arrow(draw, direction):
    """Dessiner flèches de base"""
    cx = WIDTH // 2
    cy = HEIGHT // 2
    size = 12
    if direction == "UP":
        draw.polygon([(cx, cy - size), (cx - size // 2, cy + size // 2), (cx + size // 2, cy + size // 2)], fill=255)
    elif direction == "DOWN":
        draw.polygon([(cx, cy + size), (cx - size // 2, cy - size // 2), (cx + size // 2, cy - size // 2)], fill=255)
    elif direction == "LEFT":
        draw.polygon([(cx - size, cy), (cx + size // 2, cy - size // 2), (cx + size // 2, cy + size // 2)], fill=255)
    elif direction == "RIGHT":
        draw.polygon([(cx + size, cy), (cx - size // 2, cy - size // 2), (cx - size // 2, cy + size // 2)], fill=255)
    elif direction == "OK":
        # Dessiner un cercle pour indiquer que la cible est atteinte
        draw.ellipse((cx - size//2, cy - size//2, cx + size//2, cy + size//2), outline=255)
        draw.text((cx - 4, cy - 3), "OK", fill=255)

def draw_arrow_8way(draw, direction):
    """Dessiner flèches 8 directions"""
    cx = WIDTH // 2
    cy = HEIGHT // 2
    size = 12
    
    if direction == "OK":
        # Dessiner un cercle quand la cible est atteinte
        draw.ellipse((cx - size//2, cy - size//2, cx + size//2, cy + size//2), outline=255)
        draw.text((cx - 4, cy - 3), "OK", fill=255)
    elif direction == "UP":
        draw.polygon([(cx, cy - size), (cx - size // 2, cy + size // 2), (cx + size // 2, cy + size // 2)], fill=255)
    elif direction == "DOWN":
        draw.polygon([(cx, cy + size), (cx - size // 2, cy - size // 2), (cx + size // 2, cy - size // 2)], fill=255)
    elif direction == "LEFT":
        draw.polygon([(cx - size, cy), (cx + size // 2, cy - size // 2), (cx + size // 2, cy + size // 2)], fill=255)
    elif direction == "RIGHT":
        draw.polygon([(cx + size, cy), (cx - size // 2, cy - size // 2), (cx - size // 2, cy + size // 2)], fill=255)
    elif direction == "UP_RIGHT":
        draw.polygon([(cx + size*0.7, cy - size*0.7), (cx-size*0.5, cy-size*0.1), (cx-size*0.1, cy+size*0.5)], fill=255)
    elif direction == "UP_LEFT":
        draw.polygon([(cx - size*0.7, cy - size*0.7), (cx+size*0.5, cy-size*0.1), (cx+size*0.1, cy+size*0.5)], fill=255)
    elif direction == "DOWN_RIGHT":
        draw.polygon([(cx + size*0.7, cy + size*0.7), (cx-size*0.5, cy+size*0.1), (cx-size*0.1, cy-size*0.5)], fill=255)
    elif direction == "DOWN_LEFT":
        draw.polygon([(cx - size*0.7, cy + size*0.7), (cx+size*0.5, cy+size*0.1), (cx+size*0.1, cy-size*0.5)], fill=255)

def draw_compass(draw, delta_az, delta_alt):
    """Afficher une boussole indiquant la direction de l'objet"""
    # Centre et rayon de la boussole
    cx, cy = WIDTH // 2, HEIGHT // 2
    radius = 20
    
    # Dessiner le cercle extérieur
    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=255)
    
    # Dessiner un point au centre
    draw.point((cx, cy), fill=255)
    
    # Calculer la position du point cible (limité par le cercle)
    # Normaliser les deltas pour qu'ils restent dans le cercle
    max_delta = max(abs(delta_az), abs(delta_alt), 10)  # Au moins 10° comme référence
    factor = radius / max_delta if max_delta > 0 else 0
    
    # Position du point cible
    tx = cx + int(delta_az * factor)
    ty = cy - int(delta_alt * factor)  # Inversé car y augmente vers le bas
    
    # Dessiner le point cible plus grand
    draw.ellipse((tx-3, ty-3, tx+3, ty+3), fill=255)
    
    # Dessiner une ligne du centre au point
    draw.line((cx, cy, tx, ty), fill=255)

def draw_radar(draw, delta_az, delta_alt, total_delta):
    """Afficher un radar avec anneaux concentriques"""
    cx, cy = WIDTH // 2, HEIGHT // 2
    max_radius = 25
    
    # Dessiner 3 cercles concentriques
    for r in [max_radius, max_radius*2//3, max_radius//3]:
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=255)
    
    # Calculer l'angle et la distance
    angle = math.degrees(math.atan2(delta_alt, delta_az)) if delta_az != 0 or delta_alt != 0 else 0
    
    # Normaliser la distance (1-20°)
    norm_distance = min(total_delta, 20) / 20
    distance = int(norm_distance * max_radius)
    
    # Calculer les coordonnées polaires -> cartésiennes
    x = cx + int(distance * math.cos(math.radians(angle)))
    y = cy - int(distance * math.sin(math.radians(angle)))
    
    # Dessiner le point cible
    draw.ellipse((x-4, y-4, x+4, y+4), fill=255)
    
    # Lignes de direction (comme un radar)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        dx = int(max_radius * math.cos(rad))
        dy = int(max_radius * math.sin(rad))
        draw.line((cx, cy, cx + dx, cy - dy), fill=255)
        
def toggle_guidance_mode():
    """Changer le mode de guidage au suivant"""
    global current_guidance_mode
    current_guidance_mode = (current_guidance_mode + 1) % 3 
    return current_guidance_mode

def display_instruction():
    """Afficher les instructions"""
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 10), "Point to Polaris", font=font, fill=255)
    draw.text((0, 25), "and press", font=font, fill=255)
    draw.text((0, 40), "button longer", font=font, fill=255)
    display.image(image)
    display.show()

def display_sky_map():
    """Redirection directe vers mode suivi astrophoto"""
    global current_mode
    # Au lieu d'afficher liste objets proches,
    # aller directement au mode suivi
    current_mode = MODE_TRACKING
    tracking_mode()

def tracking_mode():
    """Mode suivi pour astrophotographie avec chronomètre"""
    global button_pressed, last_update_time
    
    # Vérifier si un objet est sélectionné
    if target_alt == 0 and target_az == 0:
        # Aucun objet sélectionné, message d'erreur
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((0, 20), "ERROR: No object", font=font, fill=255)
        draw.text((0, 35), "selected", font=font, fill=255)
        display.image(image)
        display.show()
        time.sleep(2)
        return
    
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Temps écoulé depuis la sélection de l'objet
    elapsed_time = int(time.time() - last_update_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    
    # Mettre à jour la position cible toutes les 10 secondes
    current_time = time.time()
    if current_time - last_update_time > 10:
        category = categories[selected_category_index]
        object_name = celestial_database[category][selected_object_index]
        get_object_coordinates(object_name, category)
        last_update_time = current_time
    
    # Direction actuelle
    direction = calculate_direction()
    
    # Afficher nom de l'objet et position
    category = categories[selected_category_index]
    object_name = celestial_database[category][selected_object_index]
    if len(object_name) > 14:
        object_name = object_name[:12] + ".."
    
    draw.text((0, 0), f"TRACKING: {object_name}", font=font, fill=255)
    draw.text((0, 12), f"Time: {minutes:02d}:{seconds:02d}", font=font, fill=255)
    
    # Suggestions de temps d'exposition selon le type d'objet
    if category == "Sun":
        exposure_times = "1/1000s - 1/4000s"
        draw.text((0, 24), f"Exposure: {exposure_times}", font=font, fill=255)
        draw.text((0, 36), "!!! USE SOLAR FILTER !!!", font=font, fill=255)
    elif category == "Planets":
        exposure_times = "1/125s - 1/500s"
    elif category == "Moon":
        exposure_times = "1/125s - 1/1000s"
    elif category == "Stars":
        exposure_times = "1-10s"
    else:  # Ciel profond
        exposure_times = "30s - 5min"
    
    draw.text((0, 24), f"Exposure: {exposure_times}", font=font, fill=255)
    
    # Dessiner statut d'alignement
    if direction == "OK":
        draw.text((0, 36), "Alignment: OK", font=font, fill=255)
        # Dessiner symbole appareil photo pour indiquer prêt pour photo
        draw.rectangle((100, 36, 110, 42), outline=255)
        draw.rectangle((112, 37, 115, 39), outline=255)
    else:
        draw.text((0, 36), f"Alignment: {direction}", font=font, fill=255)
    
    # Indicateur de précision
    delta_alt = abs(target_alt - current_alt)
    delta_az = abs(target_az - current_az)
    if delta_az > 180:
        delta_az = 360 - delta_az
    total_delta = delta_alt + delta_az
    
    if total_delta < 2:
        precision = "Excellent!"
    elif total_delta < 5:
        precision = "Good"
    else:
        precision = "Adjust..."
    
    draw.text((0, 48), f"Precision: {precision}", font=font, fill=255)
    
    display.image(image)
    display.show()

def display_system_info():
    """Afficher informations système: GPS et encodeurs"""
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    draw.text((0, 0), "SYSTEM INFORMATION", font=font, fill=255)
    
    # Afficher coordonnées GPS
    if gps_latitude not in ["N/A", "ERR", "NO FIX"]:
        draw.text((0, 10), f"Lat: {gps_latitude[:8]}", font=font, fill=255)
        draw.text((0, 20), f"Lon: {gps_longitude[:8]}", font=font, fill=255)
        draw.text((0, 30), f"Alt: {gps_altitude:.1f}m", font=font, fill=255)
        draw.text((0, 40), f"Sat: {gps_satellites}", font=font, fill=255)
    else:
        draw.text((0, 10), f"GPS: {gps_latitude}", font=font, fill=255)
    
    # Afficher valeurs encodeurs
    draw.text((0, 50), f"Enc: Az={current_az:.1f}° Alt={current_alt:.1f}°", font=font, fill=255)
    
    display.image(image)
    display.show()

def display_level_selection():
    """Afficher menu de sélection de niveau de difficulté"""
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    draw.text((0, 0), "DIFFICULTY LEVEL:", font=font, fill=255)
    
    # Afficher niveaux disponibles
    for i, level in enumerate(niveaux_observation):
        prefix = ">" if i == selected_level_index else " "
        draw.text((0, 15 + i*12), f"{prefix} {level}", font=font, fill=255)
    
    display.image(image)
    display.show()

def calibrate_on_polaris():
    """Calibration séquentielle: Polaris → 180° → Horizon → Zenith"""
    global az_counter, alt_counter, current_alt, current_az
    global gps_latitude, gps_longitude, gps_altitude, gps_time, IS_CALIBRATING
    
    IS_CALIBRATING = True

    # ÉTAPE 1: Calibration sur Polaris
    display.fill(0)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 0), "STEP 1: POLARIS", font=font, fill=255)
    draw.text((0, 15), "Point telescope to", font=font, fill=255)
    draw.text((0, 30), "POLARIS", font=font, fill=255)
    draw.text((0, 45), "Press when ready", font=font, fill=255)
    display.image(image)
    display.show()
    
    # Attendre appui bouton
    wait_for_button_press()
    
    try:
        # Calculer position de Polaris
        observer = create_observer()
        polaris = ephem.readdb(star_catalog["Polaris"])
        polaris.compute(observer)
        
        # Convertir en degrés
        real_alt = float(polaris.alt) * 180 / math.pi
        real_az = float(polaris.az) * 180 / math.pi
        
        # Calibrer l'azimut sur Polaris
        az_steps_per_degree = ENCODER_STEPS_PER_REVOLUTION * AZIMUTH_GEAR_RATIO / 360.0
        az_counter = int(real_az * az_steps_per_degree)
        current_az = real_az % 360.0
        
        # ÉTAPE 2: Rotation 180° en azimut
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "STEP 2: 180° ROTATION", font=font, fill=255)
        draw.text((0, 15), "Rotate telescope", font=font, fill=255)
        draw.text((0, 30), f"180° from {real_az:.1f}°", font=font, fill=255)
        draw.text((0, 45), "Press when ready", font=font, fill=255)
        display.image(image)
        display.show()
        
        # Attendre appui bouton
        wait_for_button_press()
        
        # ÉTAPE 3: Calibration altitude à l'horizon (0°)
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "STEP 3: HORIZON", font=font, fill=255)
        draw.text((0, 15), "Point telescope to", font=font, fill=255)
        draw.text((0, 30), "HORIZON (0°)", font=font, fill=255)
        draw.text((0, 45), "Press when ready", font=font, fill=255)
        display.image(image)
        display.show()
        
        # Attendre appui bouton
        wait_for_button_press()
        
        # Enregistrer valeur horizon
        ALT_CALIB_HORIZON_COUNT = alt_counter
        print(f"Horizon calibrated at {ALT_CALIB_HORIZON_COUNT} pulses")
        
        # ÉTAPE 4: Calibration altitude au zénith (90°)
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), "STEP 4: ZENITH", font=font, fill=255)
        draw.text((0, 15), "Point telescope to", font=font, fill=255)
        draw.text((0, 30), "ZENITH (90°)", font=font, fill=255)
        draw.text((0, 45), "Press when ready", font=font, fill=255)
        display.image(image)
        display.show()
        
        # Attendre appui bouton
        wait_for_button_press()
        
        # Enregistrer valeur zénith
        ALT_CALIB_ZENITH_COUNT = alt_counter
        print(f"Zenith calibrated at {ALT_CALIB_ZENITH_COUNT} pulses")
        
        # Vérifier valeurs valides
        if ALT_CALIB_ZENITH_COUNT == ALT_CALIB_HORIZON_COUNT:
            display.fill(0)
            image = Image.new("1", (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)
            draw.text((0, 20), "CALIBRATION ERROR", font=font, fill=255)
            draw.text((0, 35), "Same values detected!", font=font, fill=255)
            display.image(image)
            display.show()
            time.sleep(2)
            ALT_CALIBRATED = False
        else:
            # Calibration réussie
            ALT_CALIBRATED = True
            
            # Message de réussite final
            display.fill(0)
            image = Image.new("1", (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), "CALIBRATION COMPLETE", font=font, fill=255)
            draw.text((0, 20), "All steps finished", font=font, fill=255)
            draw.text((0, 35), "successfully", font=font, fill=255)
            display.image(image)
            display.show()
            time.sleep(2)
        
    except Exception as e:
        print(f"CALIBRATION ERROR: {e}")
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((0, 20), "CALIBRATION ERROR", font=font, fill=255)
        draw.text((0, 35), str(e)[:20], font=font, fill=255)
        display.image(image)
        display.show()
        time.sleep(2)
    finally:
        IS_CALIBRATING = False

def get_object_coordinates(object_name, category):
    """Calculer position objet céleste et définir comme cible"""
    global gps_latitude, gps_longitude, gps_altitude, gps_time, target_alt, target_az
    
    try:
        # Créer observateur à position GPS actuelle
        observer = ephem.Observer()
        
        # Gérer formats GPS non-numériques et utiliser données précises
        try:
            lat = float(gps_latitude)
            lon = float(gps_longitude)
            observer.lat = str(lat)
            observer.lon = str(lon)
            observer.elevation = gps_altitude  # Utiliser altitude pour plus de précision
            
            # Utiliser temps GPS si disponible
            if gps_time:
                observer.date = ephem.Date(gps_time)
            else:
                observer.date = ephem.now()
                
        except ValueError:
            # Si GPS non disponible, utiliser position par défaut (Paris)
            observer.lat = '48.8566'
            observer.lon = '2.3522'
            observer.elevation = 35  # Altitude de Paris en mètres
            observer.date = ephem.now()
            print(f"GPS not available, using default position")
            
        # Définir objet selon nom et catégorie
        celestial_object = None
        
        if category == "Planets":
            if object_name == "Mercury":
                celestial_object = ephem.Mercury()
            elif object_name == "Venus":
                celestial_object = ephem.Venus()
            elif object_name == "Mars":
                celestial_object = ephem.Mars()
            elif object_name == "Jupiter":
                celestial_object = ephem.Jupiter()
            elif object_name == "Saturn":
                celestial_object = ephem.Saturn()
            elif object_name == "Uranus":
                celestial_object = ephem.Uranus()
            elif object_name == "Neptune":
                celestial_object = ephem.Neptune()
        elif category == "Moon":
            celestial_object = ephem.Moon()
        elif category == "Sun":  # Avertissement supprimé
            celestial_object = ephem.Sun()
        elif category == "Stars" and object_name in star_catalog:
            celestial_object = ephem.readdb(star_catalog[object_name])
        elif category == "Deep Sky" and object_name in dso_catalog:
            celestial_object = ephem.readdb(dso_catalog[object_name])
                
        if celestial_object:
            celestial_object.compute(observer)
            # Convertir de radians en degrés
            alt = float(celestial_object.alt) * 180 / math.pi
            az = float(celestial_object.az) * 180 / math.pi
            
            # Garantir que l'altitude est entre 0 et 90°
            # Si l'objet est sous l'horizon, le signaler mais ne pas modifier l'altitude
            if alt < 0:
                print(f"Warning: {object_name} is below horizon (Alt={alt:.1f}°)")
            elif alt > 90:
                # Si l'objet est au-delà du zénith, le pointage doit se faire en inversant l'azimut
                # et en prenant le complément de l'altitude par rapport à 180°
                print(f"Object {object_name} is beyond zenith, adjusting pointing.")
                alt = 180 - alt
                az = (az + 180) % 360
            
            # Définir comme cible
            set_target(min(90, max(0, alt)), az)  # S'assurer que l'altitude cible est entre 0-90°
            print(f"Object {object_name} set as target: Alt={alt:.1f}°, Az={az:.1f}°")
            return True
            
    except Exception as e:
        print(f"Error calculating coordinates: {e}")
        return False

def do_routine():
    """Routine principale de gestion des modes d'affichage"""
    global button_pressed, current_mode, last_update_time
    global last_az, last_alt, selected_object_index
    global IS_CALIBRATING  
    
    if IS_CALIBRATING:
        return
    
    if current_mode == MODE_GPS_WAIT:
        display_gps_wait()  # Afficher écran d'attente GPS
        
        # Procéder automatiquement à l'étape suivante si GPS bon
        if (gps_quality >= 2 and gps_satellites >= 4 and 
            isinstance(gps_latitude, str) and 
            gps_latitude not in ["N/A", "ERR", "NO FIX"] and
            len(gps_latitude) > 3):
            print(f"GPS fixed with {gps_satellites} satellites, quality: {gps_quality}")
            current_mode = MODE_INSTRUCTION
            button_pressed = True
    
    elif current_mode == MODE_INSTRUCTION:
        display_instruction()
    
    elif current_mode == MODE_CALIBRATION:
        # Lancer directement la calibration si ce n'est pas déjà en cours
        if not IS_CALIBRATING:
            IS_CALIBRATING = True
            calibrate_on_polaris()  # Lance directement la calibration
            IS_CALIBRATING = False
            current_mode = MODE_MAIN_MENU
            button_pressed = True
        
    elif current_mode == MODE_MAIN_MENU:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        draw.text((0, 0), "MAIN MENU:", font=font, fill=255)
        
        # Afficher options menu principal
        for i in range(len(main_menu_options)):
            prefix = ">" if i == selected_main_menu_index else " "
            draw.text((0, 15 + i*10), f"{prefix} {main_menu_options[i]}", font=font, fill=255)
                    
        display.image(image)
        display.show()
    
    elif current_mode == MODE_CATEGORY:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        draw.text((0, 0), "CATEGORIES:", font=font, fill=255)
        
        # Afficher catégorie sélectionnée et autres
        for i in range(min(4, len(categories))):
            idx = (selected_category_index + i) % len(categories)
            prefix = ">" if i == 0 else " "
            draw.text((0, 15 + i*10), f"{prefix} {categories[idx]}", font=font, fill=255)
        
        display.image(image)
        display.show()
        
    elif current_mode == MODE_LEVEL_SELECTION:
        # Nouveau mode: sélection niveau de difficulté
        display_level_selection()
    
    elif current_mode == MODE_SELECTION:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        category = categories[selected_category_index]
        draw.text((0, 0), f"Cat: {category}", font=font, fill=255)
        
        # Afficher plus d'objets maintenant qu'il y a plus d'espace
        objects = celestial_database[category]
        for i in range(min(5, len(objects))):
            idx = (selected_object_index + i) % len(objects)
            prefix = ">" if i == 0 else " "
            draw.text((0, 15 + i*10), f"{prefix} {objects[idx]}", font=font, fill=255)
        
        display.image(image)
        display.show()
    
    elif current_mode == MODE_POINTING:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Mettre à jour coordonnées cibles toutes les 30 secondes
        current_time = time.time()
        if current_time - last_update_time > 30:  # Mettre à jour toutes les 30 secondes
            category = categories[selected_category_index]
            object_name = celestial_database[category][selected_object_index]
            get_object_coordinates(object_name, category)
            last_update_time = current_time

        # Calculer deltas
        delta_alt = target_alt - current_alt
        delta_az = target_az - current_az

        # Ajuster delta_az pour rotation 360°
        if abs(delta_az) > 180:
            delta_az = delta_az - 360 if delta_az > 0 else delta_az + 360
        
        # Calculer delta total pour précision
        total_delta = abs(delta_alt) + abs(delta_az)
        
        # Toujours calculer direction pour besoins de débogage
        direction = calculate_direction()
        
        # Dessiner différentes visualisations de guidage selon mode
        if current_guidance_mode == GUIDANCE_MODE_ARROWS_8WAY:
            draw_arrow_8way(draw, direction)
        elif current_guidance_mode == GUIDANCE_MODE_COMPASS:
            draw_compass(draw, delta_az, delta_alt)
        elif current_guidance_mode == GUIDANCE_MODE_RADAR:
            draw_radar(draw, delta_az, delta_alt, total_delta)

        # Afficher nom objet
        category = categories[selected_category_index]
        object_name = celestial_database[category][selected_object_index]
        # Limiter nom si trop long
        if len(object_name) > 18:
            object_name = object_name[:15] + "..."
        draw.text((2, 0), f"Target: {object_name}", font=font, fill=255)
        
        # Afficher indicateur de précision
        if total_delta < 2:
            precision = "Excellent!"
        elif total_delta < 5:
            precision = "Good"
        elif total_delta < 10:
            precision = "Medium"
        else:
            precision = f"Gap: {total_delta:.1f}°"
        
        draw.text((2, HEIGHT - 18), f"Precision: {precision}", font=font, fill=255)

        display.image(image)
        display.show()
        
        # Sauvegarder dernières valeurs pour prochaine itération
        last_az = current_az
        last_alt = current_alt

        # Afficher informations de débogage
        if DEBUG_MODE:
            print(f"Direction: {direction}, Delta Alt: {target_alt-current_alt:.1f}, Delta Az: {target_az-current_az:.1f}")

        display.image(image)
        display.show()
        
        # Sauvegarder dernières valeurs pour prochaine itération
        last_az = current_az
        last_alt = current_alt
    
    elif current_mode == MODE_SKY_MAP:
        # Nouveau mode carte du ciel
        display_sky_map()
    
    elif current_mode == MODE_TRACKING:
        # Nouveau mode suivi avec chronomètre
        tracking_mode()
        
    elif current_mode == MODE_RECOMMENDATIONS:
        display.fill(0)
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # En-tête avec niveau actuel et statut filtre
        level = niveaux_observation[selected_level_index]
        filter_status = "now" if visible_now else "all"
        draw.text((0, 0), f"Level: {level}", font=font, fill=255)
        draw.text((0, 10), f"Visible: {filter_status}", font=font, fill=255)
        
        # Afficher objets recommandés
        if len(recommended_objects) > 0:
            for i in range(min(4, len(recommended_objects))):
                idx = (selected_object_index + i) % len(recommended_objects)
                obj = recommended_objects[idx]
                prefix = ">" if i == 0 else " "
                draw.text((0, 25 + i*10), f"{prefix} {obj['nom']}", font=font, fill=255)
        else:
            draw.text((0, 25), "No visible objects", font=font, fill=255)
        
        display.image(image)
        display.show()
    
    elif current_mode == MODE_SYSTEM_INFO:
        # Afficher informations système
        display_system_info()
    
    button_pressed = False

def shutdown(sig=None, frame=None):
    """Arrêt propre du système"""
    global stop_threads
    stop_threads = True
    display.fill(0)
    display.show()
    GPIO.cleanup()
    print("Clean shutdown. GPIO released.")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    
    # Charger catalogues étendus si fichier existe
    try:
        from celestial_database_extended import load_extended_catalogs
        load_extended_catalogs()
        print("Extended database loaded successfully.")
    except ImportError:
        print("Using standard database.")
    
    # Configuration des encodeurs
    setup_encoders()
    
    # Démarrage des threads GPS et encodeurs
    gps_thread = Thread(target=update_gps_data, daemon=True)
    gps_thread.start()

    angle_thread = Thread(target=update_angles, daemon=True)
    angle_thread.start()
    
    # Attendre l'initialisation des threads
    time.sleep(1)
    
    # Thread du bouton
    button_thread = Thread(target=check_button, daemon=True)
    button_thread.start()

    # Initialiser objets recommandés
    update_visible_recommendations()
    
    # Initialiser mode système
    current_mode = MODE_GPS_WAIT
    
    print("System started, waiting for GPS...")
    
    try:
        while True:
            do_routine()
            time.sleep(0.1)
    except KeyboardInterrupt:
        shutdown()