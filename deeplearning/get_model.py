import nltk
import numpy as np
import model_tflearn as md
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

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
    bow = [0]*len(md.getWords())
    for s in sentence_words:
        for i, w in enumerate(md.getWords()):
            if w == s:
                bow[i] = 1

    return(np.array(bow))


# Previsões
print("\nImprimindo a previsão da classe das 4 sentenças de teste: ")
print(md.getCategories[np.argmax(model.predict([get_tf_record(sent_1)]))])
print(md.getCategories[np.argmax(model.predict([get_tf_record(sent_2)]))])
print(md.getCategories[np.argmax(model.predict([get_tf_record(sent_3)]))])
print(md.getCategories[np.argmax(model.predict([get_tf_record(sent_4)]))])
