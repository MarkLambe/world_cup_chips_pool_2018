import json
from fractions import Fraction
import os


def convert_win_odds_to_probability(odds_string):
    if odds_string == "EVS":
        return 0.5
    elif odds_string == "0":
        return 0
    else:
        nums = odds_string.split("/")
        return round(float(nums[1]) / (float(nums[1]) + float(nums[0])), 4)

"""
filename = 'data.json'

with open(filename, 'r') as json_file:
    work_file = json.load(json_file)

for team in work_file["Teams"]:
    team["winning_odds"] = convert_win_odds_to_float(team["winning_odds"])

os.remove(filename)
with open(filename, 'w') as new_file:
    json.dump(work_file, new_file, indent=4, ensure_ascii=False)
"""