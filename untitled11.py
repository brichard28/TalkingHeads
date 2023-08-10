# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 12:41:40 2023

@author: maana
"""

import random

possible_conditions = ["match left", "mismatch left", "match right", "mismatch right"]
trials_per_block = 10
blocks = []

# Define the trial combinations for each block
block_1_trials = ["match right", "match left"] * (trials_per_block // 2)
block_2_trials = ["mismatch right", "mismatch left"] * (trials_per_block // 2)
block_3_trials = ["match right", "match left", "mismatch right", "mismatch left"] 

# Combine the trial combinations for each block
blocks.append(block_1_trials)
blocks.append(block_2_trials)
blocks.append(block_3_trials)

# Shuffle the trials within each block
for block in blocks:
    random.shuffle(block)

# Print the generated blocks
for block_num, block in enumerate(blocks, start=1):
    print(f"Block {block_num}:")
    for trial in block:
        print(trial)
