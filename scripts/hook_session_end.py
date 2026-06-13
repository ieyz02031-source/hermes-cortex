#!/usr/bin/env python3
"""Hermes Brain - Session End Hook (Python wrapper)"""
import subprocess
import sys
import os

PYTHON = r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe"
SCRIPT_DIR = r"D:\Hermes\skills\hermes-cortex\scripts"

for script in ["hot_cache.py", "maintain.py"]:
    script_path = os.path.join(SCRIPT_DIR, script)
    try:
        subprocess.run(
            [PYTHON, script_path],
            capture_output=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
    except Exception:
        pass

sys.exit(0)
