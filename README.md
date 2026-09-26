# fast_eda

A team of Claude Code agents that turns a dataset into **checked findings** and a **clean voice-controlled slide deck** in about 90 minutes.

## Use it (say this to Claude Code, in the folder with the data)

> Clone https://github.com/ryan-kosiba/fast_eda into ./fast_eda, then read fast_eda/START.md and follow it.

That's it. The Manager takes over, asks you 2-3 quick questions, and runs the team.

Plugin install (optional): `/plugin marketplace add ryan-kosiba/fast_eda`, then `/plugin install fast-eda@fast-eda`, then `/fast-eda:fast-eda`.

## The team

| Agent | Job |
|---|---|
| **Manager** (the main session) | Runs the plan, keeps the clock, keeps the `brain/` notes, the only one who asks you questions |
| **EDA** | Profiles every file: missing data, odd values, how tables connect, what moves together |
| **Business** | Turns your goal into metrics and a ranked list of questions worth testing |
| **Analysis** (2-3 in parallel) | Tests the questions with real code and stats |
| **Dashboard** | Builds a filterable dashboard inside the deck (plus a standalone file). The Manager asks you what it should show first |
| **Fact Checker** | Re-computes every number from scratch before it goes on a slide |
| **Slides** | Builds `output/deck.html` in a clean, consistent style |

The **communication-style** skill keeps every message to you short and plain.

## Flow

```
 0-3   Setup           install.sh → brain/ + output/
 3-15  Look + ask      EDA agent  ‖  Manager asks you the business goal
15-25  Plan            Business agent → you pick the questions
25-60  Dig             Analysis agents ‖ ‖  → brain/03_findings.md
~50    Dashboard brief Manager asks you: what question, which numbers, which filters
60-80  Build + check   Slides ‖ Dashboard ‖ Fact Checker → output/deck.html
80-90  Land it         serve deck, 5-line talk track
```

## The deck
- One HTML file. It always fits the screen (1600×900 stage, scaled to fit).
- ↓/↑ = main slides. →/← = side slides with breakdowns.
- **Voice (Chrome):** press **V**, then say "Jarvis next", "Jarvis back", "Jarvis more", "Jarvis go to recommendations", or "Jarvis slide 3".
- **Dashboards** inside the deck: filters, stat tiles and charts update together. "Jarvis, filter Premium" or "Jarvis, clear filters".
- G = menu, N = speaker notes, F = fullscreen.
- Demo: `open skills/slide-deck/template/deck.html`

## Files
```
START.md                 Manager playbook (the entry point)
PASTE_PROMPT.md          backup: one prompt to paste if cloning is not allowed
install.sh               sets up brain/, output/, .claude/ in the data folder
agents/                  one file per helper agent
skills/                  eda, business-objective, deep-analysis, dashboard, fact-check, slide-deck, communication-style, fast-eda
tests/test_voice.js      voice command tests: node tests/test_voice.js
brain_template/          the shared notes every agent reads and writes
```
