# ViMax Lessons For Jianying Automation

Use this reference when improving the user's short-video automation workflow after reviewing `HKUDS/ViMax`.

## What To Borrow

- Director-style decomposition: split a video task into script analysis, shot planning, material selection, assembly, and review.
- Storyboard-first workflow: generate a shot-level plan before rendering, instead of only rotating media files.
- Role-based checks:
  - Screenwriter: identifies script sections and narrative intent.
  - Director: decides pacing, scene order, visual rhythm, and opening hook.
  - Producer: maps available local assets to each shot and flags missing material.
  - Reviewer: checks repetition, face/watermark/subtitle risk, aspect ratio, audio, and delivery rules.
- Visual anchors: choose 3-5 core visuals for a project and return to them deliberately.
- Consistency checks: preserve city/topic/style continuity, avoid accidental mixed-city footage, and prevent same-subject fatigue.
- Retry loop: if preview contact sheets reveal repeated shots, overlong images, weak opening, or risky frames, automatically re-plan and re-render when feasible.

## What Not To Copy

- Do not replace the user's real local footage with generic AI-generated video for city/history/book-selling projects.
- Do not use AI-generated visuals for real artifacts, people, ruins, books, or city landmarks unless the user explicitly requests generated imagery.
- Do not overcomplicate ordinary first cuts with unnecessary agent ceremony; use the director-style flow only where it improves the result.
- Do not invent historical visuals when authentic footage or stills are available.

## Director-Style Editing Flow

For book-selling/history/city narration projects:

1. Script analysis:
   - Split the copy into narrative sections: hook, question, historical setup, person/event, evidence, city/material logic, book value, final conversion.
   - Extract important nouns: city, building, artifact, person, book title, place, process, era.

2. Visual anchor selection:
   - Pick 3-5 recurring anchor visuals.
   - Examples:
     - Anyang: Wenfeng Tower, oracle bones, Yinxu, Fu Hao artifacts, book/page visuals.
     - Jingdezhen: city aerial, blue-and-white cup, kiln/process, Chang River/wharf, book/page visuals.
     - Huizhou: aerial/ancient town, horse-head wall, patio, rain/stone road, book/page visuals.

3. Shot plan:
   - For each script section, assign shot purpose: establish, evidence, detail, atmosphere, contrast, book/product return.
   - Use visual rhythm: wide -> medium -> close detail -> evidence, then reset.
   - Avoid consecutive same-category shots unless creating a deliberate montage.

4. Assembly:
   - Use local materials first.
   - Enforce house limits: images max 3 seconds, single video source max 1 minute or 10% of total duration, 9:16 by default, no subtitles/BGM unless requested.
   - Preserve opening instruction when the user names a specific opening clip.

5. Review and retry:
   - Generate opening and full-video contact sheets.
   - Check for repeated subjects, repeated images, weak opening, clear faces, watermarks, burned-in subtitles, black bars, bad crop, and off-topic footage.
   - If any major issue appears, adjust source order, reduce/replace repeated material, or shorten risky shots and re-render.

## Storyboard Fields To Prefer

When creating `storyboard.csv` or a richer `shot_plan.json`, include:

- `script_section`
- `narrative_intent`
- `shot_purpose`
- `visual_anchor`
- `source_name`
- `source_path`
- `source_start`
- `timeline_start`
- `timeline_end`
- `duration`
- `media_kind`
- `category`
- `risk_notes`
- `replacement_candidates`

## Quality Standard

A good automated first cut should feel intentionally directed:

- The first 3 seconds clearly signal the topic.
- The middle does not become a same-looking museum/archive/object montage.
- The clip alternates between place, artifact, process, and evidence.
- Important people/books/artifacts appear near the relevant narration.
- Book-selling videos return to the book or reading value near the end.
- The output comes with enough review artifacts to support fast human decisions.
