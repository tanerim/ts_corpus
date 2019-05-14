#################################################
###### TS_PosTagger API Python Interaction ######
######     Türker Sezer && Taner Sezer     ######
#################################################
import os
import sys
import pycurl
import simplejson as json
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import re

f = str(sys.argv[1])

# Convert input text to white-spaced text


def white(text):
    txt = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([<,.!";:]>)', r'\1 \2 ', text)
    return txt


url = 'https://nlp.tscorpus.com/api/parser/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, headers)
# print (r.text)
# print (white(text))
punctuations = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''

if not sys.stdout.isatty():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def postag(girdi):
    requsted_input = {"text": girdi, "fields": "postag"}
    postag = ((requests.post(url, requsted_input, headers)).text)
    fetched_result = postag.strip(punctuations)
    gen_output = re.sub(r'^.*\"', '', fetched_result)
    if gen_output == " No_Lemma":
        gen_output = girdi
    return gen_output


def d_tag(girdi):
    requsted_input = {"text": girdi, "fields": "tag"}
    postag = ((requests.post(url, requsted_input, headers)).text)
    fetched_result = postag.strip(punctuations)
    gen_output = re.sub(r'^.*\"', '', fetched_result)
    if gen_output == " No_Lemma":
        gen_output = girdi
    return gen_output


def lemma(girdi):
    requsted_input = {"text": girdi, "fields": "lemma"}
    lemmas = ((requests.post(url, requsted_input, headers)).text)
    fetched_result = lemmas.strip(punctuations)
    gen_output = re.sub(r'^.*\"', '', fetched_result)
    if gen_output == "No_Lemma":
        gen_output = girdi
    else:
        gen_output == fetched_result
    return gen_output


def morph(girdi):
    requsted_input = {"text": girdi, "fields": "morph"}
    morph = ((requests.post(url, requsted_input, headers)).text)
    fetched_result = morph.strip(punctuations)
    gen_output = re.sub(r'^.*\"', '', fetched_result)
    if gen_output == " No_Lemma":
        gen_output = girdi
    return gen_output

# for line in text:
#    clean = white(line)
#    gen_output = []
#    gen_output.append(lemma(clean))
#    print (gen_output[0])


print("PosTag: ", postag(f))
print("Derived_From: ", d_tag(f))
print("Lemma: ", lemma(f))
print("Moph: ", morph(f))
