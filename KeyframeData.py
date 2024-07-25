'''
Exporting Keyframe Data from Maya
To export joint keyframe data from Autodesk Maya, you can use the following Python script. 
This script assumes that you have some familiarity with running scripts in the Maya environment

'''

import maya.cmds as cmds
import csv

def export_joint_keyframes():
    joints = cmds.ls(type='joint')
    csv_file_path = 'C:/path_to_your_directory/joint_keyframes.csv'
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Joint Name', 'Frame', 'Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z', 'Label']
        writer.writerow(headers)
        
        # Assume you define frame ranges for each label
        label_ranges = {'walkingA': range(1, 26), 'walkingB': range(26, 51), 'walkingC': range(51, 76), 'walkingD': range(76, 101)}
        
        for frame in range(1, 101):  # Adjust frame range as needed
            cmds.currentTime(frame)
            # Determine label for current frame
            current_label = None
            for label, frange in label_ranges.items():
                if frame in frange:
                    current_label = label
                    break
            
            for joint in joints:
                translate = cmds.getAttr(f"{joint}.translate")[0]
                rotate = cmds.getAttr(f"{joint}.rotate")[0]
                writer.writerow([joint, frame] + list(translate) + list(rotate) + [current_label])

    print("Export complete.")



# # Import the necessary modules
# import maya.cmds as cmds
# import csv

# def export_joint_keyframes():
#     # List all joints in the scene
#     joints = cmds.ls(type='joint')

#     # Define the CSV file path
#     csv_file_path = 'C:/path_to_your_directory/joint_keyframes.csv'

#     # Open a CSV file to write
#     with open(csv_file_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         # Write the headers
#         headers = ['Joint Name', 'Frame', 'Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z']
#         writer.writerow(headers)
        
#         # Iterate over each frame of your animation
#         for frame in range(1, 101):  # Adjust frame range as needed
#             cmds.currentTime(frame)  # Set current frame
#             for joint in joints:
#                 # Get translation and rotation values
#                 translate = cmds.getAttr(f"{joint}.translate")[0]
#                 rotate = cmds.getAttr(f"{joint}.rotate")[0]
#                 # Write data to CSV
#                 writer.writerow([joint, frame] + list(translate) + list(rotate))

#     print("Export complete.")

#     #columns =  ['Joint', 'Frame', 'TranslateX', 'TranslateY', 'TranslateZ', 'RotateX', 'RotateY', 'RotateZ']

