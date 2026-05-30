#!/usr/bin/env python3
"""
Build session→ID mapping CSV from extracted JSON and a session map config.

Session map JSON format:
{
  "2": {"title": "Data Analytics Using Numpy", "sources": [
    {"tab": "NumPy assessments", "sections": ["Lecture 1", "Lecture 2", "Lecture 3", "Lecture 4"]}
  ]},
  "3": {"title": "...", "ids": ["27195", "28047"]}  // explicit ID list overrides sources
}

Usage:
  python build_mapping.py --extracted extracted.json --map session_map.json --output mapping.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def collect_ids(extracted: dict, tab: str, sections: list[str] | None) -> list[str]:
    tab_data = extracted.get("tabs", {}).get(tab, {})
    all_sections = tab_data.get("sections", {})
    if sections is None:
        sections = list(all_sections.keys())
    ids: list[str] = []
    seen: set[str] = set()
    for sec in sections:
        for item in all_sections.get(sec, []):
            pid = item["id"]
            if pid not in seen:
                seen.add(pid)
                ids.append(pid)
    return ids


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--extracted", type=Path, required=True)
    p.add_argument("--map", type=Path, required=True, help="Session map JSON")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    extracted = json.loads(args.extracted.read_text())
    session_map = json.loads(args.map.read_text())

    rows = [["Session Number", "Session Details", "Problem ID List"]]
    for session_num in sorted(session_map, key=lambda x: int(x)):
        cfg = session_map[session_num]
        title = cfg["title"]
        if "ids" in cfg:
            ids = cfg["ids"]
        else:
            ids = []
            for src in cfg.get("sources", []):
                ids.extend(collect_ids(extracted, src["tab"], src.get("sections")))
            # dedupe preserving order
            seen: set[str] = set()
            ids = [i for i in ids if i not in seen and not seen.add(i)]
        rows.append([session_num, title, ", ".join(ids)])

    with args.output.open("w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"Wrote {args.output} ({len(rows) - 1} sessions)")


if __name__ == "__main__":
    main()
