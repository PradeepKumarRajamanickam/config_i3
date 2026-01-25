#!/usr/bin/env python3
import sys
import i3ipc
import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Timer

# --- Logging Configuration ---
LOG_DIR = Path.home() / ".logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "run_or_focus.log"

handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_i3_connection():
    try:
        return i3ipc.Connection()
    except Exception as e:
        logger.error(f"Failed to connect to i3 IPC: {e}")
        sys.exit(1)

def wait_for_and_focus(class_name, instance, title):
    """Listens for a new window matching criteria and focuses it."""
    i3_event = get_i3_connection()

    def on_window_new(i3, event):
        w = event.container
        match = True
        if class_name and w.window_class != class_name: match = False
        if instance and w.window_instance != instance: match = False
        if title and (not w.name or title.lower() not in w.name.lower()): match = False
        
        if match:
            logger.info(f"New window detected: {w.name}. Focusing...")
            w.command('focus')
            i3.main_quit()

    i3_event.on('window::new', on_window_new)
    
    # Timeout after 10 seconds so the script doesn't hang if launch fails
    Timer(10, i3_event.main_quit).start()
    i3_event.main()

def run_or_focus(command, class_name=None, instance=None, title=None, role=None):
    i3 = get_i3_connection()
    tree = i3.get_tree()
    windows = tree.leaves()
    target = None

    # 1. Try to find existing window
    if class_name or instance or role or title:
        for w in windows:
            match = True
            if class_name and w.window_class != class_name: match = False
            if instance and w.window_instance != instance: match = False
            if role and w.window_role != role: match = False
            if title and (not w.name or title.lower() not in w.name.lower()): match = False
            
            if match:
                target = w
                break

    if target:
        logger.info(f"Focusing existing window: {target.name}")
        target.command('focus')
    else:
        # 2. Launch and wait for the new window to appear
        logger.info(f"Launching: {command}")
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # We don't need 'role' for detection usually as apps don't set it immediately,
        # so we match on class/instance/title which are set on creation.
        wait_for_and_focus(class_name, instance, title)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="i3wm Run-or-Focus Tool")
    parser.add_argument('command', help="Command to execute")
    parser.add_argument('-c','--class_name', help="Match by WM_CLASS")
    parser.add_argument('-i','--instance', help="Match by instance name")
    parser.add_argument('-r','--role', help="Match WM_WINDOW_ROLE")
    parser.add_argument('-t','--title', help="Match by substring in window title")

    args = parser.parse_args()
    run_or_focus(args.command, args.class_name, args.instance, args.title, args.role)
