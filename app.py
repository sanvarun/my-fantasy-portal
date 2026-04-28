import streamlit as st
from itertools import combinations

st.set_page_config(page_title="IPL Team Builder", layout="wide")

# --- SAVED SQUADS DATABASE ---
SQUADS = {
    "PBKS": [
        {"name": "Prabhsimran Singh", "role": "WK"}, {"name": "Vishnu Vinod", "role": "WK"},
        {"name": "Shreyas Iyer", "role": "BAT"}, {"name": "Priyansh Arya", "role": "BAT"},
        {"name": "Nehal Wadhera", "role": "BAT"}, {"name": "Marcus Stoinis", "role": "AR"},
        {"name": "Shashank Singh", "role": "AR"}, {"name": "Azmatullah Omarzai", "role": "AR"},
        {"name": "Marco Jansen", "role": "AR"}, {"name": "Arshdeep Singh", "role": "BOWL"},
        {"name": "Yuzvendra Chahal", "role": "BOWL"}, {"name": "Lockie Ferguson", "role": "BOWL"},
        {"name": "Harpreet Brar", "role": "BOWL"}
    ],
    "RR": [
        {"name": "Dhruv Jurel", "role": "WK"}, {"name": "Donovan Ferreira", "role": "WK"},
        {"name": "Yashasvi Jaiswal", "role": "BAT"}, {"name": "Shimron Hetmyer", "role": "BAT"},
        {"name": "Ravindra Jadeja", "role": "AR"}, {"name": "Riyan Parag", "role": "AR"},
        {"name": "Wanindu Hasaranga", "role": "AR"}, {"name": "Jofra Archer", "role": "BOWL"},
        {"name": "Ravi Bishnoi", "role": "BOWL"}, {"name": "Sandeep Sharma", "role": "BOWL"},
        {"name": "Tushar Deshpande", "role": "BOWL"}, {"name": "Nandre Burger", "role": "BOWL"}
    ]
}

st.title("🏏 Smart Fantasy Portal")

# --- STEP 1: SELECT TEAMS ---
st.sidebar.header("Match Selection")
team1 = st.sidebar.selectbox("Select Team 1", ["PBKS"])
team2 = st.sidebar.selectbox("Select Team 2", ["RR"])

# Combine the players from both selected teams
match_players = []
for p in SQUADS[team1]:
    match_players.append({"name": p['name'], "team": team1, "role": p['role']})
for p in SQUADS[team2]:
    match_players.append({"name": p['name'], "team": team2, "role": p['role']})

# --- STEP 2: SHORTLIST ---
st.header(f"Shortlist Players: {team1} vs {team2}")
player_names = [f"{p['name']} ({p['team']} - {p['role']})" for p in match_players]

selected_display_names = st.multiselect("Pick players you think will perform:", player_names)

# --- STEP 3: GENERATE ---
if len(selected_display_names) >= 11:
    if st.button("Generate All Valid Teams"):
        # Filter the original data based on selection
        shortlist = [p for p in match_players if f"{p['name']} ({p['team']} - {p['role']})" in selected_display_names]
        
        valid_teams = []
        limit = 100 # Stop at 100 teams to keep it fast
        
        for combo in combinations(shortlist, 11):
            roles = [p['role'] for p in combo]
            if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                valid_teams.append(combo)
            if len(valid_teams) >= limit: break
            
        st.success(f"Found {len(valid_teams)} combinations!")
        for i, team in enumerate(valid_teams):
            with st.expander(f"Team {i+1}"):
                for p in team:
                    st.text(f"{p['name']} | {p['role']} | {p['team']}")
else:
    st.info("Please select at least 11 players from the list above.")
