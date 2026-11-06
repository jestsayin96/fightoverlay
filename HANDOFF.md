# Jester's Village — handoff

A Twitch stream overlay. Chat members become adventurers who march in from the
left; monsters and bosses come from the right; they meet and fight along the
bottom of the frame. Runs as a single OBS Browser Source.

**Live:** https://jestsayin96.github.io/fightoverlay/
**Repo:** https://github.com/jestsayin96/fightoverlay

---

## 1. What exists

### Delivery
One self-contained `index.html`. No build step, no server, no dependencies.
A GitHub Actions workflow publishes it to Pages on every push to `main`, so
OBS points at a URL and a refresh picks up changes.

### Connection
- **Chat avatars need no credentials.** Twitch permits anonymous IRC reads, so
  the overlay joins `wss://irc-ws.chat.twitch.tv:443` as `justinfan<random>`.
  Type a channel name, press START.
- **Follows, subs and channel points are optional** and need a token with
  `moderator:read:followers`, `channel:read:redemptions`,
  `channel:read:subscriptions`. Entered in the setup panel, stored in that
  browser only.

### Architecture
Three layers, deliberately separated:

| Layer | Responsibility |
|---|---|
| `PLATFORMS` | One entry per service. Owns transport only (IRC, EventSub). Translates to `Game.*`. |
| `Game` | Four normalised events: `chat`, `follow`, `sub`, `redeem`. The only surface the outside world touches. |
| Simulation + render | Knows nothing about Twitch. |

Adding YouTube or Kick is a new `PLATFORMS` entry plus a setup button. Nothing
in the game changes. A commented stub marks the spot.

### Simulation
- Two armies. Heroes enter at `heroGate` (left), monsters at `mobGate` (right).
- Each advances on the nearest enemy; on contact they stop and trade blows.
- With nothing to fight they walk to a hold line and mill about on foot.
- Downed heroes crawl off, wait ~9s, and march back on at full health.
- Monsters die permanently. A boss cleaves everything in range.
- Dead air spawns a wandering monster every 5s while under 8 monsters.

### Identity and persistence
A viewer's username hash decides their class, their signature spell and their
sprite — the same person is the same character forever. Levels, kills, deaths,
hats and colours persist in `localStorage`, so regulars are already on screen
when the overlay opens. **Wipe Save** resets everyone.

### Abilities
Eight signature spells assigned by username: Fireball, Chain Lightning,
Whirlwind, Holy Smite, Frost Nova, Venom Cloud, Mending Light, Crescent Slash.
Meteor unlocks at level 10. Damage scales with level. The spell also decides
the character's class.

### Art
`sprites/dungeon/` — 0x72 "DungeonTileset II", CC0. Six hero classes, eight
monsters, three bosses, upscaled 3x onto a 112x120 cell with the feet anchored
at (56,112) so nothing jumps between animations.

`sprites/knight_*.png` — generated, unused. Kept as a reference for the
extraction pipeline. Its walk frames differ by only 3-6% of silhouette, so the
character slid instead of walking.

### Chat commands
`!jump` `!dance` `!wave` `!sit` `!hat` `!color red` `!stats`

---

## 2. Known problems

Ordered by how much they hurt.

### Characters clump
Everyone advances to the same point and piles into a heap, nameplates stacking
six deep. Needs per-entity spacing — a desired separation from neighbours, or
staggered hold positions — so they form a line.

### No attack or death animation
The CC0 pack ships idle, run and one hurt frame. An attack currently lunges
forward through the walk frames while the slash arc and sparks carry the hit;
death holds the hurt pose and topples. Readable, but a workaround.

### The field is lopsided
Heroes crowd one spot while stragglers trail behind and monsters sit near the
right edge. `heroHold` / `mobHold` want retuning against a real stream.

### Every viewer of a class looks identical
A sprite is a fixed image, so all knights are the same knight. The fix is
runtime palette-swapping: the sheets use a tight known palette, so remapping
armour colours per username would give everyone a distinct look from one sheet.

### Untested on a live stream
Nobody has watched this with real chat moving. Readability over bright
gameplay, pacing during quiet chat, and whether it distracts the streamer are
all unknown.

---

## 3. Worth adding

**Progression people can feel.** Levels exist but do little. A visible rank,
gear that changes the sprite, or a "what happened to my guy overnight" recap
would give viewers a reason to return.

**A stage counter.** Nothing persists across streams except per-viewer stats.
A monster-kill count that climbs all month turns isolated fights into a
campaign.

**Chat feedback.** The overlay cannot talk back — it reads chat anonymously.
Sending requires a bot token, but `!stats` answering in chat would close the
loop.

**Sound.** Silent. A hit thud and a boss roar would carry a lot.

**A settings UI.** Tuning constants live in the `T` block in source. Fine for
one person, insufficient for anyone else.

**YouTube and Kick.** The seam exists; nobody has built through it.

---

## 4. Tuning

Everything worth changing is the `T` block near the top of the script.

| Setting | Effect |
|---|---|
| `stripTop` / `stripBot` | How high up the frame fighters stand |
| `march` | Walk speed, px/sec |
| `heroHold` / `mobHold` | Where each side waits with nothing to fight |
| `maxHeroes` / `maxMobs` | Bodies on screen |
| `idleSpawn` / `idleFloor` | Monster rate during dead air |
| `engage` | Distance before swinging |

Sprite scale is the `112x120` cell and `ANCHOR_*` constants above `SPRITES`.

Keys for testing outside OBS: `S` setup, `D` demo, `B` boss, `M` monster,
`H` hero, `L` loot.

---

## 5. Lessons worth keeping

**Image generators cannot make animation frames.** Measured: the generated
attack and death sheets changed 40-74% of silhouette between frames, but the
walk changed 3-6% — it drew the same pose four times. Big pose changes work;
subtle cyclic ones do not.

**Reference images fix character drift.** Text-only prompts produced a
different knight each sheet. Attaching the first sheet as a reference held it.

**Key on a colour the art never uses.** A flat magenta background keys out
cleanly; erode one pixel to kill JPEG fringe.

**Anchor on ground contact, not the bounding box.** A sword extending sideways
drags a bbox-centred anchor and makes the character slide mid-swing.

**Pre-rendered 3D is a different look, not a better one.** Rendering a 3D model
down to 60px does not produce hand-drawn pixel art. If the target is pixel art,
3D is the wrong tool.

**Check animation in motion, not stills.** A sign error made every character
moonwalk for hours; it was invisible in screenshots and obvious in two seconds
of movement.
