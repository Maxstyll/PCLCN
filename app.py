# Import dos pacotes
import os
import glob
import json
import sqlite3
import icu
import polyglot
import pickle

from polyglot.text import Text, Word
from polyglot.downloader import downloader
from polyglot.mapping import Embedding

fileName = "dicPolicial.pickle"

# https://sites.google.com/site/rmyeid/projects/polyglot
# http://nbviewer.jupyter.org/gist/aboSamoor/6046170


def loadMyTagger(fileName):
    return pickle.load(open(fileName, "rb"))

embeddings = loadMyTagger(fileName)

downloader.download("embeddings2.pt")
downloader.download("pos2.pt")

# Inicial aplicativo

# Criar o Banco de Dados
con = sqlite3.connect('./db/dadosDipol.db')
cur = con.cursor()

sql_create_miniFrase = 'CREATE TABLE IF NOT EXISTS miniFrases '\
'(id integer primary key AUTOINCREMENT, '\
'texto varchar(200), '\
'entidade varchar(50), '\
'arquivo varchar(140))'
cur.execute(sql_create_miniFrase)
sql_insert_miniFrase = 'insert into miniFrases (texto, entidade, arquivo) values (?, ?, ?)'


# Criar as Tabelas palavras
sql_create_palavras = 'CREATE TABLE IF NOT EXISTS  palavras '\
'(id integer primary key AUTOINCREMENT, '\
'palavra varchar(50), '\
'tag varchar(10), '\
'entidade varchar(50), '\
'arquivo varchar(140))'
cur.execute(sql_create_palavras)
sql_insert_palavra = 'insert into palavras (palavra, tag, entidade, arquivo) values (?, ?, ?, ?)'


# Abrir arquivo
path = './doc'
entidades = ['acaoAutor', 'acaoVitima', 'acesso', 'armaAutor', 'autor', 'bensVitima', 'caracteristicaFisicaPessoa', 'caracteristicaVeiculo', 'deslocamentoAutor', 'idadeAutor', 'instrumentoAutor', 'local', 'quantidade', 'vestimentaAutor']

for filename in glob.glob(os.path.join(path, '*.json')):
    keys_file  = open(filename, 'r', encoding='utf8')
    keys_json = json.loads(keys_file.read()) # Convert arquivo para json

    for entidade in entidades:
        print("Arquivo: " + filename + " - Entidade:  " + entidade)
        acaoAutor = keys_json[entidade]
        # Fazer splite de frase para palavas
        for dadosText in acaoAutor:        
            vtTexto = dadosText
            text = Text(vtTexto, hint_language_code='pt')
        
            #Gravar palavras
            try:
                # Identificar em qual classes variaveis a palavra se enquadra (artigo, adjetivo, pronome, numeral, substantivo e verbo)
                for word, tag in text.pos_tags:
                    neighbors = embeddings.nearest_neighbors(word)
                    for w,d in zip(neighbors, embeddings.distances(word, neighbors)):
                        print("{:<8}{:.4f}".format(w,d))

                    # Garantir nao ter palavras duplicadas
                    sql_search_palavra = " Select count(id) from palavras Where palavra = ? And tag = ? "
                    where = (word, tag)
                    for count in cur.execute(sql_search_palavra, where).fetchall():
                        if count[0] == 0:
                            rec = (word, tag, entidade, filename)
                            cur.execute(sql_insert_palavra, rec)
            except Exception as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                print (message)
                
                rec = (vtTexto, 'error digitacao', filename)
                cur.execute(sql_insert_palavra, rec)

            #Gravar dados para regra de contesto semantico
            try:
                qtdePalavras = vtTexto.split()
                if(len(qtdePalavras) > 1):
                    rec = (vtTexto, entidade, filename)
                    cur.execute(sql_insert_miniFrase, rec)
            except:
                rec = (vtTexto, entidade, 'error dados')
                cur.execute(sql_insert_miniFrase, rec)

            con.commit()

# Identificar em qual intencao ele se enquadra (fugir, subtrair, coacao, simulando, portar, agrecao, abordagem, quantidade, vestir, deslocar, veiculo, arma, Autor, caracteristicaAutor, acaoVitiva, bensVitima, outros)
