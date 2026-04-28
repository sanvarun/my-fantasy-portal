import streamlit as st
from itertools import combinations
from fpdf import FPDF
import base64

st.set_page_config(page_title="Pro Fantasy Portal", layout="wide")

# --- SQUAD DATA ---
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

def create_pdf(teams):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="My Fantasy Teams - PBKS vs RR", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    
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

st.title("🏏 Fantasy Portal with PDF Export")

# --- SELECTION ---
col1, col2 = st.columns(2)
shortlist = []
with col1:
    st.header("PBKS")
    for p in SQUADS["PBKS"]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"pbks_{p['name']}"):
            shortlist.append(p)
with col2:
    st.header("RR")
    for p in SQUADS["RR"]:
        if st.checkbox(f"{p['name']} ({p['role']})", key=f"rr_{p['name']}"):
            shortlist.append(p)

# --- GENERATE ---
if len(shortlist) >= 11:
    if st.button("Generate & Save Teams", type="primary"):
        valid_teams = []
        for combo in combinations(shortlist, 11):
            roles = [p['role'] for p in combo]
            if all(roles.count(r) >= 1 for r in ['BAT', 'WK', 'AR', 'BOWL']):
                valid_teams.append(combo)
            if len(valid_teams) >= 100:
                break
        
        if valid_teams:
            st.success(f"Generated {len(valid_teams)} teams!")
            
            # PDF Download Button
            pdf_data = create_pdf(valid_teams)
            st.download_button(
                label="📥 Download Teams as PDF",
                data=pdf_data,
                file_name="my_fantasy_teams.pdf",
                mime="application/pdf"
            )
            
            # Display Preview
            for i, team in enumerate(valid_teams[:10]):
                with st.expander(f"Team {i+1} Preview"):
                    st.write(", ".join([p['name'] for p in team]))
else:
    st.info("Select 11 players to begin.")
