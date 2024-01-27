#
# Km_RobustVideoMatting v1.0
# RVM for nuke
# Nuke tool Developed By Hossein Karamian
# 
# www.hkaramian.com
# kmworks.call@gmail.com
#
#    _  __  __  __ 
#   | |/ / |  \/  |
#   | ' /  | \  / |
#   |  <   | |\/| |
#   |_|\_\ |_|  |_|
#

"""
Changes Log :
v1.0 | first release
v0.8 | fix minor bugs
v0.7 | cleaning code
v0.6 | create read node from output, and set start frame (if input is file input, user needs to set start frame)
v0.5 | add file input
v0.4 | add node input, precomp render 
v0.3 | Dependencies tab : check dependencies, set custom python
v0.2 | Installing dependencies using Miniconda - Creating venv for Km_RVM
v0.1 | Basic concept and GUI



Dev Docs : 
- Our files : 
    - ./RVM_Core/KM_RVM_Run_Win.py : run convert_video function
    - ./RVM_Core/KM_inference.py : convert_video defenition. command prompt code, where shows progress while it's running
    - ./RVM_Core/Run.cmd : we run KM_RVM_Run_Win.py using conda python (or custom python) here.
    - ./RVM_Node/RVM_Node.nk
        - Run btn 
        - Check Dependecies btn 
        - knobChanged Callback
        - onCreate Callback
        (it's easier to use knob scripter plugin for editing callbacks)
    - ./Anaconda Prompt.cmd
    - ./init.py
    - ./menu.py
    - ./params.json

"""

import os
import json

nuke.pluginAddPath('./RVM_Node/icon')

Km_RVM_Plugin_Path = os.path.dirname(__file__).replace('\\', '/')
#Km_RVM_Python_Path = os.path.expanduser("~").replace('\\', '/') + "/miniconda3/envs/km_rvm/python.exe"
json_file = Km_RVM_Plugin_Path +"/params.json"

def create_params_json_file():
    data = {"processed_frames": "", 
            "input_path": "", 
            "python_type": "Miniconda",           
            "device_GPU": True, 
            "python_path": "C:/Users/%USERNAME%/miniconda3/envs/km_rvm/python.exe",
            "process_is_done": True,
            "total_frames": "",
            "first_frame": "",
            "chunk_size": "10",
            "current_data_path": ""
            }
    json_string = json.dumps(data, indent=4)
    with open(json_file, 'w') as f:
        f.write(json_string)

# create params.json if doesn't exists.
if not os.path.exists(json_file):
    create_params_json_file()

# load params json file
with open(json_file, 'r') as f:
    data = json.load(f)

os.environ['Km_RVM_Plugin_Path'] = Km_RVM_Plugin_Path
os.environ['Km_RVM_Python_Path'] = data["python_path"]

Run_File_Path_Win = Km_RVM_Plugin_Path + "/RVM_Core/KM_RVM_Run_Win.py"
CMD_File_Path = Km_RVM_Plugin_Path+"/RVM_Core/Run.cmd"


def Update_Run_cmd_file():
    """ Create Run.cmd file (based on plugin path) """
    with open(json_file, 'r') as f:
        data = json.load(f)
    python_path = "\"" + data["python_path"] + "\""
    with open(CMD_File_Path, 'w') as f:
        f.writelines([python_path +' "'+Run_File_Path_Win+'"\n',
                    #'pause\n',
                    'exit\n',
                    '\n'])
    #print("Km_RobustVideoMatting : Run.cmd file updated")
        

Update_Run_cmd_file()