# MoneyPrinterTurbo Lessons For Jianying Automation

Use this reference when improving the user's short-video automation workflow after reviewing `harry0703/MoneyPrinterTurbo`.

## What To Borrow

- Pipeline thinking: topic/script -> voiceover -> media inventory -> visual matching -> subtitles -> BGM -> render -> review.
- Configuration-first editing: expose stable choices for aspect ratio, shot duration, subtitle style, BGM volume, source limits, image limits, and output variants.
- Multi-version generation: when useful, create 2-3 first-cut variants such as steady, faster-paced, and sales-ending-focused.
- Batch/report workflow: generate storyboard CSV, source-usage JSON, preview contact sheets, and a short quality report for each output.
- Subtitle timing options: prefer true audio timestamps when available; otherwise use script-length timing as a preview fallback.
- Local material support: prefer the user's curated local footage over generic online stock footage.

## What Not To Copy

- Do not copy generic "one-click topic to video" style when the user has provided curated city/history/book-selling materials.
- Do not over-rely on online stock footage; use the user's folders first.
- Do not produce random BGM, subtitles, title cards, or AI text unless the user asks.
- Do not optimize for platform-review evasion or duplicate-content tricks.
- Do not let automation override the user's house rules: 9:16 by default, no subtitles unless requested, yellow Jianying size-16 subtitles when requested, no BGM unless requested, people allowed as atmosphere, avoid clear faces/watermarks, image clips max 3 seconds.

## Skill Upgrades To Keep

1. Material scoring:
   - Classify each source as opening shot, city aerial, street atmosphere, artifact/detail, book/reading, process/craft, history/person, night scene, or risky.
   - Prefer high-impact shots for the first 3 seconds.
   - Down-rank clips with burned-in subtitles, platform marks, strong logos, obvious face closeups, or poor framing.

2. Story-to-visual matching:
   - Match script sections to source categories instead of only rotating filenames.
   - Use big view -> evidence/detail -> atmosphere rhythm inside each major section.
   - Return to book/product visuals near the ending for book-selling videos.

3. Multi-version first cuts:
   - `steady`: 6-10 second shots, calmer documentary rhythm.
   - `fast`: 3-6 second shots, more visual changes.
   - `sales-focus`: stronger opening hook and stronger final book/product return.

4. Parameter profile:
   - Default aspect ratio: 9:16, 1080x1920.
   - Default subtitles: off.
   - Requested subtitles: Jianying system font, size 16, yellow fill, black outline/shadow, centered, safe lower-middle placement.
   - Default BGM: off.
   - Image clip limit: max 3 seconds per image.
   - Video source limit: max 1 minute or 10% of total duration, whichever is smaller.
   - Avoid consecutive same-category shots unless the story needs a deliberate montage.

5. Quality report:
   - Output duration and aspect ratio.
   - Audio presence.
   - Subtitle/BGM status.
   - Image usage and max image duration.
   - Top source usage and repeated-source warnings.
   - Contact-sheet preview paths.
   - Risk notes for visible faces, burned-in subtitles, logos, or watermarks.

## Preferred Direction

Treat MoneyPrinterTurbo as an engineering reference for automation structure, not as an editorial style target. The user's videos should still feel like curated book-selling/history shorts built from their own local materials, with deliberate visual matching and low repetition.
