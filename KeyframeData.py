'''
Exporting Keyframe Data from Maya
To export joint keyframe data from Autodesk Maya, you can use the following Python script. 
This script assumes that you have some familiarity with running scripts in the Maya environment

'''
# Import the necessary modules
import maya.cmds as cmds
import csv

def export_joint_keyframes():
    # List all joints in the scene
    joints = cmds.ls(type='joint')

    # Define the CSV file path
    csv_file_path = 'C:/path_to_your_directory/joint_keyframes.csv'

    # Open a CSV file to write
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        headers = ['Joint Name', 'Frame', 'Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z']
        writer.writerow(headers)
        
        # Iterate over each frame of your animation
        for frame in range(1, 101):  # Adjust frame range as needed
            cmds.currentTime(frame)  # Set current frame
            for joint in joints:
                # Get translation and rotation values
                translate = cmds.getAttr(f"{joint}.translate")[0]
                rotate = cmds.getAttr(f"{joint}.rotate")[0]
                # Write data to CSV
                writer.writerow([joint, frame] + list(translate) + list(rotate))

    print("Export complete.")
