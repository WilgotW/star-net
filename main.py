import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# Load and preprocess the dataset
star_data = pd.read_csv('star_data.csv')
label_encoder_color = LabelEncoder()
label_encoder_class = LabelEncoder()
star_data['Star color encoded'] = label_encoder_color.fit_transform(star_data['Star color'])
star_data['Spectral Class encoded'] = label_encoder_class.fit_transform(star_data['Spectral Class'])

X = star_data[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)']].values
Y = star_data[['Star type', 'Star color encoded', 'Spectral Class encoded']].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)
X_train_tensor = torch.tensor(X_train, dtype=torch.float)
Y_train_tensor = torch.tensor(Y_train, dtype=torch.float)
X_test_tensor = torch.tensor(X_test, dtype=torch.float)
Y_test_tensor = torch.tensor(Y_test, dtype=torch.float)

train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Define the neural network
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

# Training the model
model = StarNet(len(label_encoder_color.classes_), len(label_encoder_class.classes_))
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion_regression = nn.MSELoss()
criterion_classification = nn.CrossEntropyLoss()

num_epochs = 1000
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        star_type, star_color, spectral_class = model(inputs)
        loss_type = criterion_regression(star_type, labels[:, 0].view(-1, 1))
        loss_color = criterion_classification(star_color, labels[:, 1].long())
        loss_class = criterion_classification(spectral_class, labels[:, 2].long())
        loss = loss_type + loss_color + loss_class
        loss.backward()
        optimizer.step()

# Function for making predictions
def predict_star_characteristics(temp, lum, rad):
    user_input_scaled = scaler.transform([[temp, lum, rad]])
    user_input_tensor = torch.tensor(user_input_scaled, dtype=torch.float)
    
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():  # Inference without tracking gradients
        star_type_pred, star_color_pred, spectral_class_pred = model(user_input_tensor)
    
    # Round the star type to the nearest whole number
    star_type = round(star_type_pred.item())
    star_color = label_encoder_color.inverse_transform([star_color_pred.argmax().item()])[0]
    spectral_class = label_encoder_class.inverse_transform([spectral_class_pred.argmax().item()])[0]
    
    return star_type, star_color, spectral_class


class Star:
    def __init__(self, star_type, color, spectral_class):
        # Conversion from star type number to its string representation
        star_type_dict = {
            0: "Brown Dwarf",
            1: "Red Dwarf",
            2: "White Dwarf",
            3: "Main Sequence",
            4: "Supergiant",
            5: "Hypergiant"
        }
        # Convert star type from int to string description
        self.starType = star_type_dict.get(star_type, "Unknown")
        self.color = color
        self.spectralClass = spectral_class

    def __str__(self):
        return f"Star Type: {self.starType}, Color: {self.color}, Spectral Class: {self.spectralClass}"


# Example usage
temp = float(input("Enter temperature (K): "))
lum = float(input("Enter luminosity (L/Lo): "))
rad = float(input("Enter radius (R/Ro): "))

predicted_star_type, predicted_star_color, predicted_spectral_class = predict_star_characteristics(temp, lum, rad)

predicted_star = Star(predicted_star_type, predicted_star_color, predicted_spectral_class)
print(predicted_star)

