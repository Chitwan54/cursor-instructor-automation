---
name: cohort-assignment-pipeline
description: >-
  End-to-end cohort assignment workflow — syllabus + assignment trackers in,
  session→ID mapping CSV and syllabus paste out. Wraps map-session-assignments
  for any cohort (DA, ML, DL). Use when setting up assignments for a new
  cohort, term, or course section.
---

# Cohort Assignment Pipeline

Orchestrates the full assignment mapping workflow for **any cohort**.

## Quick start

```
Inputs:
  1. Syllabus sheet URL (internal)
  2. Assignment tracker URL(s)

Say: "Run cohort assignment pipeline for {course name}"
```

## Pipeline steps

```
- [ ] 1. Create/update cohort config (config/cohorts/{slug}.yaml)
- [ ] 2. Run map-session-assignments skill (read .cursor/skills/map-session-assignments/SKILL.md)
- [ ] 3. Output: {slug}_assignments_mapping.csv + paste_ids.tsv
- [ ] 4. Optional: paste column G on internal syllabus (Editor access required)
- [ ] 5. Optional: reply in course Slack thread
```

## Cohort config template

Create `config/cohorts/da101-2029.yaml`:

```yaml
slug: da101-2029
course_name: Data Analytics 101 — Term 4
syllabus:
  sheet_id: 1imxzP8mIFM0TtgvYOOkcf0uSrzuomhEyrQQUSv3AYWo
  gid: "2103434812"
assignment_sources:
  - name: Python/DAV-1
    sheet_id: 117UG9MLArvQ3c8RA8UDOLEXRGGBlDTM3u3dfyLXi-WU
    tabs: [NumPy assessments, Pandas assessments, Data Viz assessments]
  - name: DAV-2 Stats
    sheet_id: 1GB88Ddqh35BlXus1VNvn4SjfhLC2NHoYVlHrWMzSmvQ
    tabs: [Assessments]
mapping_notes:
  skip_sessions: [1]
  combine_homework: true
  syllabus_paste_column: G
```

## Per-cohort checklist

- [ ] Syllabus sessions aligned with lecture plan
- [ ] All assignment source tabs identified
- [ ] User confirmed lecture→session splits
- [ ] Exclusions applied (red / not in use)
- [ ] Test-set IDs flagged (ML topics)
- [ ] Internal syllabus updated OR blocker documented
- [ ] Course thread updated

## Related skills

- **Core extraction:** [map-session-assignments](../map-session-assignments/SKILL.md)
- **Example:** [map-session-assignments/examples.md](../map-session-assignments/examples.md)
