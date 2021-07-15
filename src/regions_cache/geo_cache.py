#!/usr/bin/env python3

import sys
import json
from geopy.geocoders import Nominatim

inFile = sys.argv[1]
print(inFile)

def geolocate(address, attempt=1, MAX_ATTEMPTS=5):
    try:
        return Nominatim(user_agent='ABetterChance').geocode(address)
    except Exception:
        if attempt <= MAX_ATTEMPTS:
            return geolocate(address, attempt=attempt+1)
        else:
            return "ADDRESS NOT FOUND"

with open(inFile) as file:
    schoolsList = json.load(file)

for school in schoolsList:
    address = geolocate(school['Address'])
    try:
        school['Coordinates'] = (address.latitude, address.longitude)
    except AttributeError:
        school['Coordinates'] = None

with open(inFile, 'w') as file:
    json.dump(schoolsList, file)
