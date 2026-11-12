# fightoverlay

A Twitch stream overlay for [JestSayin96](https://twitch.tv/JestSayin96). Viewers who
talk in chat become adventurers who march in from the left. Monsters and bosses come
from the right. They meet in the middle and fight.

## Running it

**In OBS:** add a Browser source pointing at

```
https://jestsayin96.github.io/fightoverlay/?channel=YOURTWITCHNAME
```

Set it to **1920x1080**, and untick both **Shutdown source when not visible** and
**Refresh browser when scene becomes active** — either one wipes your viewers' hats and
points on every scene change. Put the source above your gameplay in the scene.

That is all the chat avatars need. Twitch allows anonymous chat reading, so there is no
token, no Client ID, and nothing to sign in to.

You can also leave the channel off the URL and set it in the panel: right-click the
source, choose **Interact**, press `S`, type the channel and press START.

## Running it on another channel

Nothing is hardcoded to one channel, so a second streamer does not need a copy, a fork
or a deploy of their own. They point their own OBS at the same hosted page with their
own name on it:

```
https://jestsayin96.github.io/fightoverlay/?channel=THEIRNAME
```

Their viewers' progress lives in their own browser, under a save key of their own (see
**Progress saves**), so the two channels never see each other's levels, coins or hats.

For follows, subs and channel points they need their **own** Twitch application — those
are tied to a broadcaster's account, not to this page. They register one as described
below and set its OAuth Redirect URL to this same page.

The trade-off worth saying out loud: they are running *this* copy. If this Pages site
changes or goes away, theirs changes or goes away with it.

Note that doing this is permitted by the [LICENSE](LICENSE); hosting their own public
copy is not.

## Optional: follows, subs and channel points

These need a Twitch token with three scopes:

- `moderator:read:followers`
- `channel:read:redemptions`
- `channel:read:subscriptions`

Generate one at twitchtokengenerator.com and type the Client ID and token into the
setup panel. They are stored in your browser only and are never sent anywhere except
Twitch.

**Never put the token in the URL.** This page is public; a token in a query string is
visible to anyone with the link.

With a token connected:

| Event | What happens |
|---|---|
| Follow | They join the monster side |
| Subscribe | They join the heroes, crowned |
| Channel points — title contains `boss`/`raid`/`titan` | Summons a boss |
| Channel points — title contains `loot`/`chest`/`treasure` | Drops a chest |
| Channel points — title contains `monster`/`mob`/`horde` | Spawns a tougher monster |

## Chat commands

Actions: `!jump` `!dance` `!wave` `!sit` `!hug name` `!attack name` `!bomb` `!explode` `!hat` `!color red` `!vstats` `!hideavatar`

Points: `!vpoints` `!vshop` `!vbuy crown` `!vgive name 10` `!vtop` `!avatar mage` `!random`

Minigames: `!vduel name 10` then `!accept` · `!vslots 10` · `!royale` then `!join` · `!basketball` then `!shoot 5`

Broadcaster and mods only: `!boss` · `!megaboss` · `!mass dance` · `!royale` · `!basketball`. Bosses are
deliberately not a free command - viewers summon them with channel points, and
a free equivalent would make the reward worthless. `!monster` and `!loot` do
not exist for the same reason.

Fun: `!8ball will I win` · `!roll 2d6` · `!log` shows the battle log for 15 seconds · `!vhelp`

Floor: `!lounge` parks the monsters so chat just hangs out. `!war` brings the horde back.
Mods: `!mass dance` (also hug, attack, bomb, explode, jump) · `!megaboss`.

**Why the `v` prefix.** Two neighbours own bare command names on this channel.
StreamElements owns `!points` `!shop` `!buy` `!top` `!give` `!slots` and `!duel`, and
answers them with its own store errors while this overlay acts on the same message.
Bellmire HD - the town sim that runs as the main view on the same stream - owns
`!stats` `!help` and `!commands`. Everything moved rather than asking anyone to switch
half of either off. Typing an old name tells you where it went.

`!roll` stays bare here. Bellmire's `!roll` was an alias of `!guild` - the Guild Roll,
a roster, not dice - and it has no viewer-facing dice command at all. A viewer typing
`!roll` wants dice, which is what this does. `!vroll` still answers as a silent alias.
`!log` is bare too: Bellmire's Chronicle is on-screen furniture, not a command.

**Channel point rewards are an allowlist.** A reward whose title contains none of this
overlay's keywords is ignored in silence. It used to fall through to a chest, which
meant every reward on the channel - song requests, TTS, anything belonging to another
app - dropped loot here.

**`!royale` and `!basketball` are mods-only**, because both take the whole strip over
and the main view opens its own panes; two takeovers at once is a mess on stream.

**The follower monster is off by default** (`followMonster`), because another app on
this channel owns follow alerts. The sub crown is unaffected.

## Abilities

Each viewer's signature spell is derived from their username, so the same person always
casts the same thing. Fireball, Chain Lightning, Whirlwind, Holy Smite, Frost Nova,
Venom Cloud, Mending Light, Crescent Slash — and Meteor once they reach level 10. The
spell also decides their class and silhouette.

## Progress saves

Levels, kills, deaths, hats and colours are kept in the browser's local storage, so your
regulars keep their characters between streams. **Wipe Save** in the setup panel resets
everyone to level 1, for the current channel only.

The ledger is keyed per channel (`jv-save-v1:<channel>`), so running two channels in one
browser keeps their audiences separate. Progress saved under the older single global key
is carried across on first load rather than reset — the first channel to load claims it,
and a marker stops any later channel inheriting a stranger's levels.

It is per browser, so OBS and your desktop browser each keep their own copy, and clearing
site data clears it.

## Tuning

Everything worth adjusting is in the `T` block near the top of the script:

| Setting | Does |
|---|---|
| `stripTop` / `stripBot` | How high up the screen the fighters stand |
| `march` | Walking speed in px/sec |
| `heroHold` / `mobHold` | Where each side waits when there is nothing to fight |
| `maxHeroes` / `maxMobs` | How many bodies on screen at once |
| `idleSpawn` / `idleFloor` | How often monsters wander in during dead air |
| `engage` | How close they get before swinging |

Character size is the `depth()` function just below the render header.

## Keys (for testing outside OBS)

`S` setup · `D` demo · `B` boss · `M` monster · `H` hero · `L` loot
`G` hangout · `R` royale · `K` hoop · `V` show/hide the battle log

These only work when the page has focus, so in OBS you need **Interact**. They are not
shown on screen — that corner now carries hints aimed at viewers instead.

## License

**Copyright (c) 2026 Jose Luis Estrada (JestSayin96). All rights reserved.
Proprietary — not open source, not public domain.** See [LICENSE](LICENSE).

This repository is public so GitHub Pages can serve it, and a browser overlay has to
transmit its own source in order to render. Neither is a licence.

**You may not** sell it, redistribute it, host a public copy, extract or re-draw its
artwork for another project, or train a model on it.

All 21 characters in `sprites/` are original works drawn for this project — no stock, no
asset packs, no CC0. Each is separately copyrightable and infringement is assessed **per
work**. The commit history timestamps every sprite from its first pixel, so authorship
is not arguable. Infringing copies are met with DMCA notices to the host, the storefront
and the payment processor.

**Permission is available and often granted to anyone who asks first** — open an
[issue](https://github.com/jestsayin96/fightoverlay/issues). Asking costs you a message.
