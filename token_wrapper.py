#!/usr/bin/env python3

import thulac

thu1 = thulac.thulac(seg_only=False, model_path="thulac/models")

def tokenize(doc):
  # doc is a string
  term2tf = {}
  for word, cls in thu1.cut(doc):
    if cls != 'w' and cls != '':
      if word not in term2tf:
        term2tf[word] = 0
      term2tf[word] += 1
  return list(term2tf.items())
