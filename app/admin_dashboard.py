import streamlit as st
import pandas as pd
from database import get_all_predictions


def admin_dashboard():
    # ---------- Sidebar ----------
    with st.sidebar:
        st.markdown("### 🛠 Admin Panel")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("📊 Admin Dashboard")
    st.caption("View and monitor all user predictions")

    data = get_all_predictions()

    if data:
        df = pd.DataFrame(
            data,
            columns=[
                "ID", "Username", "Gender", "SSC %",
                "HSC %", "Degree %", "Aptitude %",
                "MBA %", "Prediction", "Timestamp"
            ]
        )

        # ---------- Metrics ----------
        col1, col2 = st.columns(2)
        col1.metric("Total Predictions", len(df))
        col2.metric(
            "Placed Count",
            len(df[df["Prediction"] == "Placed"])
        )

        st.divider()
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            "placement_predictions.csv",
            "text/csv"
        )
    else:
        st.info("No prediction data available")

    st.markdown("---")
    st.caption("Admin Panel | Placement Prediction System")
