import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
from database import insert_prediction, get_user_predictions
from career_recomm import recommend_career

# ── Model loading ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading ML models...")
def load_models():
    try:
        placement = pickle.load(open("models/placement_status_model.pkl", "rb"))
        tier_model = pickle.load(open("models/company_tier_model.pkl", "rb"))
        tier_encoder = pickle.load(open("models/company_tier_encoder.pkl", "rb"))
        return placement, tier_model, tier_encoder
    except Exception as e:
        st.error(f"Failed to load models: {str(e)}")
        st.stop()

placement_model, tier_model, tier_encoder = load_models()

binary_map = {"Yes": 1, "No": 0}

# Example companies per tier (customize as needed)
COMPANY_EXAMPLES = {
    "Tier 1": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Goldman Sachs"],
    "Tier 2": ["Infosys", "TCS", "Accenture", "Cognizant", "Wipro", "Deloitte"],
    "Tier 3": ["HCL", "Tech Mahindra", "Mindtree", "Mphasis", "Hexaware"],
    "Tier 4": ["Mid-size IT firms", "Startups", "Local companies"]
}

def user_dashboard():
    st.title("🎓 Placement & Career Guidance")

    tab_predict, tab_career, tab_history = st.tabs([
        "📊 Placement Prediction",
        "🧭 Career Recommendations",
        "📜 My Prediction History"
    ])

    # ── Placement Prediction Tab ─────────────────────────────────────────────
    with tab_predict:
        st.subheader("Predict Your Placement Chance")

        with st.form("placement_form"):
            col1, col2 = st.columns(2)

            with col1:
                cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5, step=0.1)
                internships = st.number_input("Internships", 0, 10, 1)
                projects = st.number_input("Projects", 0, 15, 2)
                workshops = st.number_input("Workshops / Certifications", 0, 20, 0)

            with col2:
                aptitude = st.number_input("Aptitude Score", 0, 100, 70)
                soft_skills = st.slider("Soft Skills Rating", 1.0, 5.0, 3.5, step=0.1)
                extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"], index=1)
                training = st.selectbox("Placement Training Attended", ["Yes", "No"], index=0)

            col3, col4 = st.columns(2)
            with col3:
                ssc = st.number_input("SSC Marks (%)", 0.0, 100.0, 85.0, step=0.5)
            with col4:
                hsc = st.number_input("HSC Marks (%)", 0.0, 100.0, 82.0, step=0.5)

            predict_btn = st.form_submit_button("Get Prediction", type="primary", use_container_width=True)

        if predict_btn:
            with st.spinner("Analyzing your profile..."):
                input_data = {
                    "CGPA": cgpa,
                    "Internships": internships,
                    "Projects": projects,
                    "Workshops/Certifications": workshops,
                    "AptitudeTestScore": aptitude,
                    "SoftSkillsRating": soft_skills,
                    "ExtracurricularActivities": binary_map[extracurricular],
                    "PlacementTraining": binary_map[training],
                    "SSC_Marks": ssc,
                    "HSC_Marks": hsc
                }

                df = pd.DataFrame([input_data])
                expected_order = [
                    "CGPA", "Internships", "Projects", "Workshops/Certifications",
                    "AptitudeTestScore", "SoftSkillsRating", "ExtracurricularActivities",
                    "PlacementTraining", "SSC_Marks", "HSC_Marks"
                ]
                df = df[expected_order]

                # Prediction
                prob = placement_model.predict_proba(df)[0][1] if hasattr(placement_model, "predict_proba") else None
                placed = int(placement_model.predict(df)[0])

                if placed == 1:
                    prob_display = f"{prob:.1%}" if prob is not None else "strong"
                    st.success(f"🎉 High placement probability ({prob_display})")

                    tier_code = tier_model.predict(df)[0]
                    tier = tier_encoder.inverse_transform([tier_code])[0]
                    st.markdown(f"**Expected Company Tier**: **{tier}** 🏢")

                    # Show example companies
                    if tier in COMPANY_EXAMPLES:
                        st.markdown(f"**Example companies in {tier}** (typical recruiters):")
                        st.write(", ".join(COMPANY_EXAMPLES[tier]))
                    else:
                        st.caption("No example companies defined for this tier yet.")
                else:
                    st.warning("⚠️ Lower placement probability at this stage")

                # Save
                success = insert_prediction(
                    st.session_state.user_id,
                    cgpa, internships, projects, workshops, aptitude,
                    soft_skills, binary_map[extracurricular], binary_map[training],
                    ssc, hsc, placed
                )
                if success:
                    st.caption(f"Prediction saved • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                else:
                    st.error("Failed to save prediction")

    # ── Career Recommendation Tab ────────────────────────────────────────────
    with tab_career:
        st.subheader("Career Path Recommendations")

        course = st.selectbox("Your current / completed course", 
                             ["BTech", "BCA", "MCA", "MBA", "BSc", "BCom", "Other"])

        interest = st.selectbox("Primary area of interest", 
                               ["Technology", "Data & Analytics", "Management", 
                                "Finance", "Marketing", "Design", "Research"])

        skills = st.text_area("Your skills (comma separated)", 
                             placeholder="Python, SQL, React, Communication, Figma, Power BI",
                             height=100)

        if st.button("Get Career Recommendations", type="primary"):
            if not skills.strip():
                st.warning("Please enter at least a few skills for better recommendations.")
            else:
                with st.spinner("Finding best-fit careers..."):
                    recs = recommend_career(course, skills, interest)
                    st.success("Here are your top career recommendations:")
                    for rec in recs:
                        st.markdown(
                            f"**{rec['title']}** (Confidence: **{rec['confidence']}%**)\n*Why?* {rec['reasons']}",
                            unsafe_allow_html=False
                        )
                        st.markdown("---")

    # ── Prediction History Tab ───────────────────────────────────────────────
    with tab_history:
        st.subheader("Your Previous Predictions")

        history = get_user_predictions(st.session_state.user_id)

        if not history:
            st.info("You haven't made any predictions yet.")
        else:
            df_hist = pd.DataFrame(history)

            df_hist = df_hist.rename(columns={
                "cgpa": "CGPA",
                "internships": "Internships",
                "projects": "Projects",
                "aptitude_score": "Aptitude Score",
                "soft_skills": "Soft Skills",
                "placement_status": "Placed",
                "predicted_at": "Date"
            })

            desired = ["CGPA", "Internships", "Projects", "Aptitude Score", "Soft Skills", "Placed", "Date"]
            available = [col for col in desired if col in df_hist.columns]

            if "Placed" in df_hist.columns:
                df_hist["Placed"] = df_hist["Placed"].map({1: "Yes ✅", 0: "No"})

            st.dataframe(
                df_hist[available].sort_values("Date", ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.DatetimeColumn("Date", format="D MMM YYYY • h:mm a"),
                    "CGPA": st.column_config.NumberColumn("CGPA", format="%.2f"),
                    "Soft Skills": st.column_config.NumberColumn("Soft Skills", format="%.1f"),
                }
            )