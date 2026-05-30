# Example: Data Analytics 101 (Term 4)

## Inputs

| Input | URL / file |
|-------|------------|
| Internal syllabus | `1imxzP8mIFM0TtgvYOOkcf0uSrzuomhEyrQQUSv3AYWo` (gid `2103434812`) |
| Python/DAV-1 tracker | `117UG9MLArvQ3c8RA8UDOLEXRGGBlDTM3u3dfyLXi-WU` |
| DAV-2 stats tracker | `1GB88Ddqh35BlXus1VNvn4SjfhLC2NHoYVlHrWMzSmvQ` |
| Feature Engineering doc | `1WXDkyLmUomxOACFl7LnqLJ4Rpn_R6nOISoZZ81plFMs` |
| DSML Content Sheet (LR) | `1DMcEZGXUCmqSIx7krauAJcSKhCcqmeJ1sN_Ld7ZdanE` |

## User decisions

- Include assignments + homework (combined in one ID list)
- Move subplots problems (19255, 24026) from Session 5 → Session 6
- Leave Session 1 unchanged (prior semester)
- Exclude red / not-in-use problems
- Drop Problem Name column in final output
- Stats split: Session 7 (Lec 6,8,10,11), Session 9 (Lec 1–5), Session 10 (Lec 7,9)

## Mapping result

| Session | Source | IDs |
|---------|--------|-----|
| 2 | NumPy assessments (all lectures) | 49 |
| 3 | Pandas Lec 1–3 | 41 |
| 4 | Pandas Lec 4–5 | 19 |
| 5 | Data Viz Lec 1–2 (minus subplots) | 8 |
| 6 | Data Viz Lec 3 + subplots | 8 |
| 7 | DAV-2 Lec 6,8,10,11 | 19 |
| 8 | FE doc (FE-1 + FE-2) | 21 |
| 9 | DAV-2 Lec 1–5 | 46 |
| 10 | DAV-2 Lec 7,9 | 17 |
| 11 | DSML Intro to ML (LR rows) | 7 (test-set IDs) |
| 12 | DSML Intro to ML (Logistic rows) | 4 (test-set IDs) |
| 13–14 | — | N/A (business cases) |

## Extraction commands used

```bash
# Python/DAV-1
curl -sL "https://docs.google.com/spreadsheets/d/117UG9MLArvQ3c8RA8UDOLEXRGGBlDTM3u3dfyLXi-WU/export?format=xlsx" \
  -o ~/Downloads/Python-DAV-1-Tracker.xlsx
python .cursor/skills/map-session-assignments/scripts/extract_ids.py \
  --input ~/Downloads/Python-DAV-1-Tracker.xlsx

# DAV-2 stats
curl -sL "https://docs.google.com/spreadsheets/d/1GB88Ddqh35BlXus1VNvn4SjfhLC2NHoYVlHrWMzSmvQ/export?format=xlsx" \
  -o ~/Downloads/Assessment-mapping-DAV-2.xlsx
python .cursor/skills/map-session-assignments/scripts/extract_ids.py \
  --input ~/Downloads/Assessment-mapping-DAV-2.xlsx --tab Assessments

# Feature Engineering (docx export)
python .cursor/skills/map-session-assignments/scripts/extract_ids.py \
  --docx ~/Downloads/DAV-3-Assessments-and-Homework.docx
```

## Sample output row

```csv
Session Number,Session Details,Problem ID List
2,Data Analytics Using Numpy,"26957, 19028, 23116, ..."
```

## Syllabus paste

- Target: column G, rows 3–13
- Blocked: view-only access for instructor account → required Editor from Rahul
- Files prepared: `paste_ids.tsv`, `DA101_assignments_mapping.csv`

## Adapting for ML / DL courses

Same workflow; expect:

- More DSML Content Sheet tabs (`Intro to ML and NN`, supervised assessments)
- Test-set IDs more common for bundled assignments
- Multiple assignment source files (one per module)
- Syllabus may have fewer coding sessions and more case-study-only rows

Always present draft mapping with ID counts before finalizing.
