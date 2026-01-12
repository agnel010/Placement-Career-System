import streamlit as st

st.set_page_config(
    page_title="Placement and Career System",
    layout="centered"
)

st.title("Placement Prediction and Career Recommendation System")
st.write("Prototype User Interface (Demo Version)")

st.divider()

st.subheader("Student Details")

name = st.text_input("Student Name")
course = st.selectbox("Course", ["BCA", "MCA", "BTech", "MBA", "Other"])
cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1)
internships = st.number_input("Number of Internships", 0, 10)
aptitude = st.slider("Aptitude Score", 0, 100)
skills = st.text_input("Skills (comma separated)")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Predict Placement"):
        st.success("Result: Placed (Demo Output)")
        st.write("Placement Probability: 78%")

with col2:
    if st.button("Recommend Career"):
        st.info("Recommended Career: Data Analyst (Demo Output)")

st.divider()

st.caption(
    "Note: This is a prototype user interface. "
    "Machine learning models will be integrated in the final version."
)
