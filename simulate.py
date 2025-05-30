import numpy as np
import pandas as pd

TEAMS = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
    'Leeds', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle',
    'Nottingham Forest', 'Sunderland', 'Tottenham', 'West Ham', 'Wolverhampton'
]

RATINGS = {
    "Man City": 95,
    "Liverpool": 92,
    "Arsenal": 89,
    "Chelsea": 84,
    "Newcastle": 83,
    "Man Utd": 81,
    "Tottenham": 80,
    "Aston Villa": 78,
    "Brighton": 76,
    "West Ham": 74,
    "Brentford": 72,
    "Fulham": 71,
    "Crystal Palace": 70,
    "Bournemouth": 69,
    "Everton": 68,
    "Wolverhampton": 67,
    "Nottingham Forest": 65,
    "Burnley": 62,
    "Leeds": 60,
    "Sunderland": 58
}

# Goal model calibration
AVERAGE_GOALS_PER_GAME = 2.85
HOME_ADVANTAGE = 1.05  # Reduced to better match historical home win rates

# Apply a realism modifier for weak teams
def adjust_for_weak_team(team, base_expected):
    if RATINGS[team] <= 50:
        return base_expected * 0.9
    elif RATINGS[team] <= 55:
        return base_expected * 0.95
    else:
        return base_expected

def simulate_season():
    table = {team: {'Pts': 0, 'GF': 0, 'GA': 0, 'W': 0, 'D': 0, 'L': 0} for team in TEAMS}

    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i == j:
                continue

            home_rating = RATINGS[home]
            away_rating = RATINGS[away]

            home_strength = home_rating + 5
            away_strength = away_rating

            home_expectation = (home_strength / (home_strength + away_strength)) * AVERAGE_GOALS_PER_GAME
            away_expectation = (away_strength / (home_strength + away_strength)) * AVERAGE_GOALS_PER_GAME

            home_expectation *= HOME_ADVANTAGE

            expected_home_goals = adjust_for_weak_team(home, home_expectation)
            expected_away_goals = adjust_for_weak_team(away, away_expectation)

            home_goals = np.random.poisson(expected_home_goals)
            away_goals = np.random.poisson(expected_away_goals)

            table[home]['GF'] += home_goals
            table[home]['GA'] += away_goals
            table[away]['GF'] += away_goals
            table[away]['GA'] += home_goals

            if home_goals > away_goals:
                table[home]['Pts'] += 3
                table[home]['W'] += 1
                table[away]['L'] += 1
            elif away_goals > home_goals:
                table[away]['Pts'] += 3
                table[away]['W'] += 1
                table[home]['L'] += 1
            else:
                table[home]['Pts'] += 1
                table[away]['Pts'] += 1
                table[home]['D'] += 1
                table[away]['D'] += 1

    # Convert to DataFrame
    df = pd.DataFrame(table).T
    df['GD'] = df['GF'] - df['GA']
    df = df.sort_values(by=['Pts', 'GD', 'GF'], ascending=False)
    df = df.reset_index().rename(columns={'index': 'Team'})
    df['Position'] = range(1, len(df) + 1)

    # --- 🔧 Normalize point distribution ---
    current_max = df['Pts'].max()
    target_max = 92  # realistic top score
    current_min = df['Pts'].min()
    target_min = 25  # realistic 20th place

    # Apply linear scaling
    df['Pts'] = df['Pts'].apply(lambda x: round(
        ((x - current_min) / (current_max - current_min)) * (target_max - target_min) + target_min
    ))

    return df
