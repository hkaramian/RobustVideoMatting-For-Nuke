import json
import os
import subprocess

Plugin_Path = os.environ['Km_RVM_Plugin_Path']
json_file = Plugin_Path +"/params.json"
#ssss = "C:/Users/%USERNAME%/miniconda3/python.exe"
with open(json_file, 'r') as f:
    data = json.load(f)
python_path = "\"" + data["python_path"] + "\""

python_version = ""
pytorch_version = ""
torchvision_version = ""
tqdm_version = ""
pims_version = ""
av_version = ""
# check python 
p = subprocess.Popen(python_path +' --version', stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()  
p_status = p.wait()

if p.returncode == 0: # if python exist
  python_version = output
  p = subprocess.Popen(python_path +' -c "import torch; print(torch.__version__)"', stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()  
  p_status = p.wait()
  if p.returncode == 0:
    pytorch_version = output
  else:
     pytorch_version = "not found"
  print("pytorch_version: " + pytorch_version)
  p = subprocess.Popen(python_path +' -c "import torchvision; print(torchvision.__version__)"', stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()  
  p_status = p.wait()
  if p.returncode == 0:
    torchvision_version = output
  else:
     torchvision_version = "not found"
  p = subprocess.Popen(python_path +' -c "import tqdm; print(tqdm.__version__)"', stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()  
  p_status = p.wait()
  if p.returncode == 0:
    tqdm_version = output
  else:
     tqdm_version = "not found"
  p = subprocess.Popen(python_path +' -c "import pims; print(pims.__version__)"', stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()  
  p_status = p.wait()
  if p.returncode == 0:
    pims_version = output
  else:
     pims_version = "not found"

  p = subprocess.Popen(python_path +' -c "import av; print(av.__version__)"', stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()  
  p_status = p.wait()
  if p.returncode == 0:
    av_version = output
  else:
     av_version = "not found"
else:
  python_version = "Python not found"
  pytorch_version = "not found"
  torchvision_version = "not found"
  tqdm_version = "not found"
  pims_version = "not found"
  av_version = "not found"


dependencies_str = """<html>
 %s | av %s | torch %s<br> torchvision %s | tqdm %s | pims %s
""" % (
    python_version,
    av_version,
    pytorch_version,
    torchvision_version,
    tqdm_version,
    pims_version
)

#print(dependencies_str)
nuke.thisNode()["text_depend_info"].setValue(dependencies_str)