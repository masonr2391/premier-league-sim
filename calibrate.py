import numpy as np
import pandas as pd
from simulate import simulate_season
from collections import Counter

# Define the number of simulations
NUM_SIMULATIONS = 1000

# Initialize counters
win_counts = Counter()
top4_counts = Counter()
relegation_counts = Counter()

for _ in range(NUM_SIMULATIONS):
    season = simulate_season()
    season_sorted = season.sort_values('Position')

    # League winner
    winner = season_sorted.iloc[0]['Team']
    win_counts[winner] += 1

    # Top 4 teams
    top4_teams = season_sorted.iloc[:4]['Team']
    for team in top4_teams:
        top4_counts[team] += 1

    # Relegated teams (positions 18-20)
    relegated_teams = season_sorted.iloc[-3:]['Team']
    for team in relegated_teams:
        relegation_counts[team] += 1

# Calculate percentages
teams = list(win_counts.keys())
print("Team\tWin%\tTop4%\tRelegation%")
for team in teams:
    win_pct = (win_counts[team] / NUM_SIMULATIONS) * 100
    top4_pct = (top4_counts[team] / NUM_SIMULATIONS) * 100
    relegation_pct = (relegation_counts[team] / NUM_SIMULATIONS) * 100
    print(f"{team}\t{win_pct:.2f}\t{top4_pct:.2f}\t{relegation_pct:.2f}")

