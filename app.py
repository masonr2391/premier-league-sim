import streamlit as st
import pandas as pd
from simulate import simulate_season
from collections import Counter

st.set_page_config(page_title="Premier League Simulator", layout="wide")

st.title("🔮 2025–26 Premier League Simulator")

runs = st.slider("Number of simulations", min_value=1000, max_value=10000, step=1000, value=1000)
    
placements = []
progress_bar = st.progress(0)

with st.spinner(f"Simulating {runs:,} seasons..."):
    for i in range(runs):
        try:
            df = simulate_season()
            placements.append(df)
        except Exception as e:
            st.warning(f"Simulation {i+1} failed: {e}")

        if i % 100 == 0:
            progress_bar.progress(i / runs)

if placements:
    all_tables = pd.concat(placements)
else:
    st.error("No simulation data was generated. Please try again.")
    st.stop()


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

st.header("📈 Explore Best/Worst Season for a Team")

# UI controls
team_options = df['Team'].tolist()
selected_team = st.selectbox("Select a team", team_options)
best_or_worst = st.selectbox("Select best or worst season", ["Best", "Worst"])

# Find the simulation where the selected team had their best/worst position
def get_best_or_worst_table(placements, team, mode="Best"):
    if mode == "Best":
        best_index = min(
            enumerate(placements),
            key=lambda x: x[1].loc[x[1]['Team'] == team, 'Position'].values[0]
        )[0]
    else:
        best_index = max(
            enumerate(placements),
            key=lambda x: x[1].loc[x[1]['Team'] == team, 'Position'].values[0]
        )[0]
    return placements[best_index]

# Get the table and show it
selected_table = get_best_or_worst_table(placements, selected_team, best_or_worst)
st.subheader(f"{best_or_worst} Season for {selected_team}")
st.dataframe(selected_table[['Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD', 'Position']])

