# Jester's Village — handoff

A Twitch stream overlay. Chat members become adventurers who march in from the
left; monsters and bosses come from the right; they meet and fight along the
bottom of the frame. Runs as a single OBS Browser Source.

**Live:** https://jestsayin96.github.io/fightoverlay/
**Repo:** https://github.com/jestsayin96/fightoverlay

---


## The crowd piles up vertically, not horizontally

Worth knowing before you try to fix the clumping, because three obvious
approaches were tried and measured and all of them failed.

The fight concentrates: with 16 heroes, 60% of the bodies sit in the
busiest four of sixteen screen columns. Attempts to spread them sideways:

| approach | spread | cost |
|---|---|---|
| snap each duel to the nearest of 11 columns | 63% -> 60% | none, kept |
| deal columns to duels by rank order | 63% -> 55% | combat 43% -> 22% |
| widen the fight band (four widths tried) | no change | within noise |
| rally each pair to a computed meeting point | good | kill rate -75% |

Rank-dealing and rally points both fail the same way: `assignFoes`
re-pairs by distance every 0.4s, so the assignment keeps changing and
fighters chase a target that moves out from under them.

What actually worked was the other axis. Widening the lane from 111px to
161px halved the bodies close enough to overlap on screen - 62 pairs to
31 - with combat unchanged. If it still looks crowded, widen the lane
further before touching the horizontal logic again; 185px was measured
at 28 pairs, so there is a little more room, with diminishing returns.

## Art pipeline (Pixelwright -> overlay)

Every character on the field is original art now: six heroes, eight
monsters, three bosses. Nothing borrows the 0x72 pack's hurt frame to
fake an attack, nothing carries an upstream licence, and nothing in
`sprites/dungeon/` is referenced any more.

Eight upright humanoids would have read as one shape in eight colours at
stream size, so the last monster drawn, Swampy, is deliberately wider
than it is tall: a bog mound with a bump head and a pseudopod instead of
an arm. It is the only death in the cast that is not a figure falling
over -- it flattens into a puddle, via a second `body` variant rather
than a squash (see below).

| set | height | cells | feet |
|---|---|---|---|
| knight | 66px | 80x80 | (36,74) |
| paladin | 62px | 80x80 | (40,74) |
| mage | 62px | 80x80 | (40,74) |
| barbarian | 62px | 80x80 | (40,74) |
| cleric | 56px | 80x80 | (40,74) |
| rogue | 56px | 80x80 | (40,74) |
| mob_skelet | 54px | 80x80 | (40,74) |
| mob_goblin | 52px | 80x80 | (38,72) |
| mob_orc_warrior | 62px | 80x80 | (40,74) |
| mob_imp | 50px | 80x80 | (40,74) |
| mob_chort | 58px | 80x80 | (40,74) |
| mob_zombie | 58px | 80x80 | (40,74) |
| mob_masked_orc | 58px | 80x80 | (40,74) |
| mob_swampy | 58px tall, 74px wide | 80x80 | (40,74) |
| boss_demon | 90px | 112x112 | (58,102) |
| boss_ogre | 88px | 112x112 | (56,102) |
| boss_bigzombie | 88px | 112x112 | (58,102) |

Each has idle (2), walk (4), attack (7) and death (4) frames. The three
bosses are drawn on a 56x56 canvas rather than 40x40, so they export to a
112x112 cell; `defSprite`'s geometry argument is what lets them share a
lane with the 80x80 heroes.

### Drawing a new one

1. Rig it in Pixelwright: armBack, legBack, body, head, legFront,
   armFront, a weapon parented to armFront, and a `smear`. Give armFront
   and the weapon `raised` and `struck` variants and the smear
   `up`/`mid`/`down`.
2. Parts **cannot rotate**, so a swing needs a redrawn arm and weapon per
   key pose. Children inherit the parent's `dx/dy`, so keep a child's own
   offset to 1-2px or limbs detach.
3. The smear's default variant is whatever you write first, and it shows
   at rest - hide it explicitly in every frame that is not mid-swing.
4. `project_audit` until only deliberate findings remain. The recurring
   one: where the head's bottom outline sits on the body's top outline it
   reads as a thick dark bar at the neck. Make the lower row a dark shade
   of the fill, not a second outline, and keep the outline at its ends.
5. `export_build` preset `png-frames` at **scale 3**, then
   `build_char.py <name> <srcdir> <outdir>`. It recovers the true 40x40
   pixels (asserting the export really was a clean block upscale) and
   re-renders at 2x.
6. Register with `defSprite(key, files, geo)`. **Check two numbers the
   script gives you rather than trusting them:** `ax` is the bounding-box
   centre, which is wrong whenever anything juts out to one side - a
   weapon, or the Demon's wing, which dragged `ax` 10px off - so use the
   centre of the feet; and the figure height is whatever you happened to
   draw, so compare it against the table above before accepting it.
7. Monsters: add the name to `MOB_SPRITES`. Bosses: add a `defSprite`
   *after* the `BOSS_SPRITES.forEach` loop so it overrides the 0x72
   entry that loop makes.

**A big squash breaks the outline; draw the extreme pose as a variant
instead.** `rows: -n` takes rows out of the middle and leaves the rest
untouched, so the moment it eats past a shape's uniform middle it stacks
a wide row straight onto a narrow one and the outline cannot get round
the corner. Swampy's `-12` collapse produced gaps the shoulders and the
tapered base could not be redrawn out of, because no single silhouette
survives being cut by two thirds. The fix was a second `body` variant
drawn as an actual puddle, switched in for the last two death frames.
Stretching has the mirror-image fault: `rows: +n` repeats the middle row,
so a row with a 3-wide side outline becomes a solid dark slab. If a pose
needs more than about a third of a part removed or added, it is a new
picture, not a transform.

**Two mistakes that cost the most time, both the same shape.** An edge
that steps sideways faster than one pixel per row leaves the outline
behind and the audit fills with PX007 gaps - the Demon's wing stepped 2
per row and produced 103 of them, fixed by giving each step a two-wide
outline tread. And a key map cannot hold two letters that differ only in
case (`S`/`s`, `R`/`r`): the write is rejected outright. Drawing the Big
Zombie with both in mind brought it in at 6 findings against the Demon's
118.

`animOf` plays real `attack`/`death` clips when a set has them and
returns `real:true`; `drawSprite` then skips the lean-and-rotate faking
and the drawn slash arc, which would double up on the blade's own smear.

## Combat

The numbers are steered, not fixed. Hero damage scales with how many
viewers are watching and with which abilities their names roll, and the
fight is bistable - survivors accumulate, dilute the heroes' focus and
survive longer still. One set of constants measured across seeds gave
monster lifetimes anywhere from 2 to 32 seconds.

Two controllers in `steerDifficulty`:

- `V.mobTough` steers monster health toward `T.targetLife` (9s).
- `V.mobPower` steers monster damage toward `T.targetDowns`
  (0.5 knockdowns per hero per minute), fed by `V.downEma`.

If you change combat, measure it: drive `step(dt)` in a loop headlessly,
sample **every step** (a knockdown lasts 0.42s and will slip between
once-a-second samples), and run several name seeds - one run is noise.
Count knockdowns from `e.state === "down"` transitions, and note that
`yeet()` sets that state too.

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
`sprites/dungeon/` — 0x72 "DungeonTileset II", CC0. Still vendored, no longer
drawn: every hero, monster and boss on the field is original art, and no name
is held back waiting to be redrawn. Nothing in `index.html` references the
pack; it could be deleted outright without changing what the overlay draws.

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
