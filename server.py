#!/usr/bin/env python3
import time
import json
from flask import Flask, request, jsonify
from common import *
app = Flask(__name__)

import searcher
# from token_wrapper import tokenize

def load_json_file(filename):
  with open("data/" + filename, "r") as f:
    data = f.read()
    return json.loads(data)

def load_page(page_id):
  if (page_id[0] == 'q'):
    return load_json_file("question.json")
  elif (page_id[0] == 'd'):
    return load_json_file("doctor.json")
  else:
    return None

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/search_all", methods=['POST'])
def search_all():
  content = request.get_json(silent=True)
  if "section" not in content:
    sections = section_map.values()
  else:
    sections = {section_map[s] for s in content["section"]}
  result = searcher.search_all(content["s"], sections)
  return jsonify([load_page(r) for r in result])

@app.route("/search_question", methods=['POST'])
def search_question():
  content = request.get_json(silent=True)
  return jsonify([load_page('q')])
