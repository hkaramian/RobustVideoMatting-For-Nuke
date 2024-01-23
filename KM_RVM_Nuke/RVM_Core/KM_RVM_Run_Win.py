import json
import os
import torch


Plugin_Path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

# get input seq directory path
params_file = Plugin_Path +"/../params.json"
with open(params_file, "r") as file:
    loaded_data = json.load(file)
current_data_path = str(loaded_data["current_data_path"]) + "/"
input_path = str(loaded_data["input_path"])
chunk_size = int(loaded_data["chunk_size"])
# Sample video path for test and debug
#video_path = Current_Path+"/../Sample/Sample_Input/person_short.mp4"

device_GPU = False
if (loaded_data["device_GPU"]):
    if torch.cuda.is_available() :
        device_GPU = True
        print("Device : GPU")
    else:
        print("Device : CPU (GPU is selected, but Cuda device is not available on this machine)")
else:
    print("Device : CPU")



from model import MattingNetwork
if device_GPU : 
    model = MattingNetwork('mobilenetv3').eval().cuda()  # or "resnet50"
else:
    model = MattingNetwork('mobilenetv3').eval().cpu()  # or "resnet50"
model.load_state_dict(torch.load(Plugin_Path+"/downloaded_model_km/rvm_mobilenetv3.pth"))
# model = MattingNetwork('resnet50').eval().cpu()  # or "resnet50"
# model.load_state_dict(torch.load(Current_Path+"/downloaded_model_km/rvm_resnet50.pth"))

# # Load the model from hub.
# model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3") # or "resnet50"
    
result_path = current_data_path

from KM_inference import convert_video

convert_video(
    model,                           # The model, can be on any device (cpu or cuda).
    input_source = input_path,        # A video file or an image sequence directory.
    output_type = 'png_sequence',             # Choose "video" or "png_sequence"
    output_composition = result_path+"com/",    # File path if video; directory path if png sequence.
    output_alpha = result_path+"alpha/",          # [Optional] Output the raw alpha prediction.
    #output_foreground = result_path+"fgr/",     # [Optional] Output the raw foreground prediction.
    output_video_mbps = 4,             # Output video mbps. Not needed for png sequence.
    downsample_ratio = None,           # A hyperparameter to adjust or use None for auto.
    seq_chunk = chunk_size,                    # Process n frames at once for better parallelism.
)