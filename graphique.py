#Pandas for data handling
import pandas as pd
#Matplotlib to draw the graph
import matplotlib as plt
import matplotlib.pyplot as pyplot
#Time class to measure the time taken
import datetime
from time import ctime

data = pd.read_csv('data.csv', sep=',') #if diary (sep=;) if help (sep=,)
print(data)

#collect score = Y  for each mood
#collect date = X

moods = ["sadness", "joy", "fear", "analytical", "anger", "confident", "tentative", "neutral"]

n = len(data.index)
rightData = data[['date', 'mood', 'score']] #get the entries out
sortedData = rightData.sort_values(by=['mood'])
clearedData = sortedData.dropna()
noIndexData = clearedData.reset_index(drop=True)
print(clearedData)

print(noIndexData.loc[0, :].to_frame())

yo=pd.DataFrame()

yo = yo.append(noIndexData.loc[0, :].to_frame())
sadnessDF = noIndexData[noIndexData.mood == 'sadness']#example for sadness

print(sadnessDF)
print(type(sadnessDF['date'].tolist()))
dates = sadnessDF['date']#convert the dates so they can be plotted in a graph
rightDates=pd.to_datetime(dates)
scores = sadnessDF['score']
pyplot.plot(rightDates, scores)
pyplot.show()

