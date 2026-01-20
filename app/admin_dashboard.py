import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_predictions

def admin_dashboard():
    st.title("📊 Admin Dashboard – Placement Insights")
    st.caption("Overview of all student placement predictions")

    # Fetch all prediction records (with username joined)
    data = get_all_predictions()

    if not data:
        st.info("No predictions have been made yet.")
        return

    df = pd.DataFrame(data)

    # Rename columns for clean display
    df = df.rename(columns={
        "id": "Prediction ID",
        "username": "Student",
        "cgpa": "CGPA",
        "internships": "Internships",
        "projects": "Projects",
        "workshops": "Workshops / Certs",
        "aptitude_score": "Aptitude Score",
        "soft_skills": "Soft Skills",
        "extracurricular": "Extracurricular",
        "placement_training": "Placement Training",
        "ssc_marks": "SSC (%)",
        "hsc_marks": "HSC (%)",
        "placement_status": "Placed",
        "predicted_at": "Predicted At"
    })

    # Convert boolean-like fields for better readability
    df["Placed"] = df["Placed"].map({1: "Yes", 0: "No"})
    df["Extracurricular"] = df["Extracurricular"].map({1: "Yes", 0: "No"})
    df["Placement Training"] = df["Placement Training"].map({1: "Yes", 0: "No"})

    # ── Key Metrics ───────────────────────────────────────────────────────────
    cols = st.columns([1, 1, 1, 1])

    total = len(df)
    placed_count = (df["Placed"] == "Yes").sum()
    placement_rate = placed_count / total if total > 0 else 0
    unique_students = df["Student"].nunique()

    cols[0].metric("Total Predictions", f"{total:,}")
    cols[1].metric("Students Placed", f"{placed_count:,}", delta_color="normal")
    cols[2].metric("Placement Rate", f"{placement_rate:.1%}")
    cols[3].metric("Unique Students", unique_students)

    # ── Visualizations ────────────────────────────────────────────────────────
    st.subheader("Placement Overview")

    tab_overview, tab_by_cgpa = st.tabs(["Summary", "CGPA & Aptitude"])

    with tab_overview:
        fig_pie = px.pie(
            df, 
            names="Placed", 
            title="Placed vs Not Placed",
            color="Placed",
            color_discrete_map={"Yes": "#22c55e", "No": "#ef4444"}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab_by_cgpa:
        fig_scatter = px.scatter(
            df,
            x="CGPA",
            y="Aptitude Score",
            color="Placed",
            size="Internships",
            hover_data=["Student", "Projects", "Soft Skills", "Predicted At"],
            color_discrete_map={"Yes": "#22c55e", "No": "#ef4444"},
            title="CGPA vs Aptitude Score by Placement Outcome",
            opacity=0.7
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ── Data Table ────────────────────────────────────────────────────────────
    st.subheader("All Prediction Records")

    st.dataframe(
        df.style
          .format({
              "CGPA": "{:.2f}",
              "Soft Skills": "{:.1f}",
              "SSC (%)": "{:.1f}",
              "HSC (%)": "{:.1f}",
              "Predicted At": lambda x: pd.to_datetime(x).strftime("%Y-%m-%d %H:%M")
          })
          .highlight_max(subset="CGPA", color="#d1fae5")
          .highlight_min(subset="CGPA", color="#fee2e2"),
        use_container_width=True,
        hide_index=True
    )

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download all predictions (CSV)",
        data=csv,
        file_name="placement_predictions_export.csv",
        mime="text/csv",
        use_container_width=True
    )