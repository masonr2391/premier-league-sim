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
        return base_expected * 0.9  # reduce goal rate for bottom teams
    elif RATINGS[team] <= 55:
        return base_expected * 0.95
    else:
        return base_expected

def simulate_season():
        MAX_GOALS_PER_TEAM = 5  # Cap to prevent unrealistic high scores
    table = {team: {'Pts': 0, 'GF': 0, 'GA': 0, 'W': 0, 'D': 0, 'L': 0} for team in TEAMS}
    
    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i == j:
                continue

            home_rating = RATINGS[home]
            away_rating = RATINGS[away]

            # Scale ratings into expected goals
home_strength = home_rating + 5  # small home advantage boost
away_strength = away_rating

# Ratio-based expected goals model
home_expectation = (home_strength / (home_strength + away_strength)) * AVERAGE_GOALS_PER_GAME
away_expectation = (away_strength / (home_strength + away_strength)) * AVERAGE_GOALS_PER_GAME

# Optional: Slight skew for realism
home_expectation *= 1.05  # 5% home boost
away_expectation *= 0.95


            expected_home_goals = adjust_for_weak_team(home, raw_home_goals)
            expected_away_goals = adjust_for_weak_team(away, raw_away_goals)

            # Simulate goals using Poisson distribution
# Simulate goals using Poisson distribution and cap results
home_goals = np.random.poisson(home_expectation)
away_goals = np.random.poisson(away_expectation)






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
