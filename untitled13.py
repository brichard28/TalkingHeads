# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:01:12 2023

@author: maana
"""

from PIL import Image, ImageDraw

# Set the size of each square and the dimensions of the checkerboard
square_size = 40
board_width = 5
board_height = 5

# Create a new image with the desired size
image_width = board_width * square_size
image_height = board_height * square_size
image = Image.new("RGB", (image_width, image_height))

# Create a draw object to manipulate the image
draw = ImageDraw.Draw(image)

# Define the colors for the two alternating squares
color1 = (255, 255, 255)  # White
color2 = (0, 0, 0)        # Black

# Iterate over the checkerboard
for x in range(board_width):
    for y in range(board_height):
        # Calculate the position of the current square
        square_x = x * square_size
        square_y = y * square_size

        # Determine the color of the square based on its position
        if (x + y) % 2 == 0:
            color = color2
        else:
            color = color1

        # Draw the square
        draw.rectangle([(square_x, square_y), (square_x + square_size, square_y + square_size)], fill=color)

# Save the image
image.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\checkerboard2.png")