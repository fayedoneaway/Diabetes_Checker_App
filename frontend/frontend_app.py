import streamlit as st
import requests

st.set_page_config(page_title="Diabetes Checker", page_icon="🔵")

for key in ["bmi", "age", "glucose", "symptoms"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "show_result" not in st.session_state:
    st.session_state.show_result = False

st.title("🔵 Diabetes Checker App")
st.write("Please enter all information required.")

def clear_bmi():
    if st.session_state["bmi"] == 0.0:
        st.session_state["bmi"] = None

def clear_age():
    if st.session_state["age"] == 0:
        st.session_state["age"] = None

def clear_glucose():
    if st.session_state["glucose"] == 0.0:
        st.session_state["glucose"] = None

bmi = st.number_input("BMI (click box to edit)", min_value=0.0, step=0.1, key="bmi")
age = st.number_input("Age (click box to edit)", min_value=0, step=1, key="age")

glucose = st.number_input("Glucose Level (click box to edit)", min_value=0.0, step=1.0, key="glucose")

st.info("""Enter all symptoms that apply to you. Separated by commas:
    Frequent urination,
     Sudden loss of weight,
     Increased thirst or hunger,
     Nausea and Vomiting,
     Blurry Vision,
     Urinary Tract Infection""")
symptom_answers = st.text_input(
    "Keywords acceptable:",
    placeholder= "weight loss, increased thirst, nausea vomiting, blurry vision, UTI",
    key="symptoms")

if st.button("Click Here to Check:"):
    st.session_state.show_result = True

if st.session_state.show_result:
    answer = symptom_answers or " "    

     if None in [st.session_state["bmi"], st.session_state["age"], st.session_state["glucose"]]:
        st.error("Please fill out all fields before submitting.")
        st.stop()

    symptoms = [s.strip() for s in answer.split(",") if s.strip()]

    payload= {
        "bmi": st.session_state["bmi"],
        "age": st.session_state["age"],
        "glucose": st.session_state["glucose"],
        "symptoms": symptoms}
    st.write("Payload:", payload)

    try:
        response = requests.post(
            "https://diabetes-checker-app-25ps.onrender.com/predict/diabetes",
            json= payload)
        result = response.json()

        st.subheader("Result")
        st.json(result)

    except Exception as e:
        st.error(f"Error connecting to server: {e}")

if st.button("Do Another Check"):
    st.session_state.clear()
    st.rerun()


st.write("Status:", response.status_code)
st.write("Response:", response.text[:200])
