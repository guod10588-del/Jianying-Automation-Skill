# Open-Source Routes

Use this reference when the task mentions GitHub tools, `JianyPro`, `JianYing-Auto`, `pyJianYingDraft`, `AutoCut`, `ProPainter`, `E2FGVI`, `Video Subtitle Remover`, `VideoSubFinder`, `Inpaint-Anything`, or AI watermark/subtitle/object removal.

## Guardrails

- Use cleanup/inpainting only on user-owned, licensed, or otherwise authorized footage.
- Prefer selecting clean source footage over removing watermarks from questionable sources.
- Do not spend time installing large GPU models until the user approves the tradeoff.
- Check each repo's license, model weights, CUDA/PyTorch version, and Windows support before adopting it.
- Keep the workflow modular: each tool should read from an input folder and write clean intermediate files, not mutate originals.

## Route A: Jianying Draft Libraries

Examples: `pyJianYingDraft`, `JianyPro`, `JianYing-Auto`, `JianYingProDraft`, CapCut/Jianying draft CLIs.

Use when:

- The user wants an editable Jianying draft, not only a rendered MP4.
- The current Jianying version stores readable or library-compatible draft files.
- The workflow needs programmatic tracks, text, subtitle segments, audio, transitions, effects, or template assembly.

Typical flow:

1. Generate or collect media assets.
2. Normalize assets with FFmpeg.
3. Use the draft library to create a draft folder.
4. Add video/audio tracks, text/caption tracks, transitions, and timing.
5. Register the draft with Jianying's draft root if the library does not do so.
6. Open Jianying for human review and export.

Codex wrapper shape:

```text
input: project folder, script, voiceover, assets, target resolution
output: Jianying draft folder + optional preview MP4 + storyboard CSV
```

Implementation note:

- Standardize on one library per machine. Do not mix multiple draft writers in the same project unless necessary.
- Add a small smoke test draft before using a library on a long project.

## Route B: ASR Text-Based Cutting

Example: `mli/autocut`.

Use when:

- A video contains speech and the user wants text-level removal.
- The user asks to delete filler words such as `呃`, `那个`, repeated phrases, or off-topic sentences.
- The final output should be a cut video or an editable timeline/project.

Typical flow:

1. Run ASR on source video/audio.
2. Produce editable transcript with timestamps.
3. Use Codex as the transcript editor: remove filler words, dead air, repeated text, or requested topics.
4. Convert edited transcript back into cut intervals.
5. Export MP4 or handoff project.

Quality note:

- Always preserve a reviewable transcript diff and cut list.
- For Chinese speech, verify ASR punctuation and homophones before cutting aggressively.

## Route C: Subtitle/Text Removal

Examples: `Video Subtitle Remover`, `Video-SubFinder`, subtitle-removal pipelines.

Use when:

- Text is hard-burned into the pixels.
- The text region is predictable, often lower third subtitles.
- The user owns/has permission to clean the source footage.

Typical flow:

1. Detect subtitle/text area automatically or use fixed coordinates.
2. Generate masks over subtitle frames.
3. Run traditional fill or AI inpainting.
4. Export a clean intermediate video.
5. Add new subtitles in the Jianying/FFmpeg stage.

Quality note:

- Moving backgrounds, transparent text, large lower-third captions, and high-contrast outlines can leave artifacts.
- Sample multiple preview frames before accepting the result.

## Route D: Video Inpainting/Object Removal

Examples: `ProPainter`, `E2FGVI`, `Flow-guided Video Inpainting`, ProPainter WebUI, ComfyUI ProPainter nodes.

Use when:

- A logo, person, object, or watermark moves over time.
- Crop/sticker/mosaic would look too rough.
- GPU resources and setup time are acceptable.

Typical flow:

1. Create a mask for the unwanted region/object.
2. Track or propagate the mask across frames.
3. Run video inpainting.
4. Rebuild audio and metadata with FFmpeg if needed.
5. Validate temporal consistency and artifacts.

Quality note:

- Inpainting is strongest when the hidden background is predictable or visible in nearby frames.
- It is weak when the removed object covers important unique detail for most of the clip.

## Route E: SAM-Assisted Masking

Examples: `Inpaint-Anything`, SAM + tracking + inpainting workflows.

Use when:

- The user can identify the object/text/watermark in a frame.
- Automatic detection is unreliable.
- A click/box/point prompt can produce a better mask than rectangle coordinates.

Typical flow:

1. Extract or display the first representative frame.
2. Use SAM point/box prompt to segment the unwanted object.
3. Propagate or track the mask through the video.
4. Run the selected image/video inpainting backend.
5. Export clean intermediate footage.

## Agent Architecture

Recommended pipeline:

```text
source media
  -> screen for risky people/subtitles/watermarks
  -> optional cleanup route B/C/D/E
  -> normalized clean media folder
  -> route A or FFmpeg first-draft assembly
  -> preview MP4 + subtitle sidecar + storyboard
  -> Jianying draft or UI import
```

## Selection Matrix

- Need editable Jianying project: Route A.
- Need remove filler speech: Route B.
- Need remove hard subtitles: Route C.
- Need remove moving object/person/watermark: Route D.
- Need better masks from user click/box: Route E.
- Need fast first draft with clean sources: FFmpeg hybrid flow from `SKILL.md`.
