Web Search and Mining Group Project
========

# Install

```
wget http://thulac.thunlp.org/source/Models_v1_v2.zip
# extract and move `models` directory into `thulac`

pip3 install flask
FLASK_APP=server.py flask run
```

# Design

## Crawler

## Indexer
Tokenizer: THULAC

Inverted Index

## Searcher
Web Server: Flask

Interface:

```
post /search_all {s: "query string", region: ["title", "detail"], type: "doctor"}
parameter:
  s is query string
  region is an array ("title" "detail" "answer" "name" "expert" "profile")
  type in ["doctor", "question"], or omit it
  
=> return all related pages in json
```

## Frontend
