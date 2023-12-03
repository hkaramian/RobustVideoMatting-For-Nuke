## Km_RobustVideoMatting
<a href="https://github.com/PeterL1n/RobustVideoMatting" target="_blank">RobustVideoMatting</a> Plugin for Foundry Nuke

Robust Video Matting(RVM) is specifically designed for robust human video matting. Unlike existing neural models that process frames as independent images, RVM uses a recurrent neural network to process videos with temporal memory. RVM can perform matting in real-time on any videos without additional inputs. It achieves **4K 76FPS** and **HD 104FPS** on an Nvidia GTX 1080 Ti GPU.


<br>

## Showreel
Watch the showreel video ([YouTube](https://youtu.be/Jvzltozpbpk))  to see the model's performance. 

<p align="center">
    <a href="https://youtu.be/Jvzltozpbpk">
        <img src="documentation/images/showreel.gif">
    </a>
</p>

All footage in the video are available in [Google Drive](https://drive.google.com/drive/folders/1VFnWwuu-YXDKG-N6vcjK_nL7YZMFapMU?usp=sharing).

<br>


## Installation
### Install plugin
1. Copy 'KM_RVM_Nuke' folder to nuke plugin path (.nuke folder)
2. Add following line to init.py file in the nuke plugin path :
```python
nuke.pluginAddPath('./KM_RVM_Nuke')
```
### Install Dependencies
#### Method 1 (recomended) :
1. Install Miniconda from here : 
https://docs.conda.io/projects/miniconda/en/latest/

2. Open "Anaconda_Prompt" located in KM_RVM_Nuke folder (or simply search "Anaconda Prompt" in windows search bar)
So run bellow commands line by line
```sh
conda create -n km_rvm python=3.8.5
conda activate km_rvm
pip install -r ./requirements_inference.txt
```

All set up, You ready to go ! 

#### Method 2  :
If you have own python installed and you are familiar with installing packages, then install dependencies using "requirements_inference_Km.txt" file.
Then in dependencies tab of the gizmo, set python path to you custom python. 

<center>
<a href="https://vimeo.com/664873484" target="_blank">Watch at Vimeo</a>

- - - - - - - - - - - - - - - - - - - - - - - - 
</center>

 
 

### Compatibility
OS : Window

Nuke Version: 15.x, 14.x, 13.x, 12.x 



### Installation



### ScreenShots
<p align="center">
<img src="https://user-images.githubusercontent.com/93508495/149018084-81afa661-64d6-4ff8-88d3-294df1f36e59.png">
</p>

 
Also Avaiable in : 

<a href="" target="_blank">NukePedia</a>


