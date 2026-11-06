# fightoverlay

A Twitch stream overlay for [JestSayin96](https://twitch.tv/JestSayin96). Viewers who
talk in chat become adventurers who march in from the left. Monsters and bosses come
from the right. They meet in the middle and fight.

## Running it

**In OBS:** add a Browser source pointing at

```
https://jestsayin96.github.io/fightoverlay/
```

Set it to 1920x1080. To reach the setup screen inside OBS, right-click the source and
choose **Interact**.

Type your channel name and press START. That is all the chat avatars need — Twitch
allows anonymous chat reading, so there is no token, no Client ID, and nothing to sign
in to.

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

Actions: `!jump` `!dance` `!wave` `!sit` `!hug name` `!attack name` `!bomb` `!explode` `!hat` `!color red` `!stats` `!hideavatar`

Points: `!points` `!shop` `!buy crown` `!give name 10` `!leaderboard` `!avatar mage` `!random`

Minigames: `!duel name 10` then `!accept` · `!slots 10` · `!boss` · `!royale` then `!join` · `!basketball` then `!shoot 5`

Floor: `!lounge` parks the monsters so chat just hangs out. `!war` brings the horde back.
Mods: `!mass dance` (also hug, attack, bomb, explode, jump).

## Abilities

Each viewer's signature spell is derived from their username, so the same person always
casts the same thing. Fireball, Chain Lightning, Whirlwind, Holy Smite, Frost Nova,
Venom Cloud, Mending Light, Crescent Slash — and Meteor once they reach level 10. The
spell also decides their class and silhouette.

## Progress saves

Levels, kills, deaths, hats and colours are kept in the browser's local storage, so your
regulars keep their characters between streams. **Wipe Save** in the setup panel resets
everyone to level 1.

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
