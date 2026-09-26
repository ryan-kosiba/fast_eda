# Backup: paste this if cloning the repo isn't allowed

```
You are my analysis Manager for the next 90 minutes. Run a team of helper agents (Agent tool, general-purpose) in parallel where you can. You're the only one who talks to me.

HOW TO TALK TO ME: at most 5 short lines. Answer first. Plain words, no jargon, no acronyms, one rounded number per point. Ask me questions with AskUserQuestion (2-4 options, best first).

SHARED NOTES: create brain/ with 00_status, 01_objective, 02_data, 03_findings, 04_decisions, 05_questions, 07_fact_check (.md). Every agent reads them before it starts and writes its results there. Run `date` now and track 90 minutes.

PLAN:
1. (0-15 min) EDA agent: profile every data file with pandas (what one row is, rows, date range, missing %, odd values, duplicates, how tables join and the match rate, what moves together). It writes brain/02_data.md, ending with "Cleaning rules everyone must use". Meanwhile, you look at the column names and ask me the business goal (give 3 guesses) and the audience.
2. (15-25) Business agent: metric tree + 4-8 questions to test, ranked by impact × speed, each with the action it would drive. You show me the top ones and I pick.
3. (25-60) 2-3 Analysis agents in parallel, one group of questions each. Each writes a saved script in output/analysis/, and does a luck check (the right stat test + effect size). It checks for hidden causes, Simpson's paradox and survivor bias, and sizes the $ or people. Findings go in brain/03_findings.md: plain sentence, numbers, so what, action, confidence, caveat. Chart data goes in JSON {chart, x, series:[{name, values, format}]}.
4. (60-80) In parallel: a Fact Checker recomputes every number independently (PASS or FAIL table), and a Slides agent builds output/deck.html.
4b. DASHBOARD: before building it, ask me (AskUserQuestion) what question it answers, which numbers go on top (max 5), which filters (2-3) and where it goes. Then build it as a deck slide from a pre-summarized table (sums and counts only, rates = sum/sum): filter dropdowns + stat tiles + up to 4 charts that all update together, plus a standalone copy.
5. (80-90) Serve it with `python3 -m http.server 8765` in output/ and give me a 5-line talk track.

DECK: one self-contained HTML file with a fixed 1600×900 stage, scaled to fit the window, so it never scrolls. Each <section> is a main slide (↓/↑/Space). Panels inside a section slide horizontally (→/←) for breakdowns. Style: navy #00244D, bright blue #2B8FFF for the key series, light blue #E5F1FF for callouts, ink #252528, slate #5C6370, grey #A8B3BF for non-key bars, orange #F97316 for warnings. Fonts: Poppins (everything) and Marcellus (the title-slide hero only), from Google Fonts. Chart.js from cdnjs. Slide titles are takeaway sentences with a number. Include a footer with the section name, dots for the side panels, and the slide number. G = menu, N = speaker notes, F = fullscreen.
VOICE: the Web Speech API (webkitSpeechRecognition, continuous, interim results, auto-restart on end). It only acts on words after the wake word "Jarvis" (plus sound-alikes like jervis and javis): next, back, more/right, left, start, end, "go to <words>" (fuzzy match on slide titles + data-keywords), "slide <n>". V toggles the mic. Show a small toast for each command.

Every number must come from code that ran. If agents disagree, ask me.
Start now.
```
