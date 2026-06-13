#!/bin/bash
# Hermes Brain - Session Start Hook
PYTHON="/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe"
SCRIPT_DIR="D:/Hermes/skills/hermes-cortex/scripts"
$PYTHON "$SCRIPT_DIR/hot_cache.py" > /dev/null 2>&1
exit 0
