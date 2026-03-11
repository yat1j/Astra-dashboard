import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="ASTRA Mission Control", layout="wide")

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

st.markdown("<h1 style='text-align:center'>🚀 ASTRA Mission Control</h1>", unsafe_allow_html=True)

st.write("Adaptive Skill Telemetry & Readiness Analyzer")

st.divider()

st.header(" Student Telemetry Input")

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

calculate = st.button("🚀 Calculate Mission Readiness")


if calculate:

    dsa_raw = easy*1 + medium*3 + hard*5
    dsa = min((dsa_raw/900)*100,100)

    project_score = {
        "Basic Project":30,
        "CRUD Application":50,
        "Full Stack":70,
        "AI/ML Project":85,
        "Deployed Product":100
    }[project]

    internship_score = {
        "None":20,
        "Local Company":55,
        "Startup":70,
        "Mid-size Tech":85,
        "Large Tech":100
    }[internship]

    level_base = {
    "College":40,
    "State":67,
    "National":87,
    "International":95
    }[hackathon_level]

    placement_bonus = {
    "Participation":0,
    "Top 10":4,
    "Finalist":6,
    "Winner":8
    }[hackathon_position]

    hackathon_score = min(level_base + placement_bonus,100)
    core_cs = (cgpa/10)*100

    bonus = 2

    dsa = min(dsa + bonus,100)
    project_score = min(project_score + bonus,100)
    internship_score = min(internship_score + bonus,100)
    hackathon_score = min(hackathon_score + bonus,100)
    core_cs = min(core_cs + bonus,100)


    if mode == "Product Company":
        w_dsa,w_proj,w_cs,w_int,w_hack = 0.40,0.20,0.20,0.10,0.10

    elif mode == "Startup":
        w_dsa,w_proj,w_cs,w_int,w_hack = 0.25,0.35,0.10,0.10,0.20

    else:
        w_dsa,w_proj,w_cs,w_int,w_hack = 0.25,0.15,0.30,0.20,0.10

    readiness = (
        w_dsa*dsa +
        w_proj*project_score +
        w_cs*core_cs +
        w_int*internship_score +
        w_hack*hackathon_score
    )

    st.divider()
    st.header(" Mission Summary")

    skills = {
    "DSA": dsa,
    "Projects": project_score,
    "Core CS": core_cs,
    "Internship": internship_score,
    "Hackathon": hackathon_score
    }

    best_skill = max(skills, key=skills.get)
    weak_skill = min(skills, key=skills.get)

    col1,col2,col3 = st.columns(3)

    col1.metric("Placement Readiness",round(readiness,1))
    col2.metric("Top Strength",best_skill)
    col3.metric("Area to Improve",weak_skill)

    st.header("🛰 Mission Control")

    if readiness >= 75:
        st.success(" Mission Ready")
    elif readiness >= 60:
        st.warning(" Mission Improving")
    else:
        st.error(" Mission Risk")

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

    st.subheader("Subsystem Telemetry")

    st.write(" DSA Engine")
    st.progress(dsa/100)

    st.write(" Project Payload")
    st.progress(project_score/100)

    st.write(" Core Navigation")
    st.progress(core_cs/100)

    st.write(" Internship Dock")
    st.progress(internship_score/100)

    st.write(" Hackathon Sensor")
    st.progress(hackathon_score/100)


    def subsystem_status(score):
        if score >= 75:
            return "🟢 Healthy"
        elif score >= 60:
            return "🟡 Warning"
        else:
            return "🔴 Critical"

    st.subheader("Subsystem Health Status")

    st.write(" DSA Engine:", subsystem_status(dsa))
    st.write(" Project Payload:", subsystem_status(project_score))
    st.write(" Core Navigation:", subsystem_status(core_cs))
    st.write(" Internship Dock:", subsystem_status(internship_score))
    st.write(" Hackathon Sensor:", subsystem_status(hackathon_score))

    st.header("Skill Analytics")

    categories = ['DSA','Projects','Core CS','Internship','Hackathons']
    values = [dsa,project_score,core_cs,internship_score,hackathon_score]

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
    st.header("Verification Status")

    st.write("Hackathon Certificate:", "Uploaded " if hackathon_cert else "Not Uploaded ❌")
    st.write("Internship Proof:", "Uploaded " if internship_doc else "Not Uploaded ❌")
    st.write("GitHub Repository:", "Provided " if github_link else "Not Provided ❌")


