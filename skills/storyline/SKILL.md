---
name: storyline
description: How the Manager builds the story WITH the human, grounded in what the agents actually found. It checks in as results arrive, confirms every claim against its evidence, re-confirms when numbers change, and makes sure the presenter truly understands the story before any slide is built. Use from the first findings until the deck is approved.
---

# Storyline skill (the Manager does this with the human, never alone)

**Two gates before any slide gets built. Both live in `brain/06_story.md`:**
- `Story: approved vN`: the human agrees with the story
- `Presenter understands: yes`: the human confirmed they can explain it and defend it

The human is presenting, so it's their story. You're the editor who keeps it honest.

---

## Stage 1: Story so far (during Phase 3, each time an Analysis agent returns)
Don't wait until the end. Each time findings come back, update `06_story.md` (`Status: forming`) and give the human a **3-line check-in**:
```
New: <finding in plain words, one number> (confidence: high/med/low)
Story so far: <one sentence where the story is heading>
Question: <keep going this way / dig deeper on X / drop Y?>
```
Ask with `AskUserQuestion` only when their answer changes what the agents do next. Otherwise just inform.

## Stage 2: Draft from the evidence (after the analysis and the first fact check)
Read `01_objective.md`, `03_findings.md` and `07_fact_check.md`. Every claim in the story must point to a finding **and** its fact-check status.

```markdown
# Story
Status: draft v1
Story: not approved
Presenter understands: not yet

## Big message (one sentence a CEO would repeat)
We lose half of new members in 90 days, and a 7-day follow-up is the cheapest fix, worth about $1.2M a year.

## The ask
Approve a 60-day test of automatic follow-ups.

## Flow
| # | Slide title (takeaway sentence) | Evidence | Checked? | Chart idea | Side panels |
|---|---|---|---|---|---|
| 1 | Title + date + presenter + attendees | - | - | - | - |
| 2 | Agenda: "Three things: the problem, the cause, the fix" | - | - | numbered list | - |
| 3 | Half of new members are gone by day 90 | F1: 51% (n=4,210) | ✅ PASS | line by starting month | by plan |
| 3 | A 7-day follow-up doubles who stays | F2: 62% vs 31% | ⏳ pending | bar, highlight | by plan, trend |

## Left out (and why)
- F3: real but small ($40K) → appendix

## Weak spots
- F2 is a link, not proof it causes it → the ask is a test, not a rollout

## Tough questions + answers
1. "Is it causal?" → No. Engaged people may ask for follow-ups. That's why we propose a test.
```

Structure (tell them what you'll say → say it → tell them what you said):
- **Intro:** the title slide, then an **agenda slide** that states the big message and the 3 main points up front.
- **Body:** the findings, each framed as **value to the company** (what it's worth, what to do), not "what I analyzed".
- **Close:** a short **summary** slide that repeats the 3 points, plus the ask. End on the ask, not on "Questions?".
- **Pacing:** main slides ≈ the talk length in minutes (about one per minute; about one per 30 seconds for a quick 5-minute talk). Count only main slides. Side panels, the dashboard and the appendix are backup for Q&A. Get the time limit from `01_objective.md` → Presentation details, and ask the human if it's missing.
- **Company fit:** tie the ask to the company's goals and current challenges (`01_objective.md` → Company context).

Rules:
- **Answer first.** The big message and the ask come first, then the proof. Shape: situation → problem → why → what to do → what it's worth.
- 3 strong findings beat 6. A finding that doesn't support the big message goes to the appendix.
- Titles are full sentences with a number. Someone who reads only the titles should get the story.
- **Never stretch a number to fit the story.** If the evidence is weaker than the wording, soften the wording.
- A slide built on a ❌ FAIL finding can't stay as is. Fix it or cut it.

## Stage 3: Confirm the story with the human
Show it in **at most 14 lines**, with the evidence on every line:
```
Big message: <one sentence>
Ask: <one sentence>
Flow:
 2. <title>: F1 51% ✅
 3. <title>: F2 62% vs 31% ⏳
 ...
Left out: <F#s>
Weakest point: <one line>
```
Ask with `AskUserQuestion`: **"Does this story match what you'd want to say?"**
- "Yes, now check I've got it" → go to Stage 4
- "Change the order or what's in"
- "Change the big message"
- "Walk me through it slide by slide" → one slide at a time: title / evidence / caveat, then "Keep / change / cut?"

Loop: update the file (v2, v3…), show only what changed, and ask again. Log every decision in `04_decisions.md`.

## Stage 4: Make sure the presenter understands (required, about 5 min)
The goal: the human can explain every slide in their own words, and handle the tough questions. Give them a **presenter brief**, one block per slide, in plain words:
```
Slide 3: "A 7-day follow-up doubles who stays"
 What it means: People who got a call within a week were twice as likely to still be around 3 months later.
 How we know: We compared 4,210 new members: 1,700 got a follow-up, 2,510 didn't. We counted who was still active on day 90.
 Watch out: It's a link, not proof. Say "linked to", not "causes".
```
Then ask with `AskUserQuestion`: **"How do you want to check you've got it?"**
- "Quiz me with 3 tough questions" (Recommended) → ask them one at a time, wait for the human's answer in plain text, then give quick feedback: ✅ good, or a better one-line answer.
- "Let me explain the big message back" → the human types it, and you check it matches the evidence and point out anything missing or overstated.
- "I've got it, skip the check"
- "Explain slide # again"

When the human is confident, set `Presenter understands: yes` and log it.

## Stage 5: Approve, and re-confirm if anything changes
- Both gates are passed: set `Story: approved vN` and start the Slides agent with "Build exactly this story."
- **After approval, if a number changes** (a fact-check FAIL, a late finding, a dashboard mismatch): stop, show the human the change in 2 lines ("Slide 3 was 62% vs 31%, and is now 58% vs 33%. The message still holds / needs softening"), and get a yes before the deck changes. Bump the version.
- **Clock:** if it's past minute 72 and the gates aren't passed, say in one line: "We're at minute X. Build from v<N> now and keep checking your understanding while it builds?"
