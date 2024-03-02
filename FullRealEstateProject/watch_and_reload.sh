#!/bin/bash

PROJECT_DIR="/debtfreesolutions/FullRealEstateProject"
PIDFILE="$PROJECT_DIR/gunicorn.pid"
LOGFILE="$PROJECT_DIR/watcher_debug.log"

echo "Watcher script started. Monitoring for changes..." | tee -a $LOGFILE

inotifywait -m -e close_write -r --format "%w%f" "$PROJECT_DIR" | while read file; do
  if [[ "$file" == *.py ]]; then
    echo "$(date): Detected change in $file" | tee -a $LOGFILE
    if [ -f "$PIDFILE" ]; then
      echo "$(date): Reloading Gunicorn..." | tee -a $LOGFILE
      kill -HUP $(cat "$PIDFILE")
      echo "$(date): Gunicorn reloaded successfully." | tee -a $LOGFILE
    else
      echo "$(date): PID file not found. Is Gunicorn running?" | tee -a $LOGFILE
    fi
  fi
done
