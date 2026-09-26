---
name: eda
description: Exploratory data analysis for fast_eda. Profiles every data file (shape, missing data, odd values, how tables connect, what moves together) and writes a plain-language data summary to brain/02_data.md. Use at the start of any dataset analysis.
---

# EDA skill

## Step 1: Auto-profile (2 min)
```bash
python3 FE/skills/eda/scripts/profile.py WORK --out WORK/output/eda
```
This prints a profile and saves `output/eda/profile.json` and `output/eda/profile.md`. Needs pandas. If it's missing, run `pip install pandas numpy scipy openpyxl pyarrow`.

## Step 2: Check what the script can't (5-8 min)
Write short pandas code (save it to `output/eda/checks.py`) that answers:
1. **What is one row?** One patient, one visit, one payment? Check it against the key column.
2. **Time.** What date range does it cover? Are any months partial or empty? (The last month is often partial, so flag it.) Are there dates in the future?
3. **Joins.** For each link the profile found, do a test join. How many rows match? Does the join multiply rows by accident?
4. **Missing data.** Which columns have gaps? Are the gaps random, or tied to a group or time (for example, everything missing before March)?
5. **Odd values.** Negatives where there shouldn't be any, ages over 110, prices of 0, the same thing spelled 3 ways, test or dummy rows.
6. **What moves together.** Top links between numbers (already in the profile), plus the biggest gaps in the main outcome between groups. Just a first look, no deep dives.
7. **The main outcome columns.** Name the 1-3 columns that look like what the business cares about (revenue, retention, visits, rating, cost).

## Step 3: Write `brain/02_data.md`
Use this shape. Keep it tight: no more than about 60 lines.

```markdown
# Data
## Files
| Table | One row = | Rows | Dates | Key |
## How they connect
- visits.patient_id → patients.id (98% match, 1.2k visits have no patient)
## Main outcomes
- `revenue` (visits): what it is, total, trend in one line
## Data quality problems (worst first)
- [HIGH] 12% of visits have no price. They're all before Mar 2024. Fix: leave those months out of revenue trends.
## Early signals (for the Business agent)
- ...5 bullets max, each with one number
## Cleaning rules everyone must use
- Drop 312 test accounts (email ends with @test.com)
- The last month is partial, so leave it out of trends
```

"Cleaning rules" matters most. Every later agent must use the same rules, so the numbers match.

## Optional: EDA HTML report
If there's time, or if they ask, build `output/eda/eda_report.html` using the slide-deck brand colors (see `FE/skills/slide-deck/brand.md`): a table summary, a missing-data heatmap and top distributions.
