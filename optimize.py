#!/usr/bin/env python3
"""Generate responsive WebP variants of the selected imagery into kohatu-netlify-deploy/img/."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "source-assets")
OUT = os.path.join(ROOT, "kohatu-netlify-deploy", "img")
os.makedirs(OUT, exist_ok=True)

# slug: (source file, list of widths)
SELECT = {
    "hero-ford": ("020_550900365_10161594751527665_3703909578489256557_n.jpg", [1920, 1200, 800, 480]),
    "five-year-plan": ("007_20250426_124819.jpg", [1200, 800, 480]),
    "clarence": ("019_549692246_10161594753137665_3708416476590052993_n.jpg", [1200, 800, 480]),
    "sounds-like": ("023_550175877_10161594757552665_741821476584042005_n.jpg", [1200, 800, 480]),
    "festival": ("052_387688757_162449086935078_1276021459364570294_n.jpg", [1920, 1200, 800, 480]),
    "wellington": ("024_548463621_10161594754972665_3313435273558230910_n.jpg", [1200, 800, 480]),
    "summer-series": ("026_20250920_150918.jpg", [1200, 800, 480]),
    "trail-rides": ("038_387825234_162441896935797_3264029164828823338_n__281_29.jpg", [1200, 800, 480]),
    "park-aerial": ("000_387072303_162448633601790_244005482169707362_n.jpg", [1200, 800, 480]),
    "training": ("037_387157355_162450536934933_2284897858670734675_n.jpg", [800, 480]),
    "gallery-mud": ("012_IMG_8263.jpeg", [800, 480]),
    "gallery-air": ("048_IMG_20231016_075817_906.jpg", [800, 480]),
    "gallery-wheelie": ("046_387158444_162446190268701_4508653828871323354_n.jpg", [800, 480]),
    "gallery-jetty": ("021_549734812_10161594752137665_5374699393601451324_n.jpg", [800, 480]),
    "gallery-tractor": ("032_522854773_606671165846199_4349808515705543324_n.jpg", [800, 480]),
    "gallery-gate": ("008_20250426_124815.jpg", [800, 480]),
    "logo-stacked": ("logo-stacked.png", [600]),
    "emblem": ("emblem.png", [320, 96]),
}

for slug, (fname, widths) in SELECT.items():
    im = Image.open(os.path.join(SRC, fname))
    has_alpha = im.mode in ("RGBA", "LA") or "transparency" in im.info
    im = im.convert("RGBA" if has_alpha else "RGB")
    for w in widths:
        if im.width <= w:
            out = im
        else:
            out = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        path = os.path.join(OUT, f"{slug}-{min(w, im.width)}.webp")
        out.save(path, "WEBP", quality=82, method=6)
        print(f"{os.path.basename(path):36s} {out.width}x{out.height}  {os.path.getsize(path)//1024} KB")
