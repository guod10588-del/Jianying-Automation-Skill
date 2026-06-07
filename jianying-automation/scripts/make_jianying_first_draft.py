from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path


DEFAULT_EXCLUDE_KEYWORDS = [
    "人脸",
    "正脸",
    "大脸",
    "采访",
    "口播",
    "字幕",
    "水印",
    "logo",
    "账号",
    "抖音",
    "快手",
    "小红书",
    "bilibili",
    "B站",
]


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="ignore",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stdout)
    return proc


def find_ffmpeg(explicit: str | None) -> Path:
    candidates = [
        explicit,
        r"D:\BaiduNetdiskDownload\crvideomate\ffmpeg\ffmpeg.exe",
        r"D:\JianyingPro\10.0.0.13832\ffmpeg.exe",
        "ffmpeg",
    ]
    for item in candidates:
        if not item:
            continue
        path = Path(item)
        if path.exists() or item == "ffmpeg":
            return path
    raise SystemExit("ffmpeg not found; pass --ffmpeg.")


def media_info(ffmpeg: Path, path: Path) -> dict[str, float | int | str]:
    proc = run([str(ffmpeg), "-hide_banner", "-i", str(path)], check=False)
    text = proc.stdout
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if not match:
        raise RuntimeError(f"Could not read duration for {path}")
    hours, minutes, seconds = match.groups()
    duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    video_match = re.search(r"Video:.*?,\s*(\d+)x(\d+)[,\s]", text)
    width, height = (0, 0)
    if video_match:
        width, height = map(int, video_match.groups())
    return {"duration": duration, "width": width, "height": height, "path": str(path)}


def clean_script(raw: str) -> str:
    markers = [
        "下面是**精细润色后的口播版**：",
        "下面是精细润色后的口播版：",
        "口播版：",
    ]
    for marker in markers:
        if marker in raw:
            raw = raw.split(marker, 1)[1]
            break
    raw = re.sub(r"\*\*|#+|^-+\s*$", "", raw, flags=re.MULTILINE)
    lines = [line.strip() for line in raw.replace("\r\n", "\n").split("\n")]
    return "\n".join(line for line in lines if line).strip()


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[。！？；.!?;])", text.replace("\n", ""))
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def make_subtitles(sentences: list[str], duration: float) -> list[dict[str, float | str]]:
    weights = [max(8, len(sentence)) for sentence in sentences]
    total = sum(weights)
    cursor = 0.0
    rows: list[dict[str, float | str]] = []
    for sentence, weight in zip(sentences, weights):
        length = max(1.4, min(7.0, duration * weight / total))
        rows.append({"start": cursor, "end": cursor + length, "text": sentence})
        cursor += length
    scale = duration / float(rows[-1]["end"])
    for row in rows:
        row["start"] = float(row["start"]) * scale
        row["end"] = float(row["end"]) * scale
    return rows


def write_ass(path: Path, rows: list[dict[str, float | str]], width: int, height: int) -> None:
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Microsoft YaHei,68,&H0000E8FF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,5,1,2,80,80,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out = [header]
    for row in rows:
        text = str(row["text"]).replace("{", "").replace("}", "")
        if len(text) > 28:
            midpoint = len(text) // 2
            cut = max(text.rfind("，", 0, midpoint + 6), text.rfind("、", 0, midpoint + 6))
            if cut > 8:
                text = text[: cut + 1] + r"\N" + text[cut + 1 :]
        out.append(f"Dialogue: 0,{ass_time(float(row['start']))},{ass_time(float(row['end']))},Main,,0,0,0,,{text}\n")
    path.write_text("".join(out), encoding="utf-8-sig")


def choose_keyword(text: str) -> str:
    table = [
        ("云冈|石窟|佛|造像", "yungang"),
        ("古城|城墙|边城|城池", "old-city"),
        ("长城|边关|边塞|防线|戍边", "frontier"),
        ("恒山|悬空寺|山", "mountain"),
        ("美食|刀削面|烟火", "food"),
        ("历史|王朝|北魏|辽金|明朝", "history"),
        ("航拍|地图|北方|平原", "aerial"),
    ]
    for pattern, keyword in table:
        if re.search(pattern, text):
            return keyword
    return "general"


def choose_video(keyword: str, videos: list[dict[str, float | int | str]], index: int) -> dict[str, float | int | str]:
    needles = {
        "yungang": ["云冈", "石窟"],
        "old-city": ["古城", "城墙"],
        "frontier": ["长城", "边"],
        "mountain": ["恒山", "悬空寺"],
        "food": ["美食", "刀削面"],
        "history": ["博物馆", "北魏", "风华"],
        "aerial": ["航拍"],
        "general": [""],
    }[keyword]
    matches = [v for v in videos if any(n.lower() in Path(str(v["path"])).name.lower() for n in needles)]
    if not matches:
        matches = videos
    return matches[index % len(matches)]


def is_risky_source(path: Path, keywords: list[str]) -> bool:
    normalized = str(path).lower()
    return any(keyword.lower() in normalized for keyword in keywords if keyword)


def build_shots(rows: list[dict[str, float | str]], videos: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    end = float(rows[-1]["end"])
    cursor = 0.0
    index = 0
    shots: list[dict[str, float | str]] = []
    while cursor < end - 0.1:
        text = "".join(str(row["text"]) for row in rows if float(row["start"]) < cursor + 6 and float(row["end"]) > cursor)
        keyword = choose_keyword(text)
        video = choose_video(keyword, videos, index)
        duration = min(5.4 + (index % 3) * 0.5, end - cursor)
        source_duration = float(video["duration"])
        start_cap = max(0.0, source_duration - duration - 0.2)
        source_start = 0.0 if start_cap <= 0 else (index * 7.37) % start_cap
        shots.append(
            {
                "index": index + 1,
                "start": cursor,
                "end": cursor + duration,
                "duration": duration,
                "keyword": keyword,
                "source": str(video["path"]),
                "source_start": source_start,
            }
        )
        cursor += duration
        index += 1
    return shots


def make_segment(ffmpeg: Path, shot: dict[str, float | str], output: Path, width: int, height: int, codec: str) -> None:
    vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},fps=30,setsar=1"
    args = [
        str(ffmpeg),
        "-y",
        "-hide_banner",
        "-ss",
        f"{float(shot['source_start']):.3f}",
        "-t",
        f"{float(shot['duration']):.3f}",
        "-i",
        str(shot["source"]),
        "-an",
        "-vf",
        vf,
    ]
    if codec == "libx264":
        args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24"]
    else:
        args += ["-c:v", "mpeg4", "-b:v", "5500k"]
    args += ["-pix_fmt", "yuv420p", str(output)]
    run(args)


def concat_segments(ffmpeg: Path, segment_paths: list[Path], output: Path) -> None:
    list_file = output.parent / "concat_list.txt"
    list_file.write_text("".join(f"file '{path.as_posix()}'\n" for path in segment_paths), encoding="utf-8")
    run([str(ffmpeg), "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output)])


def make_tonal_bgm(ffmpeg: Path, output: Path, duration: float) -> None:
    graph = (
        f"sine=frequency=196:duration={duration}:sample_rate=44100[a0];"
        f"sine=frequency=246.94:duration={duration}:sample_rate=44100[a1];"
        "[a0]volume=0.025[a0v];[a1]volume=0.018[a1v];"
        f"[a0v][a1v]amix=inputs=2,afade=t=in:st=0:d=4,afade=t=out:st={max(0, duration - 8):.3f}:d=8"
    )
    run([str(ffmpeg), "-y", "-hide_banner", "-filter_complex", graph, "-t", f"{duration:.3f}", str(output)])


def final_mix(
    ffmpeg: Path,
    video: Path,
    voice: Path,
    bgm: Path,
    subtitle: Path,
    output: Path,
    duration: float,
    codec: str,
) -> None:
    ascii_dir = Path(r"D:\jianying_auto_tmp")
    ascii_dir.mkdir(parents=True, exist_ok=True)
    ascii_sub = ascii_dir / "subs.ass"
    shutil.copyfile(subtitle, ascii_sub)
    sub_path = ascii_sub.as_posix().replace(":", r"\:")
    graph = (
        f"[0:v]ass='{sub_path}'[v];"
        "[1:a]volume=1.0[voice];"
        "[2:a]volume=0.18[bgm];"
        "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
    )
    args = [
        str(ffmpeg),
        "-y",
        "-hide_banner",
        "-i",
        str(video),
        "-i",
        str(voice),
        "-i",
        str(bgm),
        "-filter_complex",
        graph,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-t",
        f"{duration:.3f}",
    ]
    if codec == "libx264":
        args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22"]
    else:
        args += ["-c:v", "mpeg4", "-b:v", "7000k"]
    args += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)]
    run(args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Jianying-ready first-draft MP4, subtitles, and storyboard.")
    parser.add_argument("--project", required=True, help="Project directory containing video assets.")
    parser.add_argument("--script", required=True, help="Narration/copy text file.")
    parser.add_argument("--voice", required=True, help="Voiceover audio file.")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to <project>/自动剪辑输出.")
    parser.add_argument("--ffmpeg", default=None, help="Path to ffmpeg.exe.")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--codec", choices=["libx264", "mpeg4"], default="libx264")
    parser.add_argument(
        "--exclude-keyword",
        action="append",
        default=[],
        help="Additional path/name keyword to exclude from source video selection. Can be repeated.",
    )
    parser.add_argument(
        "--allow-risky-visuals",
        action="store_true",
        help="Disable default source filtering for people, subtitles, watermarks, logos, and platform marks.",
    )
    args = parser.parse_args()

    project = Path(args.project)
    script_path = Path(args.script)
    voice_path = Path(args.voice)
    output_dir = Path(args.output_dir) if args.output_dir else project / "自动剪辑输出"
    tmp_dir = output_dir / "_tmp_segments"
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = find_ffmpeg(args.ffmpeg)
    duration = float(media_info(ffmpeg, voice_path)["duration"])
    text = clean_script(script_path.read_text(encoding="utf-8"))
    rows = make_subtitles(split_sentences(text), duration)

    exclude_keywords = [] if args.allow_risky_visuals else [*DEFAULT_EXCLUDE_KEYWORDS, *args.exclude_keyword]
    videos = []
    excluded_sources = []
    for path in sorted(project.rglob("*.mp4")):
        if output_dir in path.parents:
            continue
        if is_risky_source(path, exclude_keywords):
            excluded_sources.append(str(path))
            continue
        try:
            info = media_info(ffmpeg, path)
        except RuntimeError:
            continue
        if float(info["duration"]) >= 2:
            videos.append(info)
    if not videos:
        raise SystemExit("No usable clean .mp4 source videos found. Retry with --allow-risky-visuals only if the user approves.")

    subtitle = output_dir / "auto_subtitles.ass"
    storyboard = output_dir / "storyboard.csv"
    plan = output_dir / "edit_plan.json"
    bgm = output_dir / "auto_bgm.wav"
    final = output_dir / "auto_first_draft.mp4"

    write_ass(subtitle, rows, args.width, args.height)
    make_tonal_bgm(ffmpeg, bgm, duration)
    shots = build_shots(rows, videos)

    with storyboard.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "start", "end", "duration", "keyword", "source", "source_start"])
        writer.writeheader()
        writer.writerows(shots)

    segment_paths: list[Path] = []
    for shot in shots:
        segment = tmp_dir / f"seg_{int(shot['index']):04d}.mp4"
        make_segment(ffmpeg, shot, segment, args.width, args.height, args.codec)
        segment_paths.append(segment)

    visual = tmp_dir / "visual_cut.mp4"
    concat_segments(ffmpeg, segment_paths, visual)
    final_mix(ffmpeg, visual, voice_path, bgm, subtitle, final, duration, args.codec)

    plan.write_text(
        json.dumps(
            {
                "id": str(uuid.uuid4()),
                "duration": duration,
                "shot_count": len(shots),
                "subtitle_count": len(rows),
                "output_mp4": str(final),
                "subtitle_ass": str(subtitle),
                "storyboard_csv": str(storyboard),
                "excluded_sources": excluded_sources,
                "exclude_keywords": exclude_keywords,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"OUTPUT={final}")
    print(f"SUBTITLE={subtitle}")
    print(f"STORYBOARD={storyboard}")


if __name__ == "__main__":
    main()
