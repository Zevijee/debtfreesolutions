#!/bin/bash

# Path to your Django project directory
PROJECT_DIR="/debtfreesolutions/FullRealEstateProject"

# Command to start Gunicorn
GUNICORN_CMD="gunicorn --bind 0.0.0.0:8000 --pid $PROJECT_DIR/gunicorn.pid FullRealEstateProject.wsgi:application"

# Log file for script activity
LOG_FILE="/path/to/your/logfile.log"

# Start Gunicorn
echo "Starting Gunicorn..."
$GUNICORN_CMD &

# Record the initial Gunicorn PID
PID=$(cat $PROJECT_DIR/gunicorn.pid)

# Monitor for changes and restart Gunicorn
while true; do
  # Check file changes (adjust if needed)
  CHANGES=$(inotifywait -r -e modify,move,create,delete -q $PROJECT_DIR/*.py)

  # If changes detected, restart Gunicorn and log details
  if [[ -n "$CHANGES" ]]; then
    # Log change detection timestamp (adjust format/location as needed)
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Changes detected in project files." >> $LOG_FILE

    echo "Changes detected, restarting Gunicorn..."
    kill -SIGINT $PID
    sleep 1
    PID=$(cat $PROJECT_DIR/gunicorn.pid)

    # Log Gunicorn restart timestamp (adjust format/location as needed)
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Gunicorn restarted with PID $PID." >> $LOG_FILE
  fi
done
