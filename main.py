import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# Load and preprocess the dataset
star_data = pd.read_csv('./star_data.csv')
label_encoder_color = LabelEncoder()
label_encoder_class = LabelEncoder()
star_data['Star color encoded'] = label_encoder_color.fit_transform(star_data['Star color'])
star_data['Spectral Class encoded'] = label_encoder_class.fit_transform(star_data['Spectral Class'])

X = star_data[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)']].values
Y = star_data[['Star type', 'Star color encoded', 'Spectral Class encoded']].values

# Preprocess the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Scale the entire dataset

# Convert to tensors
X_tensor = torch.tensor(X_scaled, dtype=torch.float)
Y_tensor = torch.tensor(Y, dtype=torch.float)

# Create a TensorDataset and DataLoader
dataset = TensorDataset(X_tensor, Y_tensor)
data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Neural network definition
class StarNet(nn.Module):
    def __init__(self, num_colors, num_classes):
        super(StarNet, self).__init__()
        self.fc1 = nn.Linear(3, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc_out_type = nn.Linear(64, 1)  # For Star type
        self.fc_out_color = nn.Linear(64, num_colors)  # For Star color
        self.fc_out_class = nn.Linear(64, num_classes)  # For Spectral Class

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        star_type = self.fc_out_type(x)
        star_color = self.fc_out_color(x)
        spectral_class = self.fc_out_class(x)
        return star_type, star_color, spectral_class

# Model instantiation
model = StarNet(len(label_encoder_color.classes_), len(label_encoder_class.classes_))
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion_regression = nn.MSELoss()
criterion_classification = nn.CrossEntropyLoss()

# Model training
num_epochs = 5000
for epoch in range(num_epochs):
    for inputs, labels in data_loader:
        optimizer.zero_grad()
        star_type, star_color, spectral_class = model(inputs)
        loss_type = criterion_regression(star_type, labels[:, 0].view(-1, 1))
        loss_color = criterion_classification(star_color, labels[:, 1].long())
        loss_class = criterion_classification(spectral_class, labels[:, 2].long())
        loss = loss_type + loss_color + loss_class
        loss.backward()
        optimizer.step()
    if epoch % 100 == 0:  # Adjust the printing frequency as needed
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Star class definition for packaging prediction results
class Star:
    def __init__(self, star_type, color, spectral_class):
        star_type_dict = {0: "Brown Dwarf", 1: "Red Dwarf", 2: "White Dwarf",
                          3: "Main Sequence", 4: "Supergiant", 5: "Hypergiant"}
        self.starType = star_type_dict.get(star_type, "Unknown")
        self.color = color
        self.spectralClass = spectral_class

    def __str__(self):
        return f"Star Type: {self.starType}, Color: {self.color}, Spectral Class: {self.spectralClass}"

# Prediction function
def predict_star_characteristics(temp, lum, rad):
    user_input_scaled = scaler.transform([[temp, lum, rad]])
    user_input_tensor = torch.tensor(user_input_scaled, dtype=torch.float)
    model.eval()
    with torch.no_grad():
        star_type_pred, star_color_pred, spectral_class_pred = model(user_input_tensor)
    star_type = round(star_type_pred.item())
    star_color = label_encoder_color.inverse_transform([star_color_pred.argmax().item()])[0]
    spectral_class = label_encoder_class.inverse_transform([spectral_class_pred.argmax().item()])[0]
    return Star(star_type, star_color, spectral_class)

