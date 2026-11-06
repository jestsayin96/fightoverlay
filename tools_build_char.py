"""Turn a Pixelwright png-frames export into overlay sprite strips.

The export is a clean 3x block upscale, so the true art is recovered by
sampling one pixel per block (asserted, not assumed) and re-rendered at 2x
so figures sit beside the 0x72 pack at a comparable height.
"""
from PIL import Image
import os, sys, json, glob

name     = sys.argv[1]                       # e.g. "goblin"
src      = sys.argv[2]                       # folder of <name>-001.png ...
out      = sys.argv[3]
SRC_SCALE, OUT_SCALE = 3, 2
CLIPS = [("idle",1,2), ("walk",3,6), ("attack",7,13), ("death",14,17)]
os.makedirs(out, exist_ok=True)

def recover(path):
    im = Image.open(path).convert("RGBA")
    w,h = im.size
    assert w % SRC_SCALE == 0 and h % SRC_SCALE == 0, (path, im.size)
    small = Image.new("RGBA", (w//SRC_SCALE, h//SRC_SCALE))
    sp, dp = im.load(), small.load()
    for y in range(small.height):
        for x in range(small.width):
            dp[x,y] = sp[x*SRC_SCALE, y*SRC_SCALE]
    assert small.resize(im.size, Image.NEAREST).tobytes() == im.tobytes(), \
        f"{path}: export was not a clean {SRC_SCALE}x upscale"
    return small

art = {}
for clip,a,b in CLIPS:
    files = [f"{src}/{name}-{i:03d}.png" for i in range(a,b+1)]
    for f in files:
        if not os.path.exists(f): raise SystemExit(f"missing {f}")
    art[clip] = [recover(f) for f in files]

# one anchor for every clip, taken from the standing pose
bb   = art["idle"][0].getbbox()
cell = art["idle"][0].width * OUT_SCALE
ax   = ((bb[0]+bb[2])//2) * OUT_SCALE
ay   = bb[3] * OUT_SCALE                       # foot line
fh   = ay - bb[1]*OUT_SCALE                    # figure height above it
print(f"{name}: cell {cell}x{cell}  anchor ({ax},{ay})  fh {fh}  "
      f"figure {(bb[3]-bb[1])*OUT_SCALE}px tall")

for clip, frames in art.items():
    big = [f.resize((f.width*OUT_SCALE, f.height*OUT_SCALE), Image.NEAREST)
           for f in frames]
    strip = Image.new("RGBA", (cell*len(big), cell), (0,0,0,0))
    for i,f in enumerate(big): strip.paste(f, (i*cell, 0))
    p = f"{out}/{clip}.png"
    strip.save(p, optimize=True)
    print(f"  {clip:7s} {len(big)} frames  {strip.size}  {os.path.getsize(p):5d} B")

print(json.dumps({"cw":cell,"ch":cell,"ax":ax,"ay":ay,"fh":fh}))
