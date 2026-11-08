import argparse, asyncio, json, os, subprocess, sys
from pathlib import Path

OUT = Path("output")
ASSETS = Path("assets")
OUT.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

def voice(text, path):
    try:
        import edge_tts
        async def make():
            await edge_tts.Communicate(text, "en-US-GuyNeural", rate="+5%").save(str(path))
        asyncio.run(make())
        return True
    except Exception as exc:
        print(f"Voice generation failed: {exc}", file=sys.stderr)
        return False

def get_background():
    local = ASSETS / "minecraft_parkour.mp4"
    if local.exists():
        return local
    url = os.getenv("BACKGROUND_URL", "").strip()
    if not url:
        raise RuntimeError("Add an authorised gameplay file at assets/minecraft_parkour.mp4 or set BACKGROUND_URL to a direct authorised MP4/WebM/MOV URL.")
    if not url.lower().split("?")[0].endswith((".mp4", ".webm", ".mov")):
        raise RuntimeError("BACKGROUND_URL must be a direct media-file URL, not a YouTube watch page. Do not scrape YouTube.")
    run(["curl", "-fL", "--retry", "3", "--max-time", "180", "-o", str(local), url])
    return local

def srt_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    total = int(seconds)
    return f"00:{total // 60:02d}:{total % 60:02d},{ms:03d}"

def write_captions(text, path):
    words = text.split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
    block = []
    cursor = 0.0
    for number, chunk in enumerate(chunks, 1):
        duration = max(1.0, len(chunk.split()) * 0.36)
        block.extend([str(number), f"{srt_time(cursor)} --> {srt_time(cursor + duration)}", chunk.upper(), ""])
        cursor += duration
    path.write_text("\n".join(block), encoding="utf-8")
    return cursor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--batch", type=int, default=1)
    args = parser.parse_args()
    topics = json.loads(Path("scripts/topics.json").read_text(encoding="utf-8"))
    background = get_background()
    for offset in range(args.batch):
        idx = (args.index + offset) % len(topics)
        story = topics[idx]
        script = " ".join([story["hook"], story["story"], story["ending"], story["cta"]])
        slug = f"byteforge_story_{idx+1:02d}"
        audio = OUT / f"{slug}.mp3"
        captions = OUT / f"{slug}.srt"
        final = OUT / f"{slug}.mp4"
        if not voice(script, audio):
            raise RuntimeError("Narration unavailable. Failing the job rather than silently producing a mute video.")
        narration_duration = audio_duration(audio)
        write_captions(script, captions, narration_duration)
        # -an on the gameplay input is intentional: no audio from the source video is retained.
        srt_path = str(captions.resolve()).replace("\\", "/").replace(":", "\\:")
        video_filter = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,"
            f"subtitles='{srt_path}':force_style='FontName=DejaVu Sans,FontSize=52,Bold=1,"
            "PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,BorderStyle=1,"
            "Outline=3,Shadow=1,Alignment=2,MarginV=250'"
        )
        run([
            "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(background), "-i", str(audio),
            "-vf", video_filter,
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "23", "-c:a", "aac", "-b:a", "160k", "-shortest",
            "-movflags", "+faststart", "-map_metadata", "-1", str(final)
        ])
        metadata = {
            "title": story["title"],
            "description": story["cta"] + "\n\nMinecraft gameplay credit: Orbital / OrbitalNCG — https://www.youtube.com/watch?v=u7kdVe8q5zs",
            "script": script,
            "fictional_story": True,
            "review_required": True,
            "source_gameplay_audio": "removed",
            "gameplay_source": "OrbitalNCG — https://www.youtube.com/watch?v=u7kdVe8q5zs",
            "rights_reminder": "Confirm the creator's current reuse terms and provide required attribution before publishing."
        }
        (OUT / f"{slug}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(f"Created {final}")

if __name__ == "__main__":
    main()
