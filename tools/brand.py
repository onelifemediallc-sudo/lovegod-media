from PIL import Image, ImageDraw, ImageFont
import os
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts") + "/"
BG = (0x51, 0xB5, 0xA9); Y = (0xF8, 0xE3, 0x4C); WH = (255, 255, 255)
def lora(size, w=600):
    f = ImageFont.truetype(G + "Lora-Variable.ttf", size); f.set_variation_by_axes([w]); return f
def card(lines, out, ref=None, size=64, lh=None, sig=True):
    W = H = 1080; lh = lh or int(size * 1.4)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    fv = lora(size); fr = ImageFont.truetype(G + "Poppins-Medium.ttf", 30)
    extra = 110 if ref else 0
    y = (H - (len(lines) * lh + extra)) // 2 - 10
    for l in lines:
        d.text((W/2, y), l, font=fv, fill=Y, anchor="ma"); y += lh
    if ref:
        d.rectangle((W/2 - 40, y + 26, W/2 + 40, y + 29), fill=WH)
        d.text((W/2, y + 56), ref, font=fr, fill=WH, anchor="ma")
    if sig: d.text((W/2, H - 80), "Love God.", font=lora(34), fill=Y, anchor="ma")
    im.save(out)
