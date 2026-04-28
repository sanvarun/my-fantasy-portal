import streamlit as st
from itertools import combinations
from fpdf import FPDF

st.set_page_config(page_title="PBKS vs RR - Side Selector", layout="wide")

# --- DATABASE ---
SQUADS = {
    "PBKS": [
        {"name": "Prabhsimran Singh", "role": "WK"}, {"name": "Shreyas Iyer", "role": "BAT"},
        {"name": "Priyansh Arya", "role": "BAT"}, {"name": "Cooper Connolly", "role": "BAT"},
        {"name": "Shashank Singh", "role": "BAT"}, {"name": "Marcus Stoinis", "role": "BAT"},
        {"name": "Marco Jansen", "role": "BOWL"}, {"name": "Xavier Bartlett", "role": "BOWL"},
        {"name": "Vijaykumar Vyshak", "role": "BOWL"}, {"name": "Arshdeep Singh", "role": "BOWL"},
        {"name": "Yuzvendra Chahal", "role": "BOWL"}, {"name": "Nehal Wadhera", "role": "BAT"},
        {"name": "Suryansh Shedge", "role": "AR"}, {"name": "Harpreet Brar", "role": "BOWL"},
        {"name": "Vishnu Vinod", "role": "WK"}, {"name": "Yash Thakur", "role": "BOWL"},
        {"name": "Ben Dwarshuis", "role": "BOWL"}, {"name": "Praveen Dubey", "role": "BOWL"},
        {"name": "Lockie Ferguson", "role": "BOWL"}, {"name": "Azmatullah Omarzai", "role": "BOWL"},
        {"name": "Mitchell Owen", "role": "AR"}, {"name": "Harnoor Singh", "role": "BAT"},
        {"name": "Musheer Khan", "role": "BAT"}, {"name": "Pyla Avinash", "role": "BAT"},
        {"name": "Vishal Nishad", "role": "AR"}
    ],
    "RR": [
        {"name": "Dhruv Jurel", "role": "WK"}, {"name": "Riyan Parag", "role": "BAT"},
        {"name": "Yashasvi Jaiswal", "role": "BAT"}, {"name": "Vaibhav Suryavanshi", "role": "BAT"},
        {"name": "Shimron Hetmyer", "role": "BAT"}, {"name": "Donovan Ferreira", "role": "WK"},
        {"name": "Ravindra Jadeja", "role": "BOWL"}, {"name": "Jofra Archer", "role": "BOWL"},
        {"name": "Tushar Deshpande", "role": "BOWL"}, {"name": "Nandre Burger", "role": "BOWL"},
        {"name": "Brijesh Sharma", "role": "BOWL"}, {"name": "Ravi Bishnoi", "role": "BOWL"},
        {"name": "Lhuan-dre Pretorius", "role": "WK"}, {"name": "Ravi Singh", "role": "WK"},
        {"name": "Sandeep Sharma", "role": "BOWL"}, {"name": "Shubham Dubey", "role": "BAT"},
        {"name": "Adam Milne", "role": "BOWL"}, {"name": "Dasun Shanaka", "role": "BAT"},
        {"name": "Kuldeep Sen", "role": "BOWL"}, {"name": "Sushant Mishra", "role": "BOWL"},
        {"name": "Yudhvir Singh Chorka", "role": "BOWL"}, {"name": "Kwena Maphaka", "role": "BOWL"},
        {"name": "Vignesh Puthur", "role": "BOWL"}, {"name": "Yash Raj Punja", "role": "BOWL"},
        {"name": "Aman Rao Peralta", "role": "BOWL"}
    ]
}

# --- PDF LOGIC ---
def create_pdf(teams):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="FANTASY TEAMS - PBKS VS RR", ln=True, align='C')
    pdf.ln(5)
    for i, team in enumerate(teams):
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, txt=f"TEAM {i+1}:", ln=True)
        pdf.set_font("Arial", size=9)
        names = ", ".join([f"{p['name']} ({p['role']})" for p in team])
        pdf.multi_cell(0, 6, txt=names)
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR ---
st.sidebar.title("⚙️ Match Setup")
match_name = st.sidebar.selectbox("Select Match", ["PBKS vs RR"])
st.sidebar.write("Step 1: Check your favorites.")
st.sidebar.write("Step 2: Hit Generate.")
st.sidebar.write("Step 3: Save PDF.")

# --- MAIN SCREEN ---
st.title("🏏 Player Shortlist")
col1, col2 = st.columns(2)
shortlist = []

with col1:
    st.markdown("### 🔴 PBKS Squad")
    for p in SQUADS["PBKS"]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"p_{p['name']}"):
            shortlist.append(p)

with col2:
    st.markdown("### 🔵 RR Squad")
    for p in SQUADS["RR"]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"r_{p['name']}"):
            shortlist.append(p)

st.divider()

# --- RESULTS ---
if len(shortlist) >= 11:
    if st.button("🚀 Generate 100 Teams", type="primary"):
        valid_teams = []
        for combo in combinations(shortlist, 11):
            roles = [p['role'] for p in combo]
            if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                valid_teams.append(combo)
            if len(valid_teams) >= 100: break
        
        st.success(f"Generated {len(valid_teams)} combinations!")
        
        # Download Link
        pdf_bytes = create_pdf(valid_teams)
        st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="teams.pdf", mime="application/pdf")
        
        # Grid Display
        grid = st.columns(3)
        for i, team in enumerate(valid_teams):
            with grid[i % 3]:
                with st.expander(f"Team {i+1}"):
                    for p in team:
                        st.write(f"- {p['name']}")
else:
    st.info("Pick at least 11 players from the squads above.")
