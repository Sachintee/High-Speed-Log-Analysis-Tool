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

# 3. Install dependencies (SQLite is built-in, but this is good practice)
# We don't need external libraries for this specific mini-project, but we include pip
# to demonstrate dependency management.
# pip install pandas (Uncomment this if you want to use pandas for advanced analysis)

# 4. EXECUTION AND PERFORMANCE MONITORING
echo "-----------------------------------------------------"
echo " Running Log Analysis (Monitoring Execution Time) "
echo "-----------------------------------------------------"

# Use the 'time' command to measure the wall clock time, user time, and system time.
# This is a key deliverable for the HPC and Algorithms components.
time python3 "$PYTHON_SCRIPT"

# 5. Deactivate environment
deactivate
echo "-----------------------------------------------------"
echo "Script finished. Environment deactivated."
echo "====================================================="

# You can add more advanced Linux tasks here, like:
# - Checking CPU usage with 'top -n 1 -b' during execution
# - Configuring file permissions for the log file
