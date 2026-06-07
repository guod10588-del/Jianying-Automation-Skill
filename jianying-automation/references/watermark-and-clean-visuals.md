# Watermark And Clean Visuals

## Default Rule

For the user's later Jianying/video edits, avoid source shots that contain:

- visible people or talking heads
- burned-in creator subtitles
- platform watermarks
- account handles
- logos that are not intentionally part of the video
- UI overlays or repost marks

Prefer clean footage: architecture, landscapes, aerials, scenery, cultural artifacts, empty streets, food closeups without faces, textures, and detail shots.

When the clip is important and authorized for cleanup, consider specialist inpainting/subtitle-removal tools from `open-source-routes.md` before using visible coverups. Use Jianying sticker cover, masked blur/mosaic, or crop as fast fallback methods.

## Screening Workflow

1. Filter obvious risky files by name/path keywords such as `人物`, `人像`, `采访`, `口播`, `字幕`, `水印`, `logo`, `抖音`, `快手`, `小红书`, `B站`, `bilibili`, `账号`.
2. Sample preview frames from uncertain clips before selecting them.
3. If a clip is otherwise valuable but has a small edge watermark, prefer crop.
4. If crop would damage the frame, cover or mask the watermark.
5. Record the repair method in the storyboard.

## Repair Flow 1: Sticker Or Text Cover

Use when the watermark is near an edge or the background is too complex for a seamless repair.

In Jianying:

1. Import the video and place it on the main timeline.
2. Add a sticker or text layer.
3. Use the user's account name or logo if a branded cover is appropriate.
4. Position and resize it to cover the original watermark.
5. Stretch the sticker/text layer across the full clip or full video.

Automation note:

- UI automation can add the sticker/text and stretch it.
- Draft automation can add a text/sticker material track when the schema is readable.

## Repair Flow 2: Masked Blur Or Mosaic

Use when the background is relatively plain or textured and the watermark is not at the edge.

In Jianying:

1. Duplicate the video layer.
2. Align the duplicate exactly above the original.
3. Apply blur or mosaic to the upper layer.
4. Add a rectangular mask around only the watermark/text.
5. Adjust feathering and size so only the watermark area is affected.
6. Stretch the effect across the needed duration.

Draft automation note:

- This usually means adding a second video segment above the original.
- Add or update the mask parameters such as `center_x`, `center_y`, `size_x`, and `size_y`.
- Add the blur/mosaic effect to the masked upper layer.

## Repair Flow 3: Crop

Use when the watermark is at the top, bottom, or side edge and losing a little edge content is acceptable.

In Jianying:

1. Select the video clip.
2. Open the crop tool, often available with `Alt+C`.
3. Move the crop edge inward until the watermark is gone.
4. Preserve the target aspect ratio when possible.
5. Confirm and let Jianying scale the crop to fill the frame.

Draft automation note:

- Modify the clip crop fields when the draft schema is readable.
- In FFmpeg, use `crop` plus `scale` to remove edge watermark regions.

## Decision Guide

- Edge watermark and composition can survive crop: use crop.
- Edge watermark but crop harms subject/composition: use sticker/text cover.
- Interior watermark on plain background: use masked blur/mosaic.
- Interior watermark on important detail: avoid the clip if possible.
- Existing subtitles across the lower third: avoid the clip unless cropping is acceptable.
