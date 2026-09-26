# Brand tokens (default theme)

| Token | Value | Use |
|---|---|---|
| Navy (primary) | `#00244D` | Titles, title-slide background, main chart series |
| Bright blue | `#2B8FFF` | Buttons on their site, highlights, the "hero" data series |
| Light blue fill | `#E5F1FF` | Callout boxes, highlighted table rows |
| Ink | `#252528` | Body text |
| Slate | `#5C6370` | Secondary text, captions, sources |
| Surface | `#F6F8FA` | Page background behind slides, card fill |
| Line | `#E1E6EC` | Borders, gridlines |
| Orange accent | `#F97316` | Use sparingly: "watch out" or negative callouts |
| Teal | `#359797` | Extra chart series, "good" callouts |
| Soft blue | `#9DC9FF` | Extra chart series, "comparison" bars |
| Grey | `#A8B3BF` | "Other" or "before" bars (de-emphasized) |

**Fonts** (Google Fonts):
- **Poppins** 400/500/600/700: everything (their site uses Poppins for both titles and body)
- **Marcellus**: only the big hero line on the title slide and section dividers (their site uses it as the "hero" font)

**Shape:** rounded corners 8px on cards, 9999px (pill) on tags and buttons. Lots of white space. Flat, no heavy shadows. At most one soft shadow on cards.

**Logo:** loaded from `(none)`, with a text fallback ("brand" in blue #2B8FFF, Poppins 600).

**Chart rules:** the one series that proves the point = bright blue. Everything else = grey or soft blue. Navy for the "total" or the main line. No 3D, no pies with more than 3 slices.
