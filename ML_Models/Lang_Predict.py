###############################
##### Language Prediction #####
###  tanersezerr@gmail.com  ###
###############################
import os
import sys
# import pyfasttext
from pyfasttext import FastText

# Read File
f = open(sys.argv[1])
text = f.read()

# Load Model
model = FastText('Tr_or_Eng.bin')

# Convert file to single line
# so the model could process whole file as a whole


def single_line(text):
    for line in text:
        line.replace('\n', '')
    return line

# Get prediction for the given file


def predict(text):
    girdi = single_line(text)
    cats = (model.predict(girdi))
    return cats


print(predict(text))

# Get prediction for the file with probability rate


def predict_proba(text):
    girdi = single_line(text)
    cats_prob = (model.predict_proba(girdi))
    return cats_prob


print(predict_proba(text))
