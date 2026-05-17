#!/usr/bin/env python3
"""json2csv – tiny JSON to CSV converter.

Accepts a JSON file (or reads from STDIN) containing a list of objects.
Outputs CSV to STDOUT.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

def load_json(source: Path | None) -> list[dict]:
    """Load JSON from a file or STDIN and return a list of dictionaries."""
    if source is None:
        data = json.load(sys.stdin)
    else:
        with source.open('r', encoding='utf-8') as f:
            data = json.load(f)
    if not isinstance(data, list):
        raise ValueError('JSON top-level structure must be a list of objects')
    return data

def determine_fields(records: list[dict], explicit: list[str] | None) -> list[str]:
    """Return column order.
    If explicit list is given, use it (add any missing keys found in data).
    Otherwise, infer order from first record and then any additional keys.
    """
    if explicit:
        fields = explicit[:]
        # Append any keys not covered by explicit order, preserving discovery order
        seen = set(fields)
        for rec in records:
            for k in rec.keys():
                if k not in seen:
                    fields.append(k)
                    seen.add(k)
        return fields
    # Infer from first record, then any others
    if not records:
        return []
    fields = list(records[0].keys())
    seen = set(fields)
    for rec in records[1:]:
        for k in rec.keys():
            if k not in seen:
                fields.append(k)
                seen.add(k)
    return fields

def main() -> None:
    parser = argparse.ArgumentParser(description='Convert JSON array of objects to CSV')
    parser.add_argument('json_file', nargs='?', help='Path to JSON file (omit for STDIN)')
    parser.add_argument('--fields', help='Comma‑separated list of columns to output (optional)')
    args = parser.parse_args()

    source = Path(args.json_file) if args.json_file else None
    try:
        records = load_json(source)
    except Exception as e:
        sys.stderr.write(f'Error loading JSON: {e}\n')
        sys.exit(1)

    explicit_fields = [f.strip() for f in args.fields.split(',')] if args.fields else None
    fields = determine_fields(records, explicit_fields)

    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for rec in records:
        writer.writerow(rec)

if __name__ == '__main__':
    main()
