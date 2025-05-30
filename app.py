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

if placements:
    all_tables = pd.concat(placements)
else:
    st.error("No simulation data was generated. Please try again.")
    st.stop()

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

st.header("📊 Season Outcome Summary")
st.dataframe(pd.DataFrame(results).sort_values("Titles", ascending=False))

st.header("📈 Explore Best/Worst Season for a Team")

# UI controls
team_options = placements[0]['Team'].tolist()
selected_team = st.selectbox("Select a team", team_options)
best_or_worst = st.selectbox("Select best or worst season", ["Best", "Worst"])

# Function to get position and points of a team in a table
def get_team_metrics(table, team):
    row = table[table['Team'] == team]
    if not row.empty:
        return int(row['Position'].values[0]), int(row['Pts'].values[0])
    return 999, -1  # fallback

# Function to get the best/worst table for the selected team
def get_team_metrics(table, team):
    row = table[table['Team'] == team]
    if row.empty:
        return (999, -1)
    return int(row['Position'].values[0]), int(row['Pts'].values[0])

def get_best_or_worst_table(placements, team, mode="Best"):
    if mode == "Best":
        # Best: prioritize best (lowest) position, then highest points
        return min(placements, key=lambda tbl: (get_team_metrics(tbl, team)[0], -get_team_metrics(tbl, team)[1]))
    else:
        # Step 1: Find the worst (highest number) position this team ever finished
        worst_position = max(get_team_metrics(tbl, team)[0] for tbl in placements)

        # Step 2: Filter only the tables where the team finished in that exact worst position
        tied_tables = [tbl for tbl in placements if get_team_metrics(tbl, team)[0] == worst_position]

        # Step 3: From those, return the one where they had the fewest points
        return min(tied_tables, key=lambda tbl: get_team_metrics(tbl, team)[1])


# Get the table and show it
selected_table = get_best_or_worst_table(placements, selected_team, best_or_worst)

st.subheader(f"{best_or_worst} Season for {selected_team}")
st.dataframe(
    selected_table[['Team', 'W', 'D', 'L', 'Pts', 'GF', 'GA', 'GD', 'Position']].sort_values("Position")
)
