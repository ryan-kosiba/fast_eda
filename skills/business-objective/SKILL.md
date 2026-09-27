---
name: business-objective
description: Turns a business goal plus a data summary into the metrics that matter and a ranked list of questions worth testing. Use after the goal is known and the data is profiled, before deep analysis.
---

# Business Objective skill

Inputs: `brain/01_objective.md` (the goal, the audience, what they asked for) and `brain/02_data.md`.

## 0. What business is behind this data?
Before any metrics, name the business. Look at the tables and columns and ask: who pays, for what, and what does it cost to deliver?

Write:
- **Business type:** one line. ("Subscription telehealth: members pay monthly, doctors see them online.") If unsure, list the top 2 guesses and what in the data points to each.
- **How the money usually splits:** a typical revenue and cost breakdown for this kind of business, from general industry knowledge. Rough %, and say it's a typical range, not this company's numbers.

  ```
  Revenue (typical subscription telehealth)
    Membership fees ........ 60-80%
    Per-visit / add-ons .... 10-25%
    Partner / B2B deals .... 5-20%
  Costs
    Doctor time ............ 35-50%   ← biggest cost
    Getting new members .... 15-30%
    Tech + support ......... 10-20%
    Pharmacy / labs ........ 5-15%
  ```
- **Where this data fits:** for each big line above, can this data move it? Mark 💰 revenue lever, ✂️ cost lever, or — (not in the data). Name the tables/columns.
- **Revenue or cost story?** Pick which side this data can say more about, in one sentence, and why. ("Visit-level data with doctor time and no prices → this is mostly a cost story: doctor time per visit.") If both, say which is bigger in dollars.

Use this to steer everything below: the metric tree should hang off the biggest line the data can touch, and questions should target the biggest levers first.

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
- **Why it matters:** the money or patient effect if it's true. Tie it to a line from step 0 and say if it's revenue (💰) or cost (✂️). Rough size, like "about 5% of revenue" or "doctor time is ~40% of costs, so 10% fewer minutes ≈ 4% of costs".
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
Write the whole thing to `brain/01_objective.md` under `## Business model`, `## Metric tree` and `## Questions to test`.
