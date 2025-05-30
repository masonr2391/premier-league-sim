import streamlit as st
import pandas as pd
from simulate import simulate_season
from collections import Counter

st.set_page_config(page_title="Premier League Simulator", layout="wide")

st.title("\U0001F52E 2025–26 Premier League Simulator")

runs = st.slider("Number of simulations", min_value=1000, max_value=10000, step=1000, value=1000)

# Run simulations once per unique "runs" input
if "placements" not in st.session_state or st.session_state.runs != runs:
    st.session_state.placements = []
    st.session_state.runs = runs

    progress_bar = st.progress(0)
    with st.spinner(f"Simulating {runs:,} seasons..."):
        for i in range(runs):
            try:
                df = simulate_season()
                st.session_state.placements.append(df)
            except Exception as e:
                st.warning(f"Simulation {i+1} failed: {e}")

            if i % 100 == 0:
                progress_bar.progress(i / runs)

placements = st.session_state.placements

if placements:
    all_tables = pd.concat(placements)
else:
    st.error("No simulation data was generated. Please try again.")
    st.stop()

# Position stats
position_counts = {team: Counter() for team in placements[0]['Team']}
for table in placements:
    for i, row in table.iterrows():
        position_counts[row['Team']][row['Position']] += 1

results = []
for team in placements[0]['Team']:
    positions = position_counts[team]
    most_common = positions.most_common(1)[0][0]
    results.append({
        "Team": team,
        "Titles": positions[1],
        "Top 4 Finishes": sum(positions[p] for p in range(1, 5)),
        "Relegated (18-20)": sum(positions[p] for p in range(18, 21)),
        "Most Common Position": most_common
    })

st.header("\U0001F4CA Season Outcome Summary")
st.dataframe(pd.DataFrame(results).sort_values("Titles", ascending=False))

st.header("\U0001F50D View Best or Worst Season for a Team")

team_options = placements[0]['Team'].tolist()
selected_team = st.selectbox("Choose a team", team_options, key="team_select")
mode = st.selectbox("Choose view", ["Best", "Worst"], key="mode_select")

# --- Find the best or worst season by position, then points ---
def get_team_position_and_points(table, team):
    row = table[table['Team'] == team]
    if row.empty:
        return (999, -1)  # fallback
    return int(row['Position'].values[0]), int(row['Pts'].values[0])

def get_best_or_worst_table(placements, team, mode="Best"):
    reverse = mode == "Worst"

    def sort_key(tbl):
        pos, pts = get_team_position_and_points(tbl, team)
        return (pos, pts if not reverse else -pts)

    return sorted(placements, key=sort_key, reverse=reverse)[0]

selected_table = get_best_or_worst_table(placements, selected_team, mode)

st.subheader(f"{mode} Season for {selected_team}")
st.dataframe(
    selected_table[['Position', 'Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD']].sort_values("Position")
)

st.header("\U0001F4C8 Explore Best/Worst Season for a Team (Legacy Test)")

# Additional select to validate UI
selected_team_2 = st.selectbox("Select a team", team_options, key="team_select_2")
best_or_worst = st.selectbox("Select best or worst season", ["Best", "Worst"], key="mode_select_2")

selected_table_2 = get_best_or_worst_table(placements, selected_team_2, best_or_worst)

st.subheader(f"{best_or_worst} Season for {selected_team_2}")
st.dataframe(
    selected_table_2[['Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD', 'Position']].sort_values("Position")
)
