import json
import os


filename = 'data.json'

DEFAULT_SEEDS = {
    "Germany": 3,
    "Brazil": 3,
    "Spain": 4,
    "Belgium": 5,
    "France": 4,
    "Argentina": 5,
    "Uruguay": 8,
    "Portugal": 8,
    "England": 8,
    "Colombia": 8,
    "Mexico": 10,
    "Switzerland": 10,
    "Poland": 10,
    "Croatia": 10,
    "Costa Rica": 12,
    "Denmark": 12,
    "Russia": 12,
    "Sweden": 12,
    "Nigeria": 15,
    "Egypt": 15,
    "Iceland": 15,
    "Serbia": 15,
    "Peru": 20,
    "Morocco": 20,
    "Senegal": 20,
    "Iran": 20,
    "South Korea": 22,
    "Australia": 22,
    "Japan": 22,
    "Tunisia": 22,
    "Panama": 25,
    "Saudi Arabia": 25
}

with open(filename, 'r') as jsonfile:
    json_file = json.load(jsonfile)

for team in json_file['Teams']:
    if team['name'] in DEFAULT_SEEDS:
        team['seed_value'] = DEFAULT_SEEDS[team['name']]

os.remove(filename)
with open(filename, 'w') as newfile:
    json.dump(json_file, newfile, indent=4, ensure_ascii=False)
