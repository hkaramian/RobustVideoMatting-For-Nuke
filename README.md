## KM_RobustVideoMatting
Robust Video Matting Plugin for Foundry Nuke

<p align="center">
    <a href="https://youtu.be/Jvzltozpbpk">
        <img src="documentation/images/showreel.gif">
    </a>
</p>

[Robust Video Matting (RVM)](https://github.com/PeterL1n/RobustVideoMatting)  is specifically designed for robust human video matting. Unlike existing neural models that process frames as independent images, RVM uses a recurrent neural network to process videos with temporal memory. Since RVM uses RNN, it gives better result compare to modnet that uses CNN. CNNs have to process each frame sepearately, but an RNN can process the current frame and frames around.

<br>

Watch the video ([YouTube](https://youtu.be/yTpHI3p5pHE))  to see the installation, usage and model's performance. 


## Installation

Use the instructions bellow, or watch above video. 

### Add RVM node to Nuke
1. Copy 'KM_RVM_Nuke' folder to nuke plugin path (.nuke folder)
2. Add the following line to init.py file in the nuke plugin path :
```python
nuke.pluginAddPath('./KM_RVM_Nuke')
```
<br>
Restart nuke, now you can find RVM node via Nodes menu under "Keying" or simply search "rvm" in nodes search bar :
<p align="center">
<img src="documentation/images/menu.png">
 </p>

### Install Dependencies
#### Method 1 (recommended) :
1. Download and Install MiniConda : 
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

2. Open "Anaconda Prompt" located in "KM_RVM_Nuke" folder, or find it in windows search.
Run bellow commands, line by line
```sh
conda create -n km_rvm python=3.9.0
conda activate km_rvm
pip install "av==8.0.3" "tqdm==4.61.1" "pims==0.5"
pip install torch torchvision
```
Replace last line with this if you want to add gpu supoort (it needs download more dependencies and huge files): 
```python
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```
, change "cu118" to your graphic card Cuda version. Cuda table is provided bellow, end of this page.  

All set up, You ready to go ! 



#### Method 2  :
If you have your own python installed and you are familiar with installing packages,  install dependencies. Then in dependencies tab of the gizmo, set python path to you custom python. 



### Check Dependencies
In Dependencies tab, click on "Check Dependencies" button to show your system configs. Compare it to the requirements.  
<p align="center">
 <img src="documentation/images/Dependencies_tab.jpg">
 </p>


### Compatibility
OS : Window

Nuke Version: 15.x, 14.x, 13.x, 12.x 


## Usage

<p align="center">
create rvm node by typing KM_RVM or find it in nuke nodes menu, under keying category. 
Simply connect your input, or choose file path ! 
If you use node input, it will make a png seq precomp first. 
For feeding directly a file, you need to have it as .mp4 or png sequence.
Once job get done, roto matte node will be created. Input precomp and result will be saved in "KM_RVM_Data" folder beside your nuke project. 
Chunk size : Number of frames for parallel process. Play with this number to get better result base on your hardware

<img src="documentation/images/KM_RVM.jpg">


## Graphic Cards CUDA Version
Use this table to find out which version of pytorch cuda you need 

| Graphic Card | Compute Capability | Compatible CUDA Toolkit Version | Command
|---|---|---|---|
| NVIDIA GeForce RTX 4090 | 9.0 | 11.8 | cu118 |
| NVIDIA GeForce RTX 3080 | 7.5 | 11.8 | cu118 |
| NVIDIA GeForce RTX 3070 | 7.5 | 11.8 | cu118 |
| NVIDIA GeForce RTX 3060 | 7.5 | 11.8 | cu118 |
| NVIDIA GeForce RTX 2080 | 7.2 | 11.6 | cu116 |
| NVIDIA GeForce RTX 2070 | 7.2 | 11.6 | cu116 |
| NVIDIA GeForce GTX 1660 | 6.1 | 11.4 | cu114 |
| NVIDIA GeForce GTX 1080 | 6.1 | 11.2 | cu112 |
| NVIDIA GeForce 840M | 5.0 | 10.2 | cu102 |
 


