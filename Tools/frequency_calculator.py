####################################
#####   Frequency Calculator   #####
#####   tanersezerr@gmail.com  #####
####################################

import os
import sys
import re
import nltk


def frequency(text):
    raw = text.lower()
    tokens = nltk.word_tokenize(raw)

    word_list = nltk.Text(tokens)

    freq_dic = {}
    for word in word_list:
        try:
            freq_dic[word] += 1
        except:
            freq_dic[word] = 1

    freq_list = freq_dic.items()

    freq_list2 = [(val, key) for key, val in freq_dic.items()]
    freq_list2.sort(reverse=True)

    resultset = {}
    resultset['word_count'] = len(word_list)
    resultset['unique_count'] = len(freq_dic)
    resultset['words'] = freq_list2

    return resultset


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("""Usage: {} <filename>""".format(sys.argv[0]))
        sys.exit()

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("""Source file not found""")
        sys.exit()

    with open(filename) as f:
        output = frequency(f.read())

    # display result
    print('Tokens in text:', output['word_count'],
          '\t', 'Unique Tokens:', output['unique_count'])
    for freq, word in output['words']:
        print(f"{freq} {word}")
