#!/usr/bin/env python3
import sys
import i3ipc
import argparse
import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# --- Logging Configuration ---
LOG_DIR = Path.home() / ".logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "run_or_focus.log"

# Configure rotating logger: 1MB per file, max 5 backups
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

def run_with_properties(command, role=None):
    logger.info(f"Launching new instance: {command}")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if role:
        time.sleep(0.7)
        try:
            subprocess.run([
                "xdotool", "search", "--sync", "--pid", str(proc.pid), 
                "set_window", "--role", role
            ], check=False, capture_output=True)
            logger.info(f"Set role '{role}' for PID {proc.pid}")
        except FileNotFoundError:
            logger.warning("xdotool not found; could not set window role.")

def run_or_focus(command, 
                 class_name=None, 
                 instance=None, 
                 title=None, 
                 role=None):
    logging.info(f"Run-or-Focus called with command: {command}, class_name: {class_name}, instance: {instance}, title: {title}, role: {role}")
    i3 = get_i3_connection()
    try:
        tree = i3.get_tree()
        windows = tree.leaves()
        target = None

        if class_name  or instance or role or title:
            logger.info("Searching for existing windows matching criteria...")
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
            logger.info(f"Focusing existing window: {target.name} | class: {target.window_class} (ID: {target.window})")
            target.command('focus')
        else:
            run_with_properties(command, role=role)
            
    except Exception as e:
        logger.exception("An unexpected error occurred during run_or_focus")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="i3wm Run-or-Focus Tool")
    parser.add_argument('command', help="Command to execute")
    parser.add_argument('-c','--class_name', help="Match by WM_CLASS")
    parser.add_argument('-i','--instance', help="Match by instance name")
    parser.add_argument('-r','--role', help="Match or set WM_WINDOW_ROLE")
    parser.add_argument('-t','--title', help="Match by substring in window title")

    args = parser.parse_args()
    run_or_focus(args.command, args.class_name, args.instance, args.title, args.role)
