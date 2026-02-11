#!/bin/bash
# ============================================================
# Auto Company — Stop Loop
# ============================================================
# Gracefully stops the auto-loop process.
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
PID_FILE="$PROJECT_DIR/.auto-loop.pid"

# Method 1: Signal file (graceful, waits for current cycle to finish)
touch "$PROJECT_DIR/.auto-loop-stop"
echo "Stop signal sent. Loop will stop after current cycle completes."

# Method 2: Also send SIGTERM if PID file exists
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo "Sending SIGTERM to PID $pid..."
        kill -TERM "$pid"
    else
        echo "Process $pid not running. Cleaning up PID file."
        rm -f "$PID_FILE"
    fi
else
    echo "No PID file found."
fi
