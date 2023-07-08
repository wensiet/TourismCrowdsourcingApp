#!/bin/bash

# Pull the latest changes from the Git repository
git pull

# Create and activate a new virtual environment
echo "Setting up venv..."
source deployment/bin/activate

# Install required Python packages
pip install -r requirements.txt

# Stop any running Uvicorn server process
PIDS=$(pgrep uvicorn)
if [ -n "$PIDS" ]; then
  echo "Uvicorn server is already running, stopping process with ID $PIDS"
  kill $PIDS
fi

# Start the Uvicorn server in the background and suppress output
nohup uvicorn API:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &

# Wait for the server to start
echo "Waiting for the server to start..."
sleep 5

# Check if the server is running
PIDS=$(pgrep uvicorn)
if [ -n "$PIDS" ]; then
  echo "Uvicorn server started successfully with process ID $PIDS"
else
  echo "Failed to start Uvicorn server"
  exit 1
fi
