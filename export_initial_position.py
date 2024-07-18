import maya.cmds as cmds
import json

def export_initial_position(output_file):
    object_name = 'pCube1'
    initial_position = cmds.getAttr(f'{object_name}.translate')[0]
    data = {'initial_position': initial_position}
    with open(output_file, 'w') as f:
        json.dump(data, f)

export_initial_position('initial_position.json')
