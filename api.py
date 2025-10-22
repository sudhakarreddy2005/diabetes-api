from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("model_rf.joblib")
scaler = joblib.load("scaler.joblib")

@app.route('/', methods=['POST'])
def predict():
    try:
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

if __name__ == '__main__':
    app.run(debug=True)
