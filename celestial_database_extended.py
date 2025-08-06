"""
Base de données étendue d'objets célestes pour le pointeur astronomique.
Ce fichier contient des catalogues étendus d'étoiles, de galaxies, de nébuleuses et d'amas.
"""

# Base de données étendue des étoiles (format: "Nom,type,RA,Dec,Magnitude")
extended_star_catalog = {
    # Étoiles déjà présentes
    "Polaris": "Polaris,f|M|A0,2:31:49.09,89:15:50.8,2.0",
    "Sirius": "Sirius,f|M|A0,6:45:08.92,-16:42:58.0,-1.46",
    "Vega": "Vega,f|M|A0,18:36:56.34,38:47:01.3,0.03",
    "Betelgeuse": "Betelgeuse,f|M|A0,5:55:10.29,7:24:25.3,0.5",
    "Rigel": "Rigel,f|M|A0,5:14:32.3,-8:12:06,0.12",
    "Arcturus": "Arcturus,f|M|A0,14:15:39.67,19:10:56.7,-0.04",
    "Aldebaran": "Aldebaran,f|M|A0,4:35:55.23,16:30:33.5,0.85",
    "Deneb": "Deneb,f|M|A0,20:41:25.91,45:16:49.2,1.25",
    "Capella": "Capella,f|M|A0,5:16:41.36,45:59:52.8,0.08",
    "Antares": "Antares,f|M|A0,16:29:24.46,-26:25:55.2,1.06",
    "Altair": "Altair,f|M|A0,19:50:47.00,8:52:06.0,0.77",
    "Spica": "Spica,f|M|A0,13:25:11.57,-11:09:40.8,1.04",
    "Pollux": "Pollux,f|M|A0,7:45:18.95,28:01:34.3,1.14",
    "Fomalhaut": "Fomalhaut,f|M|A0,22:57:39.05,-29:37:20.1,1.16",
    "Regulus": "Regulus,f|M|A0,10:08:22.31,11:58:02.0,1.35",
    "Castor": "Castor,f|M|A0,7:34:35.87,31:53:18.0,1.58",
    "Procyon": "Procyon,f|M|A0,7:39:18.12,5:13:30.0,0.34",
    
    # Nouvelles étoiles ajoutées
    "Achernar": "Achernar,f|M|A0,1:37:42.85,-57:14:12.3,0.46",
    "Hadar": "Hadar,f|M|A0,14:03:49.40,-60:22:22.9,0.61",
    "Acrux": "Acrux,f|M|A0,12:26:35.90,-63:05:56.7,0.77",
    "Shaula": "Shaula,f|M|A0,17:33:36.50,-37:06:13.8,1.62",
    "Gacrux": "Gacrux,f|M|A0,12:31:09.96,-57:06:47.6,1.63",
    "Bellatrix": "Bellatrix,f|M|A0,5:25:07.86,6:20:58.9,1.64",
    "Elnath": "Elnath,f|M|A0,5:26:17.51,28:36:26.8,1.65",
    "Miaplacidus": "Miaplacidus,f|M|A0,9:13:11.98,-69:43:01.9,1.69",
    "Alnilam": "Alnilam,f|M|A0,5:36:12.81,-1:12:06.9,1.69",
    "Alnitak": "Alnitak,f|M|A0,5:40:45.52,-1:56:33.3,1.74",
    "Alioth": "Alioth,f|M|A0,12:54:01.75,55:57:35.4,1.77",
    "Dubhe": "Dubhe,f|M|A0,11:03:43.67,61:45:03.7,1.79",
    "Mirfak": "Mirfak,f|M|A0,3:24:19.35,49:51:40.2,1.80",
    "Alkaid": "Alkaid,f|M|A0,13:47:32.44,49:18:48.0,1.86",
    "Kaus Australis": "Kaus Australis,f|M|A0,18:24:10.32,-34:23:04.6,1.85",
    "Avior": "Avior,f|M|A0,8:22:30.84,-59:30:34.3,1.86",
    "Menkar": "Menkar,f|M|A0,3:02:16.78,4:05:23.7,2.54",
    "Alpheratz": "Alpheratz,f|M|A0,0:08:23.26,29:05:25.6,2.07",
    "Mirach": "Mirach,f|M|A0,1:09:43.92,35:37:14.0,2.07",
    "Almach": "Almach,f|M|A0,2:03:54.02,42:19:47.0,2.10",
    "Schedar": "Schedar,f|M|A0,0:40:30.44,56:32:14.4,2.24",
    "Caph": "Caph,f|M|A0,0:09:10.69,59:08:59.2,2.28",
    "Merak": "Merak,f|M|A0,11:01:50.48,56:22:56.7,2.37",
    "Phecda": "Phecda,f|M|A0,11:53:49.85,53:41:41.1,2.41",
    "Megrez": "Megrez,f|M|A0,12:15:25.56,57:01:57.4,3.31",
    "Mizar": "Mizar,f|M|A0,13:23:55.54,54:55:31.3,2.23",
    "Denebola": "Denebola,f|M|A0,11:49:03.58,14:34:19.4,2.14",
    "Algol": "Algol,f|M|A0,3:08:10.13,40:57:20.3,2.12",
    "Alderamin": "Alderamin,f|M|A0,21:18:34.78,62:35:07.9,2.45",
    "Alphecca": "Alphecca,f|M|A0,15:34:41.27,26:42:52.9,2.22",
    "Etamin": "Etamin,f|M|A0,17:56:36.37,51:29:20.0,2.24",
    "Kochab": "Kochab,f|M|A0,14:50:42.33,74:09:19.8,2.07",
    "Saiph": "Saiph,f|M|A0,5:47:45.39,-9:40:10.6,2.06",
    "Rasalhague": "Rasalhague,f|M|A0,17:34:56.07,12:33:36.1,2.08",
    "Nunki": "Nunki,f|M|A0,18:55:15.93,-26:17:48.2,2.05",
    "Alphekka": "Alphekka,f|M|A0,15:34:41.27,26:42:52.9,2.22",
    "Menkent": "Menkent,f|M|A0,14:06:40.95,-36:22:11.8,2.06",
    "Errai": "Errai,f|M|A0,23:39:20.90,77:37:56.2,3.21",
    "Alfirk": "Alfirk,f|M|A0,21:28:39.60,70:33:38.6,3.24",
    "Albireo": "Albireo,f|M|A0,19:30:43.29,27:57:34.7,3.05",
    "Algieba": "Algieba,f|M|A0,10:19:58.36,19:50:29.3,2.01",
    "Zubenelgenubi": "Zubenelgenubi,f|M|A0,14:50:52.71,-16:02:30.4,2.75",
    "Zubeneschamali": "Zubeneschamali,f|M|A0,15:17:00.41,-9:22:58.5,2.61",
    "Unukalhai": "Unukalhai,f|M|A0,15:44:16.07,6:25:32.3,2.63",
    "Rasalgethi": "Rasalgethi,f|M|A0,17:14:38.86,14:23:25.1,3.35",
    "Sadalmelik": "Sadalmelik,f|M|A0,22:05:47.04,-0:19:11.4,2.95",
    "Enif": "Enif,f|M|A0,21:44:11.16,9:52:30.0,2.39",
    "Scheat": "Scheat,f|M|A0,23:03:46.45,28:04:58.0,2.44",
    "Markab": "Markab,f|M|A0,23:04:45.65,15:12:18.9,2.49",
    "Algenib": "Algenib,f|M|A0,0:13:14.15,15:11:00.9,2.83",
    "Curl": "Curl,f|M|A0,5:26:17.51,28:36:26.8,1.65"
}

# Base de données étendue des objets du ciel profond (format: "Nom,type,RA,Dec,Magnitude")
extended_dso_catalog = {
    # Objets déjà présents
    "M31 (Andromede)": "M31,f|G,0:42:44.3,+41:16:9,4.3",
    "M42 (Orion)": "M42,f|G,5:35:17.3,-5:23:28,4.0",
    "M45 (Pleiades)": "M45,f|G,3:47:0.0,+24:7:0,1.2",
    "M13": "M13,f|G,16:41:41.24,+36:27:35.5,5.9",
    "M27": "M27,f|G,19:59:36.3,+22:43:16,8.1",
    "M57 (Anneau)": "M57,f|G,18:53:35.1,+33:1:45,9.0",
    "M51 (Tourbillon)": "M51,f|G,13:29:52.7,+47:11:43,8.4",
    "M101": "M101,f|G,14:3:12.6,+54:20:57,7.9",
    "M81": "M81,f|G,9:55:33.2,+69:3:55,6.9",
    "M82": "M82,f|G,9:55:52.2,+69:40:47,8.4",
    "M8 (Lagune)": "M8,f|G,18:3:37.0,-24:23:12,6.0",
    "M20 (Trifide)": "M20,f|G,18:2:23.0,-23:1:48,6.3",
    "M16 (Aigle)": "M16,f|G,18:18:48.0,-13:47:0,6.0",
    "M17 (Omega)": "M17,f|G,18:20:26.0,-16:10:36,6.0",
    
    # Nouveaux objets du ciel profond
    "M1 (Crabe)": "M1,f|G,5:34:31.94,+22:00:52.2,8.4",
    "M2": "M2,f|G,21:33:27.01,-0:49:23.7,6.6",
    "M3": "M3,f|G,13:42:11.62,+28:22:38.2,6.3",
    "M4": "M4,f|G,16:23:35.22,-26:31:32.7,5.6",
    "M5": "M5,f|G,15:18:33.22,+2:04:51.7,5.7",
    "M6 (Papillon)": "M6,f|G,17:40:20.78,-32:15:15.2,5.3",
    "M7": "M7,f|G,17:53:51.18,-34:47:34.2,3.3",
    "M9": "M9,f|G,17:19:11.78,-18:30:58.5,7.7",
    "M10": "M10,f|G,16:57:8.92,-4:05:58.0,6.6",
    "M11 (Canard)": "M11,f|G,18:51:05.98,-6:16:12.1,6.3",
    "M12": "M12,f|G,16:47:14.52,-1:56:52.1,6.6",
    "M14": "M14,f|G,17:37:36.15,-3:14:45.3,7.6",
    "M15": "M15,f|G,21:29:58.33,+12:10:01.2,6.2",
    "M18": "M18,f|G,18:19:58.14,-17:08:04.0,7.5",
    "M19": "M19,f|G,17:02:37.69,-26:16:04.6,6.8",
    "M21": "M21,f|G,18:04:13.46,-22:29:24.3,5.9",
    "M22": "M22,f|G,18:36:23.94,-23:54:17.1,5.1",
    "M23": "M23,f|G,17:56:48.43,-19:00:50.6,5.5",
    "M24 (Petit Nuage)": "M24,f|G,18:16:45.00,-18:30:00.0,4.6",
    "M25": "M25,f|G,18:31:47.00,-19:15:00.0,4.6",
    "M26": "M26,f|G,18:45:18.71,-9:23:01.0,8.0",
    "M28": "M28,f|G,18:24:32.89,-24:52:11.3,6.8",
    "M29": "M29,f|G,20:23:56.02,+38:30:30.2,6.6",
    "M30": "M30,f|G,21:40:22.12,-23:10:47.5,7.2",
    "M32": "M32,f|G,0:42:41.83,+40:51:55.0,8.1",
    "M33 (Triangulum)": "M33,f|G,1:33:50.90,+30:39:36.8,5.7",
    "M34": "M34,f|G,2:42:05.00,+42:47:00.0,5.2",
    "M35": "M35,f|G,6:08:54.00,+24:20:00.0,5.1",
    "M36": "M36,f|G,5:36:12.00,+34:08:00.0,6.0",
    "M37": "M37,f|G,5:52:18.00,+32:33:02.0,5.6",
    "M38": "M38,f|G,5:28:42.00,+35:51:18.0,6.4",
    "M39": "M39,f|G,21:32:12.00,+48:26:00.0,4.6",
    "M40": "M40,f|G,12:22:12.50,+58:04:59.0,8.4",
    "M41": "M41,f|G,6:46:00.00,-20:44:00.0,4.5",
    "M43": "M43,f|G,5:35:31.30,-5:16:02.5,7.0",
    "M44 (Praesepe)": "M44,f|G,8:40:24.00,+19:40:00.0,3.1",
    "M46": "M46,f|G,7:41:46.82,-14:48:36.0,6.1",
    "M47": "M47,f|G,7:36:35.00,-14:30:00.0,4.3",
    "M48": "M48,f|G,8:13:48.00,-5:48:00.0,5.8",
    "M49": "M49,f|G,12:29:46.76,+8:00:01.7,8.4",
    "M50": "M50,f|G,7:03:12.00,-8:20:00.0,5.9",
    "M52": "M52,f|G,23:24:48.00,+61:35:36.0,6.9",
    "M53": "M53,f|G,13:12:55.25,+18:10:05.5,7.6",
    "M54": "M54,f|G,18:55:03.27,-30:28:42.5,7.6",
    "M55": "M55,f|G,19:40:00.00,-30:58:00.0,6.3",
    "M56": "M56,f|G,19:16:35.57,+30:11:04.2,8.3",
    "M58": "M58,f|G,12:37:43.60,+11:49:05.1,9.7",
    "M59": "M59,f|G,12:42:02.31,+11:38:49.4,9.6",
    "M60": "M60,f|G,12:43:39.98,+11:33:09.8,8.8",
    "M61": "M61,f|G,12:21:54.97,+4:28:25.1,9.7",
    "M62": "M62,f|G,17:01:12.60,-30:06:44.5,6.6",
    "M63": "M63,f|G,13:15:49.27,+42:01:49.4,8.6",
    "M64 (Œil Noir)": "M64,f|G,12:56:43.76,+21:40:58.0,8.5",
    "M65": "M65,f|G,11:18:55.92,+13:05:32.0,9.3",
    "M66": "M66,f|G,11:20:15.01,+12:59:28.9,8.9",
    "M67": "M67,f|G,8:50:24.00,+11:49:00.0,6.1",
    "M68": "M68,f|G,12:39:28.01,-26:44:34.9,8.2",
    "M69": "M69,f|G,18:31:23.23,-32:20:52.7,7.6",
    "M70": "M70,f|G,18:43:12.71,-32:17:30.8,7.9",
    "M71": "M71,f|G,19:53:46.11,+18:46:42.2,8.3",
    "M72": "M72,f|G,20:53:27.94,-12:32:13.6,9.3",
    "M73": "M73,f|G,20:58:54.00,-12:38:00.0,9.0",
    "M74": "M74,f|G,1:36:41.75,+15:47:01.2,9.1",
    "M75": "M75,f|G,20:06:04.86,-21:55:17.2,8.5",
    "M76 (Petit Haltère)": "M76,f|G,1:42:18.00,+51:34:00.0,10.1",
    "M77": "M77,f|G,2:42:40.77,-0:00:47.6,8.9",
    "M78": "M78,f|G,5:46:45.00,+0:04:48.0,8.3",
    "M79": "M79,f|G,5:24:10.59,-24:31:26.8,7.7",
    "M80": "M80,f|G,16:17:02.41,-22:58:30.0,7.3",
    "M83": "M83,f|G,13:37:00.94,-29:51:56.7,8.2",
    "M84": "M84,f|G,12:25:03.72,+12:53:13.1,9.1",
    "M85": "M85,f|G,12:25:24.12,+18:11:28.9,9.1",
    "M86": "M86,f|G,12:26:11.77,+12:56:45.7,8.9",
    "M87": "M87,f|G,12:30:49.42,+12:23:28.0,8.6",
    "M88": "M88,f|G,12:31:59.16,+14:25:14.0,9.6",
    "M89": "M89,f|G,12:35:39.80,+12:33:22.6,9.8",
    "M90": "M90,f|G,12:36:49.80,+13:09:46.2,9.5",
    "M91": "M91,f|G,12:35:26.47,+14:29:46.7,10.2",
    "M92": "M92,f|G,17:17:07.39,+43:08:09.4,6.5",
    "M93": "M93,f|G,7:44:36.00,-23:52:00.0,6.2",
    "M94": "M94,f|G,12:50:53.06,+41:07:13.6,8.2",
    "M95": "M95,f|G,10:43:57.70,+11:42:13.7,9.7",
    "M96": "M96,f|G,10:46:45.84,+11:49:12.0,9.2",
    "M97 (Hibou)": "M97,f|G,11:14:47.71,+55:01:09.5,9.9",
    "M98": "M98,f|G,12:13:48.29,+14:54:01.2,10.1",
    "M99": "M99,f|G,12:18:49.60,+14:24:59.0,9.9",
    "M100": "M100,f|G,12:22:54.83,+15:49:19.5,9.3",
    "M102": "M102,f|G,15:06:29.53,+55:45:47.9,9.9",
    "M103": "M103,f|G,1:33:15.00,+60:42:00.0,7.4",
    "M104 (Sombrero)": "M104,f|G,12:40:00.00,-11:37:23.0,8.0",
    "M105": "M105,f|G,10:47:49.60,+12:34:54.0,9.3",
    "M106": "M106,f|G,12:18:57.62,+47:18:13.6,8.4",
    "M107": "M107,f|G,16:32:31.91,-13:03:13.1,8.1",
    "M108": "M108,f|G,11:11:31.40,+55:40:31.4,10.0",
    "M109": "M109,f|G,11:57:36.02,+53:22:28.0,9.8",
    "M110": "M110,f|G,0:40:22.56,+41:41:07.6,8.5",
    "NGC 253": "NGC 253,f|G,0:47:33.1,-25:17:18,7.1",
    "NGC 891": "NGC 891,f|G,2:22:33.0,+42:20:57,9.9",
    "NGC 1261": "NGC 1261,f|G,3:12:15.3,-55:12:58,8.4",
    "NGC 1514": "NGC 1514,f|G,4:09:17.0,+30:46:33,10.9",
    "NGC 2903": "NGC 2903,f|G,9:32:10.1,+21:30:03,9.7",
    "NGC 3242": "NGC 3242,f|G,10:24:46.1,-18:38:32,8.6",
    "NGC 3372 (Carina)": "NGC 3372,f|G,10:45:08.9,-59:52:04,1.0",
    "NGC 4565": "NGC 4565,f|G,12:36:20.8,+25:59:16,9.6",
    "NGC 5128 (Centaurus A)": "NGC 5128,f|G,13:25:27.6,-43:01:09,6.8",
    "NGC 5139 (Omega Cen)": "NGC 5139,f|G,13:26:47.3,-47:28:46,3.9",
    "NGC 5866": "NGC 5866,f|G,15:06:29.5,+55:45:48,9.9",
    "NGC 6025": "NGC 6025,f|G,16:03:17.0,-60:25:54,5.1",
    "NGC 6121": "NGC 6121,f|G,16:23:35.4,-26:31:31,5.8",
    "NGC 6210": "NGC 6210,f|G,16:44:29.5,+23:47:59,9.3",
    "NGC 6397": "NGC 6397,f|G,17:40:41.3,-53:40:25,5.7",
    "NGC 6543 (Œil de Chat)": "NGC 6543,f|G,17:58:33.4,+66:37:59,8.1",
    "NGC 6572": "NGC 6572,f|G,18:12:06.4,+6:51:13,9.0",
    "NGC 6633": "NGC 6633,f|G,18:27:15.1,+6:30:30,4.6",
    "NGC 6712": "NGC 6712,f|G,18:53:04.3,-8:42:21,8.2",
    "NGC 6752": "NGC 6752,f|G,19:10:52.0,-59:59:04,5.4",
    "NGC 6826": "NGC 6826,f|G,19:44:48.2,+50:31:30,8.8",
    "NGC 6960 (Dentelles)": "NGC 6960,f|G,20:45:38.0,+30:43:00,7.0",
    "NGC 7000 (Amérique)": "NGC 7000,f|G,20:58:48.0,+44:20:00,4.0",
    "NGC 7009": "NGC 7009,f|G,21:04:10.9,-11:21:48,8.3",
    "NGC 7293 (Hélix)": "NGC 7293,f|G,22:29:38.6,-20:50:13,6.5",
    "NGC 7331": "NGC 7331,f|G,22:37:04.5,+34:25:01,9.5",
    "NGC 7479": "NGC 7479,f|G,23:04:56.7,+12:19:22,11.0",
    "NGC 7662": "NGC 7662,f|G,23:25:53.6,+42:32:06,8.6",
    "IC 5146 (Cocon)": "IC 5146,f|G,21:53:24.0,+47:16:00,7.2",
    "Barnard 86": "Barnard 86,f|G,18:02:48.0,-27:50:00,12.0",
    "NGC 6888 (Croissant)": "NGC 6888,f|G,20:12:06.5,+38:21:18,7.4"
}

# Étoiles doubles notables
extended_double_stars = {
    "Albireo": "Albireo,f|D|K3+B8,19:30:43.29,27:57:34.7,3.05|5.09",
    "Mizar & Alcor": "Mizar,f|D|A1+A2,13:23:55.54,54:55:31.3,2.23|4.0",
    "Epsilon Lyrae": "Epsilon Lyrae,f|D|A3+A5,18:44:20.00,39:40:12.0,4.7|4.6",
    "Alpha Centauri": "Alpha Centauri,f|D|G2+K1,14:39:36.50,-60:50:02.3,0.01|1.33",
    "Gamma Leonis": "Gamma Leonis,f|D|K0+G7,10:19:58.40,19:50:29.3,2.37|3.64",
    "Gamma Virginis": "Gamma Virginis,f|D|F0+F0,12:41:39.70,-01:26:57.8,3.47|3.47",
    "Almach": "Almach,f|D|K3+B9,02:03:54.00,42:19:47.0,2.3|5.0",
    "Castor": "Castor,f|D|A1+A5,07:34:35.90,31:53:18.0,1.93|2.97",
    "Cor Caroli": "Cor Caroli,f|D|A0+F0,12:56:01.70,38:19:06.0,2.89|5.60",
    "61 Cygni": "61 Cygni,f|D|K5+K7,21:06:53.90,38:44:57.9,5.21|6.03"
}

# Étoiles variables notables
extended_variable_stars = {
    "Algol": "Algol,f|V|B8,3:08:10.13,40:57:20.3,2.1|3.4",
    "Mira": "Mira,f|V|M7,2:19:20.79,-2:58:39.5,3.0|10.1",
    "Delta Cephei": "Delta Cephei,f|V|F5,22:29:10.27,58:24:54.7,3.5|4.4",
    "R Leonis": "R Leonis,f|V|M8,9:47:33.49,11:25:43.7,5.8|10.0",
    "Chi Cygni": "Chi Cygni,f|V|S6,19:50:33.92,32:54:50.6,3.3|14.2",
    "R Hydrae": "R Hydrae,f|V|M7,13:29:42.78,-23:16:52.8,3.5|10.9",
    "Beta Lyrae": "Beta Lyrae,f|V|B7,18:50:04.80,33:21:45.6,3.3|4.4",
    "R Coronae Borealis": "R CrB,f|V|G0,15:48:34.42,28:09:24.3,5.7|14.8",
    "Z Ursae Majoris": "Z UMa,f|V|M5,11:56:30.22,57:52:17.6,6.2|9.4",
    "SS Cygni": "SS Cygni,f|V|K5,21:42:42.80,43:35:09.9,8.0|12.4"
}

# Astéroïdes brillants
extended_asteroids = {
    "Vesta": "Vesta,f|A,variable,variable,5.1|8.5",  # Positions variables
    "Ceres": "Ceres,f|A,variable,variable,6.7|9.3",
    "Pallas": "Pallas,f|A,variable,variable,7.0|10.0",
    "Juno": "Juno,f|A,variable,variable,7.5|11.0",
    "Iris": "Iris,f|A,variable,variable,7.8|11.2"
}

# Comètes périodiques notables
extended_comets = {
    "Halley": "Halley,f|C,variable,variable,4.0|25.0",  # Variable
    "Encke": "Encke,f|C,variable,variable,7.0|13.0",
    "Swift-Tuttle": "Swift-Tuttle,f|C,variable,variable,5.0|20.0",
    "Tempel 1": "Tempel 1,f|C,variable,variable,8.0|14.0",
    "67P (Churyumov-Gerasimenko)": "67P,f|C,variable,variable,9.0|16.0"
}

# Régions d'intérêt (nébuleuses de taille apparente importante)
extended_regions = {
    "Voie Lactée (Centre)": "Voie Lactée,f|R,18:00:00.0,-30:00:00.0,4.0",
    "Grand Nuage de Magellan": "LMC,f|G,5:23:34.5,-69:45:22.0,0.4",
    "Petit Nuage de Magellan": "SMC,f|G,0:52:44.8,-72:49:43.0,2.7",
    "Nuage d'Amérique du Nord": "NGC 7000,f|G,20:58:48.0,+44:20:00,4.0",
    "Cintura de Gould": "Cintura de Gould,f|R,8:00:00.0,-20:00:00.0,0.0",
    "Boucle de Barnard": "Barnard Loop,f|N,5:48:00.0,+00:00:00.0,5.0",
    "Nuage Moléculaire du Taureau": "TMC,f|R,4:41:00.0,+25:52:00.0,0.0",
    "Région de Rho Ophiuchi": "Rho Ophiuchi,f|R,16:28:00.0,-24:30:00.0,4.0"
}


# Fonction pour charger les catalogues dans le programme principal
def load_extended_catalogs():
    """Charge les catalogues étendus dans le programme principal"""
    import celestial_database_extended
    import sys
    
    # Accéder aux variables globales du programme principal
    from __main__ import celestial_database, star_catalog, dso_catalog, categories
    
    # Complète les catalogues existants
    star_catalog.update(celestial_database_extended.extended_star_catalog)
    dso_catalog.update(celestial_database_extended.extended_dso_catalog)
    
    # Créer de nouveaux catalogues
    double_star_catalog = celestial_database_extended.extended_double_stars
    variable_star_catalog = celestial_database_extended.extended_variable_stars
    asteroid_catalog = celestial_database_extended.extended_asteroids
    comet_catalog = celestial_database_extended.extended_comets
    region_catalog = celestial_database_extended.extended_regions
    
    # Ajouter de nouvelles catégories au menu principal
    if "Étoiles doubles" not in categories:
        categories.append("Étoiles doubles")
        celestial_database["Étoiles doubles"] = list(double_star_catalog.keys())
        celestial_database["Étoiles doubles"].sort()
        
    if "Étoiles variables" not in categories:
        categories.append("Étoiles variables")
        celestial_database["Étoiles variables"] = list(variable_star_catalog.keys())
        celestial_database["Étoiles variables"].sort()
    
    if "Astéroïdes" not in categories:
        categories.append("Astéroïdes")
        celestial_database["Astéroïdes"] = list(asteroid_catalog.keys())
        celestial_database["Astéroïdes"].sort()
    
    if "Comètes" not in categories:
        categories.append("Comètes")
        celestial_database["Comètes"] = list(comet_catalog.keys())
        celestial_database["Comètes"].sort()
        
    if "Régions célestes" not in categories:
        categories.append("Régions célestes")
        celestial_database["Régions célestes"] = list(region_catalog.keys())
        celestial_database["Régions célestes"].sort()
    
    # Met à jour les listes dans celestial_database pour les catalogues existants
    all_stars = list(star_catalog.keys())
    all_dso = list(dso_catalog.keys())
    
    # Trier les listes par ordre alphabétique
    all_stars.sort()
    all_dso.sort()
    
    # Mise à jour de celestial_database
    celestial_database["Etoiles"] = all_stars
    celestial_database["Ciel profond"] = all_dso
    
    # Créer un dictionnaire global pour stocker tous les catalogues
    global_catalogs = {
        "Etoiles": star_catalog,
        "Ciel profond": dso_catalog,
        "Étoiles doubles": double_star_catalog,
        "Étoiles variables": variable_star_catalog,
        "Astéroïdes": asteroid_catalog,
        "Comètes": comet_catalog,
        "Régions célestes": region_catalog
    }
    
    # Rendre le dictionnaire global accessible depuis le programme principal
    # pour faciliter l'accès à tous les objets
    from __main__ import globals
    globals()['all_catalogs'] = global_catalogs
    
    print(f"Catalogues étendus chargés :")
    print(f"- {len(all_stars)} étoiles")
    print(f"- {len(all_dso)} objets du ciel profond")
    print(f"- {len(double_star_catalog)} étoiles doubles")
    print(f"- {len(variable_star_catalog)} étoiles variables")
    print(f"- {len(asteroid_catalog)} astéroïdes")
    print(f"- {len(comet_catalog)} comètes")
    print(f"- {len(region_catalog)} régions célestes")