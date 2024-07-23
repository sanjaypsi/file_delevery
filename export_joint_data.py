import maya.cmds as cmds
import json

def export_joint_data(joint_names, start_frame, end_frame, file_path):
    """
    Export joint animation data to a JSON file.

    Parameters:
    - joint_names (list): List of joint names to export.
    - start_frame (int): Starting frame of the animation.
    - end_frame (int): Ending frame of the animation.
    - file_path (str): Path to the JSON file to save the data.
    """
    # Dictionary to hold all the data
    animation_data = {}

    # Loop over each frame in the specified range
    for frame in range(start_frame, end_frame + 1):
        cmds.currentTime(frame)  # Set the current time to the frame
        frame_data = {}

        # Extract data for each joint
        for joint in joint_names:
            position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
            frame_data[joint] = {'x': position[0], 'y': position[1], 'z': position[2]}
        
        animation_data[f'frame_{frame}'] = frame_data

    # Write the dictionary to a JSON file
    with open(file_path, 'w') as f:
        json.dump(animation_data, f, indent=4)

# Example usage
joint_names = ['joint1', 'joint2', 'joint3']  # Replace with your actual joint names
start_frame = 1
end_frame = 100
file_path = 'C:/path/to/your/animation_data.json'

export_joint_data(joint_names, start_frame, end_frame, file_path)
