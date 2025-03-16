#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 08:14:21 2025

@author: mecatrolab

Ce programme permet de changer la date des fichiers situés dans le dossier indiqué par le chemin d'accès
"""

from PIL import Image
import piexif
import datetime
from pathlib import Path


def get_all_file_paths(directory):
    """Fonction permettant de lister les chemins d'accès des fichiers dans un dossier directory.
    INPUT :
        directory : STR : chemin d'accès du dossier
    OUTPUT :
        file : list : liste des chemins d'accès sous forme de str
    """
    return [str(file) for file in Path(directory).rglob("*") if file.is_file()]

def change_photo_date(image_path, new_date):
    """Fonction permettant de changer la date d'un fichier indiquée dans new_date, dont le chemin d'accès est image_path.
    INPUT :
        image_path : STR : chemin d'accès du fichier
        new_date : datetime : nouvelle date du fichier
    OUTPUT :
        None
    """
    img = Image.open(image_path)    # Charger l'image
    
    exif_dict = piexif.load(img.info.get("exif", b""))  # Charger les métadonnées EXIF
    
    # Récupérer l'heure actuelle pour conserver l'heure d'origine
    if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
        original_datetime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode()
        original_time = original_datetime.split(" ")[1]  # Extraire l'heure
    else:
        original_time = "00:00:00"  # Si aucune heure trouvée, mettre minuit
    
    # Formatage de la nouvelle date avec l'heure d'origine
    formatted_date = f"{new_date.strftime('%Y:%m:%d')} {original_time}"
    
    # Modifier les champs de date
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date.encode()
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date.encode()
    
    # Convertir les métadonnées en bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Sauvegarder l'image avec les nouvelles métadonnées
    img.save(image_path, "jpeg", exif=exif_bytes)
    print(f"Date changée avec succès en {formatted_date} pour {image_path}")

# Obtention des chemins d'accès
directory = "/Users/merilcrouzet/Documents/MAUVAISE_DATE"
files = get_all_file_paths(directory)

files_number = len(files)
file_number = 1

for image_path in files :
    if ".DS_Store" not in image_path :
        new_date = datetime.datetime(2025, 2, 3)  # Nouvelle date
        change_photo_date(image_path, new_date)
        print(f"Photo {file_number} sur {files_number}")
        file_number += 1
