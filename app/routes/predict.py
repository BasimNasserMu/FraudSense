from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

predict_bp = Blueprint('predict', __name__)

# Load the model
model = joblib.load("app/models/SVMModel.pkl")

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Convert input data to DataFrame
        transaction_df = pd.DataFrame([data])

        # Drop unnecessary columns (align with Test.py)
        transaction_df = transaction_df.drop(columns=['Time', 'Class'], errors='ignore')

        # Apply scaling (align with Test.py)
        scaler = StandardScaler()
        processed_data = scaler.fit_transform(transaction_df)

        # Make prediction
        prediction = model.predict(processed_data)
        result = "Fraudulent" if prediction[0] == 1 else "Not Fraudulent"

        return jsonify({"prediction": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
