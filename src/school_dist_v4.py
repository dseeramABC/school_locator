#!/usr/bin/env python3

import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
from functools import wraps

# timer function that can be applied as a decorator
def timer(fn):
    @wraps(fn)
    def wrap(*args,**kwargs):
        ts = time.perf_counter()
        result = fn(*args,**kwargs)
        te = time.perf_counter()
        print(f"Execution time: {round(te-ts,2)}")
        return result
    return wrap

# Function to recursively attempt to geolocate a given address using
# geopy. Returns None after MAX_ATTEMPTS
## TODO: Better handling for when an address is not found/MAX_ATTEMPTS is exceeded
def geolocate(address, attempt=1, MAX_ATTEMPTS=5):
    try:
        return Nominatim(user_agent='ABetterChance').geocode(address)
    except Exception:
        if attempt <= MAX_ATTEMPTS:
            return geolocate(address, attempt=attempt+1)
        else:
            return "ADDRESS NOT FOUND"

# Calculate the distance between the school and the student's address using their
# coordinates
def schoolDist_calc(school, query_coord):
    try:
        school['Distance'] = geodesic(query_coord, school['Coordinates']).miles
    except AttributeError:
        school['Distance'] = float('inf')
    return school

# Given a student's information stored in a dictionary and a list of school
# dictionaries, return the list ranked based on the schools' distance from the
# student's address
def rankSchools(student_dict):

    query = geolocate(student_dict['Address'])
    query_coord = (query.latitude, query.longitude)

    region = student_dict['Region']
    with open(f"./regions_cache/{region.lower()}.json") as file:
        schoolsList = json.load(file)

    possibleSchools = [d for d in schoolsList if d['Student Body'] in [student_dict['Student Body'], "Coed"]]
    result = [schoolDist_calc(x, query_coord) for x in possibleSchools]

    return sorted(result, key = lambda x: x['Distance'])

@timer
def main():

    with open("./regions_cache/students.json") as file:
        students = json.load(file)

    # iterate through students and use ranksSchools function to order list of
    # schools by distance. Then, print out the rankings, schools
    for student in students:
        ranked_Schools = rankSchools(student)
        print(f"\033[4m{student['Student Name']}, {student['Student Body']} ({student['Address']})\033[0m")
        for i,d in enumerate(ranked_Schools):
            print(f"{i+1}. {d['School Name']} ({d['Student Body']}): {d['Distance']:.2f} miles")
        print("\n")

if __name__ == '__main__':
    main()
