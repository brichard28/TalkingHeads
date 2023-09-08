# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:29:03 2023

@author: maana
"""



import pandas as pd
import matplotlib.pyplot as plt

# Create a sample dataframe
df = pd.DataFrame({
    'subject Id': ['pilot002', '419_pilot2', '419_pilot3', '419_pilot4','419_pilot5'],
    'matched right': [93.33333333, 91.66666667, 78.33333333, 91.66666667,93.33333333],
    'matched left': [90, 98.33333333, 93.33333333, 100,100],
    'mismatched right': [56.66666667, 80, 66.66666667, 98.33333333,91.66666667],
    'mismatched left': [88.33333333, 93.33333333, 80, 100,98.33333333],
    
})

# Set the subject Id column as the index
df.set_index('subject Id', inplace=True)

# Create a scatter plot for each subject Id
for subject in df.index:
    plt.scatter(df.columns, df.loc[subject], label=subject)
    plt.plot(df.columns, df.loc[subject], label=subject)
    
plt.xlabel('Test Conditions')
plt.ylabel('Scores(%)')
plt.title('Scores between subjects for Different test conditions')

plt.show()

df2= pd.DataFrame({
    'subject Id': ['pilot002', '419_pilot2', '419_pilot3', '419_pilot4','419_pilot5'],
    'matched cases':[91.66666667,95,85.83333333,95.83333333,96.66666667],
    'mismatched cases':[72.5,86.66666667,73.33333333,99.16666667,95]
    })
df2.set_index('subject Id', inplace=True)

# Create a scatter plot for each subject Id
for subject in df2.index:
    plt.scatter(df2.columns, df2.loc[subject], label=subject)
    plt.plot(df2.columns, df2.loc[subject], label=subject)
plt.xlabel('Test Conditions')
plt.ylabel('Scores(%)')
plt.title('Scores between subjects for Different test conditions')
plt.show()