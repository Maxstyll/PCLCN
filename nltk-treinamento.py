import os
import glob
import json
import nltk
import pickle
# Nome do Tagger
fileName = "dicPolicial.pickle"

def getMapping():
    path = './dicionarios'
    dados = {}
    for filename in glob.glob(os.path.join(path, '*.json')):
        arquivo  = open(filename, 'r', encoding='utf8')
        mappingJson = json.loads(arquivo.read()) # Convert arquivo para json

        dados.update({k: v for k, v in mappingJson.items()})

    return dados

# Função para salvar o Tagger
def saveMyTagger(tagger, fileName):
    fileHandle = open(fileName, "wb")
    pickle.dump(tagger, fileHandle)
    fileHandle.close()

# Função para salvar o treinamento
def Training(fileName):
    # Etiquetador
    tagger = nltk.UnigramTagger(model=getMapping())
    saveMyTagger(tagger, fileName)

# Treninamento
Training(fileName)