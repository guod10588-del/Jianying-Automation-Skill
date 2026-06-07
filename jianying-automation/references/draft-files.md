# Jianying Draft Files

## Discovery

Check these locations first:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\JianyingPro\User Data\Projects" -Recurse -File
Get-ChildItem "$env:LOCALAPPDATA\Bytedance\JianyingPro" -Recurse -File
```

Look for:

- `root_meta_info.json`
- `draft_content.json`
- `draft_cover.jpg`
- draft folders listed by `draft_fold_path`

`root_meta_info.json` commonly stores a list of drafts and points to actual draft folders, which may live outside `%LOCALAPPDATA%`.

## Safety Rules

- Back up a whole draft folder before changing it.
- Preserve unknown keys and ordering where practical.
- Do not edit encrypted, binary, or opaque draft content unless the user explicitly wants experimental work.
- Prefer creating a new draft folder over modifying an existing important draft.
- Keep all source media paths absolute unless the existing draft clearly uses another convention.

## Readable Draft Workflow

1. Open `root_meta_info.json` and find the intended draft.
2. Open the referenced `draft_content.json`.
3. Confirm it is valid JSON, not encrypted/base64-like opaque content.
4. Inspect timeline units. Jianying often uses microseconds or internal tick units; infer from existing clip duration values.
5. Identify material collections for video, audio, text, effects, and tracks.
6. Add or modify entries by copying a nearby object shape and changing only IDs, path, duration, and text.
7. Update root metadata duration and modified time if the local format requires it.
8. Launch Jianying and verify the draft opens.

## Opaque Draft Workflow

If `draft_content.json` is unreadable or starts with long random-looking text:

- Treat it as encrypted or compressed by the current Jianying version.
- Do not attempt to replace it with handmade JSON.
- Use FFmpeg to generate MP4 plus sidecar subtitle/storyboard.
- Use UI automation to import the MP4 and subtitle into Jianying, or ask the user to import manually if UI automation is too brittle.

## Useful Diff Strategy

To learn the schema:

1. Create a tiny Jianying draft manually with one video, one audio, and one subtitle.
2. Copy the draft folder.
3. Make one small GUI change, such as changing subtitle text.
4. Compare the two `draft_content.json` files.
5. Implement the smallest structured mutation that reproduces that change.
