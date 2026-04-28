import streamlit as st
from itertools import combinations

# Setup the page - wide layout is best
st.set_page_config(page_title="PBKS vs RR - Full Squads", layout="wide")

# --- FULL SQUADS DATABASE (Ref: Cricbuzz Screenshot) ---
# NOTE: To improve combination logic, All-Rounders (ALL) are categorized as BAT or BOWL
# based on whether they are "Batting All-Rounders" or "Bowling All-Rounders".
# (WK still counts as WK, simple ALL are AR)
SQUADS = {
    "PBKS": [
        {"name": "Prabhsimran Singh", "role": "WK"},
        {"name": "Shreyas Iyer", "role": "BAT", "details": "(C)"},
        {"name": "Priyansh Arya", "role": "BAT"},
        {"name": "Cooper Connolly", "role": "BAT", "details": "(Bat ALL)"}, # Treat as Batting option
        {"name": "Shashank Singh", "role": "BAT", "details": "(Bat ALL)"}, # Treat as Batting option
        {"name": "Marcus Stoinis", "role": "BAT", "details": "(Bat ALL)"}, # Treat as Batting option
        {"name": "Marco Jansen", "role": "BOWL", "details": "(Bowl ALL)"}, # Treat as Bowling option
        {"name": "Xavier Bartlett", "role": "BOWL"},
        {"name": "Vijaykumar Vyshak", "role": "BOWL"},
        {"name": "Arshdeep Singh", "role": "BOWL"},
        {"name": "Yuzvendra Chahal", "role": "BOWL"},
        {"name": "Nehal Wadhera", "role": "BAT"},
        {"name": "Suryansh Shedge", "role": "AR"}, # Simple ALL count as AR
        {"name": "Harpreet Brar", "role": "BOWL"},
        {"name": "Vishnu Vinod", "role": "WK"},
        {"name": "Yash Thakur", "role": "BOWL"},
        {"name": "Ben Dwarshuis", "role": "BOWL"},
        {"name": "Praveen Dubey", "role": "BOWL", "details": "(Bowl ALL)"}, # Treat as Bowling option
        {"name": "Lockie Ferguson", "role": "BOWL"},
        {"name": "Azmatullah Omarzai", "role": "BOWL", "details": "(Bowl ALL)"}, # Treat as Bowling option
        {"name": "Mitchell Owen", "role": "AR"}, # Simple ALL count as AR
        {"name": "Harnoor Singh", "role": "BAT"},
        {"name": "Musheer Khan", "role": "BAT", "details": "(Bat ALL)"}, # Treat as Batting option
        {"name": "Pyla Avinash", "role": "BAT"},
        {"name": "Vishal Nishad", "role": "AR"} # Simple ALL count as AR
    ],
    "RR": [
        {"name": "Dhruv Jurel", "role": "WK"},
        {"name": "Riyan Parag", "role": "BAT", "details": "(Bat ALL, C)"}, # Treat as Batting option
        {"name": "Yashasvi Jaiswal", "role": "BAT"},
        {"name": "Vaibhav Suryavanshi", "role": "BAT"},
        {"name": "Shimron Hetmyer", "role": "BAT"},
        {"name": "Donovan Ferreira", "role": "WK"},
        {"name": "Ravindra Jadeja", "role": "BOWL", "details": "(Bowl ALL)"}, # Treat as Bowling option
        {"name": "Jofra Archer", "role": "BOWL"},
        {"name": "Tushar Deshpande", "role": "BOWL"},
        {"name": "Nandre Burger", "role": "BOWL"},
        {"name": "Brijesh Sharma", "role": "BOWL"},
        {"name": "Ravi Bishnoi", "role": "BOWL"},
        {"name": "Lhuan-dre Pretorius", "role": "WK"},
        {"name": "Ravi Singh", "role": "WK"},
        {"name": "Sandeep Sharma", "role": "BOWL"},
        {"name": "Shubham Dubey", "role": "BAT"},
        {"name": "Adam Milne", "role": "BOWL"},
        {"name": "Dasun Shanaka", "role": "BAT", "details": "(Bat ALL)"}, # Treat as Batting option
        {"name": "Kuldeep Sen", "role": "BOWL"},
        {"name": "Sushant Mishra", "role": "BOWL"},
        {"name": "Yudhvir Singh Chorka", "role": "BOWL"},
        {"name": "Kwena Maphaka", "role": "BOWL"},
        {"name": "Vignesh Puthur", "role": "BOWL"},
        {"name": "Yash Raj Punja", "role": "BOWL"},
        {"name": "Aman Rao Peralta", "role": "BOWL"}
    ]
}

st.title("🏏 Official PBKS vs RR - Side-by-Side Selector")

# --- SIDEBAR: MATCH INFO & SETUP ---
st.sidebar.header("Match Setup")
st.sidebar.info(f"{len(SQUADS['PBKS'])} PBKS players vs {len(SQUADS['RR'])} RR players loaded.")

# Team Selection
team1_name = st.sidebar.selectbox("Team 1", ["PBKS"])
team2_name = st.sidebar.selectbox("Team 2", ["RR"])

# --- MAIN SELECTION GRID ---
st.subheader("Step 1: Pick your shortlist from both squads")
col1, col2 = st.columns(2)

shortlist = []

with col1:
    st.markdown(f"### <span style='color: #ED1C24;'>{team1_name}</span>", unsafe_allow_html=True)
    for p in SQUADS[team1_name]:
        # Build the displayed label with details if available
        details_text = f" {p.get('details', '')}"
        label = f"{p['name']} ({p['role']}){details_text}"
        if st.checkbox(label, key=f"t1_{p['name']}"):
            # We add to the shortlist using the 'role' we assigned (BAT/BOWL/WK/AR)
            shortlist.append({"name": p['name'], "team": team1_name, "role": p['role']})

with col2:
    st.markdown(f"### <span style='color: #FF5A00;'>{team2_name}</span>", unsafe_allow_html=True)
    for p in SQUADS[team2_name]:
        details_text = f" {p.get('details', '')}"
        label = f"{p['name']} ({p['role']}){details_text}"
        if st.checkbox(label, key=f"t2_{p['name']}"):
            shortlist.append({"name": p['name'], "team": team2_name, "role": p['role']})

# --- GENERATION SECTION ---
st.divider()
st.subheader(f"Step 2: Generate Combinations ({len(shortlist)} selected)")

# Minimum check to prevent empty clicks
if len(shortlist) >= 11:
    if st.button("Generate Teams", type="primary"):
        # We need to process the roles we *actually* shortlisted (BAT/BOWL/WK/AR)
        # to ensure the combinations are valid.
        
        valid_teams = []
        limit = 100 # Adjust this if needed, 100 is safe and fast
        
        with st.spinner("Calculating billions of possibilities..."):
            for combo in combinations(shortlist, 11):
                # Count roles based on the categorization we applied (BAT/BOWL/WK/AR)
                current_roles = [p['role'] for p in combo]
                
                # Minimum Constraint: At least one of each role
                if all(current_roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                    # Check if AR role is mandatory (e.g., Suryansh Shedge was the only AR in PBKS)
                    # For most combinations, the default BAT/BOWL/WK rule is enough.
                    valid_teams.append(combo)
                
                if len(valid_teams) >= limit:
                    break
        
        if valid_teams:
            st.success(f"Created {len(valid_teams)} combinations! (Showing top {limit})")
            
            # Displaying teams in a cleaner grid format
            team_cols = st.columns(3) # Show 3 teams per row
            for i, team in enumerate(valid_teams):
                with team_cols[i % 3]:
                    with st.expander(f"📋 Team {i+1}", expanded=False):
                        # Presenting the team with visual hierarchy
                        for p in team:
                            st.write(f"• **{p['name']}** ({p['role']}) | {p['team']}")
        else:
            st.error("No valid teams found with your shortlist. Try selecting more players or a better balance of roles.")
else:
    st.warning("Please select at least 11 players total by checking the boxes above.")
