# Classificador de Texto com Deep Learning e TensorFlow

# Imports
import sys
import nltk
import json
import tflearn
import random
import string
import unicodedata
import numpy as np
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer


# Estrutura para armazenar pontuações
tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))


# Função para remover pontuações das sentenças
def remove_punctuation(text):
    return text.translate(tbl)


# Inicializa o stemmer
stemmer = LancasterStemmer()
data = None


# Leitura od arquivo JSON com os dados de treino
with open('data.json') as json_data:
    data = json.load(json_data)
    print(data)


# Gera uma lista com todas as categorias
categories = list(data.keys())
words = []


# Uma lista de tuplas com as palavras das sentenças e o nome da categoria
docs = []

for each_category in data.keys():
    for each_sentence in data[each_category]:
        # Remove a pontuação
        each_sentence = remove_punctuation(each_sentence)
        print(each_sentence)
        # Extrai as palavras de cada sentença e armazena na lista
        w = nltk.word_tokenize(each_sentence)
        print("\nPalavras tokenizadas: ", w)
        words.extend(w)
        docs.append((w, each_category))


# Stem de cada palavra, converte para minúsculo e remove duplicidades 
words = [stemmer.stem(w.lower()) for w in words]
words = sorted(list(set(words)))


# Cria as listas para os dados de treino
training = []
output = []


# Cria um array para o output
output_empty = [0] * len(categories)

for doc in docs:
    # Inicializa o bag of words para cada documento da lista
    bow = []
    # Lista de palavras tokenizadas
    token_words = doc[0]
    # Stem de cada palavra
    token_words = [stemmer.stem(word.lower()) for word in token_words]
    # Cria um array com o bag of words
    for w in words:
        bow.append(1) if w in token_words else bow.append(0)

    output_row = list(output_empty)
    output_row[categories.index(doc[1])] = 1

    # Nosso conjunto de treinamento conterá um modelo bag of words e a linha de saída que informa a qual sentença pertence.
    training.append([bow, output_row])


# Shuffle das nossas features e transforma em np.array enquanto o TensorFlow recebe uma matriz numérica
random.shuffle(training)
training = np.array(training)


# trainX contém o bag of worda e train_y contém os labels/categorias
train_x = list(training[:, 0])
train_y = list(training[:, 1])


# Reset do grafo
tf.reset_default_graph()


# Cria a rede neural
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)


# Define o modelo e configura o tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


# Treinamento
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')


# Vamos testar o modelo para algumas frases:
sent_1 = "você falou com ele ontem?"
sent_2 = "você precisa ir agora?"
sent_3 = "gostaria de me desculpar pelas falhas no relatório!"
sent_4 = "você parece alguns anos mais velho que ela!"


# Função para ajustar os dados de entrada antes de aplicar o modelo
def get_tf_record(sentence):
    global words
    # Tokenização
    sentence_words = nltk.word_tokenize(sentence)
    # Stem
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    # Bag of words
    bow = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bow[i] = 1

    return(np.array(bow))


# Previsões
print("\nImprimindo a previsão da classe das 4 sentenças de teste: ")
print(categories[np.argmax(model.predict([get_tf_record(sent_1)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent_2)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent_3)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent_4)]))])
