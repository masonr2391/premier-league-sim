import numpy as np
import pandas as pd
import random

# Hardcoded 2025–26 teams (edit names/strengths as needed)

teams = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
    'Liverpool', 'Luton', 'Man City', 'Man Utd', 'Newcastle',
    'Nottingham Forest', 'Sheffield Utd', 'Tottenham', 'West Ham', 'Wolves'
]


# Simplified team ratings (higher = stronger team)
team_ratings = {
    "Liverpool": 99,
    "Arsenal": 95,
    "Man City": 92,
    "Chelsea": 84,
    "Newcastle United": 83,
    "Tottenham Hotspur": 75,
    "Man Utd": 74,
    "Aston Villa": 72,
    "Brighton": 69,
    "Brentford": 67,
    "Bournemouth": 67,
    "Nottingham Forest": 67,
    "Crystal Palace": 66,
    "Fulham": 64,
    "Leeds United": 61,
    "West Ham United": 62,
    "Wolverhampton": 60,
    "Burnley": 54,
    "Sunderland": 46,
    "Everton": 69
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
df = df.reset_index().rename(columns={'index': 'Team'})
df['Position'] = range(1, len(df) + 1)
return df

