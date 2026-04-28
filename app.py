import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Fantasy Team Builder", layout="wide")
st.title("🏏 My Fantasy Team Generator")

# 1. Simple Data Entry
st.sidebar.header("Step 1: Enter Squads")
raw_data = st.sidebar.text_area("Paste players (Name, Team, Role) one per line. Example: V. Kohli, RCB, BAT", 
                                height=200)

# 2. Parsing the data
players = []
if raw_data:
    for line in raw_data.split('\n'):
        if ',' in line:
            parts = line.split(',')
            players.append({"name": parts[0].strip(), "team": parts[1].strip(), "role": parts[2].strip().upper()})

if players:
    # 3. Shortlisting
    st.header("Step 2: Shortlist Players (11 - 50)")
    names = [p['name'] for p in players]
    shortlist_names = st.multiselect("Select players for this match:", names)
    
    # 4. Combination Logic
    if len(shortlist_names) >= 11:
        st.success(f"Shortlisted {len(shortlist_names)} players.")
        if st.button("Generate All Probability Teams"):
            selected_players = [p for p in players if p['name'] in shortlist_names]
            
            valid_teams = []
            count = 0
            # Warning: combinations can be huge, we limit to first 500 for speed
            for combo in combinations(selected_players, 11):
                roles = [p['role'] for p in combo]
                # Rules: At least 1 of each
                if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                    valid_teams.append(combo)
                    count += 1
                if count >= 100: break # Show first 100 teams to prevent crashing
            
            st.write(f"Found {count} valid combinations (showing top 100):")
            for i, team in enumerate(valid_teams):
                with st.expander(f"Team {i+1}"):
                    for p in team:
                        st.write(f"- {p['name']} ({p['team']}) [{p['role']}]")
    else:
        st.warning("Please select at least 11 players.")
else:
    st.info("Please enter your squad list in the sidebar to start!")
