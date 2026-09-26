---
name: business-objective
description: Turns a business goal plus a data summary into the metrics that matter and a ranked list of questions worth testing. Use after the goal is known and the data is profiled, before deep analysis.
---

# Business Objective skill

Inputs: `brain/01_objective.md` (the goal, the audience, what they asked for) and `brain/02_data.md`.

## 1. Metric tree
Break the goal into things the data can measure. Example for a telehealth company:

```
Revenue = active members × visits per member × revenue per visit
            │                  │                        │
   new − lost members    repeat-visit rate          plan mix, price
```
Only use metrics the data can actually compute. Mark each one ✅ (can compute) or ❌ (missing data).

## 2. Questions to test (4-8)
For each one, write:
- **Question:** plain words. ("Do people who get a follow-up within 7 days stay longer?")
- **Why it matters:** the money or patient effect if it's true. Rough size, like "about 5% of revenue".
- **How to test:** which tables and columns, and which comparison.
- **Action if true:** what the company would *do* differently.
- **Score:** Impact (1-5) × Can we prove it in 20 min (1-5).

Rank by score. The best questions have a clear action, a big effect and a quick test.

Good kinds of questions for health and consumer data:
- **Who stays and who leaves** (retention by starting month, by channel, by first experience)
- **What happens before someone leaves** (the signals before they drop off)
- **Where the money is** (the few groups that bring in most of the value, and who's underserved)
- **Funnels** (where people drop off, step by step)
- **Operations** (wait times, capacity, how providers differ, and how that links to outcomes)
- **Time** (seasonality, trend breaks, and what changed and when)
- **Pricing and plan mix**

## 3. Storyline guess
One sentence: "If these hold, the story is: ___." This becomes the deck's main message later.

## Output
Write the whole thing to `brain/01_objective.md` under `## Metric tree` and `## Questions to test`.
