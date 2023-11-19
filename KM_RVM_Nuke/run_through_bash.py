import os

run_file  = r'"Z:/Km Files/KmWorks/KmTools/Km Gizmo Pack/test_tools/PyTorch Learn/RobustVideoMatting/RVM_Core/tmp_km_run_Win.py"'
#python_path = "c:%HOMEPATH%\miniconda3\envs\km_rvm\python.exe"
python_path = r"'C:/Users/kmdesk/miniconda3/envs/km_rvm/python.exe'"
run_cmd = python_path + " " + run_file
print(run_cmd)
#p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
#(output, err) = p.communicate()  
os.system("start /B start cmd.exe @cmd /k " + run_cmd)



# processIsDone = False
# def selfDestruct22():
#     global processIsDone
#     print(run_cmd)
#     p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
#     (output, err) = p.communicate()  
#     p_status = p.wait()
#     print("Command output: " + output)
#     # Check if process is done 
#     while not processIsDone :
#         time.sleep( 2 )
#         print(p_status)
#         print(output)
#     if "it's done now" in output:
#         processIsDone = True  
#         print("it's done now")
#         time.sleep( 1.5 )

# # def selfDestruct():
# #     while not processIsDone :
# #         time.sleep( 0.8 )
# #         cpu_usage = psutil.cpu_percent()
# #         memory_usage = psutil.virtual_memory()
# #         print (f"cpu {cpu_usage}")


# threading.Thread( None, selfDestruct22 ).start()
# # threading.Thread( None, selfDestruct ).start()



# import os
# os.system("start /B start cmd.exe @cmd /k " + run_cmd)


# environment = {} # type: Dict[str, str]
# startupinfo = None # type: ignore # this is only a windows option
# # Python 2.6 has subprocess.STARTF_USESHOWWINDOW, and Python 2.7 has subprocess._subprocess.STARTF_USESHOWWINDOW, so check for both.
# if hasattr(subprocess, '_subprocess') and hasattr(subprocess._subprocess, 'STARTF_USESHOWWINDOW'): # type: ignore # this is only a windows option
#     startupinfo = subprocess.STARTUPINFO() # type: ignore # this is only a windows option
#     startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW # type: ignore # this is only a windows option
# elif hasattr(subprocess, 'STARTF_USESHOWWINDOW'):
#     startupinfo = subprocess.STARTUPINFO() # type: ignore # this is only a windows option
#     startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW # type: ignore # this is only a windows option

# # Specifying PIPE for all handles to workaround a Python bug on Windows. The unused handles are then closed immediatley afterwards.
# proc = subprocess.Popen(run_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, env=environment)
# output, errors = proc.communicate()