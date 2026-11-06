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
