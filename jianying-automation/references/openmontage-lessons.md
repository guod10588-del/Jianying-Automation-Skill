# OpenMontage Lessons for Jianying Automation

OpenMontage is useful as a workflow reference, not as a code dependency for the
current Jianying workflow. Keep the user's local footage and Jianying/FFmpeg
pipeline as the execution base, and borrow only the production discipline below.

## What to Borrow

1. Pipeline selection before editing
   - Classify the request before cutting: local footage first cut, subtitle draft,
     no-subtitle clean montage, reference-style remake, multi-version batch cut,
     cleanup/review pass, or Jianying editable draft.
   - Announce important user-visible choices such as subtitles, BGM, opening clip,
     render path, and whether a Jianying draft will be saved.

2. Preflight and capability audit
   - Inventory scripts, voiceover, video, image, music, existing drafts, and prior
     outputs before rendering.
   - Probe duration, resolution, orientation, audio, frame rate, and health.
   - Check available execution paths: FFmpeg, Jianying draft files, Jianying UI,
     HyperFrames, and specialist cleanup tools.
   - If a requested path is unavailable, state the gap and use the next stable path.

3. Reference-video analysis
   - When the user provides a reference video or says "make it like this", analyze
     the reference before proposing cuts.
   - Capture five aspects: subject, subject motion, scene/overlays, spatial framing,
     and camera. Also note pacing, transitions, text style, color, and music use.
   - Do not carbon-copy the reference; keep the useful rhythm/style while changing
     topic, material, structure, or visual treatment enough to feel original.

4. Stage checkpoints
   - For larger book/history/city videos, treat editing as staged work:
     intake -> inventory -> script sections -> shot plan -> assembly -> review ->
     revise -> delivery.
   - Save small artifacts so the work can resume and be audited:
     `edit_plan.json`, `storyboard.csv`, `source_usage.json`,
     `quality_report.json`, preview frames/contact sheets, and optional
     `decision_log.json`.

5. Reviewer gate
   - Review the produced artifact, not the intention.
   - Findings must point to a concrete source, timestamp, frame, report field, or
     user requirement.
   - Critical issues should include a concrete fix or trigger one more re-plan.
   - Do not keep looping forever; after two automated revision rounds, deliver with
     clear warnings if unresolved problems remain.

6. Anti-slideshow and anti-repetition checks
   - Each shot should have a purpose: establish, evidence, detail, atmosphere,
     contrast, transition, or book/product return.
   - Flag repeated adjacent subject/scale/location, long static holds, decorative
     visuals with no narrative function, and overuse of the same image/video.
   - Enforce the user's house limits: image clips max 3 seconds; one source max
     1 minute or 10% of total duration, whichever is smaller, unless the user
     explicitly overrides it.

7. Runtime split
   - Use FFmpeg for deterministic first cuts, normalization, audio muxing, and MP4
     previews.
   - Use HyperFrames for title cards, chapter cards, maps, timeline explainers,
     product/book cards, and other designed inserts.
   - Use Jianying draft generation or UI automation when the user needs editable
     subtitles, Jianying presets, final manual polish, or a saved Jianying project.

## Quality Gate for Future Edits

Before saying a cut is done, check:

- Output exists, opens, and matches requested duration and 9:16 dimensions.
- Subtitle and BGM state matches the user request exactly.
- If subtitles are requested, style matches the Jianying size-16 yellow preset and
  stays inside the safe area.
- Opening 3 seconds have motion and a clear visual hook, unless user asked for a
  calm opening.
- No obvious burned-in subtitle, watermark, account handle, platform logo, or UI
  sticker dominates the frame.
- People are acceptable as atmosphere, but avoid clear front-facing close-up faces
  unless the user requests them.
- Source usage report shows no repeated source over the allowed limit.
- Contact sheets do not reveal repeated stills, black bars, bad crops, blank frames,
  or unrelated material.

## What Not to Borrow

- Do not replace the user's curated local footage with generic stock or generated
  visuals unless the user asks.
- Do not require OpenMontage's full manifest/schema system for small edits.
- Do not copy AGPL project code into this skill. Keep this file as workflow notes.
- Do not silently change render engines, add BGM, add subtitles, or add title cards
  when the user explicitly requested otherwise.
