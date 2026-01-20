import streamlit as st
import bcrypt
from database import get_connection, init_db

init_db()

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login():
    with st.form("login_form", clear_on_submit=True):
        st.markdown("### 🔐 Login")

        role_choice = st.selectbox("Login as", ["Student", "Admin"])
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

        if submitted:
            if not username.strip():
                st.error("Please enter username")
                return

            if role_choice == "Admin":
                if username == "admin" and password == "admin2026":
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.username = "admin"
                    st.session_state.user_id = 0
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")
            else:
                try:
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT id, username, password FROM users WHERE username = ? AND role = 'user'",
                            (username,)
                        )
                        user = cursor.fetchone()

                    if user and verify_password(password, user["password"]):
                        st.session_state.logged_in = True
                        st.session_state.role = "user"
                        st.session_state.username = user["username"]
                        st.session_state.user_id = user["id"]
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")

    st.markdown(
        "<small style='color: #aaaaaa;'>Forgot password? Contact your administrator.</small>",
        unsafe_allow_html=True
    )

def register_user():
    with st.form("register_form", clear_on_submit=True):
        st.markdown("### 📝 Create Account")

        username = st.text_input("Username", max_chars=30, placeholder="Choose a username")

        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="At least 8 characters")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submitted:
            if not username.strip() or len(username) < 4:
                st.error("Username must be at least 4 characters")
                return
            if len(password) < 8:
                st.error("Password must be at least 8 characters")
                return
            if password != confirm_password:
                st.error("Passwords do not match")
                return

            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    hashed_pw = hash_password(password)
                    cursor.execute(
                        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        (username, hashed_pw, "user")
                    )
                    conn.commit()

                st.success("Account created! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists")
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")