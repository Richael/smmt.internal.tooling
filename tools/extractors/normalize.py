#!/usr/bin/env python3
"""
normalize.py — turn raw MCP tool output (saved by OpenClaw) into normalized records.

Flow:
  1. OpenClaw runs an extraction playbook and saves raw tool output to data/raw/
     as JSON. Two accepted shapes:
       a) an envelope:  {"source":"apollo","tool":"search_people","data": <result>}
       b) a list of envelopes, OR a bare tool result in a file named
          <source>.<tool>.json  (source/tool inferred from the filename).
  2. This script maps every row -> NormalizedRecord and writes:
       data/normalized/<entity_type>.jsonl   (+ optional .csv)
       data/normalized/_summary.json

No secrets, no network — it only reads local files. Stdlib only.

Usage:
  python3 tools/extractors/normalize.py                 # data/raw -> data/normalized
  python3 tools/extractors/normalize.py --input examples/raw --out /tmp/out --csv
"""
from __future__ import annotations
import argparse, csv, json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                       # so `import schema` / `import mappings.*` work
import schema                                   # noqa: E402
from mappings import apollo, hubspot, youtube   # noqa: E402

REGISTRY = {"apollo": apollo, "hubspot": hubspot, "youtube": youtube}
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def _envelopes_from_file(path):
    """Yield (source, tool, data) tuples from one raw json file."""
    with open(path) as fh:
        doc = json.load(fh)
    base = os.path.basename(path)
    parts = base[:-5].split(".") if base.endswith(".json") else []
    f_source = parts[0] if parts else None
    f_tool = parts[1] if len(parts) > 1 else None

    def one(d):
        if isinstance(d, dict) and "source" in d and "tool" in d:
            return (d["source"], d["tool"], d.get("data", d.get("result")))
        return (f_source, f_tool, d)            # bare result -> infer from filename

    if isinstance(doc, list) and doc and isinstance(doc[0], dict) and "source" in doc[0]:
        for d in doc:
            yield one(d)
    else:
        yield one(doc)


def normalize_dir(input_dir, include_raw=False):
    records, skipped = [], []
    if not os.path.isdir(input_dir):
        return records, skipped
    for name in sorted(os.listdir(input_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(input_dir, name)
        try:
            for source, tool, data in _envelopes_from_file(path):
                mod = REGISTRY.get((source or "").lower())
                if not mod or not tool:
                    skipped.append((name, source, tool, "no mapper/tool"))
                    continue
                recs = mod.records(tool, data)
                if not recs:
                    skipped.append((name, source, tool, "0 records (unmapped tool or empty)"))
                records.extend(recs)
        except (json.JSONDecodeError, OSError) as e:
            skipped.append((name, None, None, f"read error: {e}"))
    return records, skipped


def write_output(records, out_dir, write_csv=False, include_raw=False):
    os.makedirs(out_dir, exist_ok=True)
    by_entity = defaultdict(list)
    for r in records:
        by_entity[r.entity_type].append(r)

    for entity, recs in by_entity.items():
        # jsonl
        with open(os.path.join(out_dir, f"{entity}.jsonl"), "w") as fh:
            for r in recs:
                fh.write(json.dumps(r.to_dict(include_raw=include_raw), default=str) + "\n")
        # csv (canonical columns for this entity)
        if write_csv:
            cols = ["id", "source", "source_tool", "extracted_at"] + list(schema.CANONICAL_ATTRS.get(entity, ()))
            with open(os.path.join(out_dir, f"{entity}.csv"), "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
                w.writeheader()
                for r in recs:
                    row = {"id": r.id, "source": r.source, "source_tool": r.source_tool,
                           "extracted_at": r.extracted_at}
                    for k, v in r.attributes.items():
                        row[k] = json.dumps(v) if isinstance(v, (list, dict)) else v
                    w.writerow(row)

    summary = {
        "total": len(records),
        "by_entity": {k: len(v) for k, v in sorted(by_entity.items())},
        "by_source": dict(Counter(r.source for r in records)),
        "target_data_points": {k: schema.ENTITY_TYPES[k] for k in sorted(by_entity)},
    }
    with open(os.path.join(out_dir, "_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=os.path.join(REPO, "data", "raw"))
    ap.add_argument("--out", default=os.path.join(REPO, "data", "normalized"))
    ap.add_argument("--csv", action="store_true", help="also write per-entity CSV")
    ap.add_argument("--include-raw", action="store_true", help="keep original payload in output")
    args = ap.parse_args(argv)

    records, skipped = normalize_dir(args.input, include_raw=args.include_raw)
    summary = write_output(records, args.out, write_csv=args.csv, include_raw=args.include_raw)

    print(f"normalized {summary['total']} records -> {args.out}")
    for entity, n in summary["by_entity"].items():
        print(f"  {entity:<15} {n:>5}   ({schema.ENTITY_TYPES[entity]})")
    if skipped:
        print(f"skipped {len(skipped)} input(s):")
        for name, src, tool, why in skipped[:20]:
            print(f"  - {name}  [{src}/{tool}]  {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
