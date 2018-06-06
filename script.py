import json
from pprint import pprint
import numpy as np
from numpy.random import choice as npChoice
LOOPS = 10

def importData():
    with open('data.json') as f:
        data = json.load(f)
        return data["Teams"], data["Groups"], data["groupStageFixtures"]

def main():
    teams, groups, groupStageFixtures = importData()
    # Start by simulating every group stage game
    groupResults = {}
    for groupFixture in groupStageFixtures:
        elements = [groupFixture["homeTeam"], 'Draw', groupFixture["awayTeam"]] 
        #weights = [groupFixture["homeWinOdds"], groupFixture["draw"], groupFixture["awayWinOdds"]]
        weights = [0.1, 0.2, 0.4]
        totalProb = np.sum(weights)
        normalisedWeights = weights / totalProb
        result = np.random.choice(elements, p=normalisedWeights)
        groupResults.update({groupFixture["homeTeam"]: {groupFixture["awayTeam"]: result}})
        # Now figure out the group tables
    pprint(groupResults)


if __name__ == "__main__":
    main()