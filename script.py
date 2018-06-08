import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
import operator

GAME_LOOPS = 1000
GAME_POINTS = {
        'GROUP_STAGE_DRAW': 1,
        'GROUP_STAGE_WIN': 2,
        'LAST_SIXTEEN_WIN': 3,
        'QUARTER_FINAL_WIN': 4,
        'SEMI_FINAL_WIN': 5,
        'THIRD_PLACE_PLAYOFF_WIN': 1,
        'FINAL_WIN': 6,
    }

def import_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data["Teams"], data["Groups"], data["groupStageFixtures"]

def convert_win_odds_to_probability(odds_string):
    if odds_string == "EVS":
        return 0.5
    elif odds_string == "0":
        return 0
    else:
        nums = odds_string.split("/")
        return round(float(nums[1]) / (float(nums[1]) + float(nums[0])), 4)

def giveTeamGamePoints(teams, team, points):
    teams[team]['game_points'] = teams[team]['game_points'] + (points * teams[team]['seed_value'])

def play_match(homeTeam, awayTeam, homeTeamOdds, drawOdds, awayTeamOdds):
    elements = [homeTeam, 'Draw', awayTeam]
    weights = [convert_win_odds_to_probability(homeTeamOdds), convert_win_odds_to_probability(drawOdds), convert_win_odds_to_probability(awayTeamOdds)]
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
            teams[result['homeTeam']]['group_stage_points'] = teams[result['homeTeam']]['group_stage_points'] + 1
            teams[result['awayTeam']]['group_stage_points'] = teams[result['awayTeam']]['group_stage_points'] + 1

            giveTeamGamePoints(teams, result['homeTeam'], GAME_POINTS['GROUP_STAGE_DRAW'])
            giveTeamGamePoints(teams, result['awayTeam'], GAME_POINTS['GROUP_STAGE_DRAW'])
        else:
            giveTeamGamePoints(teams, result['result'], GAME_POINTS['GROUP_STAGE_WIN'])
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
    nextRound = []
    for firstFixture, secondFixture in pairs:
        result1 = play_match(firstFixture["homeTeam"], firstFixture["awayTeam"], firstFixture["homeWinOdds"], firstFixture["drawOdds"], firstFixture["awayWinOdds"])
        result2 = play_match(secondFixture["homeTeam"], secondFixture["awayTeam"], secondFixture["homeWinOdds"], secondFixture["drawOdds"], secondFixture["awayWinOdds"])
        giveTeamGamePoints(teams, result1, roundMultiplier)
        giveTeamGamePoints(teams, result2, roundMultiplier)
        nextRound.append({
          "homeTeam": result1,
          "awayTeam": result2,
          "homeWinOdds": teams[result1]['winning_odds'],
          "drawOdds": "0",
          "awayWinOdds": teams[result2]['winning_odds']
        })
    return nextRound

def playFinal(teams, fixture):
    tournamentWinner = play_match(fixture["homeTeam"], fixture["awayTeam"], fixture["homeWinOdds"], fixture["drawOdds"], fixture["awayWinOdds"])
    giveTeamGamePoints(teams, tournamentWinner, GAME_POINTS['FINAL_WIN'])
    return tournamentWinner

def printGamePoints(teams):
    for team in teams:
        print("{}: {} points.".format(team, teams[team]['game_points']))

def runGame(teams, groups, groupStageFixtures, doLogs):
    group_results = run_group_stage(groupStageFixtures)
    score_group_stage(teams, groups, group_results)
    calculateGroupStageWinners(teams, groups, groupStageFixtures)
    if doLogs:
        print_group_results(teams, groups)
    roundOfSixteenFixtures = calculateRoundOfSixteenFixtures(teams, groups)
    if doLogs:
        printKnockOutRoundOfFixtures(roundOfSixteenFixtures, "Round Of 16 Fixtures")
    quarterFinalFixtures = playKnockOutRound(teams, roundOfSixteenFixtures, GAME_POINTS['LAST_SIXTEEN_WIN'])
    if doLogs:
        printKnockOutRoundOfFixtures(quarterFinalFixtures, "Quarter Final Fixtures")
    semiFinalFixtures = playKnockOutRound(teams, quarterFinalFixtures, GAME_POINTS['QUARTER_FINAL_WIN'])
    if doLogs:
        printKnockOutRoundOfFixtures(semiFinalFixtures, "Semi Final Fixtures")
    finalFixture = playKnockOutRound(teams, semiFinalFixtures, GAME_POINTS['SEMI_FINAL_WIN'])
    if doLogs:
        printKnockOutRoundOfFixtures(finalFixture, "Final Fixtures")
    tournamentWinner = playFinal(teams, finalFixture[0])
    if doLogs:
        print("{} has won the tournament!".format(tournamentWinner))
    if doLogs:
        printGamePoints(teams)

def main():
    teams, groups, groupStageFixtures = import_data()
    for i in range(GAME_LOOPS):
        runGame(teams, groups, groupStageFixtures, False)
    orderedResults = {k: v['game_points'] / GAME_LOOPS for k,v in teams.items()}
    orderedResults = sorted(orderedResults.items(), key=operator.itemgetter(1))
    pprint(orderedResults)



if __name__ == "__main__":
    main()
