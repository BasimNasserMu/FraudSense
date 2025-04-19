import os
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), "models/SVMModel.pkl")
svmModel = joblib.load(model_path)
Scaler_path = os.path.join(os.path.dirname(__file__), "models/scaler.pkl")
Scaler = joblib.load(Scaler_path)
# Initialize the scaler
scaler = StandardScaler()

@app.route('/csv', methods=['POST'])
def predict():
    try:
        # Check if a file is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(file)

        # Scale the Amount column
        df['Amount'] = Scaler.transform(df[['Amount']])

        # Define feature columns
        features = [f'V{i}' for i in range(1, 29)] + ['Amount']

        # Predict classes
        predictions = svmModel.predict(df[features])

        # Add predictions to the DataFrame
        df['Predicted_Class'] = ['Fraud' if p == 1 else 'Not Fraud' for p in predictions]

        # Convert the DataFrame to a JSON serializable format
        result = df[['Predicted_Class']].to_dict(orient='records')

        # Return the JSON response
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict_single', methods=['POST'])
def predict_single():
    try:
        # Parse the JSON request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract features from the JSON
        features = [data.get(f'V{i}', 0) for i in range(1, 29)]  # Default to 0 if a feature is missing
        amount = data.get('Amount', 0)  # Default to 0 if Amount is missing

        # Scale the Amount feature
        amount_scaled = Scaler.transform([[amount]])[0][0]

        # Combine features and scaled Amount
        features.append(amount_scaled)

        # Predict the fraud score
        prediction = svmModel.predict([features])[0]

        # Return the fraud score
        result = {"Fraud_Score": "Fraud" if prediction == 1 else "Not Fraud"}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
