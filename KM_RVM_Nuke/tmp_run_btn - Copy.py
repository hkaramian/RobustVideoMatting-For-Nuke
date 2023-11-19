import subprocess 
import json
import psutil
import time
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QThread, Signal
from PySide2.QtGui import *
import sys


params_file = os.environ.get('Km_AI_Plugin_Path')+"/params.json"
print(params_file)
# Read data from JSON file
with open(params_file, "r") as file:
    loaded_data = json.load(file)

# current_directory = os.path.dirname(os.path.abspath(__file__))
current_directory = str(loaded_data["current_data_path"])
Batch_Render = loaded_data["Batch_Render"]
print("batch bool?")
print(Batch_Render)

frame_to_render = nuke.frame()

if Batch_Render :
    print("start frame :::::::::::::::::: "+loaded_data["frame_number"])    
    print(int(loaded_data["frame_number"]))
    frame_to_render = int(loaded_data["frame_number"])
    #nuke.activeViewer().node()['frame'].setValue(int(loaded_data["frame_number"]))
    
nuke.execute(nuke.toNode('Write_i_image'), start=frame_to_render, end=frame_to_render)
nuke.execute(nuke.toNode('Write_i_mask'), start=frame_to_render, end=frame_to_render)


# create bash command 
run_file  = "\"" + os.environ.get('Km_AI_Plugin_Path')+'/Run.py'+ "\""
# python_path = '"C:/Users/kmdesk/AppData/Local/Programs/Python/Python37/python.exe"'
python_path = loaded_data["python_path"]
run_cmd = python_path + " " + run_file
current_data_path = nuke.script_directory() + "/"+nuke.thisNode().name()+"_Data" 


print(run_file)
print(current_data_path)

json_file = os.environ.get('Km_AI_Plugin_Path')+"/params.json"
with open(json_file, 'r') as f:
  data = json.load(f)

data["current_data_path"] = current_data_path
data["frame_number"] = str(frame_to_render).zfill(5)
data["end_frame"] = loaded_data["end_frame"]
data["Batch_Render"] = Batch_Render

# Write data to JSON file
with open(json_file, "w") as file:
    json.dump(data, file)


window= QWidget()
layout=QVBoxLayout()
label = QLabel("Processing")
label.setStyleSheet("color: orange; font-weight: bold;")
label2 = QLabel("CPU")
label3 = QLabel("RAM")
label4 = QLabel("If the system runs out of memory, processing will fail. So be sure you have enough free memory or make the input resolution lower.")
window.setWindowTitle("Km AI Cleaner")
window.setFixedWidth(300)
label4.setFixedWidth(300)
label4.setWordWrap(True)

# loading spinner
loading_label = QLabel("")
movie = QMovie("C:/Users/kmdesk/Desktop/nuke test/Km_AI_Cleaner/Assets/Pulse-1s-80px (1).gif")
loading_label.setMovie(movie)
movie.start()
# align widgets
label.setAlignment(Qt.AlignCenter)
loading_label.setAlignment(Qt.AlignCenter)
label2.setAlignment(Qt.AlignCenter)
label3.setAlignment(Qt.AlignCenter)
# add widgets
layout.addWidget(label)
layout.addWidget(loading_label)
layout.addWidget(label2)
layout.addWidget(label3)
layout.addWidget(label4)
window.setLayout(layout)
window.show()

processIsDone = False
currentNode = nuke.thisNode()

def selfDestruct22():
    global processIsDone
    print(run_cmd)
    p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()  
    p_status = p.wait()
    print("Command output: " + output)
    # Check if process is done 
    if "it's done now" in output:
        processIsDone = True  
        label.setText("Done !")
        label.setStyleSheet("color: green; font-weight: bold;")
        time.sleep( 1.5 )
        window.close()
        nuke.executeInMainThread( selfDestruct33, args=() )

def selfDestruct():
    while not processIsDone :
        label.setText("Processing")
        time.sleep( 0.8 )
        cpu_usage = psutil.cpu_percent()
        label2.setText("CPU : "+str(cpu_usage)+"%")
        memory_usage = psutil.virtual_memory()
        label3.setText("RAM : "+str(memory_usage.percent)+"%")

def selfDestruct33():
    # reload result read node in case it has already cached older version
    resultReadNode = currentNode.node('Read_result')
    result_path = current_data_path+"/Result/result_#####.png"
    update_read_node(resultReadNode,result_path)
    # set output to result
    currentNode["output_image"].setValue("Result")
    
    # Disable Preview Clean matte
    currentNode["preview_clean_matte"].setValue(False)
    
    # update last run text
    from datetime import datetime
    now = datetime.now()
    formatted_date_time = now.strftime("%Y/%m/%d %H:%M")
    currentNode["text_last_run"].setValue(formatted_date_time)
    print("before size")
    #currentNode["text_s_size"].setValue(str(get_directory_size(current_data_path))+" MB")
    print("Km AI Cleaner - one pass done")
    print("check for new round")
    Batch_Render = loaded_data["Batch_Render"]
    print(Batch_Render)
    next_frame_to_render = frame_to_render + 1
    if next_frame_to_render > int(loaded_data["end_frame"]):
        Batch_Render = False
        print("made batch var False")
    print(Batch_Render)
    with open(params_file, 'r') as f:
        data = json.load(f)
    data["current_data_path"] = current_data_path
    data["frame_number"] = str(frame_to_render).zfill(5)
    data["end_frame"] = loaded_data["end_frame"]
    data["Batch_Render"] = Batch_Render
    # Write data to JSON file
    with open(os.environ.get('Km_AI_Plugin_Path')+"/params.json", "w") as file:
        json.dump(data, file)
    print(Batch_Render)
    if Batch_Render :
        print("executing run button")
        currentNode['btn_run'].execute()


#def check_for_another_round():


def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    total_size_in_MB = total_size / (1024 * 1024.0)
    return   '{:.2f}'.format(total_size_in_MB)

def update_read_node(readNode,fileName):
    import re
    import glob 
    import platform
    readNode.knob('file').setValue(fileName)
    cleanPath = nukescripts.replaceHashes(fileName) 
    padRE = re.compile('%0(\d+)d') 
    padMatch = padRE.search(cleanPath)         
    if padMatch: 
        padSize = int(padMatch.group(1)) 
        frameList = sorted(glob.iglob(padRE.sub('[0-9]' * padSize, cleanPath))) 
        first = os.path.splitext(frameList[0])[0][-padSize:] 
        last = os.path.splitext(frameList[-1])[0][-padSize:] 
        if platform.system() == "Windows":
            readNode['file'].fromUserText('%s %s-%s' % (cleanPath, first, last))
        else : # for linux
            readNode['file'].fromUserText(cleanPath)
            readNode['first'].setValue(int(nuke.root()["first_frame"].getValue())) # code above doesn't work properly for linux so we set first & last from project
            readNode['last'].setValue(int(nuke.root()["last_frame"].getValue()))
            readNode['origfirst'].setValue(int(nuke.root()["first_frame"].getValue()))
            readNode['origlast'].setValue(int(nuke.root()["last_frame"].getValue()))  
    readNode.knob('reload').execute()

threading.Thread( None, selfDestruct22 ).start()
threading.Thread( None, selfDestruct ).start()



