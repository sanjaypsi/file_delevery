import csv
import maya.cmds as cmds

def export_keyframes_to_csv(joint_names, frames, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Joint Name', 'Frame', 'Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for joint in joint_names:
            for frame in frames:
                cmds.currentTime(frame)
                pos = cmds.xform(joint, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(joint, query=True, rotation=True, worldSpace=True)
                writer.writerow({
                    'Joint Name': joint,
                    'Frame': frame,
                    'Translate X': pos[0],
                    'Translate Y': pos[1],
                    'Translate Z': pos[2],
                    'Rotate X': rot[0],
                    'Rotate Y': rot[1],
                    'Rotate Z': rot[2]
                })

# Example usage
joints = cmds.ls(type='joint')
frames = [1, 5, 10]  # Including the middle pose at frame 5
export_keyframes_to_csv(joints, frames, 'keyframes_with_middle.csv')


# ===================================================================================================================================
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load data
data = pd.read_csv('keyframes_with_middle.csv')

# Prepare data
start_frame = data[data['Frame'] == 1].drop(columns=['Frame']).values
middle_frame = data[data['Frame'] == 5].drop(columns=['Frame']).values
end_frame = data[data['Frame'] == 10].drop(columns=['Frame']).values

# Concatenate start, middle, and end frames as input features
input_data = np.concatenate([start_frame, middle_frame, end_frame], axis=1)

# Create model
model = Sequential([
    Dense(128, activation='relu', input_shape=(input_data.shape[1],)),
    Dense(256, activation='relu'),
    Dense(128, activation='relu'),
    Dense(start_frame.shape[1])
])

model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(input_data, start_frame, epochs=100)

# Predict intermediate frames
num_intermediate_frames = 8
interpolated_frames = []
for i in range(1, num_intermediate_frames + 1):
    alpha = i / (num_intermediate_frames + 1)
    beta = (num_intermediate_frames + 1 - i) / (num_intermediate_frames + 1)
    interpolated_input = np.concatenate([alpha * start_frame + beta * middle_frame, 
                                         middle_frame, 
                                         alpha * middle_frame + beta * end_frame], axis=1)
    interpolated_frame = model.predict(interpolated_input)
    interpolated_frames.append(interpolated_frame)


# ===================================================================================================================================
# Save interpolated frames
def save_interpolated_keyframes_to_csv(joint_names, interpolated_frames, start_frame_num, end_frame_num, file_path):
    frames = range(start_frame_num + 1, end_frame_num)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Joint Name', 'Frame', 'Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for joint_idx, joint in enumerate(joint_names):
            for frame_idx, frame in enumerate(frames):
                interpolated_pose = interpolated_frames[frame_idx][joint_idx]
                writer.writerow({
                    'Joint Name': joint,
                    'Frame': frame,
                    'Translate X': interpolated_pose[0],
                    'Translate Y': interpolated_pose[1],
                    'Translate Z': interpolated_pose[2],
                    'Rotate X': interpolated_pose[3],
                    'Rotate Y': interpolated_pose[4],
                    'Rotate Z': interpolated_pose[5]
                })

# Example usage
save_interpolated_keyframes_to_csv(joints, interpolated_frames, 1, 10, 'interpolated_keyframes.csv')

# ===================================================================================================================================
def import_keyframes_from_csv(joint_names, file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            joint = row['Joint Name']
            frame = int(row['Frame'])
            pos = [float(row['Translate X']), float(row['Translate Y']), float(row['Translate Z'])]
            rot = [float(row['Rotate X']), float(row['Rotate Y']), float(row['Rotate Z'])]
            cmds.currentTime(frame)
            cmds.xform(joint, translation=pos, worldSpace=True)
            cmds.xform(joint, rotation=rot, worldSpace=True)

# Example usage
import_keyframes_from_csv(joints, 'interpolated_keyframes.csv')

