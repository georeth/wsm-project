#!/usr/bin/env python3
import pickle
import math
from token_wrapper import tokenize

with open("data/index/tokens.pickle", "rb") as f:
  total_doc, token2tid, tid2token = pickle.load(f)

def load_posting(tid):
  with open("data/index/posting-{}.pickle".format(tid), "rb") as f:
    posting = pickle.load(f)
  return posting

def search_all(query_str, section):
  tokens = tokenize(query_str)
  doc2score = {}

  for w, _ in tokens:
    if w in token2tid:
      tid = token2tid[w]
      posting = load_posting(tid)

      doc2tf = {}
      for doc, sec, cnt in posting:
        if sec in section:
          if doc not in doc2tf:
            doc2tf[doc] = 0
          doc2tf[doc] += cnt

      for doc, tf in doc2tf.items():
        if doc not in doc2score:
          doc2score[doc] = 0

        df = len(doc2tf)
        doc2score[doc] += (1 + math.log10(tf)) * math.log10(total_doc / df)
  print(doc2score)
  result = list(doc2score.items())
  result.sort(key=lambda x: x[1], reverse=True)
  if len(result) > 40:
    result = result[:40]
  return [ r[0] for r in result ]
