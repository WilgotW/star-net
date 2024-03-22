from flask import Flask, request, jsonify
import torch
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import torch.nn.functional as F
from flask_cors import CORS
from main import StarNet 

app = Flask(__name__)
CORS(app)

model = StarNet(len(torch.load('./model/label_encoder_color.pth').classes_), len(torch.load('./model/label_encoder_class.pth').classes_))
model.load_state_dict(torch.load('./model/model_state_dict.pth'))
model.eval() 

label_encoder_color = torch.load('./model/label_encoder_color.pth')
label_encoder_class = torch.load('./model/label_encoder_class.pth')
scaler = torch.load('./model/scaler.pth')

def predict_star_characteristics(temp, lum, rad):

    user_input_scaled = scaler.transform([[temp, lum, rad]])
    user_input_tensor = torch.tensor(user_input_scaled, dtype=torch.float)
    model.eval()
    with torch.no_grad():
        star_type_pred, star_color_pred, spectral_class_pred = model(user_input_tensor)

    star_type_dict = {0: "Brown Dwarf", 1: "Red Dwarf", 2: "White Dwarf",
                      3: "Main Sequence", 4: "Supergiant", 5: "Hypergiant"}

    star_type = star_type_dict.get(round(star_type_pred.item()), "Unknown")

    star_color = label_encoder_color.inverse_transform([star_color_pred.argmax().item()])[0]
    spectral_class = label_encoder_class.inverse_transform([spectral_class_pred.argmax().item()])[0]

    return {'starType': star_type, 'color': star_color, 'spectralClass': spectral_class}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temp = data['temperature']
    lum = data['luminosity']
    rad = data['radius']
    prediction = predict_star_characteristics(temp, lum, rad)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)
