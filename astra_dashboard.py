import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="ASTRA Mission Control", layout="wide")

# ---------- COSMOS UI ----------
st.markdown("""
<style>

.stApp {
background-image: url("https://images.unsplash.com/photo-1462331940025-496dfbfc7564");
background-size: cover;
background-attachment: fixed;
color:white;
}

h1,h2,h3,h4,h5,p,label{
color:white !important;
}

footer {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown(
"<h1 style='text-align:center'>🚀 ASTRA Mission Control</h1>",
unsafe_allow_html=True
)

st.write("Adaptive Skill Telemetry & Readiness Analyzer")

st.divider()

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs([
" Telemetry Input",
" Mission Control",
"Analytics"
])

# =====================================================
# TAB 1 — INPUT
# =====================================================

with tab1:

    st.header("Student Telemetry Input")

    mode = st.selectbox(
    " Target Career Mode",
    ["Product Company","Startup","Service Company"]
    )

    col1,col2,col3 = st.columns(3)

    with col1:
        easy = st.number_input("Easy DSA Problems",0,1000)
        medium = st.number_input("Medium DSA Problems",0,1000)
        hard = st.number_input("Hard DSA Problems",0,1000)

    with col2:
        project = st.selectbox(
        "Project Type",
        ["Basic Project","CRUD Application","Full Stack","AI/ML Project","Deployed Product"]
        )

        internship = st.selectbox(
        "Internship Type",
        ["None","Local Company","Startup","Mid-size Tech","Large Tech"]
        )

    with col3:
        hackathon_level = st.selectbox(
        "Hackathon Level",
        ["College","State","National","International"]
        )

        hackathon_position = st.selectbox(
        "Position",
        ["Participation","Top 10","Finalist","Winner"]
        )

    cgpa = st.slider("CGPA",0.0,10.0,7.0)

    st.subheader("Verification Evidence")

    hackathon_cert = st.file_uploader("Upload Hackathon Certificate",type=["pdf","png","jpg"])
    internship_doc = st.file_uploader("Upload Internship Proof",type=["pdf","png","jpg"])
    github_link = st.text_input("GitHub Project Link")

    calculate = st.button(" Calculate Mission Readiness")

# =====================================================
# CALCULATIONS
# =====================================================

if calculate:

    # ---------- DSA ----------
    dsa_raw = easy*1 + medium*3 + hard*5
    dsa = min((dsa_raw/700)*100,100)

    # ---------- PROJECT ----------
    project_score = {
        "Basic Project":30,
        "CRUD Application":50,
        "Full Stack":70,
        "AI/ML Project":85,
        "Deployed Product":100
    }[project]

    # ---------- INTERNSHIP ----------
    internship_score = {
        "None":0,
        "Local Company":40,
        "Startup":60,
        "Mid-size Tech":75,
        "Large Tech":90
    }[internship]

    # ---------- HACKATHON (IMPROVED SCORING) ----------
    level_score = {
        "College":40,
        "State":60,
        "National":80,
        "International":100
    }[hackathon_level]

    multiplier = {
        "Participation":0.6,
        "Top 10":0.8,
        "Finalist":0.9,
        "Winner":1
    }[hackathon_position]

    hackathon_score = level_score * multiplier

    # ---------- CORE ----------
    core_cs = (cgpa/10)*100
    communication = 70

    # ---------- ADAPTIVE WEIGHTS ----------
    if mode == "Product Company":
        w_dsa,w_proj,w_cs,w_int,w_hack,w_comm = 0.4,0.2,0.15,0.1,0.1,0.05
    elif mode == "Startup":
        w_dsa,w_proj,w_cs,w_int,w_hack,w_comm = 0.25,0.35,0.1,0.1,0.15,0.05
    else:
        w_dsa,w_proj,w_cs,w_int,w_hack,w_comm = 0.25,0.15,0.2,0.15,0.05,0.2

    readiness = (
        w_dsa*dsa +
        w_proj*project_score +
        w_cs*core_cs +
        w_int*internship_score +
        w_hack*hackathon_score +
        w_comm*communication
    )

# =====================================================
# TAB 2 — MISSION CONTROL
# =====================================================

    with tab2:

        # Mission banner
        if readiness >= 75:
            status = " MISSION READY"
        elif readiness >= 60:
            status = " MISSION IMPROVING"
        else:
            status = " MISSION RISK"

        st.markdown(f"<h2 style='text-align:center'>{status}</h2>", unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Readiness",round(readiness,1))
        col2.metric("DSA Score",round(dsa,1))
        col3.metric("Projects",project_score)
        col4.metric("Internship",internship_score)

        # Gauge
        gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=readiness,
        title={'text':"Placement Readiness"},
        gauge={
        'axis':{'range':[0,100]},
        'steps':[
        {'range':[0,50],'color':'red'},
        {'range':[50,70],'color':'orange'},
        {'range':[70,100],'color':'green'}
        ]
        }
        ))

        st.plotly_chart(gauge,use_container_width=True)

        st.progress(readiness/100)

        st.subheader("Subsystem Health Telemetry")

        st.write("DSA Engine")
        st.progress(dsa/100)

        st.write("Project Payload")
        st.progress(project_score/100)

        st.write("Core Navigation")
        st.progress(core_cs/100)

        st.write("Internship Dock")
        st.progress(internship_score/100)

        st.write("Hackathon Sensor")
        st.progress(hackathon_score/100)

        # ---------- STATUS LABEL ----------
        def system_status(score):
            if score >= 85:
                return "🟢 Excellent"
            elif score >= 70:
                return "🟢 Good"
            elif score >= 50:
                return "🟡 Can Improve"
            else:
                return "🔴 Critical"

        st.subheader("Subsystem Status")

        st.write(" Propulsion:",system_status(dsa))
        st.write(" Payload:",system_status(project_score))
        st.write(" Navigation:",system_status(core_cs))
        st.write(" Docking:",system_status(internship_score))
        st.write(" Hackathon Sensor:",system_status(hackathon_score))

        # ---------- STRENGTH ----------
        skills = {
        "DSA": dsa,
        "Projects": project_score,
        "Core CS": core_cs,
        "Internship": internship_score,
        "Hackathon": hackathon_score
        }

        best_skill = max(skills, key=skills.get)
        weak_skill = min(skills, key=skills.get)

        st.subheader("Insights")

        st.write(" Top Strength:", best_skill)
        st.write("⚠ Area to Improve:", weak_skill)

# =====================================================
# TAB 3 — ANALYTICS
# =====================================================

    with tab3:

        st.header("Skill Analytics")

        categories = ['DSA','Projects','Core CS','Internship','Hackathons','Communication']
        values = [dsa,project_score,core_cs,internship_score,hackathon_score,communication]

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
        ))

        radar.update_layout(
        polar=dict(radialaxis=dict(visible=True,range=[0,100])),
        showlegend=False
        )

        st.plotly_chart(radar)

        data = {"Skill":categories,"Score":values}
        pie = px.pie(data,names="Skill",values="Score")
        st.plotly_chart(pie)

        health_df = pd.DataFrame({"Subsystem":categories,"Health":values})

        heat = px.imshow([health_df["Health"]],
        labels=dict(x="Subsystem",color="Health"),
        x=health_df["Subsystem"],
        color_continuous_scale="Viridis")

        st.plotly_chart(heat)

        st.subheader("Verification Status")

        st.write("Hackathon Certificate:", "Uploaded " if hackathon_cert else "Not Uploaded ❌")
        st.write("Internship Proof:", "Uploaded " if internship_doc else "Not Uploaded ❌")
        st.write("GitHub Repository:", "Provided " if github_link else "Not Provided ❌")

