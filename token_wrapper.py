#!/usr/bin/env python3

import jieba

def tokenize(doc):
  # doc is a string
  term2tf = {}
  for word in jieba.cut(doc, cut_all=False):
      term2tf.setdefault(word, 0)
      term2tf[word] += 1
  return list(term2tf.items())
