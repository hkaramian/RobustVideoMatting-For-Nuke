
import ctypes

Plugin_Path = os.environ['Km_RVM_Plugin_Path']



# Get the current node
current_node = nuke.thisNode()
frame_range = ""
# Check if the current node has an input
if current_node.inputs():
    # Get the first input node
    input_node = current_node.input(0)

    # Check if the input node is a Read node
    if input_node.Class() == 'Read':
        # Get the frame range of the Read node
        frame_first = str(int(input_node['first'].getValue()))
        frame_last = str(int(input_node['last'].getValue()))
        frame_range = frame_first + "-"+frame_last

        # get frame range from user
        frames_input = nuke.getFramesAndViews('get range',frame_range)
        first_number = int(frames_input[0].split('-')[0])
        second_number = int(frames_input[0].split('-')[1])

        run_cmd = Plugin_Path+  "/RVM_Core/Run.cmd"
        commands = u'/k ' + r"{}".format(run_cmd)
        ctypes.windll.shell32.ShellExecuteW(
                None,
                u"", #"runas"
                u"cmd.exe",
                commands,
                None,
                1
            )
        print("It's done now from nuke !")

    else:
        # The input node is not a Read node
        nuke.message('Input is not a "Read" node.\n Connect it to a Read node directly, or Check "Precomp Input" option.')
else:
    # The current node has no inputs
    nuke.message("Current node has no input!")






# if(nuke.thisNode()["precomp_checkbox"].value()):
#     #nuke.execute(nuke.toNode('Write_i_image'), start=frame_to_render, end=frame_to_render)
#     print("render precomp")


















#p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, shell=True)
#(output, err) = p.communicate()  
#os.chmod(python_path, 0o777)
#mask = oct(os.stat(python_path).st_mode)[-3:] 
#print(mask)
#os.system("start /B start cmd.exe @cmd /k " + run_cmd)
#os.startfile(run_file, 'open')