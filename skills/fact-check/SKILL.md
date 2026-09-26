---
name: fact-check
description: Independently re-computes every number in the findings and the slide deck from the raw data, and flags anything wrong, unsupported or misleading. Use before anything is shown to the human or put on a slide.
---

# Fact Check skill

You are the skeptic. Assume every number is wrong until you get it yourself.

## Checking findings (`brain/03_findings.md`)
For each finding:
1. **Recompute it from scratch.** Write fresh code in `output/factcheck/check_F<N>.py`. Don't just re-run their script. Use `common.py` cleaning, but write the core logic yourself.
2. **Compare.** Match (within rounding) = PASS. Off = FAIL, with the right number.
3. **Check the logic:**
   - Is the comparison fair? (Same time window, same kind of people)
   - Does the plain wording match the numbers? ("Twice as likely" needs a ratio near 2×, not +2 points.)
   - Is causation claimed where there's only a link?
   - Is the dollar estimate's math shown and sensible?
   - Is a small sample or a partial month behind it?
4. **Check totals.** Does the sum of the groups equal the total? Do percentages add to 100?

## Checking the deck (`output/deck.html`)
- Pull every number from the HTML (text and chart data). Each one must trace to a PASSED finding or to `02_data.md`.
- Chart titles must match what the chart shows.
- Axis labels and units are there. Percentages are formatted as percentages.

## Checking dashboards (`output/dashboard/*.json`)
- With no filters, every stat tile must match the same number in findings or `02_data.md`.
- Pick one filter value and recompute one tile from raw data. It must match.
- Rates must be built from sums (`sum(a)/sum(b)`), never averages of rates.

## Output: `brain/07_fact_check.md`
```markdown
| Item | Claim | Recomputed | Verdict | Fix |
|---|---|---|---|---|
| F2 | 62% vs 31% | 61.8% vs 31.2% | PASS | - |
| F4 | "3× revenue" | 1.9× | FAIL | Say "almost 2×" |
| Slide 5 | $2.1M | not traced | FAIL | remove or source it |
```
Return: the count of PASS and FAIL, plus the FAIL list with fixes. Short.
