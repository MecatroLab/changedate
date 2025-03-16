#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 08:02:07 2025

@author: mecatrolab
"""

import datetime
import piexif
import subprocess
from PIL import Image
from pathlib import Path


def get_all_file_paths(directory):
    """Récupère tous les fichiers d'un dossier et sous-dossiers."""
    return [str(file) for file in Path(directory).rglob("*") if file.is_file()]


def change_photo_date(image_path, new_date, file_number, file_number_total):
    """Modifie la date des métadonnées EXIF d'une photo."""
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info.get("exif", b""))
    
    original_time = "00:00:00"
    if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
        original_datetime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode()
        original_time = original_datetime.split(" ")[1]
    
    formatted_date = f"{new_date.strftime('%Y:%m:%d')} {original_time}"
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date.encode()
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date.encode()
    
    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, "jpeg", exif=exif_bytes)
    print(f"Date changée pour {image_path} fichier n°{file_number} / {file_number_total}")

def change_video_date(video_path, new_date, file_number, file_number_total):
    """Modifie la date de création d'une vidéo avec ffmpeg."""
    formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    temp_file = video_path + ".temp.mp4"
    
    # Utilise le chemin de l'exécutable ffmpeg ici
    FFMPEG_PATH = "/usr/local/bin/ffmpeg"  # Assure-toi que ce soit le bon chemin de ffmpeg

    command = [FFMPEG_PATH, "-i", video_path, "-metadata", f"creation_time={formatted_date}",
    "-codec", "copy", temp_file]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    Path(temp_file).replace(video_path)
    print(f"Date changée pour {video_path} fichier n°{file_number} / {file_number_total}")


def process_files(directory, new_date):
    files = get_all_file_paths(directory)
    file_number = 1
    file_number_total = len(files)
    for file_path in files:
        ext = Path(file_path).suffix.lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            change_photo_date(file_path, new_date, file_number, file_number_total)
        elif ext in [".mp4", ".mov", ".avi"]:
            change_video_date(file_path, new_date, file_number, file_number_total)
        else:
            print(f"Format non supporté : {file_path}")
        file_number += 1

# Paramètres
directory = "/Users/merilcrouzet/Library/CloudStorage/OneDrive-Personnel/MAUVAISE_DATE"
new_date = datetime.datetime(2025, 3, 3) #Date sous la forme AAAA MM JJ
process_files(directory, new_date)
