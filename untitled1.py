# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 08:24:46 2023

@author: maana
"""

import pandas 
import matplotlib.pyplot as plt
df = pandas.read_excel("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\Pilot score comparison.xlsx", sheet_name='Sheet1')

# Overall score plot

x1 = df['subject Id']
y1=df['overall score']
# Create scatter plot
plt.scatter(x1, y1)

# Add labels and title
plt.xlabel('Subject ID')
plt.ylabel('Overall correct score (%)')
plt.title('Overall score')

# Show plot
plt.show()

# Matched vs Mismatched 

y2=df['Matched_avg']
y3=df['Mismatched_avg']
plt.scatter(x1, y2,label='Matched')
plt.scatter(x1, y3,label='Mismatched')
# Add labels and title
plt.xlabel('Subject ID')
plt.ylabel('Correct score (%)')
plt.title('Matched vs Mismatch')
plt.legend()
# Show plot
plt.show()


# Right match vs Right mismatch
y4=df['matched right']
y5=df['mismatched right']
plt.scatter(x1, y4,label='Matched')
plt.scatter(x1, y5,label='Mismatched')
# Add labels and title
plt.xlabel('Subject ID')
plt.ylabel('Correct score (%)')
plt.title('Matched right vs Mismatch right')
plt.legend()
# Show plot
plt.show()

# left match vs left mismatch
y4=df['matched left']
y5=df['mismatched left']
plt.scatter(x1, y4,label='Matched')
plt.scatter(x1, y5,label='Mismatched')
# Add labels and title
plt.xlabel('Subject ID')
plt.ylabel('Correct score (%)')
plt.title('Matched left vs Mismatch left')
plt.legend()
# Show plot
plt.show()

