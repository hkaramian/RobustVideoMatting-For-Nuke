
import json
import os
import sys

# params_file = str(os.environ.get('Km_AI_Plugin_Path'))+"/params.json"
# print(params_file)
# with open(params_file, "r") as file:
#     loaded_data = json.load(file)

# current_directory = str(loaded_data["current_data_path"])
# print("aaaaaaaaaaaaa")
# print(current_directory)

Plugin_Path = os.path.dirname(os.path.abspath(__file__))
path =  Plugin_Path + "/RVM_Core"
path = path.replace( "\\", "/" )
sys.path.append( path )

print("Staaaaaaaaaart Of run file")
import torch
from model import MattingNetwork

model = MattingNetwork('mobilenetv3').eval().cpu()  # or "resnet50"
trained_model_path = Plugin_Path +"/RVM_Core/downloaded_model_km/rvm_mobilenetv3.pth"
model.load_state_dict(torch.load(trained_model_path))

# print((str(os.environ.get('Km_RVM_Plugin_Path'))+"/Run.py").replace('/', '\\\\'))
# print(str(os.environ.get('Km_RVM_Miniconda_Python_Path')).replace('/', '\\\\'))


# # Load the model from hub.
# model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3") # or "resnet50"

from inference import convert_video

print("just before start")

video_path = Plugin_Path +"/Sample/Sample input/person_short.mp4"

convert_video(
    model,                           # The model, can be on any device (cpu or cuda).
    input_source=video_path,        # A video file or an image sequence directory.
    output_type='video',             # Choose "video" or "png_sequence"
    output_composition='com.mp4',    # File path if video; directory path if png sequence.
    output_alpha="pha.mp4",          # [Optional] Output the raw alpha prediction.
    output_foreground="fgr.mp4",     # [Optional] Output the raw foreground prediction.
    output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
    downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
    seq_chunk=12,                    # Process n frames at once for better parallelism.
)

print("it's done now")

