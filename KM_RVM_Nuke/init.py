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
v0.7 | add batch render (Sequence render)
v0.6 | add iteration option
v0.5 | create "processing..." window using pyside2 to show a gif image process, system CPU and RAM usage
v0.4 | basic functionality of give input and get result, updating GUI after process gets done
v0.3 | Installing dependencies using Miniconda - Creating venv for Km_RVM
v0.2 | define inputs and inside Group node graph
v0.1 | basic concept and GUI
"""

import os
import json

Km_RVM_Plugin_Path = os.path.dirname(__file__).replace('\\', '/')
Km_RVM_Miniconda_Python_Path = os.path.expanduser("~").replace('\\', '/') + "/miniconda3/envs/km_rvm/python.exe"
json_file = Km_RVM_Plugin_Path +"/params.json"

os.environ['Km_RVM_Plugin_Path'] = Km_RVM_Plugin_Path
os.environ['Km_RVM_Miniconda_Python_Path'] = Km_RVM_Miniconda_Python_Path
print("Km RVM : run_file ENV added")

Run_File_Path_Win = Km_RVM_Plugin_Path + "/RVM_Core/KM_RVM_Run_Win.py"
CMD_File_Path = Km_RVM_Plugin_Path+"/RVM_Core/Run.cmd"


def Update_Run_cmd_file():
    # Create Run.cmd file (based on plugin path)
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