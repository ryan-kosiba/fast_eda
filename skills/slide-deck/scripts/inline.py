#!/usr/bin/env python3
"""Make deck/dashboard HTML files fully self-contained (no internet needed to show charts).

Usage:
  python3 inline.py output/deck.html [output/dashboard_main.html ...]

Swaps the Chart.js CDN <script src> for the copy in ../vendor/, inline. Safe to run twice.
Fonts fall back to system fonts and the logo falls back to text when offline, so they stay as links.
"""
import re
import sys
from pathlib import Path

VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "chart.umd.min.js"
CDN = re.compile(r'<script src="https://[^"]*chart\.umd\.min\.js"></script>')


def main(paths):
    js = VENDOR.read_text()
    for p in map(Path, paths):
        html = p.read_text()
        new, n = CDN.subn(lambda _: "<script>/* Chart.js 4.4.1, inlined */\n" + js + "\n</script>", html)
        if n:
            p.write_text(new)
            print(f"{p}: Chart.js inlined ({p.stat().st_size // 1024} KB)")
        elif "Chart.js 4.4.1, inlined" in html:
            print(f"{p}: already self-contained")
        else:
            print(f"{p}: !! no Chart.js script tag found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
