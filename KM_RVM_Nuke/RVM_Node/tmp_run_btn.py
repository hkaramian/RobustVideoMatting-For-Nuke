
import ctypes
import glob
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import threading
import time

Plugin_Path = os.environ['Km_RVM_Plugin_Path']
json_file = Plugin_Path +"/params.json"
current_data_path = nuke.script_directory() + "/"+nuke.thisNode().name()+"_Data" 
precomp_temp_dir = current_data_path+"/Temp/"
alpha_output_path = current_data_path + "/alpha/" 
ref_node = nuke.thisNode() # current node as position reference
input_path = precomp_temp_dir

# Get current node
current_node = nuke.thisNode()
frame_range = ""
start_frame_number = 0

socket_data = "0"
processIsDone = False
Device_GPU = False
InputIsNodeInput = False # input : node input / selected file path
readyToRun = False

# check if GPU
if(nuke.thisNode()["checkbox_gpu"].value()):
    Device_GPU = True

# check  whether input is node input or selected file path
if(nuke.thisNode()["pulldown_node_input"].value()=="Node Input"):
    InputIsNodeInput = True


def run_rvm_core() : 
    global processIsDone
    run_cmd = Plugin_Path+  "/RVM_Core/Run.cmd"
    print(run_cmd)
    # p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
    # (output, err) = p.communicate()  
    # p_status = p.wait()
    #print("Command output: " + output)

    # Check if process is done 
    # if "Process is done" in output:
    #     processIsDone = True  
    commands = u'/k ' + r"{}".format(run_cmd)
    ctypes.windll.shell32.ShellExecuteW(
            None,
            u"", #"runas"
            u"cmd.exe",
            commands,
            None,
            1
        )

def rvm_status_update():
    print("start status update thread")
    global processIsDone
    while not processIsDone :
        #processIsDone = data["process_is_done"]
        time.sleep( 1 )
        # print("progressed frames : "+ socket_data)
        with open(json_file, 'r') as f:
            data = json.load(f)
        processIsDone = data["process_is_done"]
    print("loop ended")
    nuke.executeInMainThread( CreateReadNode, args=() )

# def rvm_socket_listener():
#     global socket_data
#     # TCP socket to get progress value from KM_inference.py
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(('localhost', 5000))
#     sock.listen(1)
#     connection, address = sock.accept()
#     # Receive progress updates from the client
#     while True:
#         data = connection.recv(1024).decode('utf-8')
#         if not data:
#             break
#         socket_data = data
#         #print(f"Progress: {progress} out of 100")
#     # Close the connection
#     connection.close()



# remove old files
if os.path.exists(precomp_temp_dir):
    shutil.rmtree(precomp_temp_dir)
if os.path.exists(current_data_path + "/alpha/"):
    shutil.rmtree(current_data_path + "/alpha/")
if os.path.exists(current_data_path + "/com/"):
    shutil.rmtree(current_data_path + "/com/")
if os.path.exists(current_data_path + "/fgr/"):
    shutil.rmtree(current_data_path + "/fgr/")


# chech if project is saved (if it has a project file)
if nuke.Root().name() == 'Root':
    nuke.message("You need to save the project first.")
else :
    # Check if current node has an input
    if InputIsNodeInput:
        if current_node.inputs() :
            # Get the frame range of project
            frame_first = str(int(nuke.root()["first_frame"].getValue()))
            frame_last = str(int(nuke.root()["last_frame"].getValue()))
            frame_range = frame_first + "-"+frame_last

            # Get frame range from user
            frames_input = nuke.getFramesAndViews('get range',frame_range)
            if frames_input : # if get range not cancelled
                frame_first = int(frames_input[0].split('-')[0])
                frame_last = int(frames_input[0].split('-')[1])
                start_frame_number = frame_first
                # Render node input to temp dir
                nuke.execute(nuke.toNode('RVM_Write_Image'), start=frame_first, end=frame_last)
                readyToRun = True
        else:
            nuke.message("Node has no input !")
    else : # if input is selected file
        if nuke.thisNode()["filename"].value() != "" :
            input_path = nuke.thisNode()["filename"].value()
            if input_path[-4:]!= ".mp4" :
                input_path = os.path.dirname(input_path) + "/"
            readyToRun = True
        else:
            nuke.message("filename is empy")


if readyToRun :
    # add data path to json file 
    with open(json_file, 'r') as f:
        data = json.load(f)
    data["current_data_path"] = current_data_path
    data["input_path"] = input_path
    data["process_is_done"] = False
    data["device_GPU"] = Device_GPU
    with open(json_file, "w") as file:
        json.dump(data, file)

    threading.Thread( None, run_rvm_core).start()
    #threading.Thread( None, rvm_socket_listener).start()
    threading.Thread( None, rvm_status_update).start()




# def rename_png_sequence():
#     """RVM png seq starts with 0, so we rename them to match with input frame numbers"""
#     global start_frame_number
#     # Specify the directory containing the PNG images
#     directory = alpha_output_path
#     print("rename : "+alpha_output_path)

#     # Get the list of PNG images in the directory
#     images = [f for f in os.listdir(directory) if f.endswith('.png')]

#     # Sort the images by their names
#     images.sort(key=lambda s: int(s.split('.')[0]))

#     # Rename the images
#     for i, image in enumerate(images):
#         new_name = '%04d.png' % (start_frame_number + i)
#         os.rename(os.path.join(directory, image), os.path.join(directory, new_name))


def CreateReadNode():
    global ref_node
    print("CreateReadNode start")
    fileName = alpha_output_path + "####.png"
    isSequence = True
    readNode = nuke.createNode("Read",inpanel=False)

    readNode.knob('frame_mode').setValue("start at")
    if InputIsNodeInput:
        readNode.knob('frame').setValue(str(start_frame_number))
    else:
        readNode.knob('frame').setValue(str(1))

    print("start set pos")
    # set position
    print("read node name :" + readNode.name())
    print("ref node name :" + ref_node.name())
    readNode.setXpos(ref_node.xpos())
    readNode.setYpos(ref_node.ypos() + ref_node.screenHeight() + 50)
    print("start create shuffle")
    # Create the Shuffle node
    shuffle2_node = nuke.createNode('Shuffle2',inpanel=False)
    layers_in =  ['rgba.red', 'rgba.red', 'rgba.red', 'rgba.red']
    layers_out = ['rgba.red', 'rgba.green', 'rgba.blue', 'rgba.alpha']
    mapping = zip([0, 0, 0, 0], layers_in, layers_out)
    shuffle2_node['mappings'].setValue(mapping)
    shuffle2_node.setYpos(readNode.ypos() + readNode.screenHeight() + 30)

    if isSequence : # using v!ctor tools code(by Victor Perez ) for creating read node for sequence . https://www.nukepedia.com/gizmos/image/vctor-tools
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


    print("CreateReadNode end")

#p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
#(output, err) = p.communicate()  
#os.chmod(python_path, 0o777)
#mask = oct(os.stat(python_path).st_mode)[-3:] 
#print(mask)
#os.system("start /B start cmd.exe @cmd /k " + run_cmd)
#os.startfile(run_file, 'open')