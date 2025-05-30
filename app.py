import streamlit as st
import pandas as pd
from simulate import simulate_season
from collections import Counter

st.set_page_config(page_title="Premier League Simulator", layout="wide")

st.title("🔮 2025–26 Premier League Simulator")

runs = st.slider("Number of simulations", min_value=1000, max_value=10000, step=1000, value=1000)
    
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


st.header("📊 Season Outcome Summary")
st.dataframe(pd.DataFrame(results).sort_values("Titles", ascending=False))
st.header("🔍 View Best or Worst Season for a Team")

team_options = df['Team'].tolist()
selected_team = st.selectbox("Choose a team", team_options, key="team_select")
mode = st.selectbox("Choose view", ["Best", "Worst"], key="mode_select")

selected_table = get_best_or_worst_table(placements, selected_team, mode)

st.subheader(f"{mode} Season for {selected_team}")
st.dataframe(
    selected_table[['Position', 'Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD']].sort_values("Position")
)

# Select team and view mode
team_options = df['Team'].tolist()
selected_team = st.selectbox("Choose a team", team_options, key="team_select")
mode = st.selectbox("Choose view", ["Best", "Worst"], key="mode_select")

# Function to get position of team in a table
def get_team_position(table, team):
    row = table[table['Team'] == team]
    if not row.empty:
        return int(row['Position'].values[0])
    return 999  # Fallback if team not found

# Find the best or worst simulation
if mode == "Best":
    best_table = min(placements, key=lambda tbl: get_team_position(tbl, selected_team))
else:
    best_table = max(placements, key=lambda tbl: get_team_position(tbl, selected_team))

# Show result
st.subheader(f"{mode} Season for {selected_team}")
st.dataframe(best_table[['Position', 'Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD']].sort_values("Position"))


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

