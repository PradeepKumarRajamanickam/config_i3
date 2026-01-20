import i3ipc
from pynput import keyboard
import subprocess

i3 = i3ipc.Connection()

def run_or_focus(criteria, launch_cmd):
    """
    Focuses a window matching the i3 criteria. 
    If not found, executes the launch_cmd.
    """
    tree = i3.get_tree()
    # Find containers matching the criteria (e.g., class="Nemo")
    # i3ipc allows querying by window_class, window_instance, window_role, etc.
    windows = tree.find_classed(criteria) if "class" in criteria else []
    
    # Generic fallback: manual search if complex criteria like 'instance' or 'role' are used
    if not windows:
        for leaf in tree.leaves():
            if all(getattr(leaf, key, None) == val for key, val in criteria.items()):
                windows.append(leaf)

    if windows:
        windows[0].command('focus')
    else:
        i3.command(f'exec --no-startup-id {launch_cmd}')

# Define your actions
def focus_nemo():
    run_or_focus({'window_class': 'Nemo'}, 'nemo')

def focus_browser():
    # Example for browser using window_role
    run_or_focus({'window_role': 'browser'}, 'google-chrome-stable')

def focus_godot(title=None):
    criteria = {'window_class': 'Godot', 'window_instance': 'Godot_Editor'}
    if title:
        criteria['name'] = title # 'name' in i3ipc refers to the window title
    run_or_focus(criteria, 'godot')

# Global Hotkey Mapping (Super+Alt+Key)
# Note: <cmd> or <win> is used for 'Super' key in pynput
with keyboard.GlobalHotKeys({
    '<cmd>+<alt>+n': focus_nemo,
    '<cmd>+<alt>+b': focus_browser,
    '<cmd>+<alt>+1': lambda: focus_godot(),
    '<cmd>+<alt>+2': lambda: focus_godot("Script Editor - Godot Engine"),
    '<cmd>+<alt>+3': lambda: focus_godot("Inspector - Godot Engine"),
    '<cmd>+<alt>+4': lambda: focus_godot("Import - Godot Engine"),
    '<cmd>+<alt>+5': lambda: focus_godot("FileSystem - Godot Engine"),
    '<cmd>+<alt>+6': lambda: focus_godot("Node - Godot Engine"),
    '<cmd>+<alt>+7': lambda: focus_godot("Scene - Godot Engine"),
}) as h:
    h.join()
