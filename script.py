import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
from make_odds_floats import convert_win_odds_to_probability as convert_to_probability
# from itertools import izip
LOOPS = 10


def import_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data["Teams"], data["Groups"], data["groupStageFixtures"]


def play_match(homeTeam, awayTeam, homeTeamOdds, drawOdds, awayTeamOdds):
    elements = [homeTeam, 'Draw', awayTeam]
    weights = [convert_to_probability(homeTeamOdds), convert_to_probability(drawOdds), convert_to_probability(awayTeamOdds)]
    total_prob = np.sum(weights)
    normalised_weights = weights / total_prob
    return np.random.choice(elements, p=normalised_weights)


def run_group_stage(group_stage_fixtures):
    group_results = []
    for group_fixture in group_stage_fixtures:
        result = play_match(group_fixture["homeTeam"], group_fixture["awayTeam"], group_fixture["homeWinOdds"], group_fixture["draw"], group_fixture["awayWinOdds"])
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


def calculateGroupStageWinners(teams, groups, groupStageFixtures):
    fixtures = {}
    for group in groups:
        firstScore = secondScore = 0
        for team in groups[group]['teams']:
            if teams[team]['group_stage_points'] > firstScore:
                secondScore = firstScore
                firstScore = teams[team]['group_stage_points']
                groups[group]['second'] = groups[group]['winner']
                groups[group]['winner'] = team
            elif teams[team]['group_stage_points'] > secondScore:
                secondScore = teams[team]['group_stage_points']
                groups[group]['second'] = team


def print_group_results(teams, groups):
    print ("\n\n\nGroup Stage Results:")
    for group in groups:
        print ("\n\n{}".format(group))
        for team in groups[group]["teams"]:
            print ("{}: {} points.".format(team, teams[team]['group_stage_points']))
        print ("\nGroup Winner: {}".format(groups[group]['winner']))
        print ("\nGroup Second: {}".format(groups[group]['second']))


def calculateRoundOfSixteenFixtures(teams, groups):
    return [
        {
          "homeTeam": groups['Group A']['winner'],
          "awayTeam": groups['Group B']['second'],
          "homeWinOdds": teams[groups['Group A']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group B']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group C']['winner'],
          "awayTeam": groups['Group D']['second'],
          "homeWinOdds": teams[groups['Group C']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group D']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group E']['winner'],
          "awayTeam": groups['Group F']['second'],
          "homeWinOdds": teams[groups['Group E']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group F']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group G']['winner'],
          "awayTeam": groups['Group H']['second'],
          "homeWinOdds": teams[groups['Group G']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group H']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group B']['winner'],
          "awayTeam": groups['Group A']['second'],
          "homeWinOdds": teams[groups['Group B']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group A']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group D']['winner'],
          "awayTeam": groups['Group C']['second'],
          "homeWinOdds": teams[groups['Group D']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group C']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group F']['winner'],
          "awayTeam": groups['Group E']['second'],
          "homeWinOdds": teams[groups['Group F']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group E']['second']]['winning_odds']
        },
        {
          "homeTeam": groups['Group H']['winner'],
          "awayTeam": groups['Group G']['second'],
          "homeWinOdds": teams[groups['Group H']['winner']]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[groups['Group G']['second']]['winning_odds']
        }
    ]
    

def printKnockOutRoundOfFixtures(fixtures, roundName):
    print("\n\n{}:".format(roundName))
    for fixture in fixtures:
        print("\n{} plays {} with odds of {} : {} : {}".format(fixture['homeTeam'], fixture['awayTeam'], fixture['homeWinOdds'], fixture['drawOdds'], fixture['awayWinOdds']))


def pairwise(iterables):
    while iterables:
        yield [iterables.pop(0), iterables.pop(0)]


def playKnockOutRound(teams, fixtures, roundMultiplier):
    pairs = pairwise(fixtures)
    # nextRound = []
    for firstFixture, secondFixture in pairs:
    # do something
        result1 = play_match(firstFixture["homeTeam"], firstFixture["awayTeam"], firstFixture["homeWinOdds"], firstFixture["drawOdds"], firstFixture["awayWinOdds"])
        result2 = play_match(secondFixture["homeTeam"], secondFixture["awayTeam"], secondFixture["homeWinOdds"], secondFixture["drawOdds"], secondFixture["awayWinOdds"])
    nextRound = {
      "homeTeam": result1,
      "awayTeam": result2,
      "homeWinOdds": teams[result1]['winning_odds'],
      "drawOdds": "0",
      "awayWinOdds": teams[result2]['winning_odds']
    }
    return nextRound
    #     nextRound.append(
    #         {
    #           "homeTeam": result1,
    #           "awayTeam": result2,
    #           "homeWinOdds": teams[result1]['winning_odds'],
    #           "drawOdds": "0",
    #           "awayWinOdds": teams[result2]['winning_odds']
    #         }
    #     )
    # return nextRound[0]


def main():
    teams, groups, groupStageFixtures = import_data()
    # Start by simulating every group stage game
    group_results = run_group_stage(groupStageFixtures)
    # import pdb; pdb.set_trace()
    # Now figure out the group tables
    score_group_stage(teams, groups, group_results)
    calculateGroupStageWinners(teams, groups, groupStageFixtures)
    print_group_results(teams, groups)
    roundOfSixteenFixtures = calculateRoundOfSixteenFixtures(teams, groups)
    printKnockOutRoundOfFixtures(roundOfSixteenFixtures, "Round Of 16 Fixtures")
    quarterFinalFixtures = playKnockOutRound(teams, roundOfSixteenFixtures, 3)
    printKnockOutRoundOfFixtures(quarterFinalFixtures, "Quarter Final Fixtures")
    semiFinalFixtures = playKnockOutRound(teams, quarterFinalFixtures, 4)
    printKnockOutRoundOfFixtures(semiFinalFixtures, "Semi Final Fixtures")
    finalFixture = playKnockOutRound(teams, semiFinalFixtures, 5)
    printKnockOutRoundOfFixtures(finalFixture, "Final Fixtures")
    tournamentWinner = play_match(finalFixture["homeTeam"], finalFixture["awayTeam"], finalFixture["homeWinOdds"], 0, finalFixture["awayWinOdds"])
    print("{} has won the tournament!".format(tournamentWinner))


if __name__ == "__main__":
    main()
