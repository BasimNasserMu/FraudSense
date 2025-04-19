from flask import Flask, request, jsonify
import joblib
import numpy as np
from app.utils.preprocessing import preprocess_input

app = Flask(__name__)

model = joblib.load("app/models/SVMModel.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    transaction = preprocess_input(data)
    
    prediction = model.predict(np.array(transaction).reshape(1, -1))
    
    result = {
        'is_fraudulent': bool(prediction[0])
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)