#!/usr/bin/env python3
import time
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from common import *
app = Flask(__name__, static_url_path='/static')
CORS(app)

import mongo_searcher as searcher
# from token_wrapper import tokenize

def load_json_file(filename):
  with open("data/" + filename, "r") as f:
    data = f.read()
    return json.loads(data)


@app.route("/")
def hello():
  return "Hello World!"

@app.route("/search_all", methods=['POST'])
def search_all():
  content = request.get_json(force=True)
  options = {}
  if "region" in content:
    options['region'] = content["region"]
  if "type" in content:
    options['type'] = content["type"]

  result = searcher.search_all(content["s"], options)
  return jsonify(result)

@app.route("/search_doctor", methods=['POST'])
def search_doctor():
  content = request.get_json(force=True)

  result = searcher.search_doctor(content["s"])
  return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
