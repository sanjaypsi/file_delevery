import os
import json
import numpy as np

# ==================================================================================================
# Helper functions
# ==================================================================================================
def load_json_data(file_path):
    """ Load data from a JSON file. """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# ==================================================================================================
def combine_data(directory):
    """ Load and combine data from all JSON files in a directory. """
    all_frames = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path   = os.path.join(directory, filename)
            data        = load_json_data(file_path)
            frames      = []
            for frame, joints in sorted(data.items()):
                # Assuming each joint's data is in the format {'x': float, 'y': float, 'z': float}
                frame_data = []
                for joint, coordinates in sorted(joints.items()):
                    frame_data.extend([coordinates['x'], coordinates['y'], coordinates['z']])
                frames.append(frame_data)
            all_frames.append(frames)

    return np.array(all_frames)

# ==================================================================================================
def prepare_sequences(data, n_steps):
    """ Prepare the sequence data and labels for LSTM training. """
    X, y = [], []
    for sequence in data:
        for i in range(len(sequence) - n_steps):
            X.append(sequence[i:i + n_steps])
            y.append(sequence[i + n_steps])

    return np.array(X), np.array(y)

# Path to the directory containing your JSON files
directory = '/path/to/json/files'

# Load and combine the animation data from JSON files
animation_data = combine_data(directory)

# Number of time steps you want to use to predict the next step
n_steps = 5

# Prepare data for training
X, y = prepare_sequences(animation_data, n_steps)

print('Shape of input data (X):',  X.shape)
print('Shape of output data (y):', y.shape)
