import sys

import i3ipc


def get_i3_connection():
    try:
        return i3ipc.Connection()
    except Exception as e:
        print(f"Failed to connect to i3 IPC: {e}")
        sys.exit(1)


i3 = get_i3_connection()

def run_or_focus(command, class_name=None, instance=None, title=None):
    try:
        tree = i3.get_tree()
        windows = tree.leaves()
        
        target = None
        for w in windows:
            match = True
            if class_name and w.window_class != class_name: match = False
            if instance and w.window_instance != instance: match = False
            if title and (not w.name or title not in w.name): match = False
            
            if match:
                target = w
                break

        if target:
            target.command('focus')
        else:
            i3.command(f'exec --no-startup-id {command}')
    except Exception as e:
        print(f"Error executing i3 command: {e}")
