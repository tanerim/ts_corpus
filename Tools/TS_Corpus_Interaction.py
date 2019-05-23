########################################################
#!/usr/bin/env python                                  #
# -*- coding: utf-8 -*-                                #
#                                                      #
# Author: Taner Sezer                                  #
# Command Line Collocation Query Script for TS Corpus  #
########################################################

import sys
import re
import logging
import httplib2
import requests
import importlib

word = str(sys.argv[1])
corpus = str(sys.argv[2])
# list of corpora
# 1- abstract_corpus_v2  delete >> animal _121
# 2- columns_v2  delete >> 2112293
# 3- dictionary_corpus_v2 >>start 	_	_ _	_  >>end 	_	_ _	_
# 4- gezi_derlemi    >> politisation beginning weakening turkish english 7195
# 5- syllable_v3 <<No results at all>>
# 6- tc_constitution >> 1924 _123 1961 _80 1982 _165
# 7- ts_corpus_ver_2     >>No Problem
# 8- ts_idiom_proverb     >>No Problem
# 9- ts_timeline_corpus      >news ttc
# 10- ts_tweets <<No results at all>>
# 11- ts_wikipedia    >>No_Problem

selection = str(sys.argv[3])
# 1- tagged
# 2- untagged
count = int(sys.argv[4])
if count > 250:
    print("Value too high")
    sys.exit()


logging.basicConfig(filename='get_collocations.log', level=logging.DEBUG)


#USERNAME = "your_username"
#PASSWORD = "your_password"


def get_collocations(word, limit=50):
    # Login and get cookies
    h = httplib2.Http(".cache")
    h.add_credentials(USERNAME, PASSWORD)
    login_url = "http://cqpweb.tscorpus.com/cqpweb/usr/redirect.php"
    response = requests.post(login_url, data={
                             'username': USERNAME, 'password': PASSWORD, 'redirect': 'userLogin', 'uT': 'y'}, allow_redirects=False)
    cookies = response.cookies
    # Generate Corpus URL using user inputs
    full_url = (
        f"http://cqpweb.tscorpus.com/cqpweb/{corpus}/concordance.php?theData={word}*&qmode=sq_nocase&pp={count}&del=begin&t=&del=end&uT=y")
    # Check if connection is valid
    try:
        response = requests.get(full_url, cookies=cookies)
    except Exception as e:
        logging.debug("{}: {}".format(word, e))
        return get_collocations(word, begin, end, limit)

    output = response.text
    # print(output)
    key = re.findall('qname=(..........+?)', output)
    if not key:
        logging.debug("\n{}\nKey: {}\n{}\n{}\n".format(
            "="*15, word, output, "="*15))
        return []

    key = key[0]
    # Reqiured for other queries - Keep it in mind
    #id = key.replace('qname=', '')
    esdizim = response.text
    aranan = re.findall('<B>(.*?)<\/B>', esdizim, re.IGNORECASE)
    sonuc = list(set([x.lower() for i, x in enumerate(aranan) if i % 2]))

    return sonuc


# Get concordance results as string
results = get_collocations(word)
print(results)

# Result is in HTML format and noisy
# clets clean results
for line in results:
    # print(type(line))
    clear_beginning = re.sub(r'^(<a|<td) class=.*escape\(\'',
                             r' ', line.rstrip(" "))
    clear_node = clear_beginning.replace(
        "<font color=&quot;#dd0000&quot;>", "<< ").replace("</font>", ">>").replace(" &quot;", "\"").replace("\"", " \"").replace(" &gt;&gt;", "")
    clear_end_1 = re.sub(r' \'\)\">.*<\/a>', r'', clear_node)
    clear_end_2 = re.sub(r'\'\) \">.*<\/a>', "", clear_end_1)
    final_check = re.sub(r'^<.*$', r'', clear_end_2)
    # Main Results with tags and some noise dependent to corpus
    final_tagged = final_check.replace("\\\'", "'")
    # Add whitespace between annotation and words
    sep_tags = re.sub(r'(?=_.*)\w', r'\t_', final_tagged)
    prefix = (r'\t_[0-9a-zA-Z]{1,150}\s')
    final_untagged = re.sub(prefix, " ", sep_tags)
    if selection == "tagged" and corpus == "ts_timeline_corpus":
        #sonuc = re.sub(r'^^(news|ttc).*', '', final_tagged)
        final_tagged = re.sub(r'^(news|ttc).*', '', sep_tags)
        print(final_tagged)
    if selection == "tagged" and corpus == "tc_constitution":
        sonuc = re.sub(
            r'^(1924|1961|1980).*[0-9]', '', final_tagged)
        print(sonuc)

    else:
        print(final_untagged)
