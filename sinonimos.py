import polyglot
from polyglot.mapping import Embedding


embeddings = embeddings.normalize_words()
neighbors = embeddings.nearest_neighbors("green")
for w,d in zip(neighbors, embeddings.distances("green", neighbors)):
  print("{:<8}{:.4f}".format(w,d))


