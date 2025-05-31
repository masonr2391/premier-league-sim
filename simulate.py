import numpy as np
import pandas as pd

TEAMS = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
    'Leeds', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle',
    'Nottingham Forest', 'Sunderland', 'Tottenham', 'West Ham', 'Wolverhampton'
]

RATINGS = {
    "Liverpool": 96,
    "Arsenal": 94,
    "Man City": 93,
    "Newcastle": 88,
    "Chelsea": 85,
    "Aston Villa": 83,
    "Brighton": 82,
    "Nottingham Forest": 81,
    "Man Utd": 79,
    "Tottenham": 78,
    "Bournemouth": 76,
    "Brentford": 75,
    "Fulham": 74,
    "Everton": 73,
    "Crystal Palace": 72,
    "West Ham": 71,
    "Wolverhampton": 70,
    "Leeds": 68,
    "Burnley": 67,
    "Sunderland": 66
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

            home_strength = home_rating + 5  # Home boost
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

    # Convert to DataFrame and rank
    df = pd.DataFrame(table).T
    df['GD'] = df['GF'] - df['GA']
    df = df.sort_values(by=['Pts', 'GD', 'GF'], ascending=False)
    df = df.reset_index().rename(columns={'index': 'Team'})
    df['Position'] = range(1, len(df) + 1)

    # --- 🔧 Soft-normalize point totals with noise ---
    current_max = df['Pts'].max()
    current_min = df['Pts'].min()
    target_max = 92 + np.random.randint(-3, 4)  # ~89–95
    target_min = 24 + np.random.randint(-4, 5)  # ~20–28

    def rescale_with_noise(x):
        scaled = ((x - current_min) / (current_max - current_min)) * (target_max - target_min) + target_min
        noise = np.random.normal(0, 1.5)  # small Gaussian noise
        return max(0, round(scaled + noise))

    df['Pts'] = df['Pts'].apply(rescale_with_noise)

    # Sort again in case noise causes rank swaps
    df = df.sort_values(by=['Pts', 'GD', 'GF'], ascending=False).reset_index(drop=True)
    df['Position'] = range(1, len(df) + 1)

    return df
