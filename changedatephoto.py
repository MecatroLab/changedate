#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 08:14:21 2025

@author: mecatrolab

This program allows you to change the date of photos located in the folder indicated by the path.
"""

from PIL import Image
import piexif
import datetime
from pathlib import Path


def get_all_file_paths(directory):
    """Function to list the paths of files in a directory folder.
    INPUT :
        directory : STR : path to the folder
    OUTPUT :
        file : list : list of paths
    """
    return [str(file) for file in Path(directory).rglob("*") if file.is_file()]

def change_photo_date(image_path, new_date):
    """Function to change the date of a file specified in new_date, whose path is image_path.
    INPUT :
        image_path : STR : path to the folder
        new_date : datetime : new date for the file
    OUTPUT :
        None
    """
    img = Image.open(image_path)    # Load image
    
    exif_dict = piexif.load(img.info.get("exif", b""))  # Load metadata EXIF
    
    # Retrieve the current time to keep the original time
    if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
        original_datetime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode()
        original_time = original_datetime.split(" ")[1]  # Extract hour
    else:
        original_time = "00:00:00"  # If no hour found, set to midnight
    
    # Formatting the new date with the original time
    formatted_date = f"{new_date.strftime('%Y:%m:%d')} {original_time}"
    
    # Change date data
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date.encode()
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date.encode()
    
    # Convert metadata into bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save image with the new date
    img.save(image_path, "jpeg", exif=exif_bytes)
    print(f"Date changée avec succès en {formatted_date} pour {image_path}")


directory = "Path/to/folder"    #Enter here the path to your files' folder
files = get_all_file_paths(directory)

files_number = len(files)
file_number = 1

for image_path in files :
    if ".DS_Store" not in image_path :
        new_date = datetime.datetime(2025, 2, 3)  #New date YYYY MM DD
        change_photo_date(image_path, new_date)
        print(f"Photo {file_number} sur {files_number}")
        file_number += 1
