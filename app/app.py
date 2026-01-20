import streamlit as st
from auth import login, register_user
from user_dashboard import user_dashboard
from admin_dashboard import admin_dashboard

st.set_page_config(
    page_title="Placement & Career Recommendation System",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"  # hide on login page
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.user_id = None

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; margin-bottom: 1.5rem;'>🎓 Placement & Career Recommendation System</h2>",
        unsafe_allow_html=True
    )

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.container():
            st.markdown("<div style='padding: 1.5rem 1rem; background: #1e1e2e; border-radius: 12px;'>", unsafe_allow_html=True)
            login()
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_register:
        with st.container():
            st.markdown("<div style='padding: 1.5rem 1rem; background: #1e1e2e; border-radius: 12px;'>", unsafe_allow_html=True)
            register_user()
            st.markdown("</div>", unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown(f"**User**: {st.session_state.username}")
        st.markdown(f"**Role**: {st.session_state.role.capitalize()}")
        st.markdown("---")
        if st.button("Logout", type="primary", use_container_width=True):
            logout()

    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()