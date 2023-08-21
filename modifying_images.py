#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:41:19 2023

@author: jeremybenik
"""

from PIL import Image, ImageDraw, ImageFont
import datetime
import imageio
import pandas as pd
import numpy as np
import glob
import os
import subprocess
import matplotlib.pyplot as plt

# Load and preprocess data
df = pd.read_csv('/Users/jeremybenik/Hilary_photos/data_files/data.csv')
temp = np.array((df['Temperature_BMP180'] * 1.8000) + 32.00)
pres = np.array(df['Sealevel_Pressure_hPa'])
aaa = [datetime.datetime.strptime(str(dt), "%Y-%m-%d_%H-%M-%S") for dt in df['Date_Time']]
df_datetime = [dt.strftime("%Y-%m-%d_%H-%M-%S") for dt in aaa]

# Load image
image_path = "/Users/jeremybenik/Hilary_photos/photos"
filenames = sorted(glob.glob(image_path + '/*.png'))
output_folder = "/Users/jeremybenik/Hilary_photos/updated_test_photos"
# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)


plt.plot(df_datetime, temp)
plt.xticks(df_datetime[::300], rotation = 45)
# %%
# List all files in the directory
files_in_directory = os.listdir(output_folder)

# Iterate through the files and remove PNG files
for file in files_in_directory:
    if file.lower().endswith(".png") or file.lower().endswith(".gif"):
        file_path = os.path.join(output_folder, file)
        try:
            os.remove(file_path)
            print(f"{file_path} deleted successfully.")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
            
for file in filenames:
    print(file)
    current_datetime = datetime.datetime.strptime(file[-23:-4], "%Y-%m-%d_%H-%M-%S")
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    printed_datetime = current_datetime.strftime("%m/%d/%Y %H:%M:%S PDT")

    try:
        location = np.where([formatted_datetime == x for x in df_datetime])[0][0]
        image = Image.open(file)
        draw = ImageDraw.Draw(image)
        
        # Load the default font
        default_font = ImageFont.load_default()
        
        # Increase the font size for the default font
        font_size = 24
        larger_font = ImageFont.truetype("/Users/jeremybenik/Downloads/times-new-roman.ttf", font_size)
        
        text_color = (255, 255, 255)
        
        # Draw date and time
        draw.text((20, image.height - 30), printed_datetime, font=larger_font, fill=text_color)
        
        # Draw temperature and pressure
        Temp_text = f' Temperature: {round(temp[location], 1)}°F'
        Pressure_text = f' Pressure: {round(pres[location], 1)} hPa'
        draw.text((15, 30), Temp_text, font=larger_font, fill=text_color)
        draw.text((15, 5), Pressure_text, font=larger_font, fill=text_color)
        
        # Draw watermark
        watermark_text = "@Jeremy_Benik_Wx"
        watermark_font = ImageFont.load_default()
        watermark_color = (255, 255, 255)
        font_size = 18
        larger_font = ImageFont.truetype("/Users/jeremybenik/Downloads/times-new-roman.ttf", font_size)
        
        draw.text((image.width - 90 - watermark_font.getsize(watermark_text)[0], image.height - 30), watermark_text, font=larger_font, fill=watermark_color)
        
        # Save the modified image
        output_filename = f"{formatted_datetime}_updated.png"
        output_path = os.path.join(output_folder, output_filename)
        image.save(output_path)
    except Exception:
        pass

print('Converting them to a gif')

# Set the input directory containing PNG images
input_directory = output_folder

# Set the output GIF file path
output_gif_path = "/Users/jeremybenik/Hilary_photos/updated_test_photos/animation.gif"

# Get a list of all PNG files in the input directory
png_files = [f for f in os.listdir(input_directory) if f.endswith(".png")]

# Sort the list of files
png_files.sort()

# Create a list to hold the image frames
image_frames = []

# Load each PNG image and add it to the list of frames
for png_file in png_files:
    image_path = os.path.join(input_directory, png_file)
    image_frames.append(imageio.imread(image_path))

# Save the frames as a GIF without compression
imageio.mimsave(output_gif_path, image_frames, format="GIF", duration=0.02)
