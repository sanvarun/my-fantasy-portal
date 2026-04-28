import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Pro Fantasy Portal", layout="wide")

# --- UPDATED SQUADS DATA ---
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

st.title("🏏 Side-by-Side Player Selector")

# --- SIDEBAR SELECTION ---
st.sidebar.header("Match Setup")
team1_name = st.sidebar.selectbox("Team 1", ["PBKS"])
team2_name = st.sidebar.selectbox("Team 2", ["RR"])

# --- MAIN SELECTION GRID ---
st.subheader("Step 1: Pick your shortlist from both squads")
col1, col2 = st.columns(2)

shortlist = []

with col1:
    st.markdown(f"### {team1_name}")
    for p in SQUADS[team1_name]:
        # Create a unique label for the checkbox
        label = f"{p['name']} ({p['role']})"
        if st.checkbox(label, key=f"t1_{p['name']}"):
            shortlist.append({"name": p['name'], "team": team1_name, "role": p['role']})

with col2:
    st.markdown(f"### {team2_name}")
    for p in SQUADS[team2_name]:
        label = f"{p['name']} ({p['role']})"
        if st.checkbox(label, key=f"t2_{p['name']}"):
            shortlist.append({"name": p['name'], "team": team2_name, "role": p['role']})

# --- GENERATION SECTION ---
st.divider()
st.subheader(f"Step 2: Generate Combinations ({len(shortlist)} selected)")

if len(shortlist) >= 11:
    if st.button("Generate Teams"):
        valid_teams = []
        # Calculate combinations (Limit to 100 for speed)
        for combo in combinations(shortlist, 11):
            roles = [p['role'] for p in combo]
            # Rule: At least 1 of each role
            if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                valid_teams.append(combo)
            if len(valid_teams) >= 100: break
        
        st.success(f"Created {len(valid_teams)} probability teams!")
        
        # Displaying teams in a cleaner grid format
        team_cols = st.columns(3) # Show 3 teams per row
        for i, team in enumerate(valid_teams):
            with team_cols[i % 3]:
                with st.expander(f"📋 Team {i+1}", expanded=False):
                    for p in team:
                        st.write(f"• **{p['name']}** ({p['role']})")
else:
    st.info("Select at least 11 players by checking the boxes above.")
