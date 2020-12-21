import os
import sys
import string
from zemberek_python import main_libs as ml
from termcolor import colored

# heceleme için zemberek api cagiralim
zemberek_api = ml.zemberek_api(
    libjvmpath="/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so",
    zemberekJarpath="zemberek_python/zemberek-tum-2.0.jar",
).zemberek()

# sesli harfler
vowels = "aeıioöuü"
# sessiz harfler
consonants = "bcçdfgğhjklmnprsştvyzxwq"
# birleşik sözcükler
# TO DO (compoundları listeden oku)
compounds = ["hanımgöbeği", "keçiboynuzu", "akşamsefası"]
# TO DO (Kısaltmalar listesi ekle)
abbr = []

# front vowels
f_vowels = "aıuo"
# back vowels
b_vowels = "eiüö"

# bulunan ünlüler için listeler
found_f = []
found_b = []

# hece sayisi bulalim
def hece_check(word):
    heceler = []
    hecele = ml.ZemberekTool(zemberek_api).kelime_hecele(word)
    for hece in hecele:
        if hece != "":
            heceler.append(hece)
    return heceler


# temel kontrol fonksiyonu
def kontrol(word):
    punctuations = [
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+" ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "{",
        "|",
        "}",
        "~",
    ]
    foreign = ["x", "w", "q"]
    space = " "
    space_k = 0
    foreign_k = 0
    numeric_k = 0
    punct_k = 0
    compound_k = 0
    # space var mi?
    if space in word:
        space_k = 1
    # x w q var mi?
    for char in foreign:
        if char in word.lower():
            foreign_k = 1
    for char in punctuations:
        if char in word:
            punct_k = 1
    if word in compounds:
        compound_k = 1
    if word.isnumeric():
        numeric_k = 1
    return (space_k, foreign_k, numeric_k, punct_k, compound_k)


# Ünlü uyumu kontrolu
def check(list1, list2, word):
    # sözcüğü karakterlere ayir
    for char in word:
        # eger f_vowel varsa found_f'e ekle
        if char in f_vowels:
            found_f.append(char)
        # eger b_vowel varsa found_b'ye ekle
        if char in b_vowels:
            found_b.append(char)
    # -tek heceli sözcük kontrolü-
    if (len(hece_check(word))) - 1 == 0:
        sonuc = print("==> Tek heceli sözcüklerde büyük ünlü uyumu aranmaz")
    # hiç ünlü yoksa
    elif len(list1) == 0 and len(list2) == 0:
        sonuc = print("Bir sorun var :) \n Sözcüğü doğru girdiğinize emin misiniz?")
    # ilk türden en az bir ikinci türden hiç yoksa
    elif len(list1) >= 1 and len(list2) == 0:
        sonuc = print(colored("==> Büyük ünlü uyumuna uygun", "green"))
    # ilk türden hiç yok ikinci türden en az bir varsa
    elif len(list1) == 0 and len(list2) >= 1:
        sonuc = print(colored("==> Büyük ünlü uyumuna uygun", "green"))
    # her iki türden de en az bir varsa
    elif len(list1) >= 1 and len(list2) >= 1:
        sonuc = print(colored("==> Büyük ünlü uyumuna uygun değil", "red"))
    return sonuc


# CLI için döngüye alalim
while True:
    # sözcük isteyelim
    print(colored("==> Kontrol edilecek sözcüğü giriniz <==\n_____", "cyan"))
    word = str(input())
    # kontrol fonksiyonu 1. parametre -boşluk varsa-
    if kontrol(word)[0] == 1:
        sonuc = print(colored("==> Boşluk içeren girdi", "blue"))
    # kontrol fonksiyonu 2 parametre -yabancı karakter-
    elif kontrol(word)[1] == 1:
        sonuc = print(colored("==> Yabancı karakter", "blue"))
    # kontrol fonksiyonu 3 parametre -yabancı karakter-
    elif kontrol(word)[2] == 1:
        sonuc = print(colored("==> Rakam girdisi işlenemez", "blue"))
    # kontrol fonksiyonu 4 parametre -yabancı karakter-
    elif kontrol(word)[3] == 1:
        sonuc = print(colored("==> Noktalama işareti işlenemez", "blue"))
    # kontrol fonksiyonu 5 parametre -yabancı karakter-
    elif kontrol(word)[4] == 1:
        sonuc = print(
            colored("==> Birleşik sözcüklerde büyük ünlü uyumu aranmaz", "blue")
        )
    else:
        # sonucu ekrana basalim
        print(check(found_f, found_b, word))
    # yeni sözcük için listeleri temizleyelim
    found_f = []
    found_b = []
