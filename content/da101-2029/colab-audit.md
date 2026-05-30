# Content Audit — DA101 Term 4 (Batch 2029) — 2026-05-30

**Source:** Internal syllabus export (`1imxzP8mIFM0TtgvYOOkcf0uSrzuomhEyrQQUSv3AYWo`, gid `2103434812`)  
**Cross-ref:** `data/classroom_ratings.csv`, `DA101_assignments_mapping.csv`, `colab_quiz_copy_links.csv`

---

## Summary

| Metric | Count |
|--------|-------|
| Total sessions | 14 |
| Sessions with Colab (library) | 4 (S3, S4, S9, S10) |
| Colab links in internal syllabus | 3 (S3, S4, S10) — **S9 URL missing** |
| Original Colab links checked (GET) | 4 — **all OK** |
| Instructor quiz copies (v2 Drive) | 4 — **all OK** |
| Sessions missing Colab | 10 |
| In-class quiz in notebooks | 4 / 4 Colab sessions (S3–S4, S9–S10) |
| Syllabus quiz column (E) populated | 0 / 14 |
| Assignment IDs mapped | 11 sessions (S2–S12) |

---

## Broken / needs attention

| Session | Colab | Issue | Fix |
|---------|-------|-------|-----|
| **S9** | Aerofit | Internal syllabus col D has **text label only** — no Colab URL | Paste `https://colab.research.google.com/drive/1RrQTf72i2qETVkSMrT1UjpXZ1G38V2Y8` back into internal sheet |
| Public syllabus | — | **No Class Material / Colab column** on student-facing sheet | Confirm learners get Colab via LMS, Slack, or instructor share |
| S2, S5–S8, S11–S12 | Missing | No Colab in internal syllabus despite hands-on topics | Add notebooks or confirm slides-only delivery is intentional |
| S8 | Missing | FE content may live in Google Doc, not Colab | Verify doc access if slides-only |
| Internal syllabus col G | — | Assignment links **not pasted** (view-only blocker) | Paste from `DA101_assignments_mapping.csv` when Editor access granted |
| S4 syllabus cell | Duplicate | Same Colab URL appears twice in col D | Cosmetic cleanup on internal sheet |
| Audit script | HEAD check | `audit_colab_links.py` marks Colab as `needs_fix` (HTTP 405 on HEAD) | Use GET or manual verify; links are reachable |

---

## Colab inventory

### Syllabus originals (view-only, all OK)

| Session | Notebook | Status |
|---------|----------|--------|
| 3 | [Pandas — Data Loading & Cleaning](https://colab.research.google.com/drive/1-VqqSRfiHq_kVv61CgtkQMALsJ45pwu2) | ok |
| 4 | [Pandas — Transformation & Cleaning](https://colab.research.google.com/drive/1hRTaHy3POrA-BkcN43fasbdm2RyZNQIA) | ok |
| 9 | [Aerofit — Descriptive Stats & Probability](https://colab.research.google.com/drive/1RrQTf72i2qETVkSMrT1UjpXZ1G38V2Y8) | ok (missing from syllabus export) |
| 10 | [Walmart — CLT & Confidence Intervals](https://colab.research.google.com/drive/1Eq2cmrOsza2-s0gUmFNevzUpe4G_5X-S) | ok |

### Instructor quiz copies (v2, editable — use in class)

| Session | Notebook | Status |
|---------|----------|--------|
| 3 | [DA101 S3 Pandas-3 (with quizzes)](https://colab.research.google.com/drive/10vo77UjoxNMqB4a4eryD0IRpsNpWKkBJ) | ok |
| 4 | [DA101 S4 Pandas-4 notes (with quizzes)](https://colab.research.google.com/drive/17Dz9S5bvlRJwkY0iK-irZ1XX7He7KFnB) | ok |
| 9 | [DA101 S9 Aerofit (with quizzes)](https://colab.research.google.com/drive/1BNhxU2PpofkxYrw0VQZDsKllo1uWPbLh) | ok |
| 10 | [DA101 S10 Walmart CLT (with quizzes)](https://colab.research.google.com/drive/1xOn53DRuPwrL-HfzFzBEjb56cfgCfFHX) | ok |

**Stale v1 quiz copies** (safe to delete): S3 `16AFtH1dtAkRInjMrbHMcR99na60oMyb7`, S4 `1JVJclqM_9rA0b2zDr9LTLPBRDM6-o4Mx`, S9 `1IDM7V70P5lcMAhQ6TC0AXaZA-2uZ8TJM`, S10 `1E-U3er_uoJEnRNCoE5oFiZrZ67v5IxeT`

---

## Elaboration opportunities

| Session | Feedback / signal | Suggestion |
|---------|-------------------|------------|
| **3** | Pace of Teaching (28%) on May 14 repeat; avg 4.57 | Add review vs new markers; trim repeated intro cells; opening quiz already injected |
| **2** | Pace + communication on NumPy (May 9); avg ~4.5 | Lightweight NumPy practice notebook or follow-along cells; highlight 5 must-do assignments in class |
| **5–6** | No feedback yet | Data Viz lacks Colab — consider shared gaming-dataset notebook |
| **7** | No feedback yet | Dense topic, 18 assignments — add in-class “interpret this histogram” exercises |
| **9** | No feedback yet | Strong assignment count (46) — ensure Colab sections map to assignment topics |
| **11–12** | Test-set IDs only | Clarify platform test workflow; optional LR/Logistic practice notebook |

---

## Quiz gaps / quiz status

| Session | Status | Notes |
|---------|--------|-------|
| **3** | In notebook + v2 Drive | Opening + IMDB merge follow-up |
| **4** | In notebook + v2 Drive | Opening after `## Content` + drug pivot follow-up |
| **9** | In notebook + v2 Drive | Generic opening Q4 + Aerofit variance follow-up |
| **10** | In notebook + v2 Drive | Opening only; hypothetical Q4 |
| **2, 5–8, 11–14** | Not in Colab | Syllabus col E empty — draft prompts below if adding slides-only checks |

### Suggested quick checks (sessions without Colab quizzes)

| Session | Suggested quick checks |
|---------|------------------------|
| **2** NumPy | (1) `arr.shape`? (2) array vs matrix multiply. (3) Predict `[1,2]+[3,4]`. (4) Discuss: NumPy vs plain lists. |
| **5** Data Viz 1 | (1) Bar vs histogram. (2) `fig, ax = plt.subplots()`. (3) Identify chart type. (4) Gaming KPI first. |
| **6** Data Viz 2 | (1) Subplot layout. (2) Color readability. (3) Misleading axis. (4) Dual-axis insight. |
| **7** Probability | (1) PDF vs CDF. (2) Mean vs median skew. (3) Distribution for cricket scores. (4) Sachin case question. |
| **8** Feature Engineering | (1) One-hot vs label. (2) Train/test split why. (3) Leakage spot. (4) Logistics raw → feature. |
| **11** Linear Regression | (1) R². (2) Residuals. (3) Coefficient sign. (4) Used car positive coef. |
| **12** Logistic Regression | (1) Sigmoid. (2) Threshold 0.5. (3) Precision vs recall. (4) Loan false approve cost. |
| **13–14** Business cases | Open discussion only |

---

## Optional follow-ups (confirm with user)

- [ ] Restore S9 Colab URL on internal syllabus col D
- [ ] Populate syllabus quiz column (E) for S2–S14 (draft prompts above)
- [ ] Paste assignment IDs to internal syllabus col G
- [ ] Trim S3 notebook intro / skip markers (pace feedback)
- [ ] Set sharing on v2 quiz Drive copies; delete stale v1 copies
- [ ] Add Colab gaps for S2, S5–S7 before next term

---

## Reuse notes (next cohort)

1. Export from **internal** syllabus — Colab links live in column D only there.
2. **S3 & S4** Pandas notebooks stable — reuse; quiz copies in `colab_quiz_copy_links.csv`.
3. **S9 & S10** stats notebooks validated — watch S9 syllabus cell for accidental URL removal.
4. Re-run `inject_colab_quizzes.py` after quiz edits; refresh Drive copies via gist workflow.
5. Assignment paste — reuse `DA101_assignments_mapping.csv`; update if tracker tabs change.
