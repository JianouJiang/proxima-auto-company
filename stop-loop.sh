#!/bin/bash
# ============================================================
# Auto Company — Stop Loop (macOS + Linux)
# ============================================================
# Gracefully stops the auto-loop process.
# Can also pause/resume daemon mode (launchd or systemd).
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
PID_FILE="$PROJECT_DIR/.auto-loop.pid"
PAUSE_FLAG="$PROJECT_DIR/.auto-loop-paused"

# Platform detection
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    LABEL="com.autocompany.loop"
    PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
else
    PLATFORM="linux"
    SERVICE_NAME="autocompany-loop"
fi

stop_loop_process() {
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
}

pause_daemon() {
    touch "$PAUSE_FLAG"
    echo "Pause flag created: $PAUSE_FLAG"
    stop_loop_process

    if [ "$PLATFORM" = "macos" ]; then
        if launchctl list 2>/dev/null | grep -q "$LABEL"; then
            launchctl unload "$PLIST_PATH" 2>/dev/null || true
            echo "Daemon unloaded (launchd)."
        fi
    else
        systemctl --user stop "$SERVICE_NAME" 2>/dev/null || true
        echo "Daemon stopped (systemd)."
    fi
    echo "Daemon paused. Resume with: ./stop-loop.sh --resume-daemon"
}

resume_daemon() {
    rm -f "$PAUSE_FLAG"
    echo "Pause flag removed."

    if [ "$PLATFORM" = "macos" ]; then
        if [ ! -f "$PLIST_PATH" ]; then
            echo "LaunchAgent plist not found: $PLIST_PATH"
            echo "Install daemon first: ./install-daemon.sh"
            exit 1
        fi
        if launchctl list 2>/dev/null | grep -q "$LABEL"; then
            launchctl unload "$PLIST_PATH" 2>/dev/null || true
        fi
        launchctl load "$PLIST_PATH"
        echo "Daemon resumed and started (launchd)."
    else
        systemctl --user start "$SERVICE_NAME"
        echo "Daemon resumed and started (systemd)."
    fi
}

case "${1:-}" in
    --pause-daemon)
        pause_daemon
        ;;
    --resume-daemon)
        resume_daemon
        ;;
    --help|-h)
        echo "Usage:"
        echo "  ./stop-loop.sh                 # Stop current loop process"
        echo "  ./stop-loop.sh --pause-daemon  # Pause daemon and stop loop"
        echo "  ./stop-loop.sh --resume-daemon # Resume daemon"
        ;;
    *)
        stop_loop_process
        ;;
esac
