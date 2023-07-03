# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:07:48 2023

@author: maana
"""

from PIL import Image, ImageDraw

# Set the size of each block and the dimensions of the grid
block_size = 50
grid_width = 5
grid_height = 5

# Create a new image with the desired size
image_width = grid_width * block_size
image_height = grid_height * block_size
image = Image.new("RGB", (image_width, image_height))

# Create a draw object to manipulate the image
draw = ImageDraw.Draw(image)

# Define the patterns and their respective colors
patterns = [
    ("solid", (255, 0, 0)),       # Solid red
    ("horizontal", (0, 255, 0)),  # Horizontal green stripes
    ("vertical", (0, 0, 255)),    # Vertical blue stripes
    ("diagonal", (255, 255, 0)),  # Diagonal yellow stripes
]

# Iterate over the grid
for x in range(grid_width):
    for y in range(grid_height):
        # Calculate the position of the current block
        block_x = x * block_size
        block_y = y * block_size

        # Get the current pattern and color
        pattern, color = patterns[(x + y) % len(patterns)]

        # Draw the block using the pattern and color
        if pattern == "solid":
            draw.rectangle([(block_x, block_y), (block_x + block_size, block_y + block_size)], fill=color)
        elif pattern == "horizontal":
            for i in range(block_y, block_y + block_size, 5):
                draw.line([(block_x, i), (block_x + block_size, i)], fill=color)
        elif pattern == "vertical":
            for i in range(block_x, block_x + block_size, 5):
                draw.line([(i, block_y), (i, block_y + block_size)], fill=color)
        elif pattern == "diagonal":
            for i in range(block_size):
                draw.line([(block_x + i, block_y), (block_x, block_y + i)], fill=color)

# Save the image
image.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\patterned_blocks.png")