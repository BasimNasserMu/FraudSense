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

@app.route('/predict', methods=['POST'])
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

        return jsonify(df[['Predicted_Class']]), 200
 
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)