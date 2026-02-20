#!/bin/bash
# ============================================================
# Auto Company — Install/Uninstall Daemon (macOS + Linux)
# ============================================================
# macOS: launchd plist in ~/Library/LaunchAgents/
# Linux: systemd user service in ~/.config/systemd/user/
#
# Usage:
#   ./install-daemon.sh             # Install and start
#   ./install-daemon.sh --uninstall # Stop and remove
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.autocompany.loop"
SERVICE_NAME="autocompany-loop"
PAUSE_FLAG="${SCRIPT_DIR}/.auto-loop-paused"

detect_platform() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux"* ]]; then
        echo "linux"
    else
        echo "unsupported"
    fi
}

PLATFORM=$(detect_platform)

# --- macOS (launchd) ---

macos_uninstall() {
    PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
    echo "Uninstalling Auto Company daemon (macOS launchd)..."
    if launchctl list | grep -q "$LABEL"; then
        launchctl unload "$PLIST_PATH" 2>/dev/null || true
        echo "Service unloaded."
    fi
    if [ -f "$PLIST_PATH" ]; then
        rm -f "$PLIST_PATH"
        echo "Plist removed: $PLIST_PATH"
    fi
    echo "Done. Daemon uninstalled."
}

macos_install() {
    PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"

    if ! command -v claude &>/dev/null; then
        echo "Error: 'claude' CLI not found. Install Claude Code first."
        exit 1
    fi

    CLAUDE_PATH="$(command -v claude)"
    CLAUDE_DIR="$(dirname "$CLAUDE_PATH")"
    NODE_DIR=""
    if command -v node &>/dev/null; then
        NODE_DIR="$(dirname "$(command -v node)")"
    fi

    DAEMON_PATH="${CLAUDE_DIR}"
    [ -n "$NODE_DIR" ] && DAEMON_PATH="${DAEMON_PATH}:${NODE_DIR}"
    DAEMON_PATH="${DAEMON_PATH}:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

    echo "Installing Auto Company daemon (macOS launchd)..."
    echo "  Project: $SCRIPT_DIR"
    echo "  Claude:  $CLAUDE_PATH"
    echo "  PATH:    $DAEMON_PATH"

    mkdir -p "$HOME/Library/LaunchAgents" "$SCRIPT_DIR/logs"
    rm -f "$PAUSE_FLAG"

    if launchctl list 2>/dev/null | grep -q "$LABEL"; then
        launchctl unload "$PLIST_PATH" 2>/dev/null || true
    fi

    cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${SCRIPT_DIR}/auto-loop.sh</string>
        <string>--daemon</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>

    <key>KeepAlive</key>
    <dict>
        <key>PathState</key>
        <dict>
            <key>${PAUSE_FLAG}</key>
            <false/>
        </dict>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>${SCRIPT_DIR}/logs/launchd-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>${SCRIPT_DIR}/logs/launchd-stderr.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>${DAEMON_PATH}</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>

    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
EOF

    echo "Plist written: $PLIST_PATH"
    launchctl load "$PLIST_PATH"
    echo ""
    echo "Daemon installed and started!"
}

# --- Linux (systemd) ---

linux_uninstall() {
    UNIT_PATH="$HOME/.config/systemd/user/${SERVICE_NAME}.service"
    echo "Uninstalling Auto Company daemon (Linux systemd)..."
    systemctl --user stop "$SERVICE_NAME" 2>/dev/null || true
    systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true
    if [ -f "$UNIT_PATH" ]; then
        rm -f "$UNIT_PATH"
        echo "Unit file removed: $UNIT_PATH"
    fi
    systemctl --user daemon-reload
    echo "Done. Daemon uninstalled."
}

linux_install() {
    UNIT_DIR="$HOME/.config/systemd/user"
    UNIT_PATH="${UNIT_DIR}/${SERVICE_NAME}.service"

    if ! command -v claude &>/dev/null; then
        echo "Error: 'claude' CLI not found. Install Claude Code first."
        exit 1
    fi

    CLAUDE_PATH="$(command -v claude)"
    CLAUDE_DIR="$(dirname "$CLAUDE_PATH")"
    NODE_DIR=""
    if command -v node &>/dev/null; then
        NODE_DIR="$(dirname "$(command -v node)")"
    fi

    DAEMON_PATH="${CLAUDE_DIR}"
    [ -n "$NODE_DIR" ] && DAEMON_PATH="${DAEMON_PATH}:${NODE_DIR}"
    DAEMON_PATH="${DAEMON_PATH}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

    echo "Installing Auto Company daemon (Linux systemd)..."
    echo "  Project: $SCRIPT_DIR"
    echo "  Claude:  $CLAUDE_PATH"
    echo "  PATH:    $DAEMON_PATH"

    mkdir -p "$UNIT_DIR" "$SCRIPT_DIR/logs"
    rm -f "$PAUSE_FLAG"

    cat > "$UNIT_PATH" << EOF
[Unit]
Description=Auto Company — Autonomous AI Loop
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${SCRIPT_DIR}
ExecStart=/bin/bash ${SCRIPT_DIR}/auto-loop.sh --daemon
Environment="PATH=${DAEMON_PATH}"
Environment="HOME=${HOME}"
Restart=on-failure
RestartSec=30
StandardOutput=append:${SCRIPT_DIR}/logs/systemd-stdout.log
StandardError=append:${SCRIPT_DIR}/logs/systemd-stderr.log

[Install]
WantedBy=default.target
EOF

    echo "Unit file written: $UNIT_PATH"

    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME"
    systemctl --user start "$SERVICE_NAME"

    echo ""
    echo "Daemon installed and started!"
    echo ""
    echo "Commands:"
    echo "  ./monitor.sh                       # Watch live logs"
    echo "  ./monitor.sh --status              # Check status"
    echo "  ./stop-loop.sh                     # Stop the loop (daemon will restart it)"
    echo "  ./stop-loop.sh --pause-daemon      # Pause daemon (no auto-restart)"
    echo "  ./stop-loop.sh --resume-daemon     # Resume daemon"
    echo "  ./install-daemon.sh --uninstall    # Remove daemon completely"
    echo "  systemctl --user status $SERVICE_NAME  # systemd status"
}

# --- Main ---

if [ "$PLATFORM" = "unsupported" ]; then
    echo "Error: Unsupported platform ($OSTYPE). Only macOS and Linux are supported."
    exit 1
fi

if [ "${1:-}" = "--uninstall" ]; then
    if [ "$PLATFORM" = "macos" ]; then
        macos_uninstall
    else
        linux_uninstall
    fi
else
    if [ "$PLATFORM" = "macos" ]; then
        macos_install
    else
        linux_install
    fi
fi
