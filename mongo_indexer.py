#!/usr/bin/env python3
import json
from pymongo import MongoClient
from token_wrapper import tokenize
from common import *

client = MongoClient()
client.drop_database('wsm')
db = client.wsm

tbl_page = db.tbl_page
tbl_index = db.tbl_index
tbl_answer = db.tbl_answer

tbl_page.create_index('page_id')
# tbl_page.create_index('name')
# tbl_page.create_index('title')

tbl_index.create_index('token')
# tbl_page.create_index('region')

def index_answer(doctor_id, answer_str):
  tokens = tokenize(answer)

  items = [ { 'token': tok, 'count': cnt, 'page_id': doctor_id }
      for tok, cnt in tokens ]

  if items:
    tbl_answer.insert_many(items)

def index_region(page_id, region, region_str):
  tokens = tokenize(region_str)

  items = [ { 'token': tok, 'count': cnt, 'region': region, 'page_id': page_id }
      for tok, cnt in tokens ]

  if items:
    tbl_index.insert_many(items)

def index_doctor(doc_str):
  doc = json.loads(doc_str)
  doc_id = "d" + doc["doc_id"]
  doc['type'] = 'doctor'
  doc['page_id'] = doc_id
  tbl_page.insert_one(doc)

  for region in ['expert', 'profile', 'name']:
    if doc[region]:
      index_region(doc_id, region, doc[region])
    else:
      print("missing doc_id={}".format(doc_id))

def index_question(question_str):
  question = json.loads(question_str)
  question_id = question["question_id"]
  question['type'] = 'question'
  question['page_id'] = question_id
  tbl_page.insert_one(question)

  for region in ['title', 'detail']:
    index_region(question_id, region, question[region])

  reply_str = ' '.join([reply["detail"] for reply in question["reply_list"]])
  index_region(question_id, 'answer', reply_str)

with open ("data/question-all.json", "r") as question:
  data = ""
  while True:
    try:
      data = question.readline()
      index_question(data)
      print("q")
    except EOFError:
      break
    except json.decoder.JSONDecodeError:
      print("data =", data)
      break

print("Question Finished")
with open ("data/doctor-all.json", "r") as doc:
  data = ""
  while True:
    try:
      data = doc.readline()
      index_doctor(data)
      print("d")
    except EOFError:
      break
    except json.decoder.JSONDecodeError:
      print("data =", data)
      break
print("Clear stopwords")

print(tbl_index.count())
tokens = list(tbl_index.distinct('token'))
for tok in tokens:
  if tbl_index.count({'token' : tok}) > stopword_thres:
    tbl_index.remove({'token' : tok})
    print("stopword {}".format(tok));

print("Indexing finished")
