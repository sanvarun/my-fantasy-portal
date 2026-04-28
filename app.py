import streamlit as st
from itertools import combinations
from fpdf import FPDF

# Set page to wide mode for side-by-side view
st.set_page_config(page_title="IPL Fantasy Portal 2026", layout="wide")

# --- OFFICIAL IPL 2026 SQUADS DATABASE ---
SQUADS = {
    "CSK": [
        {"name": "Ruturaj Gaikwad", "role": "BAT"}, {"name": "MS Dhoni", "role": "WK"},
        {"name": "Sanju Samson", "role": "WK"}, {"name": "Dewald Brevis", "role": "BAT"},
        {"name": "Shivam Dube", "role": "AR"}, {"name": "Noor Ahmad", "role": "BOWL"},
        {"name": "Anshul Kamboj", "role": "AR"}, {"name": "Khaleel Ahmed", "role": "BOWL"},
        {"name": "Gurjapneet Singh", "role": "BOWL"}, {"name": "Jamie Overton", "role": "BOWL"},
        {"name": "Mukesh Choudhary", "role": "BOWL"}, {"name": "Prashant Veer", "role": "AR"},
        {"name": "Kartik Sharma", "role": "WK"}, {"name": "Matthew Short", "role": "AR"}
    ],
    "MI": [
        {"name": "Hardik Pandya", "role": "AR"}, {"name": "Rohit Sharma", "role": "BAT"},
        {"name": "Suryakumar Yadav", "role": "BAT"}, {"name": "Jasprit Bumrah", "role": "BOWL"},
        {"name": "Tilak Varma", "role": "BAT"}, {"name": "Mitchell Santner", "role": "AR"},
        {"name": "Trent Boult", "role": "BOWL"}, {"name": "Deepak Chahar", "role": "BOWL"},
        {"name": "Shardul Thakur", "role": "AR"}, {"name": "Will Jacks", "role": "AR"},
        {"name": "Sherfane Rutherford", "role": "BAT"}, {"name": "Naman Dhir", "role": "AR"}
    ],
    "RCB": [
        {"name": "Rajat Patidar", "role": "BAT"}, {"name": "Virat Kohli", "role": "BAT"},
        {"name": "Devdutt Padikkal", "role": "BAT"}, {"name": "Phil Salt", "role": "WK"},
        {"name": "Jitesh Sharma", "role": "WK"}, {"name": "Krunal Pandya", "role": "AR"},
        {"name": "Tim David", "role": "AR"}, {"name": "Josh Hazlewood", "role": "BOWL"},
        {"name": "Bhuvneshwar Kumar", "role": "BOWL"}, {"name": "Yash Dayal", "role": "BOWL"},
        {"name": "Venkatesh Iyer", "role": "BAT"}, {"name": "Swapnil Singh", "role": "AR"}
    ],
    "DC": [
        {"name": "KL Rahul", "role": "WK"}, {"name": "Axar Patel", "role": "AR"},
        {"name": "Kuldeep Yadav", "role": "BOWL"}, {"name": "Tristan Stubbs", "role": "WK"},
        {"name": "Mitchell Starc", "role": "BOWL"}, {"name": "T Natarajan", "role": "BOWL"},
        {"name": "Nitish Rana", "role": "BAT"}, {"name": "Sameer Rizvi", "role": "BAT"},
        {"name": "David Miller", "role": "BAT"}, {"name": "Karun Nair", "role": "BAT"},
        {"name": "Abishek Porel", "role": "WK"}, {"name": "Mukesh Kumar", "role": "BOWL"}
    ],
    "KKR": [
        {"name": "Rinku Singh", "role": "BAT"}, {"name": "Sunil Narine", "role": "AR"},
        {"name": "Varun Chakaravarthy", "role": "BOWL"}, {"name": "Harshit Rana", "role": "BOWL"},
        {"name": "Ramandeep Singh", "role": "AR"}, {"name": "Cameron Green", "role": "AR"},
        {"name": "Matheesha Pathirana", "role": "BOWL"}, {"name": "Angkrish Raghuvanshi", "role": "BAT"},
        {"name": "Rahul Tripathi", "role": "BAT"}, {"name": "Manish Pandey", "role": "BAT"},
        {"name": "Ajinkya Rahane", "role": "BAT"}, {"name": "Vaibhav Arora", "role": "BOWL"}
    ],
    "RR": [
        {"name": "Ravindra Jadeja", "role": "AR"}, {"name": "Sam Curran", "role": "AR"},
        {"name": "Donovan Ferreira", "role": "WK"}, {"name": "Yashasvi Jaiswal", "role": "BAT"},
        {"name": "Riyan Parag", "role": "AR"}, {"name": "Dhruv Jurel", "role": "WK"},
        {"name": "Shimron Hetmyer", "role": "BAT"}, {"name": "Jofra Archer", "role": "BOWL"},
        {"name": "Ravi Bishnoi", "role": "BOWL"}, {"name": "Sandeep Sharma", "role": "BOWL"},
        {"name": "Tushar Deshpande", "role": "BOWL"}, {"name": "Nandre Burger", "role": "BOWL"}
    ],
    "GT": [
        {"name": "Shubman Gill", "role": "BAT"}, {"name": "Rashid Khan", "role": "BOWL"},
        {"name": "Sai Sudharsan", "role": "BAT"}, {"name": "Mohammed Siraj", "role": "BOWL"},
        {"name": "Kagiso Rabada", "role": "BOWL"}, {"name": "Jos Buttler", "role": "WK"},
        {"name": "Washington Sundar", "role": "AR"}, {"name": "Rahul Tewatia", "role": "AR"},
        {"name": "Shahrukh Khan", "role": "BAT"}, {"name": "Prasidh Krishna", "role": "BOWL"},
        {"name": "Ishant Sharma", "role": "BOWL"}, {"name": "Glenn Phillips", "role": "AR"}
    ],
    "LSG": [
        {"name": "Rishabh Pant", "role": "WK"}, {"name": "Nicholas Pooran", "role": "WK"},
        {"name": "Mayank Yadav", "role": "BOWL"}, {"name": "Mohammed Shami", "role": "BOWL"},
        {"name": "Avesh Khan", "role": "BOWL"}, {"name": "Abdul Samad", "role": "BAT"},
        {"name": "Aiden Markram", "role": "BAT"}, {"name": "Mitchell Marsh", "role": "AR"},
        {"name": "Ayush Badoni", "role": "BAT"}, {"name": "Himmat Singh", "role": "BAT"},
        {"name": "Arjun Tendulkar", "role": "AR"}, {"name": "Shahbaz Ahmed", "role": "AR"}
    ],
    "SRH": [
        {"name": "Pat Cummins", "role": "BOWL"}, {"name": "Abhishek Sharma", "role": "BAT"},
        {"name": "Travis Head", "role": "BAT"}, {"name": "Heinrich Klaasen", "role": "WK"},
        {"name": "Nitish Kumar Reddy", "role": "AR"}, {"name": "Harshal Patel", "role": "BOWL"},
        {"name": "Ishan Kishan", "role": "WK"}, {"name": "Liam Livingstone", "role": "AR"},
        {"name": "Jaydev Unadkat", "role": "BOWL"}, {"name": "Brydon Carse", "role": "BOWL"},
        {"name": "T Natarajan", "role": "BOWL"}, {"name": "Kamindu Mendis", "role": "AR"}
    ],
    "PBKS": [
        {"name": "Prabhsimran Singh", "role": "WK"}, {"name": "Shreyas Iyer", "role": "BAT"},
        {"name": "Marcus Stoinis", "role": "AR"}, {"name": "Arshdeep Singh", "role": "BOWL"},
        {"name": "Yuzvendra Chahal", "role": "BOWL"}, {"name": "Shashank Singh", "role": "AR"},
        {"name": "Nehal Wadhera", "role": "BAT"}, {"name": "Harpreet Brar", "role": "BOWL"},
        {"name": "Marco Jansen", "role": "AR"}, {"name": "Lockie Ferguson", "role": "BOWL"},
        {"name": "Azmatullah Omarzai", "role": "AR"}, {"name": "Musheer Khan", "role": "BAT"}
    ]
}

# --- PDF HELPERS ---
def create_pdf(teams):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Today's Fantasy Lineups", ln=True, align='C')
    pdf.ln(10)
    for i, team in enumerate(teams):
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, txt=f"TEAM {i+1}", ln=True)
        pdf.set_font("Arial", size=10)
        player_list = ", ".join([f"{p['name']} ({p['role']})" for p in team])
        pdf.multi_cell(0, 8, txt=player_list)
        pdf.ln(2)
        pdf.cell(0, 0, '', 'T')
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR: MATCH SETUP ---
st.sidebar.title("🏆 Match Setup")
all_teams = sorted(list(SQUADS.keys()))
team1_name = st.sidebar.selectbox("Select Team 1", all_teams, index=all_teams.index("CSK") if "CSK" in all_teams else 0)
team2_name = st.sidebar.selectbox("Select Team 2", all_teams, index=all_teams.index("MI") if "MI" in all_teams else 1)

# --- MAIN SCREEN ---
st.title(f"🏏 {team1_name} vs {team2_name}")
st.subheader("Step 1: Shortlist players from both squads")

col1, col2 = st.columns(2)
shortlist = []

with col1:
    st.markdown(f"### {team1_name} Squad")
    for p in SQUADS[team1_name]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"t1_{p['name']}"):
            shortlist.append(p)

with col2:
    st.markdown(f"### {team2_name} Squad")
    for p in SQUADS[team2_name]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"t2_{p['name']}"):
            shortlist.append(p)

st.divider()

# --- GENERATION ---
if len(shortlist) >= 11:
    if st.button("Generate 100 Best Combinations", type="primary"):
        valid_teams = []
        for combo in combinations(shortlist, 11):
            roles = [p['role'] for p in combo]
            # Standard Rule: Min 1 of each category
            if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                valid_teams.append(combo)
            if len(valid_teams) >= 100:
                break
        
        st.success(f"Generated {len(valid_teams)} teams!")
        
        # Download PDF
        pdf_data = create_pdf(valid_teams)
        st.download_button(label="📥 Download PDF", data=pdf_data, file_name="ipl_teams.pdf", mime="application/pdf")
        
        # Display Preview
        t_cols = st.columns(3)
        for i, team in enumerate(valid_teams):
            with t_cols[i % 3]:
                with st.expander(f"Team {i+1}"):
                    for p in team:
                        st.write(f"• {p['name']} ({p['role']})")
else:
    st.info("Please select at least 11 players total to start generating.")
