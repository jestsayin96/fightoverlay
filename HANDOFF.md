# Jester's Village — handoff

A Twitch stream overlay. Chat members become adventurers who march in from the
left; monsters and bosses come from the right; they meet and fight along the
bottom of the frame. Runs as a single OBS Browser Source.

**Live:** https://jestsayin96.github.io/fightoverlay/
**Repo:** https://github.com/jestsayin96/fightoverlay

---


## Art pipeline (Pixelwright -> overlay)

The knight is original art and the template for replacing the rest.

1. Draw the rig in Pixelwright (parts + variants). Parts **cannot rotate**, so a
   sword swing needs a redrawn arm/blade per key pose, plus `smear` variants for
   the blur. Children inherit the parent's `dx/dy`, so keep child offsets to 1-2px
   or limbs detach.
2. `project_audit` until clean. Stacked outline rows where two parts meet are the
   big one: make the lower row a dark shade of the fill, not a second outline.
3. `export_build` preset `png-frames` at **scale 3**, then run
   `build_knight.py`: it recovers the true 40x40 pixels (asserting the export was
   a clean block upscale) and re-renders at **2x** so figures match the 0x72
   heroes' ~60px height. Exporting straight at 3x makes them 99px — far too big.
4. Drop the strips in `sprites/<name>/` and register with `defSprite(key, files, geo)`.

`animOf` plays real `attack`/`death` clips when a set has them and returns
`real:true`; `drawSprite` then skips the lean-and-rotate faking and the drawn
slash arc, which would otherwise double up on the blade's own smear.


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
`!hug` `!attack` `!bomb` `!explode` `!duel` `!accept` `!slots`
`!boss` `!royale` `!join` `!basketball` `!shoot` `!points` `!shop` `!buy`
`!leaderboard` `!avatar` `!hideavatar` `!lounge` `!war`
`!mass dance` is moderator / broadcaster only.

---

## 2. Known problems

Ordered by how much they hurt.

### Characters used to clump — formation is in
`lineGoal` gives every fighter a file and one of two lanes. With nothing to
fight, a side spreads back from its hold line. In a fight the front file
stops `frontGap` from the enemy and each file behind steps back by up to
`fileGap`, compressed only when the lane runs out of room. `unpile` is a
last-resort nudge for two bodies on the same pixel. Nameplates step sideways
before they stack upward. Still worth a look on a real stream: a very full
lane (26 heroes) gets tight, on purpose, rather than walking off screen.

### Attack and death are still performed, not drawn
The CC0 pack still has no attack or death cells. A second pack was not
mixed in — different proportions would break the 112×120 anchor, and
generated cycles already failed the walk test. What plays now:

- **Strike:** windup (lean back on idle), contact (lunge onto the hurt
  frame plus a local slash), recover. `e.swing` decays slower so the three
  beats read.
- **Hero down:** topples backward over ~0.4s, then crawls off with dust.
- **Monster death:** topples, squashes, and bursts into pixels.

### The field still wants a live-stream pass
Hold lines and `fileGap` are tuned for a 1920×1080 source, not for how this
reads over bright gameplay. Nobody has watched it with real chat yet.

### Viewers of a class no longer share one dye
On load, each sheet's dominant saturated hue (the armor) is remapped toward
that viewer's `look.shirt` (heroes) or `look.skin` (monsters). Outline,
skin, hair and plumes stay, so a knight is still a knight. `!color red`
changes the dye because it already writes `look.shirt`. Bosses are not
dyed. Cached per sheet + hue.

### Untested on a live stream
Readability over bright gameplay, pacing during quiet chat, and whether it
distracts the streamer are all still unknown.


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
