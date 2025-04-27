import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the pre-trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), "models/SVMModel.pkl")
svmModel = joblib.load(model_path)
Scaler_path = os.path.join(os.path.dirname(__file__), "models/scaler.pkl")
Scaler = joblib.load(Scaler_path)

# Log file path
log_file = os.path.join(os.path.dirname(__file__), "prediction_logs.csv")

def log_predictions(df_log):
    # Check if the log file exists
    if os.path.isfile(log_file):
        # Read existing log file
        existing_logs = pd.read_csv(log_file)
        
        # Remove rows that are already logged
        df_log = df_log[~df_log.isin(existing_logs.to_dict(orient='list')).all(axis=1)]
    
    # Only log if there are new rows
    if not df_log.empty:
        df_log.to_csv(log_file, mode='a', header=not os.path.isfile(log_file), index=False)
@app.route('/csv', methods=['POST'])
def predict():
    try:
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
        decision_score = svmModel.decision_function(df[features])

        # Add predictions to the DataFrame
        df['Predicted_Class'] = predictions
        df['Fraud_Score'] = decision_score
        # Log to file
        log_predictions(df[features + ['Predicted_Class'] + ['Fraud_Score'])

        # Convert the DataFrame to a JSON serializable format
        result = df[['Predicted_Class']].to_dict(orient='records')
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict_single', methods=['POST'])
def predict_single():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract features
        features = [data.get(f'v{i}', 0) for i in range(1, 29)]
        amount = data.get('Amount', 0)

        # Scale the Amount feature
        amount_scaled = Scaler.transform([[amount]])[0][0]
        features.append(amount_scaled)

        # Predict
        prediction = svmModel.predict([features])[0]
        result_label = "Fraud" if prediction == 1 else "Not Fraud"
        decision_score = svmModel.decision_function([features])[0]

        # 7. Apply sigmoid to approximate probability
        fraud_score = 1 / (1 + np.exp(-decision_score))  # Sigmoid function
        fraud_score = round(fraud_score * 100, 2)  # Convert to percentage
        
        # Log input + prediction
        log_data = {f'V{i}': data.get(f'v{i}', 0) for i in range(1, 29)}
        log_data['Amount'] = amount_scaled
        log_data['Predicted_Class'] = prediction
        log_data['Fraud_Score'] = fraud_score
        df_log = pd.DataFrame([log_data])
        log_predictions(df_log)

        return jsonify({"Predicted_Class": result_label, "Fraud_Score": fraud_score}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download_log', methods=['GET'])
def download_log():
    try:
        # Check if the log file exists
        if not os.path.isfile(log_file):
            return jsonify({"error": "Log file not found"}), 404
        
        # Serve the log file
        return send_file(log_file, as_attachment=True, download_name="log_file.csv")
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
