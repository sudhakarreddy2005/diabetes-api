import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Diabetes Predictor", page_icon="🩸", layout="centered")
st.title("🩸 Diabetes Prediction App")
st.write("This app predicts the likelihood of diabetes using your health parameters.")

# --- User Inputs ---
Pregnancies = st.number_input("Number of Pregnancies", 0, 20, 2)
Glucose = st.number_input("Glucose Level", 0, 300, 120)
BloodPressure = st.number_input("Blood Pressure (mm Hg)", 0, 150, 70)
SkinThickness = st.number_input("Skin Thickness (mm)", 0, 100, 20)
Insulin = st.number_input("Insulin Level", 0, 900, 80)
BMI = st.number_input("BMI", 0.0, 60.0, 25.0, step=0.1)
DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.47, step=0.01)
Age = st.number_input("Age", 1, 100, 30)

# API endpoint (Flask running locally)
# API_URL = "http://127.0.0.1:5000/"
 API_URL = "https://diabetes-api-app-rf.onrender.com/predict"

if st.button("🔍 Predict Diabetes Risk"):
    # Prepare JSON payload
    input_data = {
        "Pregnancies": Pregnancies,
        "Glucose": Glucose,
        "BloodPressure": BloodPressure,
        "SkinThickness": SkinThickness,
        "Insulin": Insulin,
        "BMI": BMI,
        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
        "Age": Age
    }

    # Send request to Flask API
    with st.spinner("Analyzing..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()

            if "error" in result:
                st.error("❌ Error: " + result["error"])
            else:
                st.subheader("📊 Prediction Result")
                st.write(f"**Status:** {result['status']}")
                st.write(f"**Probability:** {result['probability']}%")

                if result["prediction"] == 1:
                    st.error("⚠️ High Diabetes Risk! Consult a doctor.")
                else:
                    st.success("💚 Low Risk! Maintain a healthy lifestyle.")
        except Exception as e:
            st.error(f"Connection error: {e}")
