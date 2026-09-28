---
name: fast-eda
description: Start a fast_eda run. Turns data files into checked findings and a clean slide deck with voice control, using a team of helper agents. Use when the human says "get started", "run fast_eda", "pre-brief", or hands over a dataset to analyze.
---

# fast-eda (entry point)

1. Find the fast_eda folder (`FE`, the one with `START.md`). Check, in order: `./.fast_eda`, `./fast_eda`, `~/fast_eda`, `${CLAUDE_PLUGIN_ROOT}` (from the plugin root, go two levels up from this file). If none, run: `git clone --depth 1 https://github.com/ryan-kosiba/fast_eda.git ./.fast_eda`. If that fails (no network), tell the human right away and use `PASTE_PROMPT.md` from them instead.
2. Read `FE/START.md` and follow it. You are the Manager.
3. Read `FE/skills/communication-style/SKILL.md`. Every message to the human follows it.
