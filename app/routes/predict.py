from flask import Blueprint, request, jsonify
import joblib
import pandas as pd

predict_bp = Blueprint('predict', __name__)

# Load the model and scaler
model = joblib.load("app/models/SVMModel.pkl")
scaler = joblib.load("app/models/scaler.pkl")

@predict_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(file)

        # Scale the Amount column
        df['Amount'] = scaler.transform(df[['Amount']])

        # Define feature columns
        features = [f'V{i}' for i in range(1, 29)] + ['Amount']

        # Predict classes
        predictions = model.predict(df[features])

        # Add predictions to the DataFrame
        df['Predicted_Class'] = ['Fraud' if p == 1 else 'Not Fraud' for p in predictions]

        # Return predictions as JSON
        return jsonify(df[['Predicted_Class']].to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
