import os
import glob
import sqlite3
from polyglot.text import Text, Word
from polyglot.downloader import downloader
from polyglot.mapping import Embedding

downloader.download("embeddings2.pt")
downloader.download("pos2.pt")
downloader.download("morph2.pt")
downloader.supported_tasks(lang="pt")

embeddings = Embedding.load("/Users/emersonantonio/polyglot_data/embeddings2/pt/embeddings_pkl.tar.bz2")


#neighbors = embeddings.nearest_neighbors("verde")
#for w,d in zip(neighbors, embeddings.distances("green", neighbors)):
#  print("{:<8}{:.4f}".format(w,d))


# Criar o Banco de Dados
con = sqlite3.connect('./db/dadosDipolNLTK.db')
cur = con.cursor()

sql_create = 'CREATE TABLE IF NOT EXISTS miniDicionario '\
'(' \
'  id integer primary key AUTOINCREMENT, '\
'   word varchar(50), ' \
'   radical varchar(50), ' \
'   tag varchar(50)' \
')'
cur.execute(sql_create)
sql_insert = ' insert into miniDicionario (radical, word, tag) values (?, ?, ?) '
sql_update = ' update miniDicionario  set radical = ? Where word = ? And tag = ? '

path = './dados-base'
for filename in glob.glob(os.path.join(path, '*.dic')):
    arquivo  = open(filename, 'r', encoding='utf8')
    
    for line in arquivo.readlines():
        line = line.split('/')
        text = line[0].replace('\n', '')
        print(text)
        text = Text(text, hint_language_code='pt')
        for word, tag in text.pos_tags:
            sql_search_palavra = " Select count(id) from miniDicionario Where word = ? And tag = ? "
            #radicao = text.morphemes
            where = (word, tag)
            for count in cur.execute(sql_search_palavra, where).fetchall():
                rec = ('', word, tag)
                if count[0] == 0:
                    cur.execute(sql_insert, rec)
                else:
                    cur.execute(sql_update, rec)
        
        con.commit()