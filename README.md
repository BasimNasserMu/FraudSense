# Fraud Detection API

This project is a Flask-based API for detecting fraudulent transactions using a pre-trained SVM model. The API accepts transaction data as input and returns whether the transaction is fraudulent or not.

## Project Structure

```
fraud-detection-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   └── SVMModel.pkl
│   ├── routes
│   │   └── predict.py
│   └── utils
│       └── preprocessing.py
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fraud-detection-api
   ```

2. **Create a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app/main.py
   ```

## Usage

To make a prediction, send a POST request to the `/predict` endpoint with the transaction data in JSON format. For example:

```
POST /predict
Content-Type: application/json

{
    "feature1": value1,
    "feature2": value2,
    ...
}
```

The API will respond with a JSON object indicating whether the transaction is fraudulent.

## Docker

To build and run the application using Docker, use the following commands:

1. **Build the Docker image:**
   ```
   docker build -t fraud-detection-api .
   ```

2. **Run the Docker container:**
   ```
   docker run -p 5000:5000 fraud-detection-api
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.