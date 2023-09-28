# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 17:35:18 2023

@author: maana
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 09:27:46 2023

@author: maana
"""
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample dataframe
df = pd.DataFrame({
    'subject Id': ['new_pilot1', 'new_pilot2','new_pilot4','new_pilot5'],
    'aligned right': [98.33333333,100,88.33333333,83.33333333],
    'aligned left': [100,98.33333333,71.66666667,100],
    'misaligned right': [98.33333333,96.66666667,83.33333333,96.66666667],
    'misaligned left': [98.33333333,100,80,100],
})

# Set the subject Id column as the index
df.set_index('subject Id', inplace=True)

# Calculate the standard error for each group
std_error = df.sem()

# Create a scatter plot for each subject Id
for subject in df.index:
    #.scatter(df.columns, df.loc[subject],color='grey')  # Scatter plot in blue
    plt.plot(df.columns, df.loc[subject], color='grey')  # Line plot in blue

# Add error bars
for i, col in enumerate(df.columns):
    plt.errorbar(col, df.mean()[col], yerr=std_error[col], color='black',capsize=5)
# Create a line plot for group means with same color
plt.scatter(df.columns, df.mean(), color='blue',linewidth=2)

plt.xlabel('Test Conditions')
plt.ylabel('Mean Scores(%)')
plt.title('Scores between subjects for Different test conditions')

# Create the legend for scatter plots only
plt.legend()

plt.tight_layout()
plt.show()
