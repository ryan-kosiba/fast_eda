---
name: deep-analysis
description: Tests business questions with data: splits by group, retention by starting month, funnels, drivers, and checks it isn't luck. Writes findings with numbers and saved code to brain/03_findings.md. Use for the main analysis phase.
---

# Deep Analysis skill

## Before you start
- Read `brain/01_objective.md`, `brain/02_data.md` (especially **Cleaning rules**) and `brain/04_decisions.md`.
- Put the shared loading and cleaning code in `output/analysis/common.py` (create it if it's missing; reuse it if it's there). Every analysis imports it, so the numbers match everywhere.

## Background pack (when the Manager asks for it: one agent, about 10 min)
The audience needs the baseline before the findings. Write `output/analysis/background.py` and put the results under `## Background` in `brain/03_findings.md` (IDs `B1`, `B2`…):
1. **Headline numbers** (4-5): total volume (rides, visits, orders), people (members, patients, customers), money (revenue, if it's in the data), the main outcome rate (retention, conversion), and the date range covered.
2. **Trend over time:** the main volume and the main outcome by week or month. Give the % change from start to end (or vs the same period last year, if the data covers it). **Leave out partial first and last periods.** Call out any clear break ("drops 30% after March 10").
3. **The mix:** the 1-2 splits that matter for the goal (member vs casual, plan type, channel), shown as shares, and how that mix has shifted over time.
4. **Rhythm** (only if it's strong): day of week, hour of day, or season.
Plain-language takeaway for each one, with a number ("Rides grew 12% from May to Aug, but all the growth came from members").
Chart files: `bg_kpis.json` (`chart: "kpi"`, with `values` + labels), `bg_trend.json` (line), `bg_mix.json` (bar or stacked). Same format as below.
These count as findings: the Fact Checker checks them too.

## For each question
1. Write one script: `output/analysis/q<N>_<short_name>.py`. It prints the key numbers and saves chart data to `output/analysis/q<N>_<short_name>.json`.
2. Run it. Read the output. Sanity check it: do the totals match `02_data.md`? Are the group sizes big enough (at least 30 per group)?
3. Is it luck? Use the simplest test that fits:
   - Rates between 2 groups: two-proportion z-test or chi-square
   - Averages: Mann-Whitney (skewed data) or t-test
   - Many things at once: logistic or linear regression (statsmodels if you have it, else scikit-learn), and report the effect in plain units
   - Always give the **size** of the effect, not just whether it's significant.
4. Look for traps:
   - **A hidden cause.** Does the gap survive when you control for the obvious third factor (age, plan, channel, start month)?
   - **Simpson's paradox.** Check that the pattern holds inside the main groups.
   - **Survivor bias.** Newer customers haven't had time to leave, so compare people who've been around the same amount of time.
   - **Partial last month, duplicate rows, test accounts.** Follow the cleaning rules.
5. Put a size on it: "If we moved X from A to B, that's about $___ or ___ people a year." Show the math in one line.

## Chart data format (the Slides agent reads this)
```json
{"id": "q2_followup", "title": "Follow-up in 7 days → 2× more people stay",
 "chart": "bar", "x": ["No follow-up", "Follow-up"], "series": [{"name": "Stayed 90 days", "values": [0.31, 0.62], "format": "pct"}],
 "note": "n = 4,210 people. Holds within each plan type."}
```
Chart types: `bar`, `hbar`, `line`, `stacked`, `scatter`, `table`, `kpi`.

## Write to `brain/03_findings.md`
Under your agent's heading, one block per finding:

```markdown
### F2: Follow-up within 7 days doubles 90-day retention
- **Plain:** People who got a follow-up call stayed twice as often (62% vs 31%).
- **Numbers:** n=4,210; difference +31 points; p<0.001; holds in every plan type
- **So what:** If we add follow-up to the 60% who don't get one, about 1,300 more people stay. That's about $390K a year.
- **Action:** Automatic follow-up for everyone within 7 days.
- **Confidence:** High / Medium / Low, and why
- **Caveat:** Could be that more engaged people ask for follow-ups. It's not proven to cause it.
- **Code:** output/analysis/q2_followup.py → q2_followup.json
```

Negative results count too. "We checked X, and it doesn't matter" saves the company time. Write them down briefly.
