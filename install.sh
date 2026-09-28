#!/usr/bin/env bash
# fast_eda installer. Run from the folder that holds the data:  bash fast_eda/install.sh
set -e
FE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(pwd)"

mkdir -p "$WORK/brain" "$WORK/output/eda" "$WORK/output/analysis" "$WORK/output/factcheck"
for f in "$FE"/brain_template/*.md; do
  [ -f "$WORK/brain/$(basename "$f")" ] || cp "$f" "$WORK/brain/"
done

# Keep a full local copy of the kit (START.md, skills, templates) in WORK/.fast_eda,
# so the playbook is there even with no network later.
case "$FE" in
  "$WORK"/*) ;;  # already inside the project folder
  *) rm -rf "$WORK/.fast_eda"; mkdir -p "$WORK/.fast_eda"
     (cd "$FE" && tar --exclude=.git --exclude=context --exclude=.DS_Store -cf - .) | (cd "$WORK/.fast_eda" && tar -xf -) ;;
esac

# Make skills + agents discoverable by Claude Code in this folder (optional; START.md works without it)
mkdir -p "$WORK/.claude/skills" "$WORK/.claude/agents"
for d in "$FE"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$WORK/.claude/skills/$name"; cp -R "$d" "$WORK/.claude/skills/$name"
done
cp "$FE"/agents/*.md "$WORK/.claude/agents/"

# Python packages. Only pandas + numpy are required; everything else is optional and installs in the
# background (with a short timeout) so a slow or locked-down box never blocks the run.
PIPCMD="python3 -m pip"; python3 -m pip --version >/dev/null 2>&1 || PIPCMD="pip3"
PIP="$PIPCMD install -q --disable-pip-version-check --timeout 15"
if ! python3 -c "import pandas, numpy" 2>/dev/null; then
  $PIP pandas numpy 2>/dev/null || $PIP --user pandas numpy 2>/dev/null || $PIP --break-system-packages pandas numpy 2>/dev/null \
    || echo "!! pandas/numpy missing and pip failed. Nothing will run until they're installed."
fi
OPT=""
for m in scipy statsmodels openpyxl pyarrow; do python3 -c "import $m" 2>/dev/null || OPT="$OPT $m"; done
if [ -n "$OPT" ]; then
  echo "Optional packages installing in the background:$OPT (log: output/pip_optional.log). Work without them if they fail."
  ( $PIP $OPT || $PIP --user $OPT || $PIP --break-system-packages $OPT ) > "$WORK/output/pip_optional.log" 2>&1 &
fi

echo "fast_eda ready. FE=$FE WORK=$WORK"
echo "Data files:"
find "$WORK" -maxdepth 3 -type f \( -iname '*.csv' -o -iname '*.tsv' -o -iname '*.xlsx' -o -iname '*.xls' -o -iname '*.parquet' -o -iname '*.json' -o -iname '*.jsonl' \) \
  -not -path '*/fast_eda/*' -not -path '*/.fast_eda/*' -not -path '*/output/*' -not -path '*/brain/*' -not -path '*/.claude/*' -not -path '*/node_modules/*' | head -50
