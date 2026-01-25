#!/usr/bin/env python3
import i3ipc
import subprocess

def center_mouse():
    # Establish connection to i3 IPC
    i3 = i3ipc.Connection()
    
    # Get the currently focused container
    focused = i3.get_tree().find_focused()
    
    if focused and focused.rect:
        rect = focused.rect
        # Calculate the absolute center
        center_x = rect.x + (rect.width / 2)
        center_y = rect.y + (rect.height / 2)

        # Move the mouse using xdotool
        subprocess.run(['xdotool', 'mousemove', str(int(center_x)), str(int(center_y))])
        print(f"Centered mouse on window: {focused.name}")

if __name__ == "__main__":
    center_mouse()
