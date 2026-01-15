import streamlit as st


# ---------- CORE RECOMMENDATION ENGINE ----------
def recommend_career(course, skills, interest):
    skills = [s.strip().lower() for s in skills.split(",") if s.strip()]
    recommendations = set()

    # ---------- TECHNOLOGY ----------
    if course in ["BCA", "MCA", "BTech"]:
        if any(skill in skills for skill in ["python", "java", "c++", "dsa"]):
            recommendations.add("Software Engineer")
        if any(skill in skills for skill in ["html", "css", "javascript", "react"]):
            recommendations.add("Web Developer")
        if "android" in skills or "flutter" in skills:
            recommendations.add("Mobile App Developer")

    # ---------- DATA & ANALYTICS ----------
    if any(skill in skills for skill in ["python", "sql", "excel", "power bi", "tableau"]):
        recommendations.add("Data Analyst")
    if any(skill in skills for skill in ["machine learning", "ai", "deep learning"]):
        recommendations.add("Machine Learning Engineer")
    if "statistics" in skills:
        recommendations.add("Data Scientist")

    # ---------- MANAGEMENT & BUSINESS ----------
    if course == "MBA" or interest == "Management":
        if any(skill in skills for skill in ["communication", "leadership", "management"]):
            recommendations.add("Business Analyst")
            recommendations.add("Management Trainee")
        if "operations" in skills:
            recommendations.add("Operations Manager")

    # ---------- FINANCE ----------
    if interest == "Finance":
        if any(skill in skills for skill in ["accounting", "finance", "excel"]):
            recommendations.add("Financial Analyst")
        if "investment" in skills:
            recommendations.add("Investment Analyst")

    # ---------- MARKETING ----------
    if interest == "Marketing":
        if any(skill in skills for skill in ["seo", "content", "social media", "canva"]):
            recommendations.add("Digital Marketer")
        if "branding" in skills:
            recommendations.add("Brand Strategist")

    # ---------- DESIGN ----------
    if interest == "Design":
        if any(skill in skills for skill in ["ui", "ux", "figma", "photoshop"]):
            recommendations.add("UI/UX Designer")
        if "canva" in skills:
            recommendations.add("Graphic Designer")

    # ---------- RESEARCH & EDUCATION ----------
    if interest == "Research":
        if any(skill in skills for skill in ["research", "analysis", "statistics"]):
            recommendations.add("Research Analyst")
            recommendations.add("Academic Researcher")

    # ---------- FALLBACK ----------
    if not recommendations:
        recommendations.add("Skill Enhancement Recommended")

    return sorted(recommendations)


# ---------- STREAMLIT DASHBOARD ----------
def career_dashboard():
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

    if st.button("🎯 Recommend Career"):
        careers = recommend_career(course, skills, interest)

        st.success("Recommended Career Paths:")
        for career in careers:
            st.write(f"• {career}")

        st.caption(
            "Recommendations are based on course, skills, and interest domain."
        )
