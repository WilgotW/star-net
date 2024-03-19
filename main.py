import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load and preprocess the dataset
df = pd.read_csv('./star_data.csv')
X = df[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)']]
y = df[['Star type', 'Star color', 'Spectral Class']]

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Encode the categorical outputs
color_encoder = LabelEncoder()
y['Star color'] = color_encoder.fit_transform(y['Star color'])

spectral_encoder = LabelEncoder()
y['Spectral Class'] = spectral_encoder.fit_transform(y['Spectral Class'])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Convert data into PyTorch tensors
X_train_tensor = torch.tensor(X_train.astype('float32').values)
X_test_tensor = torch.tensor(X_test.astype('float32').values)
y_train_tensor = torch.tensor(y_train.values.astype('int64'))
y_test_tensor = torch.tensor(y_test.values.astype('int64'))

# Define custom dataset
class StarDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

# Create dataset instances
train_dataset = StarDataset(X_train_tensor, y_train_tensor)
test_dataset = StarDataset(X_test_tensor, y_test_tensor)

# Create DataLoader instances
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Neural Network Model
class StarTypePredictor(nn.Module):
    def __init__(self, num_features, num_star_types, num_colors, num_spectral_classes):
        super(StarTypePredictor, self).__init__()
        self.fc1 = nn.Linear(num_features, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.type_layer = nn.Linear(16, num_star_types)
        self.color_layer = nn.Linear(16, num_colors)
        self.spectral_layer = nn.Linear(16, num_spectral_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        star_type = self.type_layer(x)
        star_color = self.color_layer(x)
        spectral_class = self.spectral_layer(x)
        return star_type, star_color, spectral_class

# Initialize the model
num_features = X_train_tensor.shape[1]
num_star_types = y_train['Star type'].nunique()
num_colors = y_train['Star color'].nunique()
num_spectral_classes = y_train['Spectral Class'].nunique()

model = StarTypePredictor(num_features, num_star_types, num_colors, num_spectral_classes)

# Training
criterion_type = nn.CrossEntropyLoss()
criterion_color = nn.CrossEntropyLoss()
criterion_spectral = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        type_pred, color_pred, spectral_pred = model(inputs)
        loss_type = criterion_type(type_pred, labels[:, 0])
        loss_color = criterion_color(color_pred, labels[:, 1])
        loss_spectral = criterion_spectral(spectral_pred, labels[:, 2])
        loss = loss_type + loss_color + loss_spectral
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# Evaluation
model.eval()  # Set the model to evaluation mode
correct_type = correct_color = correct_spectral = total = 0

with torch.no_grad():  # No gradients needed for evaluation
    for inputs, labels in test_loader:
        type_pred, color_pred, spectral_pred = model(inputs)
        _, predicted_type = torch.max(type_pred, 1)
        _, predicted_color = torch.max(color_pred, 1)
        _, predicted_spectral = torch.max(spectral_pred, 1)

        total += labels.size(0)
        correct_type += (predicted_type == labels[:, 0]).sum().item()
        correct_color += (predicted_color == labels[:, 1]).sum().item()
        correct_spectral += (predicted_spectral == labels[:, 2]).sum().item()

# Calculate and print accuracies
accuracy_type = 100 * correct_type / total
accuracy_color = 100 * correct_color / total
accuracy_spectral = 100 * correct_spectral / total

print(f'Accuracy for Star Type Prediction: {accuracy_type:.2f}%')
print(f'Accuracy for Star Color Prediction: {accuracy_color:.2f}%')
print(f'Accuracy for Spectral Class Prediction: {accuracy_spectral:.2f}%')
