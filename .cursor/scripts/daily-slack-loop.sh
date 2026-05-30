#!/usr/bin/env bash
# Sleep until next 09:00 IST, then queue daily Slack review tick. Repeats daily.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT='Run daily Slack review skill: scan instructor Slack channels, summarize action items, and send a digest DM to U07KUJ3N5J7. Do not ask for confirmation.'

seconds_until_next_9am_ist() {
  python3 - <<'PY'
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ist = ZoneInfo("Asia/Kolkata")
now = datetime.now(ist)
target = now.replace(hour=9, minute=0, second=0, microsecond=0)
if target <= now:
    target += timedelta(days=1)
print(int((target - now).total_seconds()))
PY
}

export TICK_NAME="daily_slack_review"
export PROMPT
export QUEUE="${HOME}/Library/Application Support/instructor-automation/pending-ticks.jsonl"

while true; do
  secs=$(seconds_until_next_9am_ist)
  echo "Daily Slack loop: sleeping ${secs}s until next 09:00 IST..."
  sleep "$secs"
  TICK_NAME="${TICK_NAME}" PROMPT="${PROMPT}" QUEUE="${QUEUE}" \
    bash "${SCRIPT_DIR}/emit-automation-tick.sh" "${TICK_NAME}" "${PROMPT}"
done
