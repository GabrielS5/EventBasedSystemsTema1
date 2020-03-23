import json
import random
import time
import datetime
import sys

def getConfiguration():
    with open('configuration.json') as json_file:
        data = json.load(json_file)
        return data

def getRandom(entries):
    if "frequency" not in entries[0]:
        return random.choice(entries)
    randomNumber = random.randint(0,100)
    frequencySum = 0
    for entry in entries:
        frequencySum += entry["frequency"]
        if frequencySum >= randomNumber:
            return entry
    return entries[0]

def getRandomComparator(comparators):
    comparator = getRandom(comparators)
    if "symbol" in comparator:
        return comparator["symbol"]
    return comparator

def getRandomValue(entry):
    if entry["type"] == "string":
        return getRandom(entry["values"])
    if entry["type"] == "number":
        return round(random.uniform(entry["range"]["start"],entry["range"]["end"]), 2)
    if entry["type"] == "date":
        startS = entry["range"]["start"]
        endS = entry["range"]["end"]
        start = datetime.datetime(startS["year"],startS["month"],startS["day"])
        end = datetime.datetime(endS["year"],endS["month"],endS["day"])
        date = random.random() * (end - start) + start
        return date.strftime('%d.%m.%Y')

 
configuration = getConfiguration()
size = 100
publications = []
subscriptions = []

if len(sys.argv) > 1:
    size = int(sys.argv[1])

while len(publications) <= size/2:
    for entry in configuration["entries"]:
        value = getRandomValue(entry)
        publications.append({
            "item": entry["name"],
            "value": value
        })
        if len(publications) >= size/2:
            break

for i in range(0,int(size/2)):
    entry = getRandom(configuration["entries"])
    value = getRandomValue(entry)
    comparator = getRandomComparator(entry["comparators"])
    subscriptions.append({
            "item": entry["name"],
            "value": value,
            "comparator": comparator
        })

result = {
    "publications": publications,
    "subscriptions": subscriptions
}

with open('result.json', 'w') as outfile:
    json.dump(result, outfile)
