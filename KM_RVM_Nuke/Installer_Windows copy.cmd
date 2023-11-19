curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" miniconda.exe /S
del miniconda.exe
c:%HOMEPATH%\miniconda3\_conda create -n km_rvm python=3.8.5
c:%HOMEPATH%\miniconda3\_conda activate km_rvm
pip install -r ./requirements_inference.txt
echo    ===============================================
echo    if there is no error above, We are good to go !
echo    ===============================================
pause