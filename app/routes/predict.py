from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
from app.utils.preprocessing import preprocess_data

predict_bp = Blueprint('predict', __name__)

model = joblib.load("app/models/SVMModel.pkl")

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        transaction_df = pd.DataFrame([data])
        processed_data = preprocess_data(transaction_df)
        prediction = model.predict(processed_data)
        result = "Fraudulent" if prediction[0] == 1 else "Not Fraudulent"
        return jsonify({"prediction": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500