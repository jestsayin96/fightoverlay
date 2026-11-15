#!/usr/bin/env python3
"""Generate pixel art sprite sheets for Jester's Village.

Each sprite has 4 sheets:
  idle.png   — 2 frames  (cw*2  x ch)
  walk.png   — 4 frames  (cw*4  x ch)
  attack.png — 7 frames  (cw*7  x ch)
  death.png  — 4 frames  (cw*4  x ch)

Heroes/Monsters: 80x80 cells
Bosses: 112x112 cells
"""

from PIL import Image, ImageDraw
import os, math

SPRITE_DIR = os.path.join(os.path.dirname(__file__), "..", "sprites")

# ─── colour palette ───
# Each character gets: outline, body, body_shadow, body_hi, accent, accent_dark, skin, skin_shadow, eye
OUTLINE = (20, 20, 30, 255)

def px(draw, x, y, col):
    """Draw a single pixel."""
    draw.point((x, y), fill=col)

def rect(draw, x, y, w, h, col):
    """Fill a rectangle of pixels."""
    for dy in range(h):
        for dx in range(w):
            draw.point((x+dx, y+dy), fill=col)

def outline_rect(draw, x, y, w, h, fill, border=OUTLINE):
    """Draw a filled rect with 1px outline."""
    rect(draw, x, y, w, h, border)
    rect(draw, x+1, y+1, w-2, h-2, fill)

def draw_humanoid(draw, cx, foot_y, body, body_s, body_h, accent, accent_d, skin, skin_s, eye,
                  hat_fn=None, weapon_fn=None, cape=None, shift_x=0, shift_y=0,
                  arm_angle=0, leg_spread=0, lean=0, scale=1.0):
    """Draw a humanoid pixel character.
    cx, foot_y = center x, y of feet
    """
    s = scale
    ox = cx + shift_x
    oy = foot_y + shift_y

    def si(v): return max(1, int(v * s))

    # Feet/boots
    boot_w, boot_h = si(6), si(4)
    left_foot_x = int(ox - si(5) - leg_spread)
    right_foot_x = int(ox + si(1) + leg_spread)
    outline_rect(draw, left_foot_x, int(oy - boot_h), boot_w, boot_h, accent_d)
    outline_rect(draw, right_foot_x, int(oy - boot_h), boot_w, boot_h, accent_d)

    # Legs
    leg_h = si(10)
    leg_w = si(4)
    left_leg_x = int(ox - si(4) - leg_spread)
    right_leg_x = int(ox + si(2) + leg_spread)
    outline_rect(draw, left_leg_x, int(oy - boot_h - leg_h), leg_w, leg_h, body_s)
    outline_rect(draw, right_leg_x, int(oy - boot_h - leg_h), leg_w, leg_h, body_s)

    # Torso
    torso_w, torso_h = si(14), si(14)
    torso_x = int(ox - torso_w//2 + lean)
    torso_y = int(oy - boot_h - leg_h - torso_h)
    outline_rect(draw, torso_x, torso_y, torso_w, torso_h, body)
    # Highlight strip
    rect(draw, torso_x + 2, torso_y + 2, si(3), torso_h - 4, body_h)
    # Belt
    rect(draw, torso_x + 1, torso_y + torso_h - si(3), torso_w - 2, si(2), accent)

    # Cape
    if cape:
        cape_w, cape_h = si(8), si(16)
        cape_x = int(ox + torso_w//2 - si(2))
        cape_y = torso_y + si(2)
        outline_rect(draw, cape_x, cape_y, cape_w, cape_h, cape)

    # Arms
    arm_w, arm_h = si(5), si(12)
    left_arm_x = torso_x - arm_w + 1
    right_arm_x = torso_x + torso_w - 1
    arm_y = torso_y + si(2)

    if arm_angle == 0:
        outline_rect(draw, left_arm_x, arm_y, arm_w, arm_h, skin)
        outline_rect(draw, right_arm_x, arm_y, arm_w, arm_h, skin)
    else:
        # Raised arm for attack
        outline_rect(draw, left_arm_x, arm_y, arm_w, arm_h, skin)
        outline_rect(draw, right_arm_x, arm_y - si(arm_angle), arm_w, arm_h, skin)

    # Head
    head_w, head_h = si(12), si(12)
    head_x = int(ox - head_w//2 + lean)
    head_y = torso_y - head_h + si(1)
    outline_rect(draw, head_x, head_y, head_w, head_h, skin)
    # Shadow on face
    rect(draw, head_x + head_w - si(4), head_y + si(2), si(3), head_h - si(4), skin_s)

    # Eyes
    eye_y = head_y + si(4)
    px(draw, head_x + si(3), eye_y, eye)
    px(draw, head_x + si(7), eye_y, eye)

    # Hat/helmet
    if hat_fn:
        hat_fn(draw, head_x, head_y, head_w, head_h, si)

    # Weapon
    if weapon_fn:
        weapon_fn(draw, right_arm_x + arm_w, arm_y, si, arm_angle)


def draw_monster_body(draw, cx, foot_y, body, body_s, body_h, accent, eye_col,
                      has_horns=False, has_tail=False, has_wings=False,
                      head_shape="round", shift_x=0, shift_y=0,
                      leg_spread=0, arm_up=0, scale=1.0):
    """Draw a monster character."""
    s = scale
    ox = cx + shift_x
    oy = foot_y + shift_y

    def si(v): return max(1, int(v * s))

    # Feet
    foot_w, foot_h = si(6), si(3)
    rect(draw, int(ox - si(5) - leg_spread), int(oy - foot_h), foot_w, foot_h, OUTLINE)
    rect(draw, int(ox - si(4) - leg_spread), int(oy - foot_h), foot_w - 2, foot_h - 1, body_s)
    rect(draw, int(ox + si(1) + leg_spread), int(oy - foot_h), foot_w, foot_h, OUTLINE)
    rect(draw, int(ox + si(2) + leg_spread), int(oy - foot_h), foot_w - 2, foot_h - 1, body_s)

    # Legs
    leg_h = si(8)
    leg_w = si(4)
    outline_rect(draw, int(ox - si(4) - leg_spread), int(oy - foot_h - leg_h), leg_w, leg_h, body_s)
    outline_rect(draw, int(ox + si(2) + leg_spread), int(oy - foot_h - leg_h), leg_w, leg_h, body_s)

    # Body (wider for monsters)
    torso_w, torso_h = si(16), si(14)
    torso_x = int(ox - torso_w//2)
    torso_y = int(oy - foot_h - leg_h - torso_h)
    outline_rect(draw, torso_x, torso_y, torso_w, torso_h, body)
    rect(draw, torso_x + 2, torso_y + 2, si(4), torso_h - 4, body_h)
    # Belly accent
    rect(draw, torso_x + si(4), torso_y + si(6), si(6), si(5), accent)

    # Arms
    arm_w, arm_h = si(5), si(10)
    left_arm_x = torso_x - arm_w + 1
    right_arm_x = torso_x + torso_w - 1
    arm_y = torso_y + si(3)
    outline_rect(draw, left_arm_x, arm_y, arm_w, arm_h, body_s)
    outline_rect(draw, right_arm_x, arm_y - si(arm_up), arm_w, arm_h, body_s)

    # Head
    head_w, head_h = si(14), si(12)
    head_x = int(ox - head_w//2)
    head_y = torso_y - head_h + si(2)
    outline_rect(draw, head_x, head_y, head_w, head_h, body)
    rect(draw, head_x + head_w - si(4), head_y + si(2), si(3), head_h - si(4), body_s)

    # Eyes (bigger, scarier)
    ey = head_y + si(4)
    rect(draw, head_x + si(3), ey, si(2), si(2), eye_col)
    rect(draw, head_x + si(8), ey, si(2), si(2), eye_col)

    # Horns
    if has_horns:
        for hx in [head_x + si(2), head_x + head_w - si(4)]:
            outline_rect(draw, hx, head_y - si(6), si(3), si(6), accent)

    # Tail
    if has_tail:
        tx = torso_x + torso_w
        ty = torso_y + torso_h - si(4)
        rect(draw, tx, ty, si(8), si(3), OUTLINE)
        rect(draw, tx, ty + 1, si(7), si(1), body_s)

    # Wings
    if has_wings:
        wx = torso_x - si(8)
        wy = torso_y
        # Left wing
        for i in range(si(6)):
            rect(draw, wx + i, wy + i, si(2), si(8) - i, body_s)
        # Right wing
        wrx = torso_x + torso_w + si(2)
        for i in range(si(6)):
            rect(draw, wrx + si(5) - i, wy + i, si(2), si(8) - i, body_s)


def make_sheets(name, cell_w, cell_h, draw_fn, category=""):
    """Generate all 4 animation sheets for a character."""
    out_dir = os.path.join(SPRITE_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    frames = {"idle": 2, "walk": 4, "attack": 7, "death": 4}

    for anim, count in frames.items():
        img = Image.new("RGBA", (cell_w * count, cell_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for f in range(count):
            fx = f * cell_w
            draw_fn(draw, fx, cell_w, cell_h, anim, f, count)

        img.save(os.path.join(out_dir, f"{anim}.png"))

    print(f"  ✓ {name} ({cell_w}x{cell_h})")


# ═══════════════════════════════════════════════════════════════
#  HERO DEFINITIONS
# ═══════════════════════════════════════════════════════════════

def make_hero(name, body, body_s, body_h, accent, accent_d, skin, skin_s, eye,
              hat_fn=None, weapon_fn=None, cape=None):
    """Create a hero sprite set."""
    CW, CH = 80, 80
    foot_y = 74
    cx = 40

    def draw_frame(draw, fx, cw, ch, anim, f, count):
        sy = 0
        lsp = 0
        arm = 0
        lean = 0

        if anim == "idle":
            sy = -1 if f == 1 else 0
        elif anim == "walk":
            lsp = [-2, 0, 2, 0][f]
            sy = [0, -1, 0, -1][f]
        elif anim == "attack":
            if f < 2: arm = f * 4
            elif f == 2: arm = 10
            elif f == 3: arm = 8; lean = -2
            elif f == 4: arm = 0; lean = 2
            elif f == 5: arm = 0; lean = 1
            else: arm = 0
        elif anim == "death":
            if f == 0: pass
            elif f == 1: lean = 3; sy = 2
            elif f == 2: lean = 6; sy = 5
            elif f == 3: lean = 8; sy = 10

        draw_humanoid(draw, fx + cx, foot_y, body, body_s, body_h, accent, accent_d,
                      skin, skin_s, eye, hat_fn=hat_fn, weapon_fn=weapon_fn,
                      cape=cape, shift_y=sy, leg_spread=lsp, arm_angle=arm, lean=lean)

    make_sheets(name, CW, CH, draw_frame, "hero")


def make_monster(name, body, body_s, body_h, accent, eye_col,
                 has_horns=False, has_tail=False, has_wings=False):
    """Create a monster sprite set."""
    CW, CH = 80, 80
    foot_y = 72
    cx = 40

    def draw_frame(draw, fx, cw, ch, anim, f, count):
        sy = 0; lsp = 0; arm = 0

        if anim == "idle":
            sy = -1 if f == 1 else 0
        elif anim == "walk":
            lsp = [-2, 0, 2, 0][f]
            sy = [0, -1, 0, -1][f]
        elif anim == "attack":
            if f < 2: arm = f * 3
            elif f == 2: arm = 8
            elif f == 3: arm = 6
            elif f == 4: arm = 2
            else: arm = 0
        elif anim == "death":
            if f == 0: pass
            elif f == 1: sy = 3
            elif f == 2: sy = 8
            elif f == 3: sy = 14

        draw_monster_body(draw, fx + cx, foot_y, body, body_s, body_h, accent, eye_col,
                         has_horns=has_horns, has_tail=has_tail, has_wings=has_wings,
                         shift_y=sy, leg_spread=lsp, arm_up=arm)

    make_sheets(name, CW, CH, draw_frame, "monster")


def make_boss(name, body, body_s, body_h, accent, eye_col,
              has_horns=False, has_tail=False, has_wings=False):
    """Create a boss sprite set (112x112)."""
    CW, CH = 112, 112
    foot_y = 102
    cx = 56

    def draw_frame(draw, fx, cw, ch, anim, f, count):
        sy = 0; lsp = 0; arm = 0
        sc = 1.4  # bosses are bigger

        if anim == "idle":
            sy = -2 if f == 1 else 0
        elif anim == "walk":
            lsp = [-3, 0, 3, 0][f]
            sy = [0, -2, 0, -2][f]
        elif anim == "attack":
            if f < 2: arm = f * 4
            elif f == 2: arm = 12
            elif f == 3: arm = 8
            elif f == 4: arm = 3
            else: arm = 0
        elif anim == "death":
            if f == 0: pass
            elif f == 1: sy = 4
            elif f == 2: sy = 10
            elif f == 3: sy = 18

        draw_monster_body(draw, fx + cx, foot_y, body, body_s, body_h, accent, eye_col,
                         has_horns=has_horns, has_tail=has_tail, has_wings=has_wings,
                         shift_y=sy, leg_spread=lsp, arm_up=arm, scale=sc)

    make_sheets(name, CW, CH, draw_frame, "boss")


# ═══════════════════════════════════════════════════════════════
#  HAT / WEAPON FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def hat_wizard(draw, hx, hy, hw, hh, si):
    """Pointed wizard hat."""
    brim_y = hy - si(2)
    rect(draw, hx - si(2), brim_y, hw + si(4), si(3), OUTLINE)
    rect(draw, hx - si(1), brim_y + 1, hw + si(2), si(1), (60, 40, 100, 255))
    # Point
    for i in range(si(8)):
        w = max(1, si(6) - i)
        px_x = hx + hw//2 - w//2
        rect(draw, px_x, brim_y - i - 1, w, 1, (80, 50, 130, 255))
    rect(draw, hx + hw//2 - 1, brim_y - si(8), si(2), 1, OUTLINE)

def hat_hood(draw, hx, hy, hw, hh, si):
    """Monk/assassin hood."""
    outline_rect(draw, hx - si(1), hy - si(4), hw + si(2), si(5), (70, 60, 50, 255))
    # Peak
    rect(draw, hx + hw//2 - si(1), hy - si(6), si(3), si(3), (70, 60, 50, 255))

def hat_samurai(draw, hx, hy, hw, hh, si):
    """Samurai kabuto helmet."""
    outline_rect(draw, hx - si(3), hy - si(2), hw + si(6), si(4), (100, 80, 40, 255))
    # Crest
    rect(draw, hx + hw//2 - si(1), hy - si(7), si(2), si(5), (180, 50, 30, 255))

def hat_pirate(draw, hx, hy, hw, hh, si):
    """Pirate tricorn."""
    outline_rect(draw, hx - si(2), hy - si(2), hw + si(4), si(4), (40, 30, 25, 255))
    # Skull emblem
    px(draw, hx + hw//2, hy - si(1), (200, 200, 200, 255))

def hat_ninja(draw, hx, hy, hw, hh, si):
    """Ninja mask - covers most of face."""
    rect(draw, hx, hy + si(6), hw, si(5), (30, 30, 40, 255))

def hat_bard(draw, hx, hy, hw, hh, si):
    """Bard's feathered cap."""
    outline_rect(draw, hx - si(1), hy - si(3), hw + si(2), si(4), (120, 40, 40, 255))
    # Feather
    rect(draw, hx + hw - si(2), hy - si(7), si(2), si(5), (200, 180, 50, 255))

def hat_druid(draw, hx, hy, hw, hh, si):
    """Antler crown."""
    for dx in [si(1), hw - si(3)]:
        rect(draw, hx + dx, hy - si(6), si(2), si(6), (140, 100, 50, 255))
        px(draw, hx + dx - 1, hy - si(5), (140, 100, 50, 255))
        px(draw, hx + dx + si(2), hy - si(5), (140, 100, 50, 255))

def hat_crown(draw, hx, hy, hw, hh, si):
    """Royal crown."""
    outline_rect(draw, hx - si(1), hy - si(3), hw + si(2), si(4), (200, 170, 40, 255))
    for i in range(3):
        px(draw, hx + si(2) + i * si(4), hy - si(5), (200, 170, 40, 255))
        px(draw, hx + si(2) + i * si(4), hy - si(4), (220, 50, 50, 255))

def hat_berserker(draw, hx, hy, hw, hh, si):
    """Horned helm."""
    outline_rect(draw, hx - si(1), hy - si(2), hw + si(2), si(3), (100, 90, 80, 255))
    rect(draw, hx - si(2), hy - si(7), si(3), si(6), (180, 170, 140, 255))
    rect(draw, hx + hw - si(1), hy - si(7), si(3), si(6), (180, 170, 140, 255))

def weapon_sword(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(4), si(2), si(14), (180, 180, 200, 255))
    rect(draw, wx - si(2), wy - si(arm_angle) + si(2), si(6), si(2), (140, 120, 60, 255))

def weapon_staff(draw, wx, wy, si, arm_angle):
    rect(draw, wx + si(1), wy - si(arm_angle) - si(6), si(2), si(18), (120, 80, 40, 255))
    rect(draw, wx, wy - si(arm_angle) - si(8), si(4), si(4), (80, 200, 80, 255))

def weapon_katana(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(6), si(2), si(16), (200, 210, 220, 255))
    rect(draw, wx - si(1), wy - si(arm_angle) + si(2), si(4), si(2), (180, 50, 30, 255))

def weapon_dagger(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(2), si(2), si(8), (170, 175, 185, 255))

def weapon_lute(draw, wx, wy, si, arm_angle):
    outline_rect(draw, wx - si(2), wy + si(2), si(8), si(10), (160, 110, 50, 255))
    rect(draw, wx, wy + si(5), si(3), si(3), (40, 30, 20, 255))

def weapon_cutlass(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(3), si(2), si(12), (180, 180, 190, 255))
    # Curved guard
    rect(draw, wx - si(2), wy - si(arm_angle) + si(1), si(6), si(2), (200, 170, 40, 255))

def weapon_shuriken(draw, wx, wy, si, arm_angle):
    rect(draw, wx + si(3), wy - si(arm_angle), si(4), si(4), (140, 140, 160, 255))
    px(draw, wx + si(5), wy - si(arm_angle) + si(1), (200, 200, 220, 255))

def weapon_dual_axes(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(2), si(2), si(10), (120, 80, 40, 255))
    rect(draw, wx - si(1), wy - si(arm_angle) - si(3), si(5), si(4), (160, 160, 170, 255))

def weapon_mace(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy - si(arm_angle) - si(2), si(2), si(12), (120, 80, 40, 255))
    outline_rect(draw, wx - si(1), wy - si(arm_angle) - si(5), si(5), si(5), (160, 160, 170, 255))

def weapon_crossbow(draw, wx, wy, si, arm_angle):
    rect(draw, wx, wy + si(1), si(10), si(2), (100, 70, 40, 255))
    rect(draw, wx + si(3), wy - si(2), si(2), si(6), (100, 70, 40, 255))
    rect(draw, wx + si(1), wy, si(8), si(1), (140, 130, 100, 255))


# ═══════════════════════════════════════════════════════════════
#  BUILD ALL SPRITES
# ═══════════════════════════════════════════════════════════════

print("=== 10 NEW HEROES ===")

# 1. Samurai — red/black, katana
make_hero("samurai",
    body=(60, 30, 30, 255), body_s=(40, 20, 20, 255), body_h=(90, 40, 40, 255),
    accent=(180, 50, 30, 255), accent_d=(120, 30, 20, 255),
    skin=(220, 180, 140, 255), skin_s=(180, 140, 100, 255), eye=(20, 20, 20, 255),
    hat_fn=hat_samurai, weapon_fn=weapon_katana)

# 2. Monk — brown robes, staff
make_hero("monk",
    body=(140, 110, 70, 255), body_s=(100, 80, 50, 255), body_h=(170, 140, 90, 255),
    accent=(180, 150, 90, 255), accent_d=(120, 90, 50, 255),
    skin=(200, 160, 120, 255), skin_s=(160, 120, 80, 255), eye=(40, 30, 20, 255),
    hat_fn=hat_hood, weapon_fn=weapon_staff)

# 3. Bard — red/gold, lute
make_hero("bard",
    body=(140, 40, 40, 255), body_s=(100, 30, 30, 255), body_h=(180, 60, 60, 255),
    accent=(200, 170, 40, 255), accent_d=(150, 120, 30, 255),
    skin=(210, 170, 130, 255), skin_s=(170, 130, 90, 255), eye=(30, 40, 60, 255),
    hat_fn=hat_bard, weapon_fn=weapon_lute)

# 4. Druid — green/brown, antlers
make_hero("druid",
    body=(50, 90, 50, 255), body_s=(35, 65, 35, 255), body_h=(70, 120, 70, 255),
    accent=(140, 100, 50, 255), accent_d=(100, 70, 30, 255),
    skin=(190, 160, 120, 255), skin_s=(150, 120, 80, 255), eye=(40, 80, 40, 255),
    hat_fn=hat_druid, weapon_fn=weapon_staff)

# 5. Warlock — purple/black, dark staff
make_hero("warlock",
    body=(60, 30, 80, 255), body_s=(40, 20, 55, 255), body_h=(90, 50, 120, 255),
    accent=(150, 50, 180, 255), accent_d=(100, 30, 120, 255),
    skin=(180, 160, 170, 255), skin_s=(140, 120, 130, 255), eye=(200, 50, 200, 255),
    hat_fn=hat_wizard, weapon_fn=weapon_staff, cape=(80, 40, 100, 255))

# 6. Berserker — grey/red, dual axes
make_hero("berserker",
    body=(90, 80, 70, 255), body_s=(60, 55, 48, 255), body_h=(120, 110, 95, 255),
    accent=(180, 50, 30, 255), accent_d=(130, 35, 20, 255),
    skin=(200, 170, 140, 255), skin_s=(160, 130, 100, 255), eye=(180, 40, 30, 255),
    hat_fn=hat_berserker, weapon_fn=weapon_dual_axes)

# 7. Crossbowman — brown/tan
make_hero("crossbowman",
    body=(100, 80, 50, 255), body_s=(70, 55, 35, 255), body_h=(130, 110, 70, 255),
    accent=(60, 90, 60, 255), accent_d=(40, 65, 40, 255),
    skin=(210, 175, 135, 255), skin_s=(170, 135, 95, 255), eye=(40, 50, 30, 255),
    weapon_fn=weapon_crossbow)

# 8. Priest — white/gold
make_hero("priest",
    body=(210, 200, 190, 255), body_s=(170, 160, 150, 255), body_h=(230, 225, 220, 255),
    accent=(200, 170, 40, 255), accent_d=(160, 130, 30, 255),
    skin=(200, 165, 130, 255), skin_s=(160, 125, 90, 255), eye=(40, 60, 100, 255),
    hat_fn=hat_crown, weapon_fn=weapon_mace)

# 9. Pirate — dark blue/brown
make_hero("pirate",
    body=(40, 50, 70, 255), body_s=(28, 35, 50, 255), body_h=(60, 70, 100, 255),
    accent=(140, 100, 40, 255), accent_d=(100, 70, 25, 255),
    skin=(200, 160, 120, 255), skin_s=(160, 120, 80, 255), eye=(20, 20, 20, 255),
    hat_fn=hat_pirate, weapon_fn=weapon_cutlass)

# 10. Ninja — black/dark grey
make_hero("ninja",
    body=(35, 35, 45, 255), body_s=(25, 25, 32, 255), body_h=(55, 55, 65, 255),
    accent=(140, 30, 30, 255), accent_d=(100, 20, 20, 255),
    skin=(190, 155, 120, 255), skin_s=(150, 115, 80, 255), eye=(200, 200, 200, 255),
    hat_fn=hat_ninja, weapon_fn=weapon_shuriken)


print("\n=== 5 NEW MONSTERS ===")

# 1. Spider — dark brown, red eyes
make_monster("spider",
    body=(70, 50, 30, 255), body_s=(50, 35, 20, 255), body_h=(95, 70, 45, 255),
    accent=(40, 30, 20, 255), eye_col=(200, 30, 30, 255))

# 2. Rat — grey/brown
make_monster("rat",
    body=(120, 100, 80, 255), body_s=(90, 70, 55, 255), body_h=(150, 130, 105, 255),
    accent=(170, 140, 110, 255), eye_col=(200, 50, 50, 255), has_tail=True)

# 3. Mushroom — purple/green toxic
make_monster("mushroom",
    body=(140, 80, 160, 255), body_s=(100, 55, 115, 255), body_h=(170, 110, 190, 255),
    accent=(80, 180, 80, 255), eye_col=(200, 255, 80, 255))

# 4. Eye Beast — purple, one big eye
make_monster("eyebeast",
    body=(100, 60, 130, 255), body_s=(70, 40, 95, 255), body_h=(130, 85, 165, 255),
    accent=(200, 200, 220, 255), eye_col=(255, 50, 50, 255), has_wings=True)

# 5. Bat — dark purple wings
make_monster("bat",
    body=(60, 40, 70, 255), body_s=(40, 25, 50, 255), body_h=(85, 60, 95, 255),
    accent=(80, 50, 90, 255), eye_col=(255, 200, 50, 255), has_wings=True)


print("\n=== 3 NEW REGULAR BOSSES ===")

# 1. Dragon — green/gold
make_boss("dragon",
    body=(40, 100, 40, 255), body_s=(28, 70, 28, 255), body_h=(60, 135, 60, 255),
    accent=(200, 170, 40, 255), eye_col=(255, 200, 50, 255),
    has_horns=True, has_tail=True, has_wings=True)

# 2. Lich — pale blue/purple undead wizard
make_boss("lich",
    body=(60, 60, 100, 255), body_s=(40, 40, 70, 255), body_h=(85, 85, 135, 255),
    accent=(150, 50, 200, 255), eye_col=(100, 255, 100, 255))

# 3. Minotaur — brown/red, horned
make_boss("minotaur",
    body=(120, 80, 50, 255), body_s=(85, 55, 35, 255), body_h=(155, 110, 70, 255),
    accent=(180, 50, 30, 255), eye_col=(255, 80, 50, 255),
    has_horns=True)


print("\n=== 2 NEW MEGA BOSSES ===")

# 1. Hydra — dark teal, multi-headed (drawn with extra heads)
make_boss("hydra",
    body=(30, 90, 90, 255), body_s=(20, 65, 65, 255), body_h=(50, 120, 120, 255),
    accent=(50, 150, 120, 255), eye_col=(255, 255, 80, 255),
    has_tail=True)

# 2. Death Knight — black armor, red eyes
make_boss("deathknight",
    body=(40, 35, 45, 255), body_s=(25, 22, 30, 255), body_h=(65, 58, 72, 255),
    accent=(180, 30, 30, 255), eye_col=(255, 30, 30, 255),
    has_horns=True)


print("\n✅ All 20 sprites generated!")
