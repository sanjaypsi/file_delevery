import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import matplotlib.pyplot as plt

# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load your CSV data
data = pd.read_csv('walk_cycle_data.csv')

# Ensure all data is numeric and handle missing values
data = data.apply(pd.to_numeric, errors='coerce').fillna(0)

# Extract the relevant features for the model
features = data[['TranslateX', 'TranslateY', 'TranslateZ', 'RotateX', 'RotateY', 'RotateZ']]

# Function to create sequences for in-between frame prediction
def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        seq = data.iloc[i:i+seq_length].values
        sequences.append(seq)
        labels.append(data.iloc[i+seq_length].values)
    return np.array(sequences, dtype=np.float32), np.array(labels, dtype=np.float32)

# Example: Create sequences of length 10 for in-between frame prediction
seq_length = 10
sequences, labels = create_sequences(features, seq_length)

# Inspect the sequences and labels
print(f"Sequences shape: {sequences.shape}")  # Should be (num_samples, seq_length, num_features)
print(f"Labels shape: {labels.shape}")        # Should be (num_samples, num_features)

# Ensure sequences have the correct number of features
assert sequences.shape[2] == 6, f"Expected 6 features per sequence, but got {sequences.shape[2]}"

class WalkCycleDataset(Dataset):
    def __init__(self, sequences, labels):
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        label = self.labels[idx]
        return torch.tensor(sequence, dtype=torch.float32), torch.tensor(label, dtype=torch.float32)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, input_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

# Parameters
input_size = 6  # Number of features (Translate X, Y, Z and Rotate X, Y, Z)
hidden_size = 128
num_layers = 2
batch_size = 32
num_epochs = 5
learning_rate = 0.001

# Prepare DataLoader
train_data = WalkCycleDataset(sequences, labels)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# Model, Loss, Optimizer
model = LSTMModel(input_size, hidden_size, num_layers).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training Loop
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0
    for seq, label in train_loader:
        seq, label = seq.to(device), label.to(device)
        outputs = model(seq)
        loss = criterion(outputs, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
    
    epoch_loss /= len(train_loader)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')

# Function to calculate MAE and RMSE
def calculate_metrics(model, data_loader):
    model.eval()
    mae = 0
    rmse = 0
    with torch.no_grad():
        for seq, label in data_loader:
            seq, label = seq.to(device), label.to(device)
            outputs = model(seq)
            mae += torch.mean(torch.abs(outputs - label)).item()
            rmse += torch.sqrt(torch.mean((outputs - label) ** 2)).item()
    mae /= len(data_loader)
    rmse /= len(data_loader)
    return mae, rmse

# Calculate and print the final metrics on the training data
mae, rmse = calculate_metrics(model, train_loader)
print(f'Training MAE: {mae:.4f}, RMSE: {rmse:.4f}')

# Function to predict in-between frames
def predict_in_between(model, start_frame, end_frame, num_in_between):
    model.eval()
    with torch.no_grad():
        seq = torch.tensor(np.stack([start_frame, end_frame]), dtype=torch.float32).unsqueeze(0).to(device)
        predicted_frames = []
        for _ in range(num_in_between):
            pred = model(seq)
            predicted_frames.append(pred.cpu().numpy())
            # Ensure pred is reshaped to match the dimensions of seq before concatenation
            pred = pred.unsqueeze(1)  # Change pred shape to [batch_size, 1, num_features]
            seq = torch.cat((seq[:, 1:, :], pred), dim=1)
        return np.array(predicted_frames)

# Example prediction
start_frame = features.iloc[0].values
end_frame = features.iloc[seq_length].values
num_in_between = 5
predicted_frames = predict_in_between(model, start_frame, end_frame, num_in_between)

# Convert predicted frames to DataFrame
predicted_df = pd.DataFrame(predicted_frames.squeeze(), columns=['TranslateX', 'TranslateY', 'TranslateZ', 'RotateX', 'RotateY', 'RotateZ'])

# Save the predicted frames to CSV
predicted_df.to_csv('predicted_frames.csv', index=False)

print(predicted_df)

# Visualization
def plot_frames(frames, title):
    plt.figure(figsize=(10, 6))
    for i, col in enumerate(frames.columns):
        plt.subplot(2, 3, i+1)
        plt.plot(frames[col])
        plt.title(col)
    plt.suptitle(title)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

plot_frames(predicted_df, "Predicted In-Between Frames")
