#!/usr/bin/env python3
import pickle

with open("data/index/tokens.pickle", "rb") as f:
  token2tid, tid2token = pickle.load(f)

print(token2tid)
