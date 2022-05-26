import os
import sys
import re

if len(sys.arg) != 2:
    print("Usage: hmmerhits.py <hmmer file>")

hmmer_file = sys.argv[1]

class Hit:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.eval = 0
        self.inclusion = False

class Query:
    def __init__(self, name):
        self.name = name

        self.msv_filter = 0
        self.bias_filter = 0
        self.vit_filter = 0
        self.fwd_filter = 0
        self.hits = []

queries = dict()
with open(hmmer_file, 'r') as file:
    lines = file.readlines()
    q = None
    inclusion=False
    wait = 0
    #0 = waiting for query
    #1 = waiting for query values
    stage=0
    for line in lines:

        if wait > 0:
            wait = wait - 1
            continue

        line = line.strip()
        if stage == 0:
            if line.startswith("Query: "):
        elif stage == 1:
            if line.startswith()


