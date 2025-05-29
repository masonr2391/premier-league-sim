import numpy as np
import pandas as pd
import random

# Hardcoded 2025–26 teams (edit names/strengths as needed)
TEAMS = [
    "Liverpool", "Arsenal", "Manchester City", "Chelsea", "Newcastle United",
    "Nottingham Forest", "Bournemouth", "Aston Villa", "Brentford", "Brighton",
    "Crystal Palace", "Fulham", "Tottenham Hotspur", "Leeds United",
    "West Ham United", "Manchester United", "Wolverhampton", "Burnley",
    "Sunderland"
]

# Simplified team ratings (higher = stronger team)
RATINGS = {
    "Liverpool": 95, "Arsenal": 91, "Manchester City": 89, "Chelsea": 83,
    "Newcastle United": 82, "Tottenham Hotspur": 75, "Manchester United": 74,
    "Aston Villa": 72, "Brighton": 70, "Brentford": 69, "Bournemouth": 68,
    "Nottingham Forest": 68, "Crystal Palace": 67, "Fulham": 66,
    "Leeds United": 64, "West Ham United": 63, "Wolverhampton": 62,
    "Burnley": 58, "Sunderland": 50
}

def simulate_season():
    # Create blank table
    table = {team: {'Pts': 0, 'GF': 0, 'GA': 0, 'W': 0, 'D': 0, 'L': 0} for team in TEAMS}
    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i == j:
                continue
            # Basic Poisson model using team strength
            home_attack = RATINGS[home]
            away_attack = RATINGS[away]
            home_goals = np.random.poisson(home_attack / 25)
            away_goals = np.random.poisson(away_attack / 30)

            table[home]['GF'] += home_goals
            table[home]['GA'] += away_goals
            table[away]['GF'] += away_goals
            table[away]['GA'] += home_goals

            if home_goals > away_goals:
                table[home]['Pts'] += 3
                table[home]['W'] += 1
                table[away]['L'] += 1
            elif home_goals < away_goals:
                table[away]['Pts'] += 3
                table[away]['W'] += 1
                table[home]['L'] += 1
            else:
                table[home]['Pts'] += 1
                table[away]['Pts'] += 1
                table[home]['D'] += 1
                table[away]['D'] += 1

    df = pd.DataFrame(table).T
    df['GD'] = df['GF'] - df['GA']
    df = df.sort_values(by=['Pts', 'GD', 'GF'], ascending=False)
    df['Position'] = range(1, len(df)+1)
    return df.reset_index().rename(columns={'index': 'Team'})
