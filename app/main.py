import os
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), "models/SVMModel.pkl")
model = joblib.load(model_path)

# Initialize the scaler
scaler = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.get_json()

        # Convert input data to a DataFrame
        transaction = pd.DataFrame([data])

        # Preprocess the input
        transaction_scaled = scaler.fit_transform(transaction)

        # Make prediction
        prediction = model.predict(transaction_scaled)

        # Return the result
        result = {
            "transaction": data,
            "is_fraud": bool(prediction[0])
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)