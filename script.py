import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
from make_odds_floats import convert_win_odds_to_probability as convert_to_probability
LOOPS = 10

def import_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data["Teams"], data["Groups"], data["groupStageFixtures"]


def run_group_stage(group_stage_fixtures):
    group_results = []
    for group_fixture in group_stage_fixtures:
        elements = [group_fixture["homeTeam"], 'Draw', group_fixture["awayTeam"]]
        weights = [convert_to_probability(group_fixture["homeWinOdds"]), convert_to_probability(group_fixture["draw"]), convert_to_probability(group_fixture["awayWinOdds"])]
        total_prob = np.sum(weights)
        normalised_weights = weights / total_prob
        
        result = np.random.choice(elements, p=normalised_weights)
        group_results.append({"homeTeam": group_fixture["homeTeam"], "awayTeam": group_fixture["awayTeam"],
                              "result": result})
    return group_results

def score_group_stage(teams, groups, group_results):
    for result in group_results:
        if result['result'] == 'Draw':
            teams[result['homeTeam']]['game_points'] = teams[result['homeTeam']]['game_points'] + (1 * teams[result['homeTeam']]['seed_value'])
            teams[result['awayTeam']]['game_points'] = teams[result['awayTeam']]['game_points'] + (1 * teams[result['awayTeam']]['seed_value'])

            teams[result['homeTeam']]['group_stage_points'] = teams[result['homeTeam']]['group_stage_points'] + 1
            teams[result['awayTeam']]['group_stage_points'] = teams[result['awayTeam']]['group_stage_points'] + 1
        else:
            teams[result['result']]['game_points'] = teams[result['result']]['game_points'] + (2 * teams[result['result']]['seed_value'])
            teams[result['result']]['group_stage_points'] = teams[result['result']]['group_stage_points'] + 3

def print_group_results(teams, groups):
    print ("\n\n\nGroup Stage Results:\n\n\n")
    for group in groups:
        print ("\n\n{}".format(group))
        for team in groups[group]["teams"]:
            print ("{}: {} points.".format(team, teams[team]['group_stage_points']))

def main():
    teams, groups, groupStageFixtures = import_data()
    # Start by simulating every group stage game
    group_results = run_group_stage(groupStageFixtures)
    # import pdb; pdb.set_trace()
    # Now figure out the group tables
    score_group_stage(teams, groups, group_results)
    print_group_results(teams, groups)



if __name__ == "__main__":
    main()
