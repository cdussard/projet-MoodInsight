from tkinter import *
import datetime
from time import ctime
import csv
now = datetime.datetime.now()
import pandas as pd
import numpy as np

root = Tk()
S = Scrollbar(root)
T = Text(root, height=4, width=50)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """Racontez ici votre souvenir du jour,\n
 essayez de développer sur vos émotions, et ce qui vous a fait les ressentir"""
T.insert(END, quote)

def callback():
    print("click!")
    print("file open")
    #----------------------------------------------------
    #write in a csv file
    file2=pd.read_csv('diary.csv', sep=';')
    dico = {'date': [ctime()], 'entry': [T.get("1.0", "end-1c")], 'score': 0.0}
    dfRow = pd.DataFrame.from_dict(dico)
    print(file2)
    file2 = file2.append(dfRow, ignore_index=True)
    file2.to_csv('diary.csv', sep=';', index=False)
    #-----------------------------------------------------
    #write in a txt file
    file = open('../journal.txt', 'a')
    file.write("\n"+ "Entrée du"+str(now))
    file.write("\n"+T.get("1.0", "end-1c"))
    print("written")
    file.close()
    print("file closed")
    #----------------------------------------------------
# bouton de sortie
bouton = Button(root, text="Enregistrer", command=callback)
bouton.pack()
mainloop()
