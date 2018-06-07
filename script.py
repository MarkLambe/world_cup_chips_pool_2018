import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
from make_odds_floats import convert_win_odds_to_float as convert_to_float
LOOPS = 10


def score_group_stage(group_results):
    country_points = {}
    with open('data.json', 'r') as f:
        file = json.load(f)
        for team in file["Teams"]:
            country_points[team["name"]] = 0
        for result in group_results:
            if result["result"] != 'Draw':
                country_points[result["result"]] += 1
            else:
                country_points[result["homeTeam"]] += 1
                country_points[result["awayTeam"]] += 1
    return country_points


def import_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data["Teams"], data["Groups"], data["groupStageFixtures"]


def run_group_stage(group_stage_fixtures):
    group_results = []
    for group_fixture in group_stage_fixtures:
        elements = [group_fixture["homeTeam"], 'Draw', group_fixture["awayTeam"]]
        weights = [convert_to_float(group_fixture["homeWinOdds"]), convert_to_float(group_fixture["draw"]), convert_to_float(group_fixture["awayWinOdds"])]
        total_prob = np.sum(weights)
        normalised_weights = weights / total_prob
        result = np.random.choice(elements, p=normalised_weights)
        # group_results.update({group_fixture["homeTeam"]: {group_fixture["awayTeam"]: result}})
        group_results.append({"homeTeam": group_fixture["homeTeam"], "awayTeam": group_fixture["awayTeam"],
                              "result": result})
    return group_results


def main():
    teams, groups, groupStageFixtures = import_data()
    # Start by simulating every group stage game
    group_results = run_group_stage(groupStageFixtures)
    # import pdb; pdb.set_trace()
    # Now figure out the group tables
    pprint(group_results)
    all_results = score_group_stage(group_results)
    print(all_results)


if __name__ == "__main__":
    main()
