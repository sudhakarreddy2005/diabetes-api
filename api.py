from flask import Flask, request, jsonify
import joblib
import pandas as pd

# --- Initialize Flask app ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Diabetes Prediction API is live!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model = joblib.load("model_rf.joblib")
        scaler = joblib.load("scaler.joblib")

        data = request.get_json(force=True)
        expected_cols = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        df = pd.DataFrame([data], columns=expected_cols)
        scaled = scaler.transform(df)
        prediction = model.predict(scaled)[0]
        probability = model.predict_proba(scaled)[0][1] * 100

        return jsonify({
            "prediction": int(prediction),
            "probability": round(float(probability), 2),
            "status": "Diabetic" if prediction == 1 else "Not Diabetic"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# if __name__ == "__main__":
#     app.run(debug=False)
if __name__ == '__main__':
    # ✅ Works fine both locally and on Render
    app.run(host='0.0.0.0', port=5000, debug=False)

