import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to combine data from all JSON files in a directory
def combine_data(directory):
    all_frames = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = load_json_data(file_path)
            frames = []
            for frame, joints in sorted(data.items()):
                frame_data = []
                for joint, coordinates in sorted(joints.items()):
                    frame_data.extend([coordinates['x'], coordinates['y'], coordinates['z']])
                frames.append(frame_data)
            all_frames.append(frames)
    return np.array(all_frames)

# Function to prepare sequence data for LSTM training
def prepare_sequences(data, n_steps):
    X, y = [], []
    for sequence in data:
        for i in range(len(sequence) - n_steps):
            X.append(sequence[i:i + n_steps])
            y.append(sequence[i + n_steps])
    return np.array(X), np.array(y)

# Function to create an LSTM model
def create_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=input_shape),
        LSTM(50, activation='relu'),
        Dense(input_shape[-1])  # output layer nodes should match the number of features
    ])
    return model

# Function to compile the LSTM model
def compile_model(model):
    model.compile(optimizer='adam', loss='mse')

# Function to train the LSTM model
def train_model(model, X, y, epochs=10, batch_size=32):
    model.fit(X, y, epochs=epochs, batch_size=batch_size)

# Main workflow
if __name__ == '__main__':
    # Directory containing JSON files
    directory = '/path/to/json/files'
    
    # Load and combine animation data
    animation_data = combine_data(directory)

    # Prepare sequences with a given number of timesteps
    n_steps = 5
    X, y = prepare_sequences(animation_data, n_steps)

    # Define and compile the model
    input_shape = X.shape[1:]  # (timesteps, features)
    model = create_lstm_model(input_shape)
    compile_model(model)

    # Train the model
    train_model(model, X, y, epochs=20)  # Adjust epochs and batch size as needed

    # Optionally save the model
    model.save('lstm_animation_model.h5')
