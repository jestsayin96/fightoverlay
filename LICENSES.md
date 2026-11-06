# Asset and dependency licenses

Every asset shipped in this repo, where it came from, and what we're allowed
to do with it. Add a row **when you add the asset**, not later.

## Why this file exists

The overlay may become a product one day. Copyleft licenses (GPL, CC-BY-SA)
cannot practically be removed once artwork is built on them — every derived
sprite becomes a derivative work. So this project **only accepts assets that
are CC0, public domain, originally generated for this project, or
commissioned with rights assigned.**

### Not allowed in this repo

| License | Why it's excluded |
|---|---|
| GPL / LGPL (art) | Copyleft; arguably forces the whole work to be GPL |
| CC-BY-SA | Share-alike; derivatives must carry the same license |
| CC-BY-NC | Non-commercial only |
| "Free for personal use" | Not licensed for a product |

This rules out the Liberated Pixel Cup (LPC) asset set and its character
generator, which is GPL-3.0 with CC-BY-SA art. It is a good set and a poor
fit for anything sellable. Don't use it here.


## Original art — owned outright

| Asset | Origin | License | Notes |
|---|---|---|---|
| `sprites/knight/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (36,74). 2/4/7/4 frames. |
| `sprites/goblin/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (38,72). 2/4/7/4 frames. Replaces the 0x72 goblin. |
| `sprites/mage/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 mage. |
| `sprites/rogue/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 rogue. |
| `sprites/barbarian/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 barbarian. |
| `sprites/paladin/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 paladin. |
| `sprites/cleric/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 cleric. All six hero classes are now original. |
| `sprites/ranger/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,76), 60px tall. 2/4/7/4 frames. A seventh hero class, not a replacement — the first ranged hero. |
| `sprites/skeleton/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74). 2/4/7/4 frames. Replaces the 0x72 skeleton. |
| `sprites/orc_warrior/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 62px tall. 2/4/7/4 frames. Replaces the 0x72 orc warrior and returns it to rotation. |
| `sprites/imp/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 50px tall. 2/4/7/4 frames. Replaces the 0x72 imp and returns it to rotation. |
| `sprites/chort/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 58px tall. 2/4/7/4 frames. Replaces the 0x72 chort and returns it to rotation. |
| `sprites/zombie/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 58px tall. 2/4/7/4 frames. Replaces the 0x72 zombie and returns it to rotation. |
| `sprites/masked_orc/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 58px tall. 2/4/7/4 frames. Replaces the 0x72 masked orc and returns it to rotation. |
| `sprites/swampy/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 40x40 art exported at 2x -> 80x80 cells, feet at (40,74), 58px tall and 74px wide. 2/4/7/4 frames. Replaces the 0x72 swampy and returns it to rotation. **All eight monsters are now original**, so nothing in `sprites/dungeon/` is referenced any more. |
| `sprites/ogre/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 56x56 art exported at 2x -> 112x112 cells, feet at (56,102), 88px tall. 2/4/7/4 frames. Replaces the 0x72 ogre boss. |
| `sprites/demon/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 56x56 art exported at 2x -> 112x112 cells, feet at (58,102), 90px tall. 2/4/7/4 frames. Replaces the 0x72 demon boss. Eight parts, including a wing. |
| `sprites/bigzombie/{idle,walk,attack,death}.png` | Drawn from scratch in Pixelwright for this project | **Ours.** No third-party rights. | 56x56 art exported at 2x -> 112x112 cells, feet at (58,102), 88px tall. 2/4/7/4 frames. Replaces the 0x72 big zombie boss. All three bosses are now original. |

This is the first art in the project with **no upstream license at all** — not
even CC0 attribution. It can be sold, relicensed, or redrawn freely. It is also
the first set with genuine `attack` and `death` clips rather than the borrowed
`hurt` cell the 0x72 pack forces.

That goal is now fully met. All six hero classes, all eight monsters and
all three bosses are original. No 0x72 sprite is loaded on the field, and
no name is held back waiting to be redrawn — the replacement is complete.
The pack is still vendored in `sprites/dungeon/` and still credited below,
but nothing in `index.html` references it; it could be deleted outright
without changing a pixel of what the overlay draws. `defSprite` still takes
a geometry argument, which is what let the 80x80 heroes and the 112x112
bosses share one lane while the replacement was under way.

## Sprites

| File | Source | License | Notes |
|---|---|---|---|
| `sprites/knight_idle.png` | Generated with Grok Imagine, Nov 2026 | No third-party rights claimed | Extracted, keyed and re-registered by this project |
| `sprites/knight_walk.png` | Generated with Grok Imagine, Nov 2026 | No third-party rights claimed | As above |
| `sprites/knight_attack.png` | Generated with Grok Imagine, Nov 2026 | No third-party rights claimed | As above |
| `sprites/knight_death.png` | Generated with Grok Imagine, Nov 2026 | No third-party rights claimed | As above |

**Caveat on generated art.** In the US, purely AI-generated images are not
copyrightable. They can be used and sold freely, but they can't be protected
against being copied. The art is not the moat here. If this ships as a paid
product, the character set is the thing to commission from a human — for
quality, and so the rights are actually owned. Get legal advice before
charging money.

### `sprites/dungeon/` — characters, monsters and bosses

| Field | Value |
|---|---|
| Pack | "DungeonTileset II" v1.3 |
| Author | Robert ("0x72") |
| License | **CC0 1.0** — public domain |
| Commercial use | Yes, explicitly permitted |
| Attribution | Not required; credited here anyway |
| Obtained from | A GitHub repository that vendors the pack, cloned over HTTPS |

Contains the six hero classes, eight monsters and three bosses, each with
4-frame idle and run animations (heroes also have a 1-frame hurt pose).
Source frames are 16x28 (heroes) up to 32x36 (bosses); this project scales
them 3x with nearest-neighbour and re-anchors them onto a 112x120 cell.

**Verification caveat.** The author distributes this pack on itch.io, which
is not reachable from the build environment, so the copy here came from a
third-party repository. An attempt to cross-check it byte-for-byte against a
second independent copy found no other repository carrying the pack, so that
check did not happen. The filenames, frame counts and dimensions all match
the documented pack, and CC0 permits use and modification regardless of
whether a copy was altered — but nobody has confirmed these files are
identical to the author's originals. Worth re-verifying against the itch.io
download before shipping commercially.

### `sprites/knight_*.png` — unused

Generated with Grok Imagine, Nov 2026. Kept for reference but not loaded by
the overlay: the walk sheet's four frames differ by only 3-6% of silhouette,
so the character slides rather than walks. See the caveat below on generated
art.

## Fonts

| Font | Source | License |
|---|---|---|
| Silkscreen | Google Fonts | SIL Open Font License 1.1 |
| VT323 | Google Fonts | SIL Open Font License 1.1 |

Both are OFL, which permits commercial use and embedding. They are loaded
from Google's CDN rather than bundled.

## Code

All JavaScript, HTML and CSS in this repo is original to this project. No
third-party libraries are bundled or loaded at runtime.

## Safe sources for future assets

- **Kenney** (kenney.nl) — CC0, no attribution required, commercial use fine.
- **OpenGameArt** — mixed; filter to CC0 only and record the author anyway.
- **Generated** — fine to use, see the caveat above.
- **Commissioned** — get a written assignment of rights, not just a license.
