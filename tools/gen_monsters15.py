#!/usr/bin/env python3
"""Generate 15 more monster sprites to bring the total to 30."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_sprites import make_monster

print("=== 15 NEW MONSTERS ===")

# 1. Scorpion — dark red/brown, tail
make_monster("scorpion",
    body=(100, 40, 30, 255), body_s=(70, 28, 20, 255), body_h=(130, 60, 45, 255),
    accent=(60, 30, 20, 255), eye_col=(255, 200, 50, 255), has_tail=True)

# 2. Wolf — grey/white
make_monster("wolf",
    body=(100, 100, 110, 255), body_s=(70, 70, 78, 255), body_h=(135, 135, 145, 255),
    accent=(140, 140, 150, 255), eye_col=(200, 180, 50, 255), has_tail=True)

# 3. Beetle — dark green/metallic
make_monster("beetle",
    body=(30, 80, 50, 255), body_s=(20, 55, 35, 255), body_h=(50, 110, 70, 255),
    accent=(60, 120, 80, 255), eye_col=(255, 100, 50, 255))

# 4. Harpy — purple/tan, wings
make_monster("harpy",
    body=(150, 120, 90, 255), body_s=(110, 85, 60, 255), body_h=(180, 150, 115, 255),
    accent=(120, 60, 140, 255), eye_col=(200, 50, 200, 255), has_wings=True)

# 5. Toad — dark green/yellow belly
make_monster("toad",
    body=(50, 100, 40, 255), body_s=(35, 70, 28, 255), body_h=(70, 130, 60, 255),
    accent=(180, 180, 60, 255), eye_col=(200, 200, 50, 255))

# 6. Bandit — brown/black, human-ish
make_monster("bandit",
    body=(70, 55, 40, 255), body_s=(48, 38, 28, 255), body_h=(95, 78, 58, 255),
    accent=(140, 30, 30, 255), eye_col=(200, 200, 200, 255))

# 7. Shade — translucent dark purple
make_monster("shade",
    body=(50, 30, 70, 255), body_s=(35, 20, 50, 255), body_h=(70, 45, 95, 255),
    accent=(100, 60, 140, 255), eye_col=(180, 100, 255, 255))

# 8. Golem — grey/stone
make_monster("golem",
    body=(110, 105, 100, 255), body_s=(78, 74, 70, 255), body_h=(140, 135, 130, 255),
    accent=(80, 75, 70, 255), eye_col=(100, 200, 255, 255))

# 9. Serpent — dark teal/cyan
make_monster("serpent",
    body=(30, 90, 80, 255), body_s=(20, 62, 55, 255), body_h=(45, 120, 108, 255),
    accent=(40, 140, 120, 255), eye_col=(255, 255, 80, 255), has_tail=True)

# 10. Gargoyle — dark grey, wings
make_monster("gargoyle",
    body=(70, 65, 75, 255), body_s=(48, 44, 52, 255), body_h=(95, 90, 100, 255),
    accent=(90, 85, 95, 255), eye_col=(255, 150, 50, 255), has_wings=True, has_horns=True)

# 11. Worm — pink/brown
make_monster("worm",
    body=(160, 100, 100, 255), body_s=(120, 70, 70, 255), body_h=(190, 130, 130, 255),
    accent=(130, 70, 80, 255), eye_col=(30, 30, 30, 255))

# 12. Flame Sprite — orange/red
make_monster("flamesprite",
    body=(200, 100, 30, 255), body_s=(160, 70, 20, 255), body_h=(240, 140, 50, 255),
    accent=(255, 200, 50, 255), eye_col=(255, 255, 200, 255))

# 13. Ice Elemental — light blue/white
make_monster("iceelem",
    body=(100, 160, 200, 255), body_s=(70, 120, 160, 255), body_h=(140, 200, 240, 255),
    accent=(200, 230, 250, 255), eye_col=(50, 100, 255, 255))

# 14. Scarecrow — brown/straw yellow
make_monster("scarecrow",
    body=(120, 90, 40, 255), body_s=(85, 62, 28, 255), body_h=(155, 120, 60, 255),
    accent=(180, 160, 80, 255), eye_col=(255, 150, 30, 255))

# 15. Mimic — brown/gold (treasure chest monster)
make_monster("mimic",
    body=(100, 70, 30, 255), body_s=(70, 48, 20, 255), body_h=(135, 98, 45, 255),
    accent=(200, 170, 40, 255), eye_col=(255, 50, 50, 255))

print("\n✅ 15 new monsters generated!")
