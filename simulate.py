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
    "Bournemouth": 57,
    "West Ham": 55,
    "Everton": 55,
    "Crystal Palace": 54,
    "Fulham": 53,
    "Brentford": 51,
    "Wolverhampton": 51,
    "Burnley": 48,
    "Leeds": 48,
    "Sunderland": 46
}

# Goal model calibration
AVERAGE_GOALS_PER_GAME = 2.6
HOME_ADVANTAGE = 1.1  # 10% boost to expected goals at home



def simulate_season():
    table = {team: {'Pts': 0, 'GF': 0, 'GA': 0, 'W': 0, 'D': 0, 'L': 0} for team in TEAMS}
    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i == j:
                continue

            home_rating = RATINGS[home]
            away_rating = RATINGS[away]

            # Scale ratings into expected goals
            expected_home_goals = (home_rating / (home_rating + away_rating)) * AVERAGE_GOALS_PER_GAME * HOME_ADVANTAGE
            expected_away_goals = (away_rating / (home_rating + away_rating)) * AVERAGE_GOALS_PER_GAME

            # Simulate goals using Poisson distribution
            home_goals = np.random.poisson(expected_home_goals)
            away_goals = np.random.poisson(expected_away_goals)

            # Adjust scores to reinforce realism
            if home_goals > away_goals:
                margin = home_goals - away_goals
                if margin == 1 and np.random.rand() < 0.6:
                    home_goals += 1  # boost small wins
                elif margin >= 3 and np.random.rand() < 0.3:
                    away_goals += 1  # soften big wins

            elif away_goals > home_goals:
                margin = away_goals - home_goals
                if margin == 1 and np.random.rand() < 0.6:
                    away_goals += 1
                elif margin >= 3 and np.random.rand() < 0.3:
                    home_goals += 1

            else:  # draw
                if home_goals > 2:
                    home_goals = away_goals = 2  # cap high-scoring draws
                if home_goals == 0 and np.random.rand() < 0.3:
                    home_goals = away_goals = 1  # fewer 0-0s




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
