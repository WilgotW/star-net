import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
class StarNet(nn.Module):
    def __init__(self, num_colors, num_classes):
        super(StarNet, self).__init__()
        self.fc1 = nn.Linear(3, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc_out_type = nn.Linear(64, 1)
        self.fc_out_color = nn.Linear(64, num_colors)
        self.fc_out_class = nn.Linear(64, num_classes)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        star_type = self.fc_out_type(x)
        star_color = self.fc_out_color(x)
        spectral_class = self.fc_out_class(x)
        return star_type, star_color, spectral_class

def train_model():
    star_data = pd.read_csv('./adjusted_star_data.csv')
    label_encoder_color = LabelEncoder()
    label_encoder_class = LabelEncoder()
    star_data['Star color encoded'] = label_encoder_color.fit_transform(star_data['Star color'])
    star_data['Spectral Class encoded'] = label_encoder_class.fit_transform(star_data['Spectral Class'])

    X = star_data[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)']].values
    Y = star_data[['Star type', 'Star color encoded', 'Spectral Class encoded']].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_tensor = torch.tensor(X_scaled, dtype=torch.float)
    Y_tensor = torch.tensor(Y, dtype=torch.float)

    dataset = TensorDataset(X_tensor, Y_tensor)
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

    model = StarNet(len(label_encoder_color.classes_), len(label_encoder_class.classes_))
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion_regression = nn.MSELoss()
    criterion_classification = nn.CrossEntropyLoss()

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
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    # Save model and encoders for later use
    torch.save(model.state_dict(), os.path.join("model", 'model_state_dict.pth'))
    torch.save(label_encoder_color, os.path.join("model", 'label_encoder_color.pth'))
    torch.save(label_encoder_class, os.path.join("model", 'label_encoder_class.pth'))
    torch.save(scaler, os.path.join("model", 'scaler.pth'))

if __name__ == '__main__':
    train_model()
