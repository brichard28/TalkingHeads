# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:57:57 2023

@author: maana
"""

from PIL import Image, ImageDraw

# Set the size of the block
block_size = 200

# Create a new image with the desired size
image = Image.new("RGB", (block_size, block_size))

# Create a draw object to manipulate the image
draw = ImageDraw.Draw(image)

# Draw the top half of the block in white
draw.rectangle([(0, 0), (block_size, block_size // 2)], fill=(255, 255, 255))

# Draw the bottom half of the block in black
draw.rectangle([(0, block_size // 2), (block_size, block_size)], fill=(0, 0, 0))

# Save the image
image.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\half_white_half_black.png")



# Draw the left half of the block in white
draw.rectangle([(0, 0), (block_size // 2, block_size)], fill=(255, 255, 255))

# Draw the right half of the block in black
draw.rectangle([(block_size // 2, 0), (block_size, block_size)], fill=(0, 0, 0))

# Save the image
image.save("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\half_white_half_black_vertical.png")
