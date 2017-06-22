#!/usr/bin/env python3
import math
import json
from pymongo import MongoClient
from token_wrapper import tokenize
from common import *

client = MongoClient()
db = client.wsm

tbl_page = db.tbl_page
tbl_index = db.tbl_index
total_doc = db.tbl_page.count()

def load_posting(token, options):
  find_option = { 'token' : token }
  if 'region' in options:
    find_option['region'] = {'$in': options['region']}

  print('fo', find_option)

  return list(tbl_index.find(find_option))

def search_all(query_str, options):
  tokens = tokenize(query_str)
  doc2score = {}

  
  for w, _ in tokens:
      posting = load_posting(w, options)
      print('posting', posting)

      doc2tf = {}
      for p in posting:
        print("p=",p)
        print("options=", options)
        doc = p['page_id']
        cnt = p['count']
        # FIXME
        if 'type' in options:
          if options['type'] == 'doctor':
            if doc[0] != 'd':
              continue
          elif options['type'] == 'question':
            if doc[0] == 'd':
              continue

        doc2tf.setdefault(doc, 0)
        doc2tf[doc] += cnt

      for doc, tf in doc2tf.items():
        doc2score.setdefault(doc, 0)
        df = len(doc2tf)
        if df:
          print('df = {} total={} tf={}'.format(df, total_doc, tf))
          doc2score[doc] += (1 + math.log10(tf)) * math.log10(total_doc / df)
  print(doc2score)
  result = list(doc2score.items())
  result.sort(key=lambda x: x[1], reverse=True)

  if len(result) > 40:
    result = result[:40]

  docs = []
  for r in result:
    doc = tbl_page.find_one({'page_id': r[0]}) 
    del doc['_id']
    docs.append(doc)
  return docs
