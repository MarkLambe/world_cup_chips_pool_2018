import json
from fractions import Fraction
import os


def convert_win_odds_to_float(odds_string):
    if type(odds_string) == str:
        return odds_string if odds_string.isalpha() else round(float(Fraction(odds_string)), 2)

filename = 'data.json'

with open(filename, 'r') as json_file:
    work_file = json.load(json_file)

for team in work_file["Teams"]:
    team["winning_odds"] = convert_win_odds_to_float(team["winning_odds"])

os.remove(filename)
with open(filename, 'w') as new_file:
    json.dump(work_file, new_file, indent=4, ensure_ascii=False)
