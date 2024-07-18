import maya.cmds as cmds
import json

def import_predicted_actions(input_file):
    with open(input_file, 'r') as f:
        predicted_actions = json.load(f)

    object_name = 'pCube1'  # Change this to your object's name

    for action in predicted_actions:
        frame = action['frame']
        position = action['position']
        
        cmds.currentTime(frame)
        cmds.setAttr(f'{object_name}.translate', *position)
        cmds.setKeyframe(object_name, attribute='translate', t=frame)

# Run the function with the path to your predicted actions file
import_predicted_actions('predicted_actions.json')
