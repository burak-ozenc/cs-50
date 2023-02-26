# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 10000


def main():
    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from file
    # read file and add to teams list
    with open(sys.argv[1], newline='') as teamsData:
        reader = csv.DictReader(teamsData)
        headers = reader.fieldnames

        for row in reader:
            team = {}
            for header in headers:
                team[header] = row[header]

            teams.append(team)

    counts = {}
    # Simulate N tournaments and keep track of win counts

    # simulate tournaments n times
    # if winner exists in counts
    # increase win count
    # else create a row with team name and value 1
    for simulation in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {int(counts[team]) * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    chance1 = int(team1["rating"])
    chance2 = int(team2["rating"])
    probability = 1 / (1 + 10 ** ((chance2 - chance1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []
    # Simulate games for all pairs of teams
    for i in range(0, len(teams) - 1, 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""

    # iterate through teams
    # return the winner teams name
    while len(teams) > 1:
        teams = simulate_round(teams)
    return teams[0]["team"]


if __name__ == "__main__":
    main()
