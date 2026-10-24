"""Love God. reel maker: 1080x1920, teal bg, yellow Lora verse scenes, white reference + NASB notice."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "..", "fonts") + "/"
BG = (0x51, 0xB5, 0xA9); Y = (0xF8, 0xE3, 0x4C); WH = (255, 255, 255)
NOTICE = ("Scripture quotations taken from the NASB (New American Standard Bible), Copyright © 1995 by "
          "The Lockman Foundation. Used by permission. All rights reserved. lockman.org")
def lora(s):
    f = ImageFont.truetype(FD + "Lora-Variable.ttf", s); f.set_variation_by_axes([600]); return f
def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: out.append(cur); cur = w
        out.append(cur)
    return out
def make(scenes, ref, music, out, secs=15, fps=30):
    """scenes: list of (start, end, text)."""
    W, H = 1080, 1920
    fr = ImageFont.truetype(FD + "Poppins-Medium.ttf", 40); fn = ImageFont.truetype(FD + "Poppins-Medium.ttf", 22)
    sig = lora(44)
    tmp = out + ".v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
                          "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", tmp], stdin=subprocess.PIPE)
    ease = lambda x: 1 - (1 - x) ** 3
    for k in range(secs * fps):
        t = k / fps
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        for st, en, txt in scenes:
            if not (st <= t < en): continue
            a_in = ease(min(1, (t - st) / 0.7)); a_out = 1 if en >= secs else max(0, min(1, (en - t) / 0.4)); a = a_in * a_out
            fz = lora(80 if len(txt) < 45 else (70 if len(txt) < 70 else 60))
            lines = wrap(d, txt, fz, 900); lh = int(fz.size * 1.4)
            y0 = 820 - len(lines) * lh // 2 + int((1 - a_in) * 30)
            col = tuple(int(BG[i] + (Y[i] - BG[i]) * a) for i in range(3))
            for i, l in enumerate(lines): d.text((W / 2, y0 + i * lh), l, font=fz, fill=col, anchor="ma")
        d.rectangle((W / 2 - 60, 1290, W / 2 + 60, 1294), fill=WH)
        d.text((W / 2, 1320), ref, font=fr, fill=WH, anchor="ma")
        d.text((W / 2, 1480), "Love God.", font=sig, fill=Y, anchor="ma")
        for i, l in enumerate(wrap(d, NOTICE, fn, 900)): d.text((W / 2, 1720 + i * 30), l, font=fn, fill=WH, anchor="ma")
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", music, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(tmp)
