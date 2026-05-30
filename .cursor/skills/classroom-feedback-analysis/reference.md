# Feedback parsing reference

## Slack search query templates

```
from:Classroom Feedbacks "Feedback Report" in:D0A8QEGSL3Y
from:Classroom Feedbacks "Feedback Report" "SST DA 101"
from:Classroom Feedbacks after:2026-05-01
```

## Fields to extract (regex-friendly)

| Field | Pattern |
|-------|---------|
| Class date | `class conducted on (\d+)(st\|nd\|rd\|th) (\w+), (\d{4})` |
| Batchset | `\*Batchset\*: (.+)` |
| Module | `\*Module Name\*: (.+)` |
| Topic | `\*Class Topic\*: (.+)` |
| Rating | `\*Class Rating\*: \`([\d.]+)\`` |
| Total rated | `\*Total Learners Rated\*: (\d+)` |
| Star N | `:star: N: \`(\d+)\`` |
| Top improvement | Highest count under `:wrench:` section |
| Top compliment | Highest count under `:speech_balloon:` section |
| Comments | Bullet lines after `Comments:` in thread `:v:` / `:wrench:` replies |

## Week ending date

Use **Sunday** of the week containing `class_date` for `week_ending` column.

## CSV columns

`week_ending, class_date, batchset, class_topic, class_rating, total_rated, star_1..star_5, top_improvement, top_compliment, slack_message_ts, permalink`

## Course filtering

Include only rows where `batchset` contains the `--batch-filter` string (case-insensitive).

## Dedup

Skip append if `slack_message_ts` already exists in CSV.
