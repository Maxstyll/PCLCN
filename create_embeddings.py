# import modules & set up logging
import os
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
sentences = [
    ['autor', 'autores', 'pessoas', 'desconhecidas', 'desconhecido', 'roubadores', 'adolescente', 'infrator', 'roubador', 'indivíduos', 'indivíduo', 'rapazes', 'rapaz', 'meliante', 'meliantes',  'rapazes', 'agente', 'indiciado', 'garupa', 'adolescente', 'elementos', 'garotos', 'homens', 'elemento'],
    ['portando', 'portava', 'exibia', 'exibir', 'exibiu', 'portar', 'possuirem']
]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
 
sentences = MySentences('./some/directory') # a memory-friendly iterator
#model = gensim.models.Word2Vec(sentences)

model = gensim.models.Word2Vec(iter=1)  # an empty model, no training yet
model.build_vocab(some_sentences)  # can be a non-repeatable, 1-pass generator
model.train(other_sentences)  # can be a non-repeatable, 1-pass generator

model = Word2Vec(sentences, min_count=10)  # default value is 5
model = Word2Vec(sentences, size=200)  # default value is 100
model = Word2Vec(sentences, workers=4) # default = 1 worker = no parallelization

model.accuracy('./doc/questions-words.txt')

model.save('./doc/mymodel')
new_model = gensim.models.Word2Vec.load('./doc/mymodel')

model = Word2Vec.load_word2vec_format('./doc/vectors.txt', binary=False)
# using gzipped/bz2 input works too, no need to unzip:
model = Word2Vec.load_word2vec_format('./doc/vectors.bin.gz', binary=True)

model = gensim.models.Word2Vec.load('./doc/mymodel')
model.train(more_sentences)

model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
model.doesnt_match("breakfast cereal dinner lunch".split())
model.similarity('woman', 'man')
