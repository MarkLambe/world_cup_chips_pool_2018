import pytest
import random

from script import (
    convert_win_odds_to_probability,
    play_match,
    import_data
)

teams, groups, groupStageFixtures = import_data()


def make_odds_list():
    odds_list = []
    for team in groupStageFixtures:
        odds_list.append(team['homeWinOdds'])
    return odds_list


def get_probability(x):
    return convert_win_odds_to_probability(x)


def test_evs_probability():
    assert get_probability("EVS") == 0.5


def test_nil_probability():
    assert get_probability("0") == 0


def test_random_probability():
    odds_list = make_odds_list()
    for random_odd in range(10):
        assert type(get_probability(random.choice(odds_list))) == float


def test_always_win_play():
    match = {
        "homeTeam": "Winner",
        "awayTeam": "Loser",
        "homeTeamOdds": "1/2",
        "drawOdds": "0",
        "awayTeamOdds": "0"
    }
    assert play_match(**match) == "Winner"


def test_higher_odds():
    winner_list = []
    match = {
        "homeTeam": "Favourite",
        "awayTeam": "Underdog",
        "homeTeamOdds": "1/2",
        "drawOdds": "0",
        "awayTeamOdds": "2/1"
    }
    for play in range(100):
        winner_list.append(play_match(**match))
    num_favourite_wins = winner_list.count('Favourite')
    num_underdog_wins = winner_list.count('Underdog')
    assert num_favourite_wins > num_underdog_wins and num_favourite_wins == pytest.approx(66, abs=10)
