---
name: classroom-feedback-analysis
description: >-
  Parses Classroom Feedbacks Slack DM reports, tracks class ratings in CSV,
  analyzes weekly feedback with week-on-week rating trends, and surfaces
  improvement themes. Use when the user asks for lecture feedback analysis,
  rating trends, weekly feedback review, or Sunday classroom feedback digest.
---

# Classroom Feedback Analysis

Analyze **Classroom Feedbacks** bot reports from Slack and track ratings over time.

## Config

- **Feedback DM:** `D0A8QEGSL3Y` ([link](https://scalerinternal.slack.com/archives/D0A8QEGSL3Y))
- **Ratings CSV:** `data/classroom_ratings.csv`
- **Batch filter:** `SST DA 101` in `config/instructor-automation.yaml` (change per course)

Reports arrive **~Sunday** after each week's classes.

## Workflow

```
- [ ] 1. Fetch new feedback from Slack (search > read_thread)
- [ ] 2. Parse reports + thread comments
- [ ] 3. Append to classroom_ratings.csv (dedupe by slack_message_ts)
- [ ] 4. Analyze current week + WoW trends
- [ ] 5. **Send Slack DM** to instructor (required for scheduled runs)

## Automated Sunday run

Triggered by `.cursor/scripts/sunday-feedback-loop.sh` every **Sunday 09:00 IST**.

On each run, **always** send the full Weekly Feedback summary to `config/instructor-automation.yaml` → `schedules.weekly_feedback_analysis.dm_user_id` via `slack_send_message`. Do not wait for user confirmation.

**Scheduled prompt payload:**
> Run classroom-feedback-analysis skill: fetch new Classroom Feedbacks from Slack for SST DA 101, update data/classroom_ratings.csv, produce Weekly Feedback summary with WoW trends, and send the full report as a Slack DM to U07KUJ3N5J7.

To arm: user runs `/loop` equivalent — agent starts `sunday-feedback-loop.sh` in background.

To stop: kill the sunday-feedback loop PID when user asks.
```

### Step 1: Fetch feedback

**Use Slack search** (parent message text includes ratings; `read_thread` alone may miss it):

```
slack_search_public_and_private:
  query: "from:Classroom Feedbacks Feedback Report in:D0A8QEGSL3Y {batch_filter}"
  limit: 20
```

For each result, also `slack_read_thread` on `message_ts` for free-text comments (`:v:` and `:wrench:` replies).

Filter to **current course** via `batchset` (e.g. `SST DA 101 2029 Group A`).

### Step 2: Parse

Run parser on saved search text or pipe messages:

```bash
python .cursor/skills/classroom-feedback-analysis/scripts/parse_feedback.py \
  --input /tmp/feedback_raw.txt \
  --batch-filter "SST DA 101" \
  --output /tmp/parsed_feedback.json
```

Append to CSV:

```bash
python .cursor/skills/classroom-feedback-analysis/scripts/parse_feedback.py \
  --input /tmp/feedback_raw.txt \
  --batch-filter "SST DA 101" \
  --append-csv data/classroom_ratings.csv
```

### Step 3: Analysis output

```markdown
## Weekly Feedback — Week ending {date}

### This week's classes
| Date | Batch | Topic | Rating | Δ vs prev | Rated |
|------|-------|-------|--------|-----------|-------|

### Week-on-week (course average)
- Current week avg: X.XX (n classes)
- Previous week avg: Y.YY → **+/-Z.ZZ**

### Rating trend (last 8 classes)
{simple ASCII sparkline or table}

### Top improvement themes
1. Pace of Teaching (count)
2. ...

### Top compliments
1. ...

### Verbatim comments worth acting on
- ...

### Recommended actions for next week
1. ...
```

**WoW rules:**
- Compare **course-filtered** classes only (don't mix DSML with DA101)
- `Δ vs prev` = same batch's previous class, or N/A if first
- Flag rating drop ≥ 0.3 or any 1-star votes

## Feedback message schema

Parent message contains:
- Class date, batchset, module, topic
- `Class Rating`, star distribution (1–5)
- Improvement / compliment category counts
- Thread replies: learner free-text under `:v:` and `:wrench:`

See [reference.md](reference.md) for regex patterns.
