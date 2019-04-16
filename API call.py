# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:06:30 2019

@author: cldus
"""

#The ToneAnalyzer class from WDC
from watson_developer_cloud import ToneAnalyzerV3

#Pandas for data handling
import pandas as pd
import numpy as np
import os
import json
#Time class to measure the time taken
import time
#--------------------------------------------------------------
print(os.getcwd())

#Read the diary data
diaryTxt2 = pd.read_csv('diary.csv', sep=";")
dataDiary = pd.read_csv('data.csv', sep=',')
print(dataDiary)
print(diaryTxt2)

#Make a copy of 100 rows for smaller testing
#small_data = data.head(100).copy()
small_diary = diaryTxt2   #.head(10).copy()
print(small_diary)
#To view the documentation
#print(help(ToneAnalyzerV3))

#-------------------------------------------------------------------------
#Instantiate TA Object with your Credentials
#-------------------------------------------------------------------------
tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  iam_apikey='2SBzgSzZu_dY98BsVBFjLOEthY7d4QazSuAq_fWkAkF-',
  url='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
)

#Get the current time on the clock
time_start = time.process_time()

#------------------------------------------------------------------------
#Infer the mood of the data
#------------------------------------------------------------------------


def findFirstIndex():
    firstIndex = 0
    scoreIndex = dataDiary.at[0, 'score']
    while scoreIndex != 0.0 and firstIndex < len(dataDiary.index)-1:
        print(scoreIndex, firstIndex)
        firstIndex = firstIndex + 1
        scoreIndex = dataDiary.at[firstIndex, 'score']
    return firstIndex


def tone_handlerDoc(json_output_fct):
    number_tones_fct = len(json_output_fct["document_tone"]["tones"])
    print(str(number_tones_fct) + "tones found")
    global maximum
    global moodToWrite
    global scoreToWrite
    maximum = 0
    for index in range(0, number_tones_fct):
        print("index="+str(index))
        scoreI = json_output_fct["document_tone"]["tones"][index]["score"]
        if scoreI > maximum:
            maximum = scoreI
            moodToWrite = json_output_fct["document_tone"]["tones"][index]["tone_id"]
        if maximum == 0:
            print("error ; maximumToneScore was 0")
        else:
            scoreToWrite = maximum


def tone_handlerSentence(json_outputfct2,sentenceIndex):
    global maximum
    global moodToWrite
    global scoreToWrite
    number_tones_fct2 = len(json_outputfct2["sentences_tone"][sentenceIndex]["tones"])
    for index2 in range(0, number_tones_fct2):
        scoreI2 = json_outputfct2["sentences_tone"][sentenceIndex]["tones"][index2]["score"]
        if scoreI2 > maximum:
            maximum = scoreI2
            moodToWrite = json_outputfct2["sentences_tone"][sentenceIndex]["tones"][index2]["tone_id"]
    if maximum == 0:
        print("error ; maximumToneScore was 0")
    else:
        scoreToWrite = maximum

def diaryAnalysis():
    global moodToWrite
    global scoreToWrite
    global maximum
    maximum = 0
    startIndex = findFirstIndex()
    print("Longueur du journal :" + str(len(small_diary)))
    for i in range(startIndex, len(small_diary)):
        maximum = 0  # remise a 0 pour eviter une valeur residuelle
        entry = small_diary.at[i, 'entry']
        print(entry)
        json_output = tone_analyzer.tone(entry, content_type='text/plain', content_language='fr').get_result()
        print(json.dumps(json_output, indent=2))
        moodToWrite = 'null'
        scoreToWrite = -1
        null_json = {"document_tone": {"tones": []}}
        if json_output == null_json:
            # no mood found
            moodToWrite = "neutral"
        elif "sentences_tone" not in json_output:  # only one sentence with a mood found
            tone_handlerDoc(json_output)
            print("one sentence with mood " + moodToWrite + "score" + str(scoreToWrite))
        else:  # multiple sentences
            number_sentences = json.dumps(json_output).count("sentence_id")
            print(str(number_sentences) + " phrases")
            tone_handlerDoc(json_output)
            for j in range(0, number_sentences - 1):
                tone_handlerSentence(json_output, j)
            if maximum == 0:
                print("error ; maximumToneScore was 0")

        small_diary.at[i, 'mood'] = moodToWrite
        moodToWrite = "null"
        small_diary.at[i, 'score'] = scoreToWrite
        scoreToWrite = 0.0  # Traitement par ref évite confusion par remise a 0
        print(small_diary)
    #small_diary.at[len(small_diary)+1, 'mood'] = "here"
    #small_diary.at[len(small_diary)+1, 'score'] = len(small_diary)+1

diaryAnalysis()


def lineAnalysis(json):
    global moodToWrite
    global scoreToWrite
    global maximum
    maximum = 0  # remise a 0 pour eviter une valeur residuelle
    json_output = json
    moodToWrite = 'null'
    scoreToWrite = -1
    null_json = {"document_tone": {"tones": []}}
    if json_output == null_json:
        # no mood found
        moodToWrite = "neutral"
    elif "sentences_tone" not in json_output:  # only one sentence with a mood found
        tone_handlerDoc(json_output)
    else:  # multiple sentences
        number_sentences = json.dumps(json_output).count("sentence_id")
        tone_handlerDoc(json_output)
        for j in range(0, number_sentences - 1):
            tone_handlerSentence(json_output, j)
        if maximum == 0:
            print("error ; maximumToneScore was 0")
    json_return = {
        'score': scoreToWrite,
        'mood': moodToWrite
    }
    return json_return


#Get the current time again and subract from
#previous to measure the time taken
time_end = time.process_time() - time_start

#Print the time taken
print(time_end)

#Save the enriched data to another CSV File
small_diary.to_csv('data.csv')
