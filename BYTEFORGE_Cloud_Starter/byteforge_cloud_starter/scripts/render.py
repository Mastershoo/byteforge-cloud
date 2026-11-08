import argparse, json, math, os, random, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import asyncio

W, H = 1080, 1920
OUT = Path("output")
OUT.mkdir(exist_ok=True)

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, f, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=f)[2] <= max_width: line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def frame(topic, phase, total):
    im = Image.new("RGB", (W,H), (7,12,25))
    d = ImageDraw.Draw(im)
    # subtle moving grid / orbit accents
    shift = int(phase * 2) % 100
    for x in range(-100+shift, W, 100):
        d.line((x,0,x,H), fill=(13,29,53), width=2)
    for y in range(0,H,100):
        d.line((0,y,W,y), fill=(13,29,53), width=2)
    d.ellipse((650+shift,220,1050+shift,620), outline=(0,125,210), width=5)
    d.ellipse((710+shift,280,990+shift,560), outline=(0,70,130), width=3)
    d.rounded_rectangle((65,100,1015,180), radius=30, fill=(0,65,110))
    d.text((100,118),"BYTEFORGE  /  TECHNOLOGY. DECODED.",font=font(34,True),fill=(235,247,255))
    hook = topic["hook"]
    lines = wrap(d, hook, font(76,True), 900)
    y = 510
    for line in lines:
        d.text((85,y),line,font=font(76,True),fill=(70,205,255),stroke_width=1)
        y += 100
    body = topic["body"]
    blines = wrap(d, body, font(45), 900)
    y = 900
    for line in blines:
        d.text((85,y),line,font=font(45),fill=(235,241,250))
        y += 68
    d.rounded_rectangle((70,1500,1010,1660),radius=35,outline=(0,155,230),width=4)
    d.text((105,1545),topic["cta"],font=font(38,True),fill=(255,255,255))
    d.text((85,1780),topic["tag"]+"  •  BYTEFORGE LABS",font=font(30,True),fill=(115,165,205))
    d.text((85,1840),"Educational content. Verify important claims independently.",font=font(23),fill=(130,145,165))
    return im

async def make_voice(text, path):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        await communicate.save(str(path))
        return True
    except Exception as e:
        print("Voice generation unavailable; continuing without audio:", e)
        return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=0)
    args=ap.parse_args()
    topics=json.loads(Path("scripts/topics.json").read_text(encoding="utf-8"))
    topic=topics[args.index % len(topics)]
    slug="video_{:02d}".format(args.index % len(topics)+1)
    # Render a clean vertical card video; subtle movement comes from changing frame phase.
    tmp=OUT/(slug+"_frames")
    tmp.mkdir(exist_ok=True)
    for i in range(90):
        frame(topic, i, 90).save(tmp/("frame_%04d.png"%i))
    silent=OUT/(slug+"_silent.mp4")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",str(tmp/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(silent)],check=True)
    audio=OUT/(slug+".mp3")
    script=topic["hook"]+" "+topic["body"]+" "+topic["cta"]
    has_audio=asyncio.run(make_voice(script,audio))
    final=OUT/(slug+".mp4")
    if has_audio:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(audio),"-shortest","-c:v","copy","-c:a","aac","-b:a","128k","-movflags","+faststart",str(final)],check=True)
        silent.unlink()
    else:
        silent.rename(final)
    (OUT/(slug+".json")).write_text(json.dumps({"title":topic["title"],"caption":topic["title"]+" | "+topic["cta"]+" #technology #AI #cybersecurity","script":script,"review_required":True},indent=2),encoding="utf-8")
    print("Created",final)

if __name__=="__main__": main()
