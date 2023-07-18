# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:38:00 2023

@author: maana
"""

from PIL import Image

# Dimensions of the image
width = 500
height = 300

# Create a blank image with white background
image1 = Image.new("RGB", (width, height), "white")
pixels1 = image1.load()
#image2 = Image.new("RGB", (width, height), "white")
#pixels2 = image2.load()
#image3 = Image.new("RGB", (width, height), "white")
#pixels3 = image3.load()
#image4 = Image.new("RGB", (width, height), "white")
#pixels4 = image4.load()
# Generate different color blocks
color1 = (255,255,255)   # white
#color2 = (0, 255, 0)   # Green
#color3 = (0, 0, 255)   # Blue
#color4 = (255,255,0)

# Draw the blocks on the image
for x in range(width):
    for y in range(height):
        if x < width:
            pixels1[x, y] = color1
#for x in range(width):
 #   for y in range(height):
  #      if x < width:
   #         pixels2[x, y] = color2
#for x in range(width):
 #   for y in range(height):
  #      if x < width:
   #         pixels3[x, y] = color3
#for x in range(width):
 #   for y in range(height):
  #      if x < width:
   #         pixels4[x, y] = color4
        

# Save the image


image1.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\colored_blocks_white.png")
#image2.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\colored_blocks_green.png")
#image3.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\colored_blocks_blue.png")
#image4.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\colored_blocks_yellow.png")