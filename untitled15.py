# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:09:09 2023

@author: maana
"""

from PIL import Image, ImageDraw

# Set the size of each square and the dimensions of the pattern
square_size = 40
pattern_width = 5
pattern_height = 5

# Create a new image with the desired size
image_width = pattern_width * square_size
image_height = pattern_height * square_size
image = Image.new("L", (image_width, image_height))

# Create a draw object to manipulate the image
draw = ImageDraw.Draw(image)

# Iterate over each square in the pattern
for x in range(pattern_width):
    for y in range(pattern_height):
        # Calculate the position of the current square
        square_x = x * square_size
        square_y = y * square_size

        # Determine the color of the square based on its position
        if (x + y) % 2 == 0:
            color = 255  # White
        else:
            color = 0  # Black

        # Calculate the coordinates of the diamond shape
        x1 = square_x + square_size // 2
        y1 = square_y
        x2 = square_x + square_size
        y2 = square_y + square_size // 2
        x3 = square_x + square_size // 2
        y3 = square_y + square_size
        x4 = square_x
        y4 = square_y + square_size // 2

        # Create a list of points for the diamond shape
        diamond_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        # Draw the diamond shape
        draw.polygon(diamond_points, fill=color)

# Save the image
image.save("diamond_pattern.png")
