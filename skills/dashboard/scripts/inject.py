#!/usr/bin/env python3
"""Put dashboard specs into a deck, check them, and write standalone dashboard files.

Usage:
  python3 inject.py output/deck.html output/dashboard/main.json [more.json ...]

Each JSON file is one dashboard: {"id": "main", "data": [...], "filters": [...], "kpis": [...], "charts": [...]}
Writes:
  deck.html                      (DASHBOARDS block replaced)
  dashboard_<id>.html            (same engine, shows only that dashboard, next to deck.html)
"""
import json
import re
import sys
from pathlib import Path

MAX_ROWS = 20_000
AGG = re.compile(r"(sum|avg|min|max|count|distinct)\(\s*([\w.]*)\s*\)")


def check(spec, html):
    errs, warns = [], []
    did = spec.get("id")
    if not did:
        errs.append("missing id")
    rows = spec.get("data") or []
    if not rows:
        errs.append(f"{did}: no data rows")
    if len(rows) > MAX_ROWS:
        errs.append(f"{did}: {len(rows):,} rows, max {MAX_ROWS:,}. Aggregate more (fewer dimensions or monthly instead of daily).")
    fields = set().union(*(r.keys() for r in rows)) if rows else set()

    def fields_in(expr):
        return [f for _, f in AGG.findall(expr) if f]

    for f in spec.get("filters", []):
        if f.get("field") not in fields:
            errs.append(f"{did}: filter field '{f.get('field')}' not in data")
        else:
            n = len({r.get(f['field']) for r in rows})
            if f.get("type") != "range" and n > 30:
                warns.append(f"{did}: filter '{f['field']}' has {n} values; that's a long dropdown")
    for k in spec.get("kpis", []):
        for fld in fields_in(k.get("expr", "")):
            if fld not in fields:
                errs.append(f"{did}: KPI '{k.get('label')}' uses unknown field '{fld}'")
    for c in spec.get("charts", []):
        if c.get("by") not in fields:
            errs.append(f"{did}: chart '{c.get('title')}' groups by unknown field '{c.get('by')}'")
        for m in c.get("metrics", []):
            for fld in fields_in(m.get("expr", "")):
                if fld not in fields:
                    errs.append(f"{did}: chart '{c.get('title')}' uses unknown field '{fld}'")
    if len(spec.get("kpis", [])) > 5:
        warns.append(f"{did}: more than 5 KPIs won't fit well")
    if len(spec.get("charts", [])) > 4:
        warns.append(f"{did}: more than 4 charts won't fit well")
    if f'data-dash="{did}"' not in html:
        warns.append(f'{did}: no <div class="dash" data-dash="{did}"> in the deck yet, so add the dashboard slide')
    return errs, warns


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    deck = Path(sys.argv[1])
    html = deck.read_text()
    specs = [json.loads(Path(p).read_text()) for p in sys.argv[2:]]

    all_errs = []
    for sp in specs:
        errs, warns = check(sp, html)
        all_errs += errs
        for w in warns:
            print("WARN ", w)
    if all_errs:
        for e in all_errs:
            print("ERROR", e)
        sys.exit(1)

    block = "const DASHBOARDS = " + json.dumps({sp["id"]: {k: v for k, v in sp.items() if k != "id"} for sp in specs},
                                                separators=(",", ":"), default=str) + ";"
    new, n = re.subn(r"/\* DASHBOARDS:BEGIN \*/.*?/\* DASHBOARDS:END \*/",
                     lambda _: "/* DASHBOARDS:BEGIN */\n" + block + "\n/* DASHBOARDS:END */", html, flags=re.S)
    if n != 1:
        sys.exit("ERROR could not find the DASHBOARDS:BEGIN/END markers in the deck")
    deck.write_text(new)
    print(f"OK   {deck} updated with {len(specs)} dashboard(s), {sum(len(s['data']) for s in specs):,} rows total")

    for sp in specs:
        solo = new.replace("onlyDashboard: null,", f'onlyDashboard: "{sp["id"]}",', 1)
        out = deck.parent / f"dashboard_{sp['id']}.html"
        out.write_text(solo)
        print(f"OK   {out} (standalone)")
    kb = len(new.encode()) / 1024
    print(f"Deck size: {kb:,.0f} KB" + ("  (big, so consider fewer rows)" if kb > 5000 else ""))


if __name__ == "__main__":
    main()
