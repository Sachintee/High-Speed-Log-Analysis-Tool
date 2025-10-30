#!/bin/bash

# --- LINUX ADMINISTRATION LAB: AUTOMATION AND MONITORING ---

PROJECT_DIR=$(dirname "$0")
PYTHON_SCRIPT="log_analyzer.py"
VENV_DIR="venv"

echo "====================================================="
echo " High-Speed Log File Analysis Tool Setup & Execution "
echo "====================================================="

# 1. Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found. Please install Python 3."
    exit 1
fi

# 2. Setup/Activate Python Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

# 3. Install dependencies (None needed, but shown for dependency management)

# 4. EXECUTION AND PERFORMANCE MONITORING
echo "-----------------------------------------------------"
echo " Running Log Analysis (Monitoring Execution Time) "
echo "-----------------------------------------------------"

# Use the 'time' command to measure the system time (Linux Administration)
time python3 "$PYTHON_SCRIPT"

# 5. Deactivate environment
deactivate
echo "-----------------------------------------------------"
echo "Script finished. Environment deactivated."
echo "====================================================="
