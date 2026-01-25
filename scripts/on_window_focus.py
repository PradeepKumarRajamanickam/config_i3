#!/usr/bin/env python3
import i3ipc
import subprocess
from center_mouse import *

def on_window_focus(i3, e):    
    center_mouse()

i3 = i3ipc.Connection()
i3.on('window::focus', on_window_focus)
i3.main()
