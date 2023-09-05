#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 21:20:51 2023

@author: jeremybenik
"""



# %%
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import glob
import imageio


# Load and preprocess data
df = pd.read_csv('/Users/jeremybenik/Hilary_photos/data_files/data.csv')
temp = np.array((df['Temperature_BMP180'] * 1.8000) + 32.00)
pres = np.array(df['Sealevel_Pressure_hPa'])
aaa = [datetime.datetime.strptime(str(dt), "%Y-%m-%d_%H-%M-%S") for dt in df['Date_Time']]
df_datetime = [dt.strftime("%Y-%m-%d_%H-%M-%S") for dt in aaa]

images = []
image_paths =  sorted(glob.glob("/Users/jeremybenik/Hilary_photos/updated_test_photos" + '/*.png'))

num_frames = len(image_paths)
time_series_data = np.linspace(0, num_frames, num_frames)
plot_data = np.random.rand(num_frames) * 10
# Initialize lists to store frames and image objects
frames = []
images = [Image.open(image_path) for image_path in image_paths]
new_temp = []
new_date = []
new_pres = []
# Initialize images list
# Initialize images list
images = []

# Replace the loop that populates images with the correct paths
for i in range(len(image_paths)):
    image_data = np.array(Image.open(image_paths[i]))
    images.append(image_data)
    current_datetime = datetime.datetime.strptime(image_paths[i][-31:-12], "%Y-%m-%d_%H-%M-%S")
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    printed_datetime = current_datetime.strftime("%m/%d/%Y %H:%M:%S PDT")
    location = np.where([formatted_datetime == x for x in df_datetime])[0][0]
    new_temp.append(temp[location])
    new_date.append(df_datetime[location])
    new_pres.append(pres[location])


new_dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S") for date_str in new_date]
new_date2 = [dt.strftime("%m/%d/%Y %H:%M") for dt in new_dates]
new_date = list(new_date2)
# %%
# Create figure and subplots
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[1.4, 1.1])
# Left plot
ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])

ax1.axis('off')
ax3.set_xlabel("Date", fontsize = 12, fontweight = 'bold')
ax2.set_ylabel("Temperature ($^\circ$F)", fontsize = 12, fontweight = 'bold')
ax3.set_ylabel("Pressure (hPa)", fontsize = 12, fontweight = 'bold')
ax2.set_title("Dynamic Temperature Plot", fontsize = 18, fontweight = 'bold')
ax3.set_title("Dynamic Pressure Plot", fontsize = 18, fontweight = 'bold')

ax2.grid()
ax3.grid()

# Initialize image plot on the left
img_plot = ax1.imshow(images[0])
ax1.axis('off')

# Initialize temperature plot on the right
line_temp, = ax2.plot([], [], marker='o', color='blue')
line_pres, = ax3.plot([], [], marker='o', color='red')

ax2.set_ylim(min(new_temp), max(new_temp))
ax2.set_xlim(0, num_frames)

num_labels = 5
ax3.set_xlim(0, num_frames)
ax3.set_ylim(min(new_pres), max(new_pres))
# Update function for temperature plot
def update_temp(frame):
    line_temp.set_data(np.arange(frame + 1), new_temp[:frame + 1])
    return line_temp,

def update_pres(frame):
    line_pres.set_data(np.arange(frame + 1), new_pres[:frame + 1])
    return line_pres,
# Set x-axis tick labels for the image plot
# ax1.set_xticks([frame])
# ax3.set_xticklabels(new_date, rotation=45)

ax3.set_xticklabels(new_date2[::num_frames//num_labels], rotation=45, fontsize = 10)
ax2.set_xticklabels([])
output_folder = "/Users/jeremybenik/Hilary_photos/final_photos"
# Update the plots within a loop

for frame in range(num_frames):
    img_path = image_paths[frame]
    try:
        img = Image.open(img_path)
        img_data = np.array(img)
        img_plot.set_data(img_data)
        # Update the image plot
        img_path = image_paths[frame]  # Get the path to the image file
        img = Image.open(img_path)
        img_data = np.array(img)
        img_plot.set_data(img_data)
        
        # Update the temperature plot
        update_temp(frame)
        update_pres(frame)
    
        formatted_datetime = new_dates[frame]  # Get the current date for the filename
        output_filename = f"{formatted_datetime}_final.png"
        output_path = os.path.join(output_folder, output_filename)
        
        # Save the current frame
        plt.savefig(output_path)
        
        plt.pause(0.1)
    except OSError as e:
        print(f"Error reading image file: {img_path}")
        print(e)
        continue
# Close the figure after saving all the frames
plt.close(fig)