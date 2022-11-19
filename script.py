import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
import operator


"""
Entry:
Netherlands: 8
Portugal: 8
USA: 4
Germany: 5
England: 5
Uruguay: 5
Denmark: 5


Netherlands: 97.16 points.
Portugal: 89.03 points.
USA: 72.91 points.
Germany: 68.06 points.
England: 64.57 points.
Uruguay: 62.57 points.
Denmark: 62.16 points.
Croatia: 61.04 points.
Belgium: 56.44 points.

"""
GAME_LOOPS = 100000 #5000000 was used for the actual submission, it took just over 5 hours
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


def convert_win_odds_to_probability(odds):
    if float(odds) == 0:
        return 0
    return round (1 / float(odds), 4)

def giveTeamGamePoints(teams, team, points):
    teams[team]['game_points'] = teams[team]['game_points'] + (points * teams[team]['seed_value'])


def play_match(homeTeam, awayTeam, homeWinOdds, draw, awayWinOdds):
    elements = [homeTeam, 'Draw', awayTeam]
    weights = [convert_win_odds_to_probability(homeWinOdds), convert_win_odds_to_probability(draw), convert_win_odds_to_probability(awayWinOdds)]
    total_prob = np.sum(weights)
    normalised_weights = weights / total_prob
    return np.random.choice(elements, p=normalised_weights)


def run_group_stage(group_stage_fixtures):
    group_results = []
    for group_fixture in group_stage_fixtures:
        result = play_match(**group_fixture)
        group_results.append({"homeTeam": group_fixture["homeTeam"], "awayTeam": group_fixture["awayTeam"],
                              "result": result})
    return group_results


def score_group_stage(teams, groups, group_results):
    for result in group_results:
        if result['result'] == 'Draw':
            teams[result['homeTeam']]['group_stage_points'] += 1
            teams[result['awayTeam']]['group_stage_points'] += 1

            giveTeamGamePoints(teams, result['homeTeam'], GAME_POINTS['GROUP_STAGE_DRAW'])
            giveTeamGamePoints(teams, result['awayTeam'], GAME_POINTS['GROUP_STAGE_DRAW'])
        else:
            giveTeamGamePoints(teams, result['result'], GAME_POINTS['GROUP_STAGE_WIN'])
            teams[result['result']]['group_stage_points'] += 3

"""
There's some flaws here, like if three teams are level etc. But we don't have goals scored so just going to leave
it at this.
"""
def calculateGroupStageWinners(teams, groups, groupStageFixtures, groupResults):
    for group in groups:
        thisGroupTable = [(team, teams[team]['group_stage_points']) for team in groups[group]['teams'] ]
        thisGroupTable.sort(key=lambda tup: tup[1], reverse=True)
        if thisGroupTable[0][1] != thisGroupTable[1][1]:
            groups[group]['winner'] = thisGroupTable[0][0]
            if thisGroupTable[1][1] != thisGroupTable[2][1]:
                groups[group]['second'] = thisGroupTable[1][0]
            else:
                groups[group]['second'], thirdPlace = orderTiedGroupTeams(thisGroupTable[1][0], thisGroupTable[2][0], groupResults)
        else:
            groups[group]['winner'], groups[group]['second'] = orderTiedGroupTeams(thisGroupTable[0][0], thisGroupTable[1][0], groupResults)
        
def orderTiedGroupTeams(firstTeam, secondTeam, groupResults):
    match = [m for m in groupResults if (m["homeTeam"] == firstTeam and m["awayTeam"] == secondTeam) or 
        (m["awayTeam"] == firstTeam and m["homeTeam"] == secondTeam)]
    if match[0]["result"] == "Draw" or match[0]["result"] == firstTeam:
        return firstTeam, secondTeam
    else:
        return secondTeam, firstTeam

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
          "homeWinOdds": teams[groups['Group A']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group B']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group C']['winner'],
          "awayTeam": groups['Group D']['second'],
          "homeWinOdds": teams[groups['Group C']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group D']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group E']['winner'],
          "awayTeam": groups['Group F']['second'],
          "homeWinOdds": teams[groups['Group E']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group F']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group G']['winner'],
          "awayTeam": groups['Group H']['second'],
          "homeWinOdds": teams[groups['Group G']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group H']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group B']['winner'],
          "awayTeam": groups['Group A']['second'],
          "homeWinOdds": teams[groups['Group B']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group A']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group D']['winner'],
          "awayTeam": groups['Group C']['second'],
          "homeWinOdds": teams[groups['Group D']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group C']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group F']['winner'],
          "awayTeam": groups['Group E']['second'],
          "homeWinOdds": teams[groups['Group F']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group E']['second']]['odds_to_reach_qf']
        },
        {
          "homeTeam": groups['Group H']['winner'],
          "awayTeam": groups['Group G']['second'],
          "homeWinOdds": teams[groups['Group H']['winner']]['odds_to_reach_qf'],
          "draw": "0",
          "awayWinOdds": teams[groups['Group G']['second']]['odds_to_reach_qf']
        }
    ]
    

def printKnockOutRoundOfFixtures(fixtures, roundName):
    print("\n\n{}:".format(roundName))
    for fixture in fixtures:
        print("\n{} plays {} with odds of {} : {} : {}".format(
            fixture['homeTeam'], fixture['awayTeam'], fixture['homeWinOdds'], fixture['draw'], fixture['awayWinOdds']))


def pairwise(iterables):
    while iterables:
        yield [iterables.pop(0), iterables.pop(0)]


def playKnockOutRound(teams, fixtures, roundMultiplier, next_odds_key):
    pairs = pairwise(fixtures)
    nextRound = []
    for firstFixture, secondFixture in pairs:
        result1 = play_match(**firstFixture)
        result2 = play_match(**secondFixture)
        giveTeamGamePoints(teams, result1, roundMultiplier)
        giveTeamGamePoints(teams, result2, roundMultiplier)
        nextRound.append({
          "homeTeam": result1,
          "awayTeam": result2,
          "homeWinOdds": teams[result1][next_odds_key],
          "draw": "0",
          "awayWinOdds": teams[result2][next_odds_key]
        })
    return nextRound


def playFinal(teams, fixture):
    tournamentWinner = play_match(**fixture)
    giveTeamGamePoints(teams, tournamentWinner, GAME_POINTS['FINAL_WIN'])
    return tournamentWinner


def calculateThirdPlacePlayoff(teams, semiFinalTeams, finalTeams):
    thirdPlacePlayoffTeams = np.setdiff1d(semiFinalTeams,finalTeams)
    return [{
        "homeTeam": thirdPlacePlayoffTeams[0],
        "awayTeam": thirdPlacePlayoffTeams[1],
        "homeWinOdds": teams[thirdPlacePlayoffTeams[0]]['winning_odds'],
        "draw": "0",
        "awayWinOdds": teams[thirdPlacePlayoffTeams[1]]['winning_odds']
    }]

def playThirdPlacePlayoff(teams, fixture):
    thirdPlaceWinner = play_match(**fixture)
    giveTeamGamePoints(teams, thirdPlaceWinner, GAME_POINTS['THIRD_PLACE_PLAYOFF_WIN'])
    return thirdPlaceWinner


def printGamePoints(teams):
    sorted_teams = []
    for team in teams:
        sorted_teams.append({"name": team, **teams[team]})
    sorted_teams.sort(key=lambda item: item.get("game_points") * -1)
    for team in sorted_teams:
        print("{}: {} points.".format(team["name"], round(team["game_points"] / GAME_LOOPS, 2)))


def runGame(teams, groups, groupStageFixtures, doLogs):
    group_results = run_group_stage(groupStageFixtures)
    score_group_stage(teams, groups, group_results)
    calculateGroupStageWinners(teams, groups, groupStageFixtures, group_results)
    if doLogs:
        print_group_results(teams, groups)
    roundOfSixteenFixtures = calculateRoundOfSixteenFixtures(teams, groups)
    if doLogs:
        printKnockOutRoundOfFixtures(roundOfSixteenFixtures, "Round Of 16 Fixtures")
    quarterFinalFixtures = playKnockOutRound(teams, roundOfSixteenFixtures, GAME_POINTS['LAST_SIXTEEN_WIN'], 'odds_to_reach_qf')
    if doLogs:
        printKnockOutRoundOfFixtures(quarterFinalFixtures, "Quarter Final Fixtures")
    semiFinalFixtures = playKnockOutRound(teams, quarterFinalFixtures, GAME_POINTS['QUARTER_FINAL_WIN'], 'odds_to_reach_sf')
    semiFinalTeams = [semiFinalFixtures[0]["homeTeam"], semiFinalFixtures[0]["awayTeam"],
                      semiFinalFixtures[1]["homeTeam"], semiFinalFixtures[1]["awayTeam"]]
    if doLogs:
        printKnockOutRoundOfFixtures(semiFinalFixtures, "Semi Final Fixtures")
    finalFixture = playKnockOutRound(teams, semiFinalFixtures, GAME_POINTS['SEMI_FINAL_WIN'], 'odds_to_reach_final')
    finalTeams = [finalFixture[0]["homeTeam"], finalFixture[0]["awayTeam"]]
    #thirdPlaceFixture = calculateThirdPlacePlayoff(teams, semiFinalTeams, finalTeams)
    if doLogs:
        printKnockOutRoundOfFixtures(finalFixture, "Final Fixture")
        #printKnockOutRoundOfFixtures(thirdPlaceFixture, "Third Place Fixture")
    tournamentWinner = playFinal(teams, finalFixture[0])
    #thirdPlaceWinner = playThirdPlacePlayoff(teams, thirdPlaceFixture[0])
    if doLogs:
        #print("{} has finished Third!".format(thirdPlaceWinner))
        print("{} has won the tournament!".format(tournamentWinner))
    

def printResultsToFile(teams, loopsDone):
    orderedResults = {k: v['game_points'] / loopsDone for k,v in teams.items()}
    orderedResults = sorted(orderedResults.items(), key=operator.itemgetter(1))
    with open("results/" + str(loopsDone) + " with {} loops.json".format(loopsDone), 'w') as new_json_file:
        json.dump(orderedResults, new_json_file, indent=4, ensure_ascii=False)


def main():
    teams, groups, groupStageFixtures = import_data()
    for i in range(GAME_LOOPS):
        runGame(teams, groups, groupStageFixtures, False)
        if i % (GAME_LOOPS / 10) == 0 and i != 0:
            printResultsToFile(teams, i)
    printResultsToFile(teams, GAME_LOOPS)
    printGamePoints(teams)



if __name__ == "__main__":
    main()
