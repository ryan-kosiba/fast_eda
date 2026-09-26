#!/usr/bin/env bash
# fast_eda installer. Run from the folder that holds the data:  bash fast_eda/install.sh
set -e
FE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(pwd)"

mkdir -p "$WORK/brain" "$WORK/output/eda" "$WORK/output/analysis" "$WORK/output/factcheck"
for f in "$FE"/brain_template/*.md; do
  [ -f "$WORK/brain/$(basename "$f")" ] || cp "$f" "$WORK/brain/"
done

# Make skills + agents discoverable by Claude Code in this folder (optional; START.md works without it)
mkdir -p "$WORK/.claude/skills" "$WORK/.claude/agents"
for d in "$FE"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$WORK/.claude/skills/$name"; cp -R "$d" "$WORK/.claude/skills/$name"
done
cp "$FE"/agents/*.md "$WORK/.claude/agents/"

# Python packages
python3 - <<'PY' 2>/dev/null || pip install -q pandas numpy scipy openpyxl pyarrow 2>/dev/null || pip install -q --user pandas numpy scipy openpyxl 2>/dev/null || echo "!! install pandas/numpy/scipy manually"
import pandas, numpy, scipy
PY
python3 -c "import statsmodels" 2>/dev/null || pip install -q statsmodels 2>/dev/null || true

echo "fast_eda ready. FE=$FE WORK=$WORK"
echo "Data files:"
find "$WORK" -maxdepth 3 -type f \( -iname '*.csv' -o -iname '*.tsv' -o -iname '*.xlsx' -o -iname '*.xls' -o -iname '*.parquet' -o -iname '*.json' -o -iname '*.jsonl' \) \
  -not -path '*/fast_eda/*' -not -path '*/.fast_eda/*' -not -path '*/output/*' -not -path '*/brain/*' -not -path '*/.claude/*' -not -path '*/node_modules/*' | head -50
