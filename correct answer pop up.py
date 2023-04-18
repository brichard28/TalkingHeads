# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 14:36:09 2023

@author: maana
"""
import pandas as pd
import tkinter as tk
right_answer= pd.read_csv("C:\\Users\\maana\\Desktop\\New folder\\Answerkey.csv")
right_answer= right_answer.iloc[:,1:6].values.tolist()
a=['William','orders','sixty','pretty','desks']
num_correct=0
itrial=0
for i in range(5):
    if a[i] == right_answer[itrial][i]:
        num_correct += 1
a1=str(num_correct)+" out of 5 words correct"
        
textbox = tk.Tk()
textbox.eval('tk::PlaceWindow . center')
textbox.geometry("300x100")
label = tk.Label(textbox, text=a1)
label.pack()
textbox.update()
textbox.mainloop()     