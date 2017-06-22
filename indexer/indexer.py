#!/usr/bin/env python3
import json
import pickle
from .token_wrapper import tokenize

DOCTOR = 0
QUESTION = 1

TITLE = 0
DETAIL = 1
ANSWER = 2
PROFILE = 3
MEDICIAN = 4

# entities: doctor, question, answers

# queries:
# 1. token -> question
# 2. (token, region) -> question
# 3. token -> doctor

next_tid = 0
token2tid = {}
tid2token = {}

tid2posting = {}
pid2page = {}
# posting = (page_id, region, tf)
# page = (type in "doctor"
def get_token_id(token):
  global next_tid, token2tid, tid2token
  if token not in token2tid:
    token2tid[token] = next_tid
    tid2token[next_tid] = token
    next_tid += 1
  return token2tid[token]

def index_region(page_id, region, region_str):
  global next_tid, token2tid, tid2token
  tokens = tokenize(region_str)
  for t, tf in tokens:
    tid = get_token_id(t)
    tid2posting.setdefault(tid, [])
    tid2posting[tid].append((page_id, region, tf))

def index_doctor(doc_str):
  doc = json.loads(doc_str)
  doc_id = "d" + doc["doc_id"]
  index_region(doc_id, PROFILE, doc["profile"])

def index_question(question_str):
  question = json.loads(question_str)
  question_id = question["question_id"]

  index_region(question_id, TITLE, question["title"])
  index_region(question_id, DETAIL, question["detail"])

  reply_str = ' '.join([reply["detail"] for reply in question["reply_list"]])
  index_region(question_id, ANSWER, reply_str)


with open ("data/doctor.json", "r") as doc:
      data = doc.read()
      index_doctor(data)
with open ("data/question.json", "r") as question:
      data = question.read()
      index_question(data)

with open("data/index/tokens.pickle", "wb") as f:
  pickle.dump([token2tid, tid2token], f)

# print("token2tid", token2tid)
# print("tid2token", tid2token)
# print("tid2posting", tid2posting)
print("Indexing finished")
