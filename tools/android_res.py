# -*- coding: utf-8 -*-
# Replaces Capacitor's placeholder launcher icons and splash screens in an Android project with the Hall IEQ Explorer art,
# at the size of every existing file (all densities, portrait and landscape). Used instead of @capacitor/assets, whose image
# library needs a native install script. Run from the project folder:  python tools/android_res.py android   (assets/ beside it)
import os, re, sys
from PIL import Image, ImageDraw
PROJ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "android")
ROOT = os.path.dirname(PROJ)
RES = os.path.join(PROJ, "app", "src", "main", "res")
A = os.path.join(ROOT, "assets")
icon = Image.open(os.path.join(A, "icon-only.png")).convert("RGB")
fg = Image.open(os.path.join(A, "icon-foreground.png")).convert("RGBA")
splash = Image.open(os.path.join(A, "splash.png")).convert("RGB")
INK = (0x17, 0x24, 0x2B)

def cover(im, w, h):
    """centre crop to the target aspect, then resize"""
    W, H = im.size; r = w / h
    if W / H > r: nw = int(H * r); box = ((W - nw) // 2, 0, (W - nw) // 2 + nw, H)
    else: nh = int(W / r); box = (0, (H - nh) // 2, W, (H - nh) // 2 + nh)
    return im.crop(box).resize((w, h), Image.LANCZOS)

n = 0
for d, _, files in os.walk(RES):
    for f in files:
        p = os.path.join(d, f)
        if not f.endswith(".png"): continue
        w, h = Image.open(p).size
        if f == "ic_launcher.png":
            icon.resize((w, h), Image.LANCZOS).save(p)
        elif f == "ic_launcher_round.png":
            im = icon.resize((w, h), Image.LANCZOS).convert("RGBA")
            m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).ellipse((0, 0, w - 1, h - 1), fill=255)
            out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), m); out.save(p)
        elif f == "ic_launcher_foreground.png":
            fg.resize((w, h), Image.LANCZOS).save(p)
        elif f == "splash.png":
            cover(splash, w, h).save(p)
        else:
            continue
        n += 1
# the adaptive icon's background colour
bg = os.path.join(RES, "values", "ic_launcher_background.xml")
s = open(bg, encoding="utf8").read()
s2 = re.sub(r'(<color name="ic_launcher_background">)#[0-9A-Fa-f]{6,8}(</color>)', r"\g<1>#17242B\2", s)
open(bg, "w", encoding="utf8").write(s2)
print("replaced %d images; adaptive background %s" % (n, "set" if s2 != s else "UNCHANGED"))
