#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 08:02:07 2025

@author: MecatroLab

This program allows you to change the date of photos and videos located in the folder indicated by the path.
"""

import datetime
import piexif
import subprocess
from PIL import Image
from pathlib import Path


def get_all_file_paths(directory):
    """Function that lists the paths of files in a directory folder.
    INPUT :
        directory : STR : path to the folder
    OUTPUT :
        file : list : list of paths
    """
    return [str(file) for file in Path(directory).rglob("*") if file.is_file()]


def change_photo_date(image_path, new_date, file_number, file_number_total):
    """Function to change the date of a file specified in new_date, whose path is image_path.
    INPUT :
        image_path : STR : path to the folder
        new_date : datetime : new date for the file
        file_number : INT : number of the file
        file_number_total : INT : number total of files in the folder
    OUTPUT :
        None
    """
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
    """Change the creation date of a video using ffmpeg.
    INPUT :
        image_path : STR : path to the folder
        new_date : datetime : new date for the file
        file_number : INT : number of the file
        file_number_total : INT : number total of files in the folder
    OUTPUT :
        None
    """
    formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    temp_file = video_path + ".temp.mp4"
    
    FFMPEG_PATH = "/usr/local/bin/ffmpeg"  # Enter here the path of your ffmeg on your computer, depending of your OS

    command = [FFMPEG_PATH, "-i", video_path, "-metadata", f"creation_time={formatted_date}",
    "-codec", "copy", temp_file]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    Path(temp_file).replace(video_path)
    print(f"Date changée pour {video_path} fichier n°{file_number} / {file_number_total}")


def process_files(directory, new_date):
    """Process each files from the directory, exclude files that are not photos or videos.
    INPUT :
        directory : STR : path to the folder
        new_date : datetime : new date for the file
    OUTPUT :
        None
    """
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

# Main
directory = "Path/to/folder"             # Enter here the path to your files' folder
new_date = datetime.datetime(2025, 3, 3) # Date YYYY MM DD
process_files(directory, new_date)
