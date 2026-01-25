#!/usr/bin/env python3
import i3ipc
import subprocess


def on_window_focus(i3, e):
    # Get the geometry (rect) of the focused container
    rect = e.container.rect

    # Calculate the absolute center on the screen
    center_x = rect.x + (rect.width / 2)
    center_y = rect.y + (rect.height / 2)

    # Move the mouse using absolute screen coordinates
    subprocess.run(['xdotool', 'mousemove', str(
        int(center_x)), str(int(center_y))])

    window_id = e.container.window
    print(f"center_mouse.py: i3 focus changed to window_id: {window_id}")


i3 = i3ipc.Connection()
i3.on('window::focus', on_window_focus)
i3.main()
