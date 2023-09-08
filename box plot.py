# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:10:03 2023

@author: maana
"""


import pandas as pd
import matplotlib.pyplot as plt

# Your DataFrame
df = pd.DataFrame({
    'subject Id': ['pilot725-1', 'pilot821-1', 'pilot822-1', 'pilot823-1'],
    'aligned': [94.16666667, 82.5, 95, 95.83333333],
    'misaligned': [97.5, 84.16666667, 63.33333333, 95.83333333]
})

# Create a box plot
plt.figure(figsize=(8, 6))  # Optional: Adjust the figure size

# Plot "aligned" and "misaligned" as box plots in the same figure
plt.boxplot([df['aligned'], df['misaligned']], labels=['Aligned', 'Misaligned'])
plt.xticks(fontsize=15)


# Add labels and title
plt.xlabel('Conditions',fontsize=20)
plt.ylabel('Mean Scores(%)',fontsize=20)
plt.title('Box Plot of Aligned vs. Misaligned Scores',fontsize=20)

# Show the plot
plt.show()
