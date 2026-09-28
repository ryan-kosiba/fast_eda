---
name: dashboard
description: Builds an interactive, filterable clean dashboard that lives inside the slide deck (and as a standalone file). Filters, stat tiles and charts all update together, and "Jarvis, filter Premium" works by voice. Use only after the Manager has agreed the dashboard brief with the human (brain/08_dashboard_brief.md), as a draft or final.
---

# Dashboard skill

**Don't start without `brain/08_dashboard_brief.md` filled in.** It says who uses the dashboard, which numbers go on top, which filters and which charts. The Manager gets these from the human.

## How it works
The deck engine (`FE/skills/slide-deck/template/deck.html`) already knows how to draw dashboards. You provide:
1. **A summary table** (not raw rows): one row per combination of the filter fields, holding sums and counts.
2. **A spec**: the filters, the stat tiles and the charts, as simple formulas over that table.
3. **A slide** that holds it: `<div class="dash" data-dash="main"></div>`.

`inject.py` puts the spec into the deck, checks it, and writes a standalone `dashboard_<id>.html`.

## Step 1: Build the summary table (`output/dashboard/build_<id>.py`)
- Use `output/analysis/common.py` for loading and cleaning, so the numbers match the findings.
- Group by **every filter field + every chart "by" field** (for example month × plan × channel).
- Store **additive columns only**: counts and sums (`members`, `retained`, `revenue`, `visits`, `wait_minutes_sum`). Rates are worked out in the spec (`sum(retained)/sum(members)`), so they stay right under any filter.
  - Averages: store `x_sum` and `n`, then use `sum(x_sum)/sum(n)`. Never average an average.
  - Unique people across groups can't be added up. Either store them per group (and label them honestly) or leave them out.
- Keep it under about 5,000 rows (the hard limit is 20,000). Too many? Use months instead of days, and group small categories into "Other".
- Months as `"2025-01"` strings (so they sort right and the range filter works).

## Step 2: Write the spec (`output/dashboard/<id>.json`)
```json
{
  "id": "main",
  "data": [ {"month": "2025-01", "plan": "Basic", "channel": "Search", "members": 210, "retained": 64, "revenue": 6090} ],
  "filters": [
    {"field": "plan", "label": "Plan"},
    {"field": "channel", "label": "Channel"},
    {"field": "month", "label": "Months", "type": "range"}
  ],
  "kpis": [
    {"label": "Members", "expr": "sum(members)", "format": "num"},
    {"label": "Still active at 90 days", "expr": "sum(retained)/sum(members)", "format": "pct"}
  ],
  "charts": [
    {"title": "New members by month", "chart": "line", "by": "month", "metrics": [{"name": "Members", "expr": "sum(members)", "format": "num"}]},
    {"title": "Retention by channel", "chart": "bar", "by": "channel", "metrics": [{"name": "Retention", "expr": "sum(retained)/sum(members)", "format": "pct"}], "sort": "desc", "highlight": "max"}
  ]
}
```
- `expr`: `sum(f)`, `avg(f)`, `min(f)`, `max(f)`, `count()`, `distinct(f)`, combined with `+ - * / ( )`.
- `format`: `num`, `pct` (a decimal like 0.31), `usd`.
- Chart `chart`: `bar`, `hbar`, `line`, `stacked`. Options: `sort` (`desc`/`asc`), `top` (N), `highlight` (`max`, `min` or a value), `yLabel`, `xLabel`. Several `metrics` = grouped bars or several lines.
- **Limits that fit on one slide:** 2-3 filters, at most 5 stat tiles, at most 4 charts. Want more? Make a second dashboard (a different `id`) on a side panel.
- A full working example: `FE/skills/dashboard/example_main.json`.

## Step 3: Add the slide
Put this where the brief says (the end of the deck, or a side panel off a finding):
```html
<section class="slide" data-title="Dashboard" data-keywords="dashboard explore filters">
  <div class="panel dashboard">
    <div class="kicker">Explore it yourself</div>
    <h2>Takeaway sentence for what this dashboard shows</h2>
    <div class="dash" data-dash="main"></div>
    <aside class="notes">Say: Jarvis, filter Premium. Or: Jarvis, clear filters.</aside>
  </div>
</section>
```
If the Slides agent owns `deck.html`, don't edit it. Give the Manager this snippet, and the Manager or the Slides agent inserts it.

## Step 4: Inject and check
```bash
python3 FE/skills/dashboard/scripts/inject.py WORK/output/deck.html WORK/output/dashboard/main.json
```
It stops with ERROR if a field is missing, and writes `output/dashboard_main.html` (the standalone copy).
Then check it: the unfiltered stat tiles must equal the matching numbers in `brain/03_findings.md` and `brain/02_data.md`. Recompute 2 of them in pandas and write the result in `brain/07_fact_check.md`.
If Chrome is available, screenshot it: `--screenshot ... "file://WORK/output/deck.html#<slide number>.1"`.

## Using it live
- Click the filters, or say **"Jarvis, filter Premium"**, **"Jarvis, just referral"** or **"Jarvis, clear filters"**.
- Each tile shows "All: X" under it while a filter is on, so the comparison is instant.
- While a dropdown is focused, the arrow keys control it. Press Esc to go back to moving slides.
