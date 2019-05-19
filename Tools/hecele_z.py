#####################################
# Hypenation and hypenation count   #
# using Zemberek Python Wrapper     #
# Taner Sezer                       #
# tanersezer@gmail.com              #
# 2019                              #
#####################################

import os
import sys
import re
from zemberek_python import main_libs as ml
from string import whitespace
import math
import pprint


f = open(sys.argv[1])
my_text = f.read()

#
zemberek_api = ml.zemberek_api(libjvmpath="/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so",
                               zemberekJarpath="./zemberek_python/zemberek-tum-2.0.jar").zemberek()


def white_token(girdi):
    w_white = re.sub(r'([a-zşğıiüöçA-ZŞĞIİÜÖÇ])([,.!";:])', r'\1 \2 ', girdi)
    w_token = re.sub(" ", "\n", w_white)
    return w_token


to_hece = white_token(my_text).splitlines()

nums = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
puncs = ("!", "(", ")", "-", "[", "]", "{", "}", ";", ":", ",",
         "'", "/", " < ", " > ", ".", " ^ ", " & ", "*", "_", "~", "@", "#", "*", "+", " ")
heceler = []

for word in to_hece:
    if word.startswith(nums):
        tagged = word, "Num"
        heceler.append(tagged)
    if word.startswith("<"):
        tagged = word, "XML"
        heceler.append(tagged)
    if word.startswith(puncs):
        tagged = word, "Punc"
        heceler.append(tagged)
    if not word.strip():
        tagged = "_", "_Space"
        heceler.append(tagged)
    if not word.startswith(nums) and not word.startswith(puncs) and not word.startswith(" "):
        syl = ml.ZemberekTool(zemberek_api).kelime_hecele(word)
        tagged = word, syl
        heceler.append(tagged)

for word, tags in heceler:
    tags = " ".join(tags)
    tags = tags.replace("  ", "+").replace(" ", "")
    if tags == "Num" or tags == "Punc" or tags == "XML" or tags == "_Space":
        hece_sayisi = 0
    else:
        hece_sayisi = tags.count("+")+1

    print(f"{word} {tags} {hece_sayisi}")
