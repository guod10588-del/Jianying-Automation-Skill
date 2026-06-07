---
name: jianying-automation
description: Automate JianyingPro/CapCut desktop video editing on Windows. Use when Codex needs to batch-cut videos, generate subtitles, match visuals to narration/script rhythm, prepare background music, export an MP4 first draft, import media into Jianying, operate Jianying via UI automation, or inspect/create/update Jianying draft project files such as draft_content.json and root_meta_info.json.
---

# Jianying Automation

## Operating Principle

Prefer the most deterministic route that fits the request:

1. Use FFmpeg/scripted preprocessing for first drafts, normalization, slicing, subtitles, audio mix, and MP4 export.
2. Use Jianying draft-file manipulation when a readable `draft_content.json` exists and the schema can be safely inferred from a nearby template draft.
3. Use UI automation for import/export, one-click Jianying effects, cloud/TTS features, or when draft files are encrypted/opaque.
4. Use specialist open-source preprocessors for ASR text-based cutting, subtitle/watermark cleanup, object removal, or AI inpainting before generating the Jianying handoff.
5. Use HyperFrames for deterministic video packaging such as title cards, chapter cards, end cards, animated maps/timelines, product callout cards, and other HTML/CSS/JS-rendered MP4 inserts.
6. Borrow pipeline/configuration ideas from MoneyPrinterTurbo for batch short-video automation, multi-version generation, material scoring, and quality reports, while keeping the user's curated local-material editing style.
7. Borrow director-style decomposition from ViMax for script analysis, storyboard-first planning, visual anchors, consistency checks, and retry loops, while continuing to use the user's real local footage.
8. Borrow OpenMontage's pipeline discipline for route selection, reference-video analysis, checkpoints, decision logs, anti-slideshow review, and quality gates, while keeping FFmpeg/Jianying/HyperFrames as the local execution stack.

Never overwrite original media. Write generated files to an output folder under the user's project directory, and keep temp files isolated.

Default visual constraint for the user's short-video work: people may appear as natural street, scene, dining, travel, or scale atmosphere. Avoid clear front-facing faces, close-up faces, talking-head/interview shots, creator subtitles, platform watermarks, account handles, logos, or burned-in captions. Prefer clean scenery, architecture, artifacts, landscapes, aerials, food closeups without clear faces, and texture/detail shots. If clean source footage is not available, use crop, sticker cover, or masked blur/mosaic as a repair step instead of leaving watermarks visible.

Default subtitle preference when the user wants captions/subtitles: match the user's Jianying preset from the screenshot: system font, Jianying font size `16`, yellow fill, bold-looking yellow text preset with black outline/shadow, center aligned, character spacing `0`, line spacing `0`, placed in the lower-middle safe area without exceeding the 9:16 frame. Prefer editable Jianying text/subtitle tracks over only burned-in subtitles. If generating an FFmpeg preview first, approximate this as large yellow text with a strong black outline and safe margins.

Do not implement "matrix deduplication" or platform-review evasion tactics such as imperceptible random noise, tiny color shifts, audio pitch/time perturbations, metadata churn, or other pixel/audio changes whose purpose is to bypass duplicate-content detection or machine review. Legitimate normalization, compression, color correction, accessibility subtitles, and substantive original edits are allowed when they improve quality or clarity.

## Quick Workflow

1. Inventory the project folder: media files, script/copy, voiceover, music, existing output, and Jianying drafts.
2. Probe durations, resolution, orientation, audio tracks, and file health with FFmpeg.
3. Screen source footage for clear faces, close-up people, subtitles, logos, account handles, and platform watermarks; exclude risky clips where possible.
4. Decide route:
   - `FFmpeg first draft`: best for reliable MP4 output.
   - `Draft JSON`: best for editable Jianying timelines when JSON is readable.
   - `UI automation`: best for Jianying-only controls, import/export, TTS, templates, effects, and encrypted drafts.
   - `HyperFrames packaging`: best for polished title cards, chapter cards, end cards, map/timeline explainers, and product/book callout inserts.
   - `MoneyPrinterTurbo-inspired batch flow`: best for configurable multi-version first cuts, material scoring, and quality reports from local assets.
   - `ViMax-inspired director flow`: best for story-heavy book-selling/history/city videos where script sections, visual anchors, and shot purposes should be planned before assembly.
   - `OpenMontage-inspired checkpoint flow`: best for larger edits, reference-style requests, or repeated-revision projects where route selection, stage artifacts, quality gates, and source-usage reports prevent drift.
5. Generate artifacts: MP4, `.ass` or `.srt` subtitles, storyboard CSV, edit plan JSON, and any normalized media. When subtitles are requested, also create/save an editable Jianying draft when the local draft route is available.
6. Validate: output duration, dimensions, audio presence, subtitles burned/importable, clean visuals, and preview frames.
7. Launch Jianying only after artifacts are ready, unless the task specifically requires live UI operation first.

## Route Selection

Use **FFmpeg first draft** when the user asks for automatic slicing, automatic subtitles, background music, rhythm matching, or MP4 export. It is stable and inspectable.

Use **draft-file generation** when the user needs an editable Jianying project and there is a readable unencrypted draft in the local Jianying draft directory. Compare with an existing draft before writing anything.

Use **UI automation** when the requested action depends on Jianying's GUI, such as `开始创作`, `导入素材`, built-in caption recognition, text styles, templates, exporting through Jianying, or cloud features.

Use **OpenMontage-inspired checkpoint flow** when the task is long, reference-driven, or has strict constraints. Run a preflight/capability audit first, choose the route, create a shot plan, render, review with concrete findings, and revise at most two automated rounds before delivering with any remaining warnings.

## Clean Visual Policy

Apply this policy by default for future edits:

- People are allowed when they are incidental atmosphere, back views, small figures, crowds without identifiable close faces, or part of a scene.
- Do not select shots with clear front-facing faces, close-up faces, talking heads, burned-in subtitles, creator handles, platform logos, or watermarks.
- Do not use source clips where existing subtitles compete with the generated narration subtitles.
- Prefer filename/path filtering first, then sample preview frames for uncertain clips.
- For watermarks near an edge, prefer crop if it does not damage the composition.
- For watermarks that cannot be cropped, use sticker/text cover when the cover can look intentional.
- For plain backgrounds, use masked blur/mosaic as a last-resort repair.
- Record any repaired clip in the storyboard so the user can review it later.

Read `references/watermark-and-clean-visuals.md` when source footage contains people, subtitles, logos, watermarks, or creator handles.

## Short-Video Automation Pattern

For city-history, book-selling, travel-history, and knowledge narration videos, use this structure by default:

- Treat automation as a pipeline: script/voiceover -> material inventory -> material scoring -> story-to-visual matching -> render -> preview contact sheets -> quality report.
- Before rendering, think like a director: analyze the script, choose visual anchors, create a shot plan, assemble, review, and retry if preview frames reveal problems.
- Prefer the user's local素材 over online stock素材.
- Generate multiple variants when useful: steady, faster-paced, and sales-ending-focused.
- Keep all house rules: default 9:16, no subtitles unless requested, no BGM unless requested, image clips max 3 seconds, single video source max 1 minute or 10% of total duration, avoid clear faces/watermarks.
- Do not copy generic one-click stock-video style; preserve curated book-selling/history editing.
- For larger or reference-style edits, keep checkpoint artifacts: `edit_plan.json`, `storyboard.csv`, `source_usage.json`, `quality_report.json`, preview frames/contact sheets, and optional `decision_log.json`.
- Review every cut for anti-slideshow quality: every shot needs a purpose, adjacent shots should vary subject/scale/location, and repeated sources should be flagged before delivery.

Read `references/moneyprinterturbo-lessons.md` when designing batch generation, multi-version outputs, material scoring, or automated quality reports.
Read `references/vimax-lessons.md` when designing director-style script analysis, storyboard fields, visual anchors, consistency checks, or automatic re-plan/re-render loops.
Read `references/openmontage-lessons.md` when designing route selection, reference-video analysis, checkpoint artifacts, decision logs, anti-slideshow checks, or stage-by-stage quality review.

## Subtitle Style Policy

Apply this policy by default when subtitles are requested:

- Use Jianying editable subtitles/text where practical, not just burned-in preview text.
- Style: system font, Jianying size `16`, yellow fill, black outline/shadow, centered alignment, character spacing `0`, line spacing `0`.
- Use the yellow preset style shown by the user: yellow `T` style with dark outline/background contrast.
- Keep subtitles in the lower-middle safe area and wrap lines so text never exceeds the video frame.
- Save the Jianying draft after adding subtitles so the user can adjust it manually in Jianying.
- 中文约定：有字幕任务时必须尽量在剪映里保存草稿，字幕轨道保持可编辑，方便用户后期继续调整。

## Open-Source Tool Routes

Use open-source libraries only after checking the local environment, license/usage fit, model weights, GPU needs, and whether the user has rights to edit the source footage.

Common choices:

- `pyJianYingDraft` or similar Jianying draft libraries: generate readable `draft_content.json` and draft folders from code.
- `AutoCut`/ASR text editing: transcribe speech, remove filler words or unwanted text spans, and export a cut timeline/project.
- `Video Subtitle Remover`/subtitle removal tools: remove hard subtitles or text overlays before the Jianying stage.
- `ProPainter`, `E2FGVI`, or similar video inpainting models: remove masked objects, logos, people, or watermarks when clean replacement footage is unavailable.
- `Inpaint-Anything`/SAM workflows: create masks through click/segment prompts, then remove objects or text from images/videos.

Preferred architecture for advanced cleanup:

```text
raw video
  -> specialist cleanup/inpainting tool
  -> clean intermediate video
  -> FFmpeg normalization and subtitles
  -> Jianying draft generation or UI import
  -> human review/export in Jianying
```

Read `references/open-source-routes.md` before installing or wrapping any GitHub project.

## HyperFrames Packaging Flow

Use HyperFrames after the main visual cut is assembled and before final concat/remux:

```text
script + voiceover + source footage
  -> FFmpeg first draft with clean 9:16 visual cut
  -> HyperFrames title/chapter/end-card MP4 inserts
  -> FFmpeg concat and audio remux
  -> Jianying review/export if needed
```

Default use cases:

- 2-4 second title cards, for example `洛阳｜十三朝古都`.
- Chapter cards between narration sections.
- Map, route, dynasty timeline, or key concept explainer cards.
- Book/product recommendation cards and end cards.
- Branded covers for watermark repair only when the user approves a visible cover.

Do not add sentence-by-sentence subtitles through HyperFrames when the user requested no subtitles.

Read `references/hyperframes-packaging.md` before using HyperFrames.

## Draft Safety

Before touching Jianying draft files:

- Locate draft roots from `root_meta_info.json` and the Jianying user data directory.
- Copy any target draft folder to a timestamped backup before editing.
- Treat unreadable/base64/encrypted `draft_content.json` as opaque. Do not invent a replacement unless the user explicitly wants an experimental draft.
- If the schema is readable, preserve unknown keys, IDs, material references, and timing units. Make minimal structured edits.
- Re-open Jianying only after writing the draft and updating root metadata consistently.

Read `references/draft-files.md` when working with draft folders or JSON.

## UI Automation

Use UI automation conservatively:

- Prefer keyboard shortcuts over coordinates where possible.
- Use image/template matching for buttons that have stable visual labels.
- Add pauses after opening dialogs, importing files, and starting export.
- Verify each major state with screenshot or window text before proceeding.
- Avoid destructive clicks in existing projects unless the user explicitly asked for that operation.

Read `references/ui-automation.md` before controlling Jianying through PyAutoGUI, Pywinauto, or Appium.

## FFmpeg Hybrid Flow

For book-selling, narration, documentary, city-history, or similar short-video projects:

1. Extract the final narration from the copy file.
2. Split copy into narrative sections: hook, question, history, people/events, evidence, process/material logic, book value, and final conversion.
3. Select 3-5 visual anchors for the project, such as city aerial, core landmark, artifact/detail, process scene, and book/page visuals.
4. Probe voiceover duration and build shot windows from narrative sections.
5. Filter out risky source clips by filename/path and, when practical, by sampled preview frames. Do not reject a clip only because it contains incidental people; reject it when clear faces, close-up faces, interviews, subtitles, logos, or watermarks dominate.
6. Build a storyboard/shot plan with shot purpose: establish, evidence, detail, atmosphere, contrast, or book/product return.
7. Pick visuals by narrative intent and category, then enforce anti-repetition rules across source, category, and subject.
8. Normalize visuals to target orientation, usually `1080x1920` for vertical video.
9. Mix narration with low-volume background music only when requested.
10. Burn subtitles for preview MP4 only when useful, export editable `.ass` or `.srt`, and create/save a Jianying draft with editable subtitles when available.
11. Save storyboard CSV or shot plan JSON with timeline start/end, script section, shot purpose, source path, source offset, category, and risk notes.
12. Generate contact sheets and re-plan/re-render if the review shows repeated images, repeated subjects, weak opening, bad crop, subtitles/watermarks, or clear face closeups.

Use `scripts/make_jianying_first_draft.py` as a starting point for this route. Patch it for project-specific keywords, target size, music, or style.

## Validation Checklist

Always verify these before saying the task is done:

- MP4 exists and has nonzero size.
- Duration matches the voiceover or requested target.
- Video dimensions and orientation match the platform.
- Audio stream is present.
- Captions are visible or subtitle sidecar exists. If subtitles were requested, verify the style follows the Jianying size-16 yellow preset and does not exceed the frame.
- Storyboard/edit plan exists when automatic rhythm matching was requested.
- Storyboard or shot plan includes narrative section, shot purpose, source/category, and risk notes for story-heavy edits.
- Source usage report exists for automated first cuts, including image duration limits and top repeated sources.
- Quality report or review notes exist for larger edits, reference-style edits, or any task with strict constraints such as no subtitles, no BGM, opening-clip requirements, source-usage caps, or saved Jianying drafts.
- Preview contact sheets exist for opening and full-video sampling.
- Preview frames do not show clear close-up faces, creator subtitles, platform watermarks, or account handles. Incidental people are acceptable when they are not the focus.
- Jianying has been launched only if requested or useful for the next manual step.

## Common Paths

Common Jianying executable:

```text
D:\JianyingPro\JianyingPro.exe
```

Common local draft metadata:

```text
C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft\root_meta_info.json
```

Some installations store actual draft folders elsewhere, often under a configured root such as:

```text
D:\剪映预保存\JianyingPro Drafts
```
