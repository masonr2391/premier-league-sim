import streamlit as st
import pandas as pd
from simulate import simulate_season
from collections import Counter

st.set_page_config(page_title="Premier League Simulator", layout="wide")

st.title("🔮 2025–26 Premier League Simulator")

runs = st.slider("Number of simulations", min_value=1000, max_value=10000, step=1000, value=1000)

progress_bar = st.progress(0)
with st.spinner(f"Simulating {runs:,} seasons..."):
    placements = []
    for i in range(runs):
        df = simulate_season()
        placements.append(df)
        if i % 100 == 0:
            progress_bar.progress(i / runs)


# Run simulations
st.write(f"Simulating {runs} seasons... This may take a few seconds.")
placements = []



# Aggregate results
all_tables = pd.concat(placements)
position_counts = {team: Counter() for team in df['Team']}

for table in placements:
    for i, row in table.iterrows():
        position_counts[row['Team']][row['Position']] += 1

results = []
for team in df['Team']:
    positions = position_counts[team]
    most_common = positions.most_common(1)[0][0]
    results.append({
        "Team": team,
        "Titles": positions[1],
        "Top 4 Finishes": sum(positions[p] for p in range(1, 5)),
        "Relegated (18-20)": sum(positions[p] for p in range(18, 21)),
        "Most Common Position": most_common
    })

st.header("📊 Season Outcome Summary")
st.dataframe(pd.DataFrame(results).sort_values("Titles", ascending=False))
