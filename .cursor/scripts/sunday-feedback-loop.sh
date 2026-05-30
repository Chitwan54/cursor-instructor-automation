#!/usr/bin/env bash
# Sleep until next Sunday 09:00 IST, then queue Sunday feedback tick. Repeats weekly.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT='Run classroom-feedback-analysis skill: fetch new Classroom Feedbacks from Slack for SST DA 101, update data/classroom_ratings.csv, produce Weekly Feedback summary with WoW trends, and send the full report as a Slack DM to U07KUJ3N5J7. Do not ask for confirmation.'

seconds_until_next_sunday_9am_ist() {
  python3 - <<'PY'
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ist = ZoneInfo("Asia/Kolkata")
now = datetime.now(ist)
days_ahead = (6 - now.weekday()) % 7  # Sunday = 6
target = (now + timedelta(days=days_ahead)).replace(
    hour=9, minute=0, second=0, microsecond=0
)
if target <= now:
    target += timedelta(days=7)
print(int((target - now).total_seconds()))
PY
}

while true; do
  secs=$(seconds_until_next_sunday_9am_ist)
  echo "Sunday feedback loop: sleeping ${secs}s until next Sunday 09:00 IST..."
  sleep "$secs"
  bash "${SCRIPT_DIR}/emit-automation-tick.sh" "sunday_feedback" "${PROMPT}"
done
