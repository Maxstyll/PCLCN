import os
import codecs
import glob
import json
import sqlite3
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

portugue_stops = set(stopwords.words('portuguese'))

# Criar o Banco de Dados
# os.remove("./db/dadosDipol.db") if os.path.exists("./db/dadosDipol.db") else None
con = sqlite3.connect('./db/dadosDipolNLTK.db')
cur = con.cursor()

# Criar as Tabelas miniFrase
#sql_delete_miniFrase = 'drop table miniFrases '
#cur.execute(sql_delete_miniFrase)

sql_create_miniFrase = 'CREATE TABLE IF NOT EXISTS miniFrases '\
'(id integer primary key AUTOINCREMENT, '\
'texto varchar(200), '\
'entidade varchar(50), '\
'arquivo varchar(140))'
cur.execute(sql_create_miniFrase)
sql_insert_miniFrase = 'insert into miniFrases (texto, entidade, arquivo) values (?, ?, ?)'


# Criar as Tabelas palavras
sql_create_palavras = 'CREATE TABLE IF NOT EXISTS palavras '\
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
    keys_file  = open(filename, 'r')
    keys_json = json.loads(keys_file.read()) # Convert arquivo para json
    for entidade in entidades:
        print("Arquivo: " + filename + " - Entidade:  " + entidade)
        acaoAutor = keys_json[entidade]
        # Fazer splite de frase para palavas
        for dadosText in acaoAutor:        
            text = dadosText + data
            #Separa as frases
            sentencas = sent_tokenize(text.encode("utf_8"))
            for sentenca in sentencas:
                #Remoção das stopwords
                palavas = word_tokenize(sentenca)
                for palava in palavas if palava not in portugue_stops:
                    try:
                        # Identificar em qual classes variaveis a palavra se enquadra (artigo, adjetivo, pronome, numeral, substantivo e verbo)
                        for word, tag in pos_tags(palava):
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
                    if(len(sentencas) > 1):
                        rec = (sentencas, entidade, filename)
                        cur.execute(sql_insert_miniFrase, rec)
                except:
                    rec = (sentencas, entidade, 'error dados')
                    cur.execute(sql_insert_miniFrase, rec)

                con.commit()