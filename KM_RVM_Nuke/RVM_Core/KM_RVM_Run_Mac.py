import torch
from model import MattingNetwork

model = MattingNetwork('mobilenetv3').eval().cpu()  # or "resnet50"
model.load_state_dict(torch.load('/Users/kmdesk/Km Files/KmWorks/KmTools/Km Gizmo Pack/test_tools/PyTorch Learn/RobustVideoMatting/downloaded_model_km/rvm_mobilenetv3.pth'))

# # Load the model from hub.
# model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3") # or "resnet50"

from inference import convert_video

convert_video(
    model,                           # The model, can be on any device (cpu or cuda).
    input_source='/Users/kmdesk/Km Files/KmWorks/KmTools/Km Gizmo Pack/test_tools/PyTorch Learn/sample_video/person.mp4',        # A video file or an image sequence directory.
    output_type='video',             # Choose "video" or "png_sequence"
    output_composition='com.mp4',    # File path if video; directory path if png sequence.
    output_alpha="pha.mp4",          # [Optional] Output the raw alpha prediction.
    output_foreground="fgr.mp4",     # [Optional] Output the raw foreground prediction.
    output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
    downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
    seq_chunk=12,                    # Process n frames at once for better parallelism.
)