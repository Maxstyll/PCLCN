import re
import pandas as pd
import nltk.data
import numpy as np

nltk.download('punkt')
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

opeds_df = pd.read_csv('nyt_opeds_sample.csv', encoding='utf-8')


p = opeds_df.pivot_table(index=['text_body'], columns='noun_adj', values='year', aggfunc=np.mean).round(0)
p.fillna(0, inplace=True)

columns = ["text_body", "noun_adj", "year"]
p = p.reindex(columns=columns)
p[columns] = p[columns].astype(int)

#opeds_df[['text_body','noun_adj','year']][1:10]

def sentence_to_wordlist(sentence, remove_stopwords=False):
    # 1. Remove non-letters
    sentence_text = re.sub(r'[^\w\s]','', sentence)
    # 2. Convert words to lower case and split them
    words = sentence_text.lower().split()
    # 3. Return a list of words
    return(words)


def oped_to_sentences(oped, tokenizer, remove_stopwords=False ):
    try:
        # 1. Use the NLTK tokenizer to split the text into sentences
        raw_sentences = tokenizer.tokenize(oped.strip())
        # 2. Loop over each sentence
        sentences = []
        for raw_sentence in raw_sentences:
            # If a sentence is empty, skip it
            if len(raw_sentence) > 0:
                # Otherwise, call sentence_to_wordlist to get a list of words
                sentences.append(sentence_to_wordlist(raw_sentence))
        # 3. Return the list of sentences (each sentence is a list of words, so this returns a list of lists)
        len(sentences)
        return sentences
    except:
        print('nope')

nyt_opeds = opeds_df['text_body'].tolist()
sentences = []

for i in range(0,len(nyt_opeds)):
    try:
        # Need to first change "./." to "." so that sentences parse correctly
        oped = nyt_opeds[i].replace("/.", '')
        # Now apply functions
        sentences += oped_to_sentences(oped, tokenizer)
    except:
        print('no!')

print("There are " + str(len(sentences)) + " sentences in our corpus of opeds.")


sentences[220]

import gensim
from gensim.models import Word2Vec
from gensim.models import word2vec
from gensim.models import Phrases
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

num_features = 300    # Word vector dimensionality                      
min_word_count = 50   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 6           # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

model.init_sims(replace=True)
model_name = "nytimes_oped"
model.save(model_name)
new_model = gensim.models.Word2Vec.load('nytimes_oped')

vocab = list(model.vocab.keys())
vocab[:25]

'philosophy' in model.vocab
model['philosophy']

bigramer = gensim.models.Phrases(sentences)
model = Word2Vec(bigramer[sentences], workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

trigram = Phrases(bigram[sentence_stream])
vocab = list(model.vocab.keys())
vocab[:25]

model.most_similar('race',  topn=15)

model.most_similar(positive=['race'], negative=['election'], topn=15)

model.most_similar('wiretap',  topn=15)
model.most_similar('good',  topn=15)

model.most_similar(positive=['good'], negative=['bad'], topn=15)


