# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 23:07:25 2023

@author: maana
"""

import numpy as np
# Define the AND gate truth table
X = np.array([[-1,0, 0],
              [-1,0, 1],
              [-1,1, 0],
              [-1,1, 1]])

# Desired output for the AND gate
y_true = np.array([0, 0, 0, 1])

# Initialize weights and learning rate
w = np.array([1, 2, 1])
alpha = 1

# Function to calculate the model prediction
def predict(x, weights):
    activation = np.dot(x, weights)
    return 1 if activation > 0 else 0

