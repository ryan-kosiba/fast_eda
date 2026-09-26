#!/usr/bin/env python3
"""Fast data profiler for fast_eda.

Usage: python3 profile.py <data_dir_or_files...> [--out output/eda] [--sample 200000]

--sample N reads only the first N rows of each file (fast first look). Row counts are still exact for CSVs.

Writes:
  <out>/profile.json   machine-readable profile of every table
  <out>/profile.md     short human-readable summary (copied into brain/02_data.md)
"""
import argparse
import json
import sys
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

SKIP_DIRS = {"fast_eda", ".fast_eda", "brain", "output", ".git", ".claude", "node_modules", "__pycache__"}
EXTS = {".csv", ".tsv", ".txt", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"}
MAX_ROWS_CORR = 200_000


def find_files(paths):
    files = []
    for p in map(Path, paths):
        if p.is_file() and p.suffix.lower() in EXTS:
            files.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in EXTS and not (SKIP_DIRS & set(f.parts)):
                    files.append(f)
    return files


def load(path, sample=None):
    ext = path.suffix.lower()
    if ext in {".csv", ".txt"}:
        return {path.stem: pd.read_csv(path, low_memory=False, nrows=sample)}
    if ext == ".tsv":
        return {path.stem: pd.read_csv(path, sep="\t", low_memory=False, nrows=sample)}
    if ext in {".xlsx", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None)
        return {f"{path.stem}:{k}" if len(sheets) > 1 else path.stem: v for k, v in sheets.items()}
    if ext == ".parquet":
        return {path.stem: pd.read_parquet(path)}
    if ext == ".jsonl":
        return {path.stem: pd.read_json(path, lines=True)}
    if ext == ".json":
        try:
            return {path.stem: pd.read_json(path)}
        except ValueError:
            return {path.stem: pd.json_normalize(json.loads(path.read_text()))}
    return {}


def try_dates(s):
    """Return parsed datetime series if an object column looks like dates, else None."""
    if s.dtype != object:
        return None
    sample = s.dropna().astype(str).head(500)
    if sample.empty or sample.str.len().median() < 6:
        return None
    parsed = pd.to_datetime(sample, errors="coerce")
    if parsed.notna().mean() > 0.9:
        return pd.to_datetime(s, errors="coerce")
    return None


def col_role(name, s, n):
    lname = name.lower()
    nun = s.nunique(dropna=True)
    if pd.api.types.is_datetime64_any_dtype(s):
        return "date"
    if lname in {"id", "key"} or lname.endswith(("_id", "_key")) or (lname.endswith("id") and nun > 0.5 * n):
        return "id"
    if pd.api.types.is_bool_dtype(s) or nun == 2:
        return "flag"
    if pd.api.types.is_numeric_dtype(s):
        return "number" if nun > 15 else "category"
    if nun <= max(50, 0.05 * n):
        return "category"
    return "text"


def fnum(x):
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return round(float(x), 4)
    return x


def count_rows(path):
    """Exact row count for text files without loading them."""
    with open(path, "rb") as fh:
        return max(sum(buf.count(b"\n") for buf in iter(lambda: fh.read(1 << 24), b"")) - 1, 0)


def profile_table(name, df, total_rows=None):
    n = len(df)
    for c in df.columns:
        d = try_dates(df[c])
        if d is not None:
            df[c] = d
    cols = []
    for c in df.columns:
        s = df[c]
        role = col_role(str(c), s, n)
        info = {
            "name": str(c),
            "dtype": str(s.dtype),
            "role": role,
            "missing_pct": fnum(s.isna().mean() * 100),
            "unique": int(s.nunique(dropna=True)),
        }
        if role == "date":
            info.update(min=str(s.min()), max=str(s.max()))
            vc = s.dt.to_period("M").value_counts().sort_index()
            info["rows_per_month"] = {str(k): int(v) for k, v in vc.items()}
        elif pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            d = s.describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
            info["stats"] = {k: fnum(v) for k, v in d.items()}
            info["zeros_pct"] = fnum((s == 0).mean() * 100)
            info["negatives"] = int((s < 0).sum())
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            info["outliers"] = int(((s < q1 - 3 * iqr) | (s > q3 + 3 * iqr)).sum()) if iqr > 0 else 0
        if role in {"category", "flag", "text", "id"} or s.dtype == object:
            vc = s.astype(str).value_counts(dropna=True).head(8)
            info["top_values"] = {k: int(v) for k, v in vc.items()}
        if s.dtype == object:
            st = s.dropna().astype(str)
            if len(st):
                stripped = st.str.strip().str.lower()
                if stripped.nunique() < st.nunique():
                    info["messy_text"] = f"{st.nunique() - stripped.nunique()} values only differ by case/spaces"
        cols.append(info)

    dup_rows = int(df.duplicated().sum())
    key_candidates = [c["name"] for c in cols if c["unique"] == n and c["missing_pct"] == 0 and n > 0]
    return {
        "table": name,
        "rows": total_rows or n,
        "rows_profiled": n,
        "columns": len(df.columns),
        "duplicate_rows": dup_rows,
        "key_candidates": key_candidates,
        "cols": cols,
        "correlations": correlations(df),
    }


def correlations(df, top=15):
    num = df.select_dtypes(include="number")
    num = num.loc[:, num.nunique() > 2]
    if num.shape[1] < 2:
        return []
    if len(num) > MAX_ROWS_CORR:
        num = num.sample(MAX_ROWS_CORR, random_state=0)
    corr = num.corr(method="spearman")
    pairs = []
    for a, b in combinations(corr.columns, 2):
        r = corr.loc[a, b]
        if pd.notna(r) and abs(r) >= 0.3:
            pairs.append({"a": str(a), "b": str(b), "spearman": round(float(r), 3)})
    return sorted(pairs, key=lambda p: -abs(p["spearman"]))[:top]


def _norm(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def _is_link(t1, c1, t2, c2):
    """Same column name, or `id` in one table matching `<table>_id` in the other."""
    a, b = _norm(c1), _norm(c2)
    if a == b:
        return True
    for (tab, col), other in (((t1, a), b), ((t2, b), a)):
        stem = _norm(tab.split(":")[-1])
        stems = {stem, stem.rstrip("s"), stem[:-2] if stem.endswith("es") else stem}
        if col in {"id", "key"} and other in {s + "id" for s in stems} | {s + "key" for s in stems}:
            return True
    return False


def join_candidates(tables):
    """Find columns that link tables (by name), and measure how well their values match."""
    out = []
    names = list(tables)
    for t1, t2 in combinations(names, 2):
        d1, d2 = tables[t1], tables[t2]
        for c1 in d1.columns:
            for c2 in d2.columns:
                if not _is_link(t1, c1, t2, c2):
                    continue
                if pd.api.types.is_datetime64_any_dtype(d1[c1]) or pd.api.types.is_datetime64_any_dtype(d2[c2]):
                    continue
                v1 = set(d1[c1].dropna().astype(str).unique()[:50_000])
                v2 = set(d2[c2].dropna().astype(str).unique()[:50_000])
                if not v1 or not v2:
                    continue
                inter = len(v1 & v2)
                cover = inter / min(len(v1), len(v2))
                if inter > 0:
                    out.append({
                        "left": f"{t1}.{c1}", "right": f"{t2}.{c2}",
                        "match_pct_of_smaller": round(cover * 100, 1),
                        "left_unique": len(v1), "right_unique": len(v2),
                        "left_values_missing_in_right": len(v1 - v2),
                        "right_values_missing_in_left": len(v2 - v1),
                    })
    return sorted(out, key=lambda j: -j["match_pct_of_smaller"])


def to_markdown(profiles, joins):
    L = ["# Data profile (auto)", ""]
    if any(p.get("rows_profiled") != p["rows"] for p in profiles):
        L.append("_Sampled: stats below come from the first rows of each file; row counts are exact._")
        L.append("")
    L.append("| Table | Rows | Cols | Dup rows | Key |")
    L.append("|---|---|---|---|---|")
    for p in profiles:
        L.append(f"| {p['table']} | {p['rows']:,} | {p['columns']} | {p['duplicate_rows']:,} | {', '.join(p['key_candidates'][:2]) or '-'} |")
    L.append("")
    if joins:
        L.append("## How tables connect")
        for j in joins[:15]:
            L.append(f"- {j['left']} ↔ {j['right']}: {j['match_pct_of_smaller']}% match "
                     f"({j['left_values_missing_in_right']:,} left-only, {j['right_values_missing_in_left']:,} right-only)")
        L.append("")
    for p in profiles:
        L.append(f"## {p['table']}  ({p['rows']:,} rows)")
        L.append("| Column | Role | Missing % | Unique | Notes |")
        L.append("|---|---|---|---|---|")
        for c in p["cols"]:
            notes = []
            if c["role"] == "date":
                notes.append(f"{c['min'][:10]} → {c['max'][:10]}")
            if "stats" in c:
                st = c["stats"]
                notes.append(f"median {st.get('50%')}, range {st.get('min')}–{st.get('max')}")
                if c.get("outliers"):
                    notes.append(f"{c['outliers']} extreme values")
                if c.get("negatives"):
                    notes.append(f"{c['negatives']} negatives")
            if "top_values" in c and c["role"] in {"category", "flag"}:
                tv = list(c["top_values"].items())[:4]
                notes.append("top: " + ", ".join(f"{k} ({v})" for k, v in tv))
            if c.get("messy_text"):
                notes.append(c["messy_text"])
            L.append(f"| {c['name']} | {c['role']} | {c['missing_pct']} | {c['unique']:,} | {'; '.join(notes)} |")
        if p["correlations"]:
            L.append("")
            L.append("Moves together (Spearman, |r|≥0.3): " + "; ".join(
                f"{x['a']}~{x['b']} {x['spearman']}" for x in p["correlations"][:8]))
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["."])
    ap.add_argument("--out", default="output/eda")
    ap.add_argument("--sample", type=int, default=None, help="only read the first N rows of each file")
    a = ap.parse_args()

    files = find_files(a.paths)
    if not files:
        sys.exit("No data files found.")
    tables, totals = {}, {}
    for f in files:
        try:
            loaded = load(f, a.sample)
            tables.update(loaded)
            if a.sample and f.suffix.lower() in {".csv", ".tsv", ".txt"}:
                for k in loaded:
                    totals[k] = count_rows(f)
        except Exception as e:  # keep going; report the bad file
            print(f"!! could not read {f}: {e}", file=sys.stderr)
    profiles = [profile_table(k, v, totals.get(k)) for k, v in tables.items()]
    joins = join_candidates(tables)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "profile.json").write_text(json.dumps({"files": [str(f) for f in files], "tables": profiles, "joins": joins}, indent=1, default=str))
    md = to_markdown(profiles, joins)
    (out / "profile.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
