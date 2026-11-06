from PIL import Image
import os

SRC = "/home/claude/knightzip"
OUT = "/home/claude/knightart/sheets"
os.makedirs(OUT, exist_ok=True)

# png-frames emits every animation in order: idle, walk, attack, death
CLIPS = [("idle", 1, 2), ("walk", 3, 6), ("attack", 7, 13), ("death", 14, 17)]
SRC_SCALE = 3      # what we exported at
OUT_SCALE = 2      # what the overlay wants, to sit beside the 0x72 heroes

def recover(path):
    """3x export -> the exact 40x40 art, by sampling one pixel per block."""
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    assert w % SRC_SCALE == 0 and h % SRC_SCALE == 0, (path, im.size)
    small = Image.new("RGBA", (w // SRC_SCALE, h // SRC_SCALE))
    sp, dp = im.load(), small.load()
    for y in range(small.height):
        for x in range(small.width):
            dp[x, y] = sp[x * SRC_SCALE, y * SRC_SCALE]
    # prove the block really was uniform, or the export was not a clean upscale
    assert small.resize(im.size, Image.NEAREST).tobytes() == im.tobytes(), path
    return small

art = {}
for name, a, b in CLIPS:
    art[name] = [recover(f"{SRC}/knight-{i:03d}.png") for i in range(a, b + 1)]

# one anchor for every clip: the standing pose's foot line and body centre
idle0 = art["idle"][0]
bb = idle0.getbbox()
print("idle art bbox", bb)
cell = idle0.width * OUT_SCALE
feet_y = bb[3] * OUT_SCALE                     # bottom of the boots
ctr_x = ((bb[0] + bb[2]) // 2) * OUT_SCALE
print(f"cell {cell}x{cell}  anchor ({ctr_x},{feet_y})  figure h {(bb[3]-bb[1])*OUT_SCALE}px")

for name, frames in art.items():
    big = [f.resize((f.width * OUT_SCALE, f.height * OUT_SCALE), Image.NEAREST)
           for f in frames]
    strip = Image.new("RGBA", (cell * len(big), cell), (0, 0, 0, 0))
    for i, f in enumerate(big):
        strip.paste(f, (i * cell, 0))
    p = f"{OUT}/{name}.png"
    strip.save(p, optimize=True)
    print(f"  {name:7s} {len(big)} frames  {strip.size}  {os.path.getsize(p):5d} B")
