# Import dos pacotes
import os
import glob
import json
import codecs

# Inicial aplicativo

# Abrir arquivo
path = './doc'
for filename in glob.glob(os.path.join(path, '*.json')):
    with open(filename, 'r') as keys_file:
        #keys = keys_file.read().encode('utf-8')
        #keys_json = json.loads(keys)

        keys_json = json.load(keys_file) # Convert arquivo para json
        acaoAutor = keys_json["acaoAutor"]
        for text in acaoAutor:
            vtTexto = text.splite # Fazer splite de frase para palavas
            if(vtTexto.length > 1):
                print(vtTexto) #Gravar dados para regra de contesto semantico

            for palavra in vtTexto:
                print(palavra)

# Garantir nao ter palavras duplicadas
# Insert dados em uma tabela SQLite
# Identificar em qual classes variaveis a palavra se enquadra (artigo, adjetivo, pronome, numeral, substantivo e verbo)
# Identificar em qual intencao ele se enquadra (fugir, subtrair, coacao, simulando, portar, agrecao, abordagem, quantidade, vestir, deslocar, veiculo, arma, Autor, caracteristicaAutor, acaoVitiva, bensVitima, outros)
