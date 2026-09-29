# Brand tokens (default theme)

A clean, neutral theme. If the task names a company, put its name in the footer (`<span class="logo-text">`) and on the title slide. Only swap these colors if the human asks for a specific brand.

| Token | Value | Use |
|---|---|---|
| Navy (primary) | `#00244D` | Titles, title-slide background, main chart series |
| Bright blue | `#2B8FFF` | Highlights, the "hero" data series |
| Light blue fill | `#E5F1FF` | Callout boxes, highlighted table rows |
| Ink | `#252528` | Body text |
| Slate | `#5C6370` | Secondary text, captions, sources |
| Surface | `#F6F8FA` | Page background behind slides, card fill |
| Line | `#E1E6EC` | Borders, gridlines |
| Orange accent | `#F97316` | Use sparingly: "watch out" or negative callouts |
| Teal | `#359797` | Extra chart series, "good" callouts |
| Soft blue | `#9DC9FF` | Extra chart series, "comparison" bars |
| Grey | `#A8B3BF` | "Other" or "before" bars (de-emphasized) |

**Font** (Google Fonts, falls back to system fonts offline): **Poppins** 400/500/600/700 for everything. The title-slide hero line uses Poppins 600.

**Shape:** rounded corners 8px on cards, 9999px (pill) on tags and buttons. Lots of white space. Flat, no heavy shadows. At most one soft shadow on cards.

**Logo:** text only: the company name in blue #2B8FFF, Poppins 600. No image files, so the deck stays self-contained.

**Chart rules:** the one series that proves the point = bright blue. Everything else = grey or soft blue. Navy for the "total" or the main line. No 3D, no pies with more than 3 slices.
