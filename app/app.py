import streamlit as st
import pandas as pd
import pickle

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Placement Prediction System",
    layout="centered"
)

# ---------------- Load Model ----------------
with open("models/placement_model.pkl", "rb") as file:
    placement_model = pickle.load(file)

# ---------------- Encoding Maps ----------------
gender_map = {"Male": 1, "Female": 0}
board_map = {"Central": 0, "Others": 1}
hsc_stream_map = {"Science": 2, "Commerce": 1, "Arts": 0}
degree_type_map = {"Sci&Tech": 2, "Comm&Mgmt": 1, "Others": 0}
workex_map = {"Yes": 1, "No": 0}
specialisation_map = {"Mkt&HR": 1, "Mkt&Fin": 0}

# ---------------- UI ----------------
st.title("Placement Prediction System")
st.write("Machine Learning based Placement Prediction")

st.divider()
st.subheader("Student Academic Details")

gender = st.selectbox("Gender", ["Male", "Female"])

ssc_p = st.number_input("SSC Percentage", 0.0, 100.0)
ssc_b = st.selectbox("SSC Board", ["Central", "Others"])

hsc_p = st.number_input("HSC Percentage", 0.0, 100.0)
hsc_b = st.selectbox("HSC Board", ["Central", "Others"])
hsc_s = st.selectbox("HSC Stream", ["Science", "Commerce", "Arts"])

degree_p = st.number_input("Degree Percentage", 0.0, 100.0)
degree_t = st.selectbox("Degree Type", ["Sci&Tech", "Comm&Mgmt", "Others"])

workex = st.selectbox("Work Experience", ["Yes", "No"])
etest_p = st.number_input("Aptitude Test Percentage", 0.0, 100.0)

specialisation = st.selectbox("MBA Specialisation", ["Mkt&HR", "Mkt&Fin"])
mba_p = st.number_input("MBA Percentage", 0.0, 100.0)

st.divider()

# ---------------- Prediction ----------------
if st.button("Predict Placement"):
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
        specialisation_map[specialisation],
        mba_p
    ]], columns=[
        'gender', 'ssc_p', 'ssc_b', 'hsc_p', 'hsc_b', 'hsc_s',
        'degree_p', 'degree_t', 'workex', 'etest_p',
        'specialisation', 'mba_p'
    ])

    prediction = placement_model.predict(input_data)[0]

    if prediction == "Placed":
        st.success("Prediction Result: Placed ✅")
    else:
        st.error("Prediction Result: Not Placed ❌")

st.divider()
st.caption(
    "This prediction is based on a Logistic Regression model trained on historical placement data."
)
