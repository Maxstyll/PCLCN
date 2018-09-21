import os
import codecs
import glob
import json
import sqlite3
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

portugue_stops = set(stopwords.words('portuguese'))

dadosText = "anunciouam"
sentencas = sent_tokenize(dadosText)
for sentenca in sentencas:
    #Remoção das stopwords
    palava = word_tokenize(sentenca)
    for word, tag in pos_tag(palava):
        template = "Descrição da palavra: {0} e a classificaçãon: {1}"
        message = template.format(word, tag)
        print (message)
