import streamlit as st
import pandas as pd
import pickle
from database import insert_prediction

# ---------------- Load Placement Model ----------------
with open("models/placement_model.pkl", "rb") as file:
    placement_model = pickle.load(file)

# ---------------- Encoding Maps ----------------
gender_map = {"Male": 1, "Female": 0}
board_map = {"Central": 0, "Others": 1}
hsc_stream_map = {"Science": 2, "Commerce": 1, "Arts": 0}
degree_type_map = {"Sci&Tech": 2, "Comm&Mgmt": 1, "Others": 0}
workex_map = {"Yes": 1, "No": 0}

# Abstracted domain mapping (keeps MBA model compatible)
domain_map = {
    "Technology": 1,
    "Management": 0,
    "Data & Analytics": 1,
    "Finance": 0,
    "Marketing": 0,
    "Design": 1,
    "Research": 1,
    "General": 0
}

# ---------------- Career Recommendation Engine ----------------
def recommend_career(course, skills, interest):
    skills = [s.strip().lower() for s in skills.split(",") if s.strip()]
    recommendations = set()

    # -------- Technology --------
    if course in ["BCA", "MCA", "BTech"]:
        if any(skill in skills for skill in ["python", "java", "c++", "dsa"]):
            recommendations.add("Software Engineer")
        if any(skill in skills for skill in ["html", "css", "javascript", "react"]):
            recommendations.add("Web Developer")
        if any(skill in skills for skill in ["android", "flutter"]):
            recommendations.add("Mobile App Developer")

    # -------- Data & Analytics --------
    if any(skill in skills for skill in ["python", "sql", "excel", "tableau", "power bi"]):
        recommendations.add("Data Analyst")
    if any(skill in skills for skill in ["machine learning", "ai"]):
        recommendations.add("Machine Learning Engineer")
    if "statistics" in skills:
        recommendations.add("Data Scientist")

    # -------- Management / MBA --------
    if course == "MBA" or interest == "Management":
        if any(skill in skills for skill in ["communication", "leadership", "management"]):
            recommendations.add("Business Analyst")
            recommendations.add("Management Trainee")

    # -------- Finance --------
    if interest == "Finance":
        if any(skill in skills for skill in ["finance", "accounting", "excel"]):
            recommendations.add("Financial Analyst")

    # -------- Marketing --------
    if interest == "Marketing":
        if any(skill in skills for skill in ["seo", "content", "social media", "canva"]):
            recommendations.add("Digital Marketer")

    # -------- Design --------
    if interest == "Design":
        if any(skill in skills for skill in ["ui", "ux", "figma", "photoshop", "canva"]):
            recommendations.add("UI/UX Designer")

    # -------- Research --------
    if interest == "Research":
        if any(skill in skills for skill in ["research", "analysis", "statistics"]):
            recommendations.add("Research Analyst")

    # -------- Fallback --------
    if not recommendations:
        recommendations.add("Skill Enhancement Recommended")

    return sorted(recommendations)


# ================= USER DASHBOARD =================
def user_dashboard():

    # ---------- Sidebar ----------
    with st.sidebar:
        st.markdown("### 👤 User Panel")
        st.write(f"Logged in as **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # ---------- Main Title ----------
    st.title("🎓 Placement & Career Recommendation System")
    st.caption("Placement prediction and career guidance for all students")

    tab1, tab2 = st.tabs(["📊 Placement Prediction", "🧭 Career Recommendation"])

    # ================= TAB 1: PLACEMENT =================
    with tab1:
        st.subheader("📘 Academic Details")

        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            ssc_p = st.number_input("SSC Percentage", 0.0, 100.0)
            ssc_b = st.selectbox("SSC Board", ["Central", "Others"])

        with col2:
            hsc_p = st.number_input("HSC Percentage", 0.0, 100.0)
            hsc_b = st.selectbox("HSC Board", ["Central", "Others"])
            hsc_s = st.selectbox("HSC Stream", ["Science", "Commerce", "Arts"])

        st.subheader("🎓 Higher Education")

        col3, col4 = st.columns(2)
        with col3:
            degree_p = st.number_input("Degree / Final Year Percentage", 0.0, 100.0)
            degree_t = st.selectbox("Degree Type", ["Sci&Tech", "Comm&Mgmt", "Others"])

        with col4:
            domain = st.selectbox(
                "Primary Domain Interest",
                ["Technology", "Data & Analytics", "Management", "Finance", "Marketing", "Design", "Research", "General"]
            )

        st.subheader("💼 Professional Profile")

        col5, col6 = st.columns(2)
        with col5:
            workex = st.selectbox("Work Experience", ["Yes", "No"])
        with col6:
            etest_p = st.number_input("Aptitude Test Percentage", 0.0, 100.0)

        st.divider()

        if st.button("🔮 Predict Placement", use_container_width=True):
            input_data = pd.DataFrame([[
                gender_map[gender],
                ssc_p,
                board_map[ssc_b],
                hsc_p,
                board_map[hsc_b],
                hsc_stream_map[hsc_s],
                degree_p,
                degree_type_map[degree_t],
                workex_map[workex],
                etest_p,
                domain_map[domain],
                degree_p
            ]], columns=[
                'gender', 'ssc_p', 'ssc_b', 'hsc_p', 'hsc_b', 'hsc_s',
                'degree_p', 'degree_t', 'workex', 'etest_p',
                'specialisation', 'mba_p'
            ])

            prediction = placement_model.predict(input_data)[0]

            insert_prediction(
                st.session_state.username,
                gender_map[gender],
                ssc_p,
                hsc_p,
                degree_p,
                etest_p,
                degree_p,
                prediction
            )

            if prediction == "Placed":
                st.success("🎉 High chance of getting placed!")
            else:
                st.warning("⚠️ Placement chances are low. Skill improvement recommended.")

    # ================= TAB 2: CAREER =================
    with tab2:
        st.subheader("🧭 Career Recommendation")

        course = st.selectbox(
            "Current Course",
            ["BCA", "MCA", "BTech", "MBA", "BSc", "BCom", "BA", "Other"]
        )

        interest = st.selectbox(
            "Primary Career Interest",
            ["Technology", "Data & Analytics", "Management", "Finance", "Marketing", "Design", "Research", "General"]
        )

        skills = st.text_area(
            "Enter your skills (comma separated)",
            placeholder="Python, SQL, Communication, Excel"
        )

        if st.button("Recommend Career"):
            careers = recommend_career(course, skills, interest)

            st.success("Recommended Career Paths:")
            for career in careers:
                st.write(f"• {career}")

    st.markdown("---")
    st.caption("© Placement & Career Recommendation System | Python • ML • Streamlit")
