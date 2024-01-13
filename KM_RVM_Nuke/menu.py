menu = nuke.menu("Nuke")

## Define Main Menu
menubar = nuke.menu('Nodes') ## for top menu : nuke.menu('Nuke')
Km_VFX_menu = menubar.addMenu('Keyer')
Km_VFX_menu.addCommand("KM RVM (Robust Video Matting)", "nuke.loadToolset('"+os.path.dirname(__file__)+"/RVM_Node/RVM_Node.nk')",icon="KM_RMV_icon.png", shortcut='')