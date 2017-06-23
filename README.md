Web Search and Mining Group Project
========

# Install
```
pip3 install flask pymongo jieba
./server.py
```

# Structure

```
.
├── README.md
├── common.py
├── data
│   ├── doctor-all.json
│   ├── doctor.json
│   ├── question-all.json
│   └── question.json
├── mongo_indexer.py
├── mongo_searcher.py
├── server.py
├── token_wrapper.py
└── wsm-document.docx
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
