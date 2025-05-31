import pandas as pd
import numpy as np
import random

TEAMS = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
    'Leeds', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle',
    'Nottingham Forest', 'Sunderland', 'Tottenham', 'West Ham', 'Wolverhampton'
]

TITLE_PROBS = {
    "Liverpool": 30.82, "Arsenal": 28.53, "Man City": 26.68, "Newcastle": 6.59, "Chelsea": 3.87,
    "Aston Villa": 2.42, "Brighton": 1.57, "Nottingham Forest": 1.25, "Man Utd": 0.41, "Tottenham": 0.39,
    "Bournemouth": 0.29, "Brentford": 0.21, "Fulham": 0.19, "Everton": 0.14, "Crystal Palace": 0.12,
    "West Ham": 0.09, "Wolverhampton": 0.08, "Leeds": 0.06, "Burnley": 0.04, "Sunderland": 0.03
}

TOP4_PROBS = {
    "Liverpool": 92.3, "Arsenal": 89.5, "Man City": 87.1, "Newcastle": 58.2, "Chelsea": 39.4,
    "Aston Villa": 34.7, "Brighton": 27.6, "Nottingham Forest": 18.5, "Man Utd": 8.3, "Tottenham": 5.5,
    "Bournemouth": 4.2, "Brentford": 2.7, "Fulham": 2.3, "Everton": 1.9, "Crystal Palace": 1.6,
    "West Ham": 1.4, "Wolverhampton": 1.2, "Leeds": 0.5, "Burnley": 0.3, "Sunderland": 0.2
}

RELEGATION_PROBS = {
    "Sunderland": 97.13, "Burnley": 94.88, "Leeds": 86.71, "Wolverhampton": 42.92, "West Ham": 28.43,
    "Crystal Palace": 14.62, "Everton": 12.37, "Fulham": 9.48, "Brentford": 8.29, "Bournemouth": 7.53,
    "Tottenham": 3.74, "Man Utd": 2.11, "Nottingham Forest": 0.91, "Brighton": 0.83, "Aston Villa": 0.67,
    "Chelsea": 0.43, "Newcastle": 0.31, "Man City": 0.17, "Arsenal": 0.13, "Liverpool": 0.09
}

def draw_weighted(prob_dict, n=1, exclude=set()):
    items = [(team, prob) for team, prob in prob_dict.items() if team not in exclude]
    teams, weights = zip(*items)
    total = sum(weights)
    norm_weights = [w / total for w in weights]
    return list(np.random.choice(teams, size=n, replace=False, p=norm_weights))

def simulate_season():
    title_winner = draw_weighted(TITLE_PROBS)[0]
    top4_teams = set(draw_weighted(TOP4_PROBS, 4, exclude={title_winner}))
    top4_teams.add(title_winner)
    relegated_teams = set(draw_weighted(RELEGATION_PROBS, 3))

    # Build a plausible table based on this outcome
    teams = TEAMS.copy()
    np.random.shuffle(teams)

    table_data = []
    for team in teams:
        if team == title_winner:
            pos = 1
            pts = np.random.randint(88, 95)
        elif team in top4_teams:
            pos = np.random.randint(2, 5)
            pts = np.random.randint(75, 87)
        elif team in relegated_teams:
            pos = np.random.randint(18, 21)
            pts = np.random.randint(18, 34)
        else:
            pos = np.random.randint(5, 18)
            pts = np.random.randint(35, 74)

        # Random goal data
        gf = np.random.randint(30, 90)
        ga = np.random.randint(20, 85)
        w = np.random.randint(5, 25)
        d = np.random.randint(0, 15)
        l = 38 - w - d

        table_data.append({
            "Team": team,
            "W": w,
            "D": d,
            "L": l,
            "GF": gf,
            "GA": ga,
            "GD": gf - ga,
            "Pts": pts,
            "Position": pos
        })

    df = pd.DataFrame(table_data)
    df = df.sort_values(by=['Position', 'Pts', 'GD', 'GF'], ascending=[True, False, False, False]).reset_index(drop=True)
    df['Position'] = range(1, len(df) + 1)
    return df
