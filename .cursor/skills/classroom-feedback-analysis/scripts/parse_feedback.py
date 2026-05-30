#!/usr/bin/env python3
"""Parse Classroom Feedbacks Slack report text into structured records."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATE_RE = re.compile(
    r"class conducted on (\d+)(?:st|nd|rd|th) (\w+), (\d{4})",
    re.I,
)
RATING_RE = re.compile(r"\*Class Rating\*:\s*`([\d.]+)`")
RATED_RE = re.compile(r"\*Total Learners Rated\*:\s*(\d+)")
BATCH_RE = re.compile(r"\*Batchset\*:\s*(.+)")
TOPIC_RE = re.compile(r"\*Class Topic\*:\s*(.+)")
STAR_RE = re.compile(r":star:\s*(\d):\s*`(\d+)`")
MSG_TS_RE = re.compile(r"Message_ts:\s*([\d.]+)")
PERMALINK_RE = re.compile(r"Permalink:\s*\[link\]\(([^)]+)\)")

IMPROVE_CATS = [
    "Pace of Teaching",
    "Communication style and delivery",
    "Examples and problems discussed",
    "Doubt Resolution Section",
    "Other",
]
COMPLIMENT_CATS = [
    "Efficient Pace of Teaching",
    "Organized Structure of Content Delivery",
    "Smooth Doubt Resolution",
    "Illustrative Examples and Problems Discussed",
    "Other",
]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


def week_ending(d: datetime) -> str:
    """Sunday of the week containing d."""
    days_until_sunday = (6 - d.weekday()) % 7
    if d.weekday() == 6:
        return d.strftime("%Y-%m-%d")
    return (d + timedelta(days=days_until_sunday)).strftime("%Y-%m-%d")


def parse_date(m: re.Match) -> str:
    day, month_name, year = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    month = MONTHS.get(month_name[:3].lower() if month_name[:3].lower() in MONTHS else month_name.lower())
    if not month:
        for k, v in MONTHS.items():
            if month_name.lower().startswith(k[:3]):
                month = v
                break
    if not month:
        raise ValueError(f"Unknown month: {month_name}")
    return datetime(year, month, day).strftime("%Y-%m-%d")


def top_category(text: str, categories: list[str], section_marker: str) -> str:
    if section_marker not in text:
        return ""
    section = text.split(section_marker, 1)[1]
    if ":speech_balloon:" in section and section_marker == ":wrench:":
        section = section.split(":speech_balloon:")[0]
    if ":v:" in section and section_marker == ":wrench:":
        section = section.split(":v:")[0]
    best_name, best_count = "", -1
    for cat in categories:
        m = re.search(rf"{re.escape(cat)}:\s*`(\d+)`", section)
        if m:
            count = int(m.group(1))
            if count > best_count:
                best_count, best_name = count, cat
    return best_name


def parse_block(block: str) -> dict | None:
    if "Feedback Report" not in block:
        return None
    dm = DATE_RE.search(block)
    rm = RATING_RE.search(block)
    if not dm or not rm:
        return None

    class_date = parse_date(dm)
    stars = {i: 0 for i in range(1, 6)}
    for sm in STAR_RE.finditer(block):
        stars[int(sm.group(1))] = int(sm.group(2))

    batch = BATCH_RE.search(block)
    topic = TOPIC_RE.search(block)
    rated = RATED_RE.search(block)
    ts = MSG_TS_RE.search(block)
    link = PERMALINK_RE.search(block)

    dt = datetime.strptime(class_date, "%Y-%m-%d")
    return {
        "week_ending": week_ending(dt),
        "class_date": class_date,
        "batchset": batch.group(1).strip() if batch else "",
        "class_topic": topic.group(1).strip() if topic else "",
        "class_rating": float(rm.group(1)),
        "total_rated": int(rated.group(1)) if rated else 0,
        "star_1": stars[1], "star_2": stars[2], "star_3": stars[3],
        "star_4": stars[4], "star_5": stars[5],
        "top_improvement": top_category(block, IMPROVE_CATS, ":wrench:"),
        "top_compliment": top_category(block, COMPLIMENT_CATS, ":speech_balloon:"),
        "slack_message_ts": ts.group(1) if ts else "",
        "permalink": link.group(1) if link else "",
    }


def split_blocks(text: str) -> list[str]:
    return re.split(r"(?=Hi <@|### Result \d+ of)", text)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, help="Raw Slack search export text")
    p.add_argument("--batch-filter", default="", help="Only include matching batchset")
    p.add_argument("--output", type=Path, help="Write JSON array")
    p.add_argument("--append-csv", type=Path, help="Append new rows to ratings CSV")
    p.add_argument("--analyze-csv", type=Path, help="Print WoW analysis from CSV")
    args = p.parse_args()

    if args.analyze_csv:
        analyze(args.analyze_csv, args.batch_filter)
        return

    text = args.input.read_text() if args.input else sys.stdin.read()
    records = []
    for block in split_blocks(text):
        rec = parse_block(block)
        if not rec:
            continue
        if args.batch_filter and args.batch_filter.lower() not in rec["batchset"].lower():
            continue
        records.append(rec)

    if args.output:
        args.output.write_text(json.dumps(records, indent=2))
        print(f"Wrote {len(records)} records to {args.output}")

    if args.append_csv:
        append_csv(args.append_csv, records)

    if not args.output and not args.append_csv:
        print(json.dumps(records, indent=2))


def append_csv(path: Path, records: list[dict]) -> None:
    fieldnames = [
        "week_ending", "class_date", "batchset", "class_topic", "class_rating",
        "total_rated", "star_1", "star_2", "star_3", "star_4", "star_5",
        "top_improvement", "top_compliment", "slack_message_ts", "permalink",
    ]
    existing_ts: set[str] = set()
    rows: list[dict] = []
    if path.exists():
        with path.open() as f:
            for row in csv.DictReader(f):
                existing_ts.add(row.get("slack_message_ts", ""))
                rows.append(row)
    added = 0
    for rec in records:
        if rec["slack_message_ts"] in existing_ts:
            continue
        rows.append(rec)
        existing_ts.add(rec["slack_message_ts"])
        added += 1
    rows.sort(key=lambda r: r["class_date"])
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Appended {added} rows to {path} ({len(rows)} total)")


def analyze(path: Path, batch_filter: str) -> None:
    with path.open() as f:
        rows = [r for r in csv.DictReader(f)
                if not batch_filter or batch_filter.lower() in r["batchset"].lower()]
    if not rows:
        print("No rows matching filter")
        return

    by_week: dict[str, list[float]] = {}
    for r in rows:
        by_week.setdefault(r["week_ending"], []).append(float(r["class_rating"]))

    weeks = sorted(by_week.keys())
    print("## Week-on-week rating trend\n")
    print("| Week ending | Classes | Avg rating | Δ vs prev |")
    print("|-------------|---------|------------|-----------|")
    prev_avg = None
    for w in weeks:
        ratings = by_week[w]
        avg = sum(ratings) / len(ratings)
        delta = f"{avg - prev_avg:+.2f}" if prev_avg is not None else "—"
        print(f"| {w} | {len(ratings)} | {avg:.2f} | {delta} |")
        prev_avg = avg

    print("\n## Recent classes\n")
    for r in rows[-8:]:
        print(f"- {r['class_date']} | {r['batchset'][:30]} | {r['class_topic'][:40]} | **{r['class_rating']}** ({r['total_rated']} rated)")


if __name__ == "__main__":
    main()
