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
    'subject Id': ['156973','159058','156028','157144','157837','160171','160093','160891','160927','160228','160090','160045','160339','160786','161134','160366','159763','161278','160009','160948'],
    'matched left': [96,94.66666667,93.33333333,82.66666667,94.66666667,89.33333333,97.33333333,92,93.33333333,100,92,93.33333333,82.66666667,96,97.33333333,85.33333333,93.33333333,100,88,92],
    'matched right': [98.66666667,100,90.66666667,80,100,85.33333333,100,97.33333333,96,94.66666667,86.66666667,94.66666667,94.66666667,97.33333333,90.66666667,73.33333333,96,93.33333333,78.66666667,93.33333333],
    'mismatched left': [77.33333333,77.33333333,92,76,94.66666667,74.66666667,78.66666667,90.66666667,69.33333333,54.66666667,81.33333333,64,78.66666667,70.66666667,56,41.33333333,81.33333333,65.33333333,33.33333333,66.66666667],
    'mismatched right': [77.33333333,88,84,90.66666667,81.33333333,74.66666667,85.33333333,78.66666667,89.33333333,72,56,44,72,89.33333333,74.66666667,37.33333333,82.66666667,77.33333333,45.33333333,76],
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
plt.title('Scores between subjects for Different test conditions(n=20)')

# Create the legend for scatter plots only
plt.legend()

plt.tight_layout()
plt.show()
