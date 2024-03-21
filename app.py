from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import torch
import torch.nn.functional as F
from flask_cors import CORS
from main import predict_star_characteristics
# Your existing imports and code for the model here

app = Flask(__name__)
CORS(app)
# Load and preprocess your data, define your model, train your model here

# Ensure your model and other necessary objects like scalers, label encoders are loaded here
# Assume your model is stored in 'model', scaler in 'scaler', and label encoders in their respective variables

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temp = data['temperature']
    lum = data['luminosity']
    rad = data['radius']
    predicted_star = predict_star_characteristics(temp, lum, rad)
    return jsonify({
        'starType': predicted_star.starType,
        'color': predicted_star.color,
        'spectralClass': predicted_star.spectralClass
    })

if __name__ == '__main__':
    app.run(debug=True)
