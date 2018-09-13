# Import dos pacotes
import os
import glob
import json
import sqlite3
import polyglot

from polyglot.text import Text, Word

# Inicial aplicativo

# Criar o Banco de Dados
os.remove("./db/dadosDipol.db") if os.path.exists("./db/dadosDipol.db") else None
con = sqlite3.connect('./db/dadosDipol.db')
cur = con.cursor()

# Criar as Tabelas miniFrase
sql_create_miniFrase = 'create table miniFrases '\
'(id integer primary key AUTOINCREMENT, '\
'texto varchar(200), '\
'arquivo varchar(140))'
cur.execute(sql_create_miniFrase)
sql_insert_miniFrase = 'insert into miniFrases (texto, arquivo) values (?, ?)'


# Criar as Tabelas palavras
sql_create_palavras = 'create table palavras '\
'(id integer primary key AUTOINCREMENT, '\
'palavra varchar(50), '\
'tag varchar(10), '\
'arquivo varchar(140))'
cur.execute(sql_create_palavras)
sql_insert_palavra = 'insert into palavras (palavra, tag, arquivo) values (?, ?, ?)'


# Abrir arquivo
path = './doc'
for filename in glob.glob(os.path.join(path, '*.json')):
    keys_file  = open(filename, 'r', encoding='utf8')
    keys_json = json.loads(keys_file.read()) # Convert arquivo para json
    acaoAutor = keys_json["acaoAutor"]
    for text in acaoAutor:
        vtTexto = text# Fazer splite de frase para palavas
        text = Text(vtTexto)
        for word, tag in text.pos_tags:
            rec = (word, tag, filename)
            cur.execute(sql_insert_palavra, rec)

        vtTexto = vtTexto.split()
        if(len(vtTexto) > 1):
            print(text) #Gravar dados para regra de contesto semantico
            rec = (text, filename)
            cur.execute(sql_insert_miniFrase, rec)

        con.commit()

    
# Garantir nao ter palavras duplicadas
# Insert dados em uma tabela SQLite
# Identificar em qual classes variaveis a palavra se enquadra (artigo, adjetivo, pronome, numeral, substantivo e verbo)
# Identificar em qual intencao ele se enquadra (fugir, subtrair, coacao, simulando, portar, agrecao, abordagem, quantidade, vestir, deslocar, veiculo, arma, Autor, caracteristicaAutor, acaoVitiva, bensVitima, outros)
