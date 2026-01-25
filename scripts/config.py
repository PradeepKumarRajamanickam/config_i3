#!/usr/bin/env python3
import i3ipc
import utils
# from . import *
from pynput import keyboard
import sys

P_GODOT="/media/pradeep/Data/Applications/Godot_v4.5.1-stable_linux.x86_64"
P_PROJ ="/media/pradeep/Data/projects/godot/gdtoolkit/project.godot"

CMD_GODOT = f"{P_GODOT} {P_PROJ}"

CLASS_NAME_GODOT = "Godot"

print("Initialising i3 config via python")

i3 = utils.get_i3_connection()

# # Global Hotkey Mapping
# # <cmd> = Super/Windows key | <alt> = Alt key
# hotkeys = {
#     '<cmd>+<alt>+n': lambda: utils.run_or_focus("nemo", class_name="Nemo"),
#     '<cmd>+<alt>+b': lambda: utils.run_or_focus("google-chrome-stable", instance="google-chrome"),
    
#     # Godot Editor Bindings
#     '<cmd>+<alt>+1': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title=".tscn"),
#     '<cmd>+<alt>+2': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="Script Editor"),
#     '<cmd>+<alt>+3': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="Inspector"),
#     '<cmd>+<alt>+4': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="Import"),
#     '<cmd>+<alt>+5': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="FileSystem"),
#     '<cmd>+<alt>+6': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="Node"),
#     '<cmd>+<alt>+7': lambda: utils.run_or_focus(CMD_GODOT, class_name=CLASS_NAME_GODOT, title="Scene"),
# }

# if __name__ == "__main__":
#     with keyboard.GlobalHotKeys(hotkeys) as h:
#         h.join()
