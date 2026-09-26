---
name: slide-deck
description: Builds a clean single-file HTML slide deck from checked findings. Slides always fit the screen, side slides (right/left) hold breakdowns, and "Jarvis" voice commands drive it in Chrome. Use when it's time to present results.
---

# Slide Deck skill

Template: `FE/skills/slide-deck/template/deck.html`. Brand: `FE/skills/slide-deck/brand.md`.

## Step 1: Build from the approved story (`brain/06_story.md`)
The Manager and the human write the story (the `storyline` skill). **No HTML until it says `Story: approved` and `Presenter understands: yes`.** Build it as written. The usual shape (for reference). **Main slide count ≈ talk length in minutes** (see the story):

1. **Title.** The big message, date, presenter, attendees.
2. **Agenda.** "Tell them what you'll say": the 3 main points, numbered.
3. **Context.** What the business looks like now (one chart).
4-7. **One finding per main slide.** The title is the takeaway sentence, not a topic ("Follow-ups double retention", not "Follow-up analysis"). Breakdowns, splits and "does it hold for every group" go in **side panels to the right**.
8. **Recommendations.** 3 moves, ranked, each with its size (the value to the company).
9. **Summary + the ask.** "Tell them what you told them": the 3 points again in one line each, then the ask. It's the last main slide.
9b. **Dashboard** (if `brain/08_dashboard_brief.md` says agreed): placed where the brief says.
10. **Appendix.** Method, data quality, caveats (side panels for detail).

Each finding slide = one message, one chart, one callout. At most about 40 words of body text.

## Step 2: Build `output/deck.html`
1. `cp FE/skills/slide-deck/template/deck.html WORK/output/deck.html`
2. Replace everything between `<!-- SLIDES:BEGIN -->` and `<!-- SLIDES:END -->` with your slides.
3. Replace the `CHARTS = {...}` object with real chart data (copy from `output/analysis/*.json`).
4. Change `<title>`. **Don't touch the ENGINE parts.**

### Building blocks (already styled)
| Need | Use |
|---|---|
| Main slide | `<section class="slide" data-title="Short name" data-keywords="words for voice go-to">` |
| Side slide | another `<div class="panel">` inside the same section. Add `<div class="hint-right">Breakdown →</div>` on the panel before it |
| Dark title slide | `<div class="panel title">` + kicker + `<h1>` big message + `.sub` + the `title-meta` block: `<div class="title-meta"><div><span>Date</span>…</div><div><span>Presented by</span>Ryan Kosiba</div><div class="grow"><span>Attendees</span>Name (Role) · …</div></div>`. The values come from `01_objective.md` → Presentation details |
| Section divider | `<div class="panel section">` with `<h1>` |
| Small label above title | `<div class="kicker">Finding 2</div>` |
| Takeaway title | `<h2>` |
| Content area (fills the rest) | `<div class="body">` |
| Two columns | `<div class="cols">` (or `cols wide-left` / `cols wide-right`), `cols3`, `cols4` |
| Stat tile | `<div class="card kpi"><div class="v">31%</div><div class="l">label</div><div class="d up">▲ note</div></div>` |
| Giant number | `<div class="big-number">2×</div>` |
| Highlight box | `<div class="callout">` (or `callout warn` for bad news) |
| Agenda | `<div class="rec"><div class="n">1</div><div><h3>The problem: …</h3></div></div>` × 3 (h3 only, no paragraph) |
| Recommendation | `<div class="rec"><div class="n">1</div><div><h3>…</h3><p>…</p></div></div>` |
| Table | `<table class="t">` with `class="num"` on number cells, `<tr class="hl">` to highlight a row |
| Chart | `<div class="chart"><canvas data-chart="my_id"></canvas></div>` + `CHARTS.my_id = {...}` |
| Source line | `<div class="source">n = …, dates …</div>` |
| Dashboard slide | `<div class="panel dashboard">` + `<div class="dash" data-dash="main"></div>`. The data comes from the Dashboard agent via `FE/skills/dashboard/scripts/inject.py`. Keep the `DASHBOARDS:BEGIN/END` markers |
| Speaker notes | `<aside class="notes">what to say</aside>` (N key) |

Chart spec: `{chart:"bar"|"hbar"|"line"|"stacked"|"scatter", x:[...], series:[{name, values, format:"pct"|"usd"|"num", color?}], highlight?: index, legend?: bool, yLabel?, xLabel?}`. Percentages are stored as decimals (0.31).

### Design rules
- **Keep it simple.** One idea per slide. Clean charts, the brand colors, lots of white space. No clutter, no extra transitions (the engine's subtle fade is enough), no clip art.
- **Bullets are prompts, not a script.** At most 4 bullets, each 8 words or fewer. The full wording goes in `<aside class="notes">` (the presenter brief). Nothing on a slide should be read out word for word.
- **Everything fits.** The stage is a fixed 1600×900 and scales to any screen. If a panel overflows, the engine shrinks it (down to 70%) and logs a warning. Treat that warning as a signal to cut words or split the content into a side panel.
- **Bright blue = the point.** Use `highlight` on the bar that proves the finding. Everything else is grey.
- **Titles are sentences with a number when possible.**
- **Plain language**, following the communication-style skill. No acronyms on slides.
- **Every number must be in `brain/03_findings.md` marked PASS in `brain/07_fact_check.md`.**
- Good `data-keywords` make voice "go to" work. Add 2-4 words the presenter would naturally say ("retention", "pricing", "recommendations").

## Step 3: Check it
- Syntax check: `python3 -c "import html.parser,sys; html.parser.HTMLParser().feed(open('WORK/output/deck.html').read())"`
- If Chrome or Chromium is on the machine, take a headless screenshot of a few slides to eyeball them:
  `"<chrome>" --headless=new --screenshot=output/shot1.png --window-size=1600,900 "file://WORK/output/deck.html#2.1"`
- Open `deck.html?check`: overflowing slides get an orange outline.

## Presenting (tell the human)
- Serve it: `cd output && python3 -m http.server 8765`, then open `http://localhost:8765/deck.html` in Chrome. Press **V**, allow the mic, press **F** for fullscreen.
- Voice: say "Jarvis" then talk normally: "next", "go back", "show me more", "go back to the first slide", "take me to the recommendations", "slide 3", "back out", "show notes", "stop listening", "zoom in on the retention chart", "make chart 2 bigger", "zoom out". A top-left label shows what it heard (set `showTranscript: false` for the real talk).
- Test the voice parser: `node FE/tests/test_voice.js output/deck.html`
- Keys: ↓/Space next, ↑ back, → ← side slides, G menu, N notes, Z zoom the first chart, Esc close, 1-9 jump. Click any chart to zoom it.
- Give every chart a `title` in its CHARTS spec, so "zoom in on the ___ chart" can find it by name.
- To change the wake word, edit `DECK_CONFIG.wakeWord` and `wakeAliases`.
