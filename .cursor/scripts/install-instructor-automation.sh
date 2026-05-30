#!/usr/bin/env bash
# Install launchd-managed instructor automation (run after cloning or updating scripts).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INSTALL_DIR="${HOME}/Library/Application Support/instructor-automation/scripts"
LAUNCH_AGENTS="${HOME}/Library/LaunchAgents"
LABEL="com.chitwan.instructor-automation"

mkdir -p "${INSTALL_DIR}" "${HOME}/Library/Logs/instructor-automation"

for script in emit-automation-tick.sh daily-slack-loop.sh sunday-feedback-loop.sh start-instructor-loops.sh stop-instructor-loops.sh; do
  python3 - "$REPO/.cursor/scripts/$script" "$INSTALL_DIR/$script" <<'PY'
import sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
data = src.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")
install = str(dst.parent)
data = data.replace(
    'REPO="/Users/chitwan/Desktop/Scaler/Data Analytics 101"',
    f'SCRIPT_ROOT="{install}"',
)
data = data.replace(
    "${REPO}/.cursor/scripts/",
    f"{install}/",
)
data = data.replace(
    'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"',
    f'SCRIPT_DIR="{install}"',
)
dst.write_text(data)
dst.chmod(0o755)
print("installed", dst)
PY
done

cat > "${LAUNCH_AGENTS}/${LABEL}.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${INSTALL_DIR}/start-instructor-loops.sh</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${HOME}/Library/Logs/instructor-automation/launchd.log</string>
  <key>StandardErrorPath</key>
  <string>${HOME}/Library/Logs/instructor-automation/launchd.err.log</string>
</dict>
</plist>
PLIST

# Stop any repo-path loops still running
bash "${REPO}/.cursor/scripts/stop-instructor-loops.sh" 2>/dev/null || true
pkill -f "daily-slack-loop.sh" 2>/dev/null || true
pkill -f "sunday-feedback-loop.sh" 2>/dev/null || true

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "${LAUNCH_AGENTS}/${LABEL}.plist"
echo "LaunchAgent ${LABEL} loaded."

bash "${INSTALL_DIR}/start-instructor-loops.sh"
