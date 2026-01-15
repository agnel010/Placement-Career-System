import streamlit as st
from auth import login, register_user
from user_dashboard import user_dashboard
from admin_dashboard import admin_dashboard

st.set_page_config(page_title="Placement System", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login()
    with tab2:
        register_user()
else:
    if st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "admin":
        admin_dashboard()
