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
        # Check if a file is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(file)

        # Preprocess the input data
        df_scaled = scaler.fit_transform(df)

        # Make predictions
        predictions = model.predict(df_scaled)

        # Add predictions to the DataFrame
        df['is_fraud'] = predictions

        # Convert the DataFrame to a JSON response
        result = df.to_dict(orient='records')
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)