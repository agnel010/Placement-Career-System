import streamlit as st
import sqlite3

DB_NAME = "placement_system.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ================= USER REGISTRATION =================
def register_user():
    st.title("📝 User Registration")
    st.caption("Create a new account to access the placement prediction system")

    with st.form("register_form"):
        username = st.text_input(
            "Choose Username",
            key="register_username"
        )

        # Custom label to avoid overlap
        st.markdown("**Password**")
        password = st.text_input(
            "",
            type="password",
            key="register_password",
            label_visibility="collapsed"
        )

        submit = st.form_submit_button("Register")

    if submit:
        if username.strip() == "" or password.strip() == "":
            st.error("Username and password cannot be empty")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "user")
            )
            conn.commit()
            st.success("✅ Registration successful! Please login.")
        except sqlite3.IntegrityError:
            st.error("❌ Username already exists")
        finally:
            conn.close()


# ================= LOGIN =================
def login():
    st.title("🔐 Placement System Login")
    st.caption("Login to continue")

    with st.form("login_form"):
        role = st.selectbox(
            "Login as",
            ["User", "Admin"],
            key="login_role"
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        # Custom label to avoid overlap
        st.markdown("**Password**")
        password = st.text_input(
            "",
            type="password",
            key="login_password",
            label_visibility="collapsed"
        )

        submit = st.form_submit_button("Login")

    if submit:
        # ---------- Admin Login ----------
        if role == "Admin":
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("❌ Invalid admin credentials")

        # ---------- User Login ----------
        else:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=? AND role='user'",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
