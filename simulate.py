import numpy as np
import pandas as pd

TEAMS = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
    'Leeds', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle',
    'Nottingham Forest', 'Sunderland', 'Tottenham', 'West Ham', 'Wolverhampton'
]

RATINGS = {
    "Liverpool": 99,
    "Man City": 97,
    "Arsenal": 96.5,
    "Newcastle": 84,
    "Chelsea": 79,
    "Aston Villa": 77,
    "Man Utd": 71,
    "Tottenham": 69,
    "Nottingham Forest": 63,
    "Brighton": 59,
    "Bournemouth": 56,
    "West Ham": 54,
    "Everton": 54,
    "Crystal Palace": 53,
    "Fulham": 52,
    "Brentford": 50,
    "Wolverhampton": 50,
    "Burnley": 49,
    "Leeds": 49,
    "Sunderland": 47
}


def simulate_season():
    table = {team: {'Pts': 0, 'GF': 0, 'GA': 0, 'W': 0, 'D': 0, 'L': 0} for team in TEAMS}
    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i == j:
                continue

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
