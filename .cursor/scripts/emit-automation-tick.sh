#!/usr/bin/env bash
# Queue an automation tick and notify. Used by launchd-managed loop scripts.
set -euo pipefail

TICK_NAME="${1:?tick name required}"
PROMPT="${2:?prompt required}"

STATE_DIR="${HOME}/Library/Application Support/instructor-automation"
QUEUE="${STATE_DIR}/pending-ticks.jsonl"
mkdir -p "${STATE_DIR}"

export TICK_NAME PROMPT QUEUE
python3 - <<'PY'
import json, os, datetime

tick = os.environ["TICK_NAME"]
prompt = os.environ["PROMPT"]
queue = os.environ["QUEUE"]
record = {
    "tick": tick,
    "prompt": prompt,
    "queued_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}
with open(queue, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print(f"AGENT_LOOP_TICK_{tick} " + json.dumps({"prompt": prompt}))
PY

osascript -e "display notification \"${TICK_NAME} queued — Cursor will process when active\" with title \"Instructor Automation\"" 2>/dev/null || true
