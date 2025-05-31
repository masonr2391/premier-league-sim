import pandas as pd
from simulate import simulate_season, RATINGS
from collections import Counter
import numpy as np

TEAMS = list(RATINGS.keys())
SIMULATIONS = 10000

title_counts = Counter()
top4_counts = Counter()
relegated_counts = Counter()

for _ in range(SIMULATIONS):
    table = simulate_season()

    # Title
    title_team = table.iloc[0]['Team']
    title_counts[title_team] += 1

    # Top 4
    for team in table.iloc[:4]['Team']:
        top4_counts[team] += 1

    # Relegated (bottom 3)
    for team in table.iloc[-3:]['Team']:
        relegated_counts[team] += 1

# Convert counts to percentages
title_probs = {team: (title_counts[team] / SIMULATIONS) * 100 for team in TEAMS}
top4_probs = {team: (top4_counts[team] / SIMULATIONS) * 100 for team in TEAMS}
relegation_probs = {team: (relegated_counts[team] / SIMULATIONS) * 100 for team in TEAMS}

# Combine into a dataframe
results = pd.DataFrame({
    'Team': TEAMS,
    'Title %': [round(title_probs[t], 2) for t in TEAMS],
    'Top 4 %': [round(top4_probs[t], 2) for t in TEAMS],
    'Relegated %': [round(relegation_probs[t], 2) for t in TEAMS],
    'Rating': [RATINGS[t] for t in TEAMS]
})

results = results.sort_values('Title %', ascending=False)
print(results.to_string(index=False))
