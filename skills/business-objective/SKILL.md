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
- **How the money usually splits:** a typical revenue and cost breakdown for **this** kind of business (the `Industry:` line), from general industry knowledge. Rough %, and say it's a typical range, not this company's numbers. The example below is telehealth; use the right one:
  - Online retail / DTC: product cost 35-55%, shipping + returns 10-20%, marketing to get customers 15-30%. Levers: repeat rate, basket size, discounts, returns.
  - Marketplace: revenue = take rate × sales volume; costs = marketing to both sides, support, payments. Levers: supply/demand balance, repeat buyers.
  - Subscription software: revenue = seats × price, minus churn; costs = sales + marketing 30-50%, hosting, support. Levers: churn, upgrades, payback on sales spend.

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

## How a strategist thinks (use in every step below)
Revenue, cost and profit are the scoreboard. The job is to explain the machine that makes the score, and what to do next. Check each idea against these:

1. **Does the next customer make money, and when?** Think per customer, not totals: what one customer brings in after every real cost (refunds, support, discounts), vs what it cost to get them, and how many months until that pays back. Profit and cash are different questions. ("$221 to get a customer who brings in $130" is not "ad costs are up". It means we pay people to shop here.)
2. **Will the revenue last?** Two companies with the same revenue are worth very different amounts if one keeps 42% of customers and the other 19%. Revenue shows the past. Who comes back shows next year. Say what today's retention means for next year's numbers.
3. **Where did the cost land?** When a change hit its own goal, ask which other number took the hit, on whose team, and how much later. (A shipping change raised profit per order, but fewer customers came back the next quarter.)
4. **Split the totals.** The same total can be healthy or alarming depending on the mix: new vs returning, product, channel, full price vs discount. Growth that came from discounts looks just like real demand in a total.
5. **Think about the next dollar, not the average.** Channels fill up: the next $10K on ads buys less than the first $10K did. Averages lead to bad budget calls.
6. **Cause or just linked?** Members spend 2.3× more. Does the program cause that, or does it attract people who already spend more? Did the sale bring new orders, or pull next month's orders forward at a lower price? Say when the data can't tell, and name the test that would.
7. **Also weigh:**
   - Can we undo it? A cheap test we can undo needs less proof than a one-way door.
   - What's actually scarce (cash, staff, doctor hours, engineering time)? A plan that ignores it won't work.
   - Too much riding on one thing. One channel bringing in 40% of new customers is a risk, even while it works.
   - What the data doesn't show: how customers react to price, and what else they could buy instead. Bring general knowledge and say it's an assumption.

Better question than "what does the data say?": **"What would have to be true for this plan to be the right one?"** Then test those things.

## 1. Metric tree
Break the goal into things the data can measure. Example for a telehealth company (build the one for this business):

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
- **Action if true:** what the company would *do* differently, and who owns that decision. If it doesn't change a decision, drop it.
- **Wrong if:** what would make this wrong, and how we'd check. (Often: it's who joins, not what we did; or a cost that shows up somewhere else.)
- **Score:** Impact (1-5) × Can we prove it in 20 min (1-5).

Rank by score. The best questions have a clear action, a big effect and a quick test.

Good kinds of questions for most customer data:
- **Who stays and who leaves** (retention by starting month, by channel, by first experience)
- **What happens before someone leaves** (the signals before they drop off)
- **Where the money is** (the few groups that bring in most of the value, and who's underserved)
- **Funnels** (where people drop off, step by step)
- **Operations** (wait times, capacity, how providers differ, and how that links to outcomes)
- **Time** (seasonality, trend breaks, and what changed and when)
- **Pricing and plan mix**

## 3. Storyline guess
One sentence: "If these hold, the story is: ___." This becomes the deck's main message later.

Then write it the way a Director would, in three lines:
- **Therefore we should** ___.
- **It's worth about** $___.
- **We'd be wrong if** ___, **and we'd check by** ___.

## Output
Write the whole thing to `brain/01_objective.md` under `## Business model`, `## Metric tree` and `## Questions to test`.
