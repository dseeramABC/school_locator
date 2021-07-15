#!/usr/bin/env python3

import json
import sys
import csv

inFile = sys.argv[1]
outFile = sys.argv[2]

schools = []
with open(inFile, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        schools += [row]

with open(outFile, 'w') as outfile:
    json.dump(schools, outfile)
