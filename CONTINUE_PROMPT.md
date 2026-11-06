# Prompt for continuing this project

Paste this, with `HANDOFF.md` and `index.html` attached, to pick the work up
in a fresh conversation.

---

I'm building a Twitch stream overlay called Jester's Village. It's a single
self-contained `index.html` served from GitHub Pages and loaded in OBS as a
Browser Source. Chat members become adventurers who march in from the left,
monsters and bosses come from the right, and they fight along the bottom of
the frame.

It works and is deployed. I'm improving it, not starting over.

**Read `HANDOFF.md` first** — it covers the architecture, what's known broken,
and the constraints I've already hit. Don't re-derive decisions documented
there.

Constraints that matter:

- **Everything stays in one `index.html`.** No build step, no framework, no
  runtime dependencies. It has to load as a bare file in OBS.
- **Chat must keep working with no credentials.** Anonymous Twitch IRC. Tokens
  are optional and only add follows, subs and channel points.
- **Don't break the `Game` / `PLATFORMS` separation.** Platforms own transport
  and translate into four normalised events. The simulation knows nothing about
  Twitch. This exists so YouTube and Kick can be added later.
- **Art must be CC0 or originally generated.** The repo is public, so anything
  that forbids redistributing asset files is unusable. No GPL or CC-BY-SA —
  that rules out the LPC set. See `LICENSES.md`.
- **Sprites are 112x120 cells with feet anchored at (56,112).** Any new art
  must match or nothing will line up.

What I want next, highest value first:

1. **Fix the clumping.** Characters pile into a heap at one point with
   nameplates stacking. They should spread into a line.
2. **Palette-swap per viewer** so every knight doesn't look identical. The
   sheets use a tight known palette.
3. **Attack and death animations.** The current pack has neither; both are
   faked. Either find CC0 art that includes them or improve the fake.

When you change anything animated, **verify it in motion** — capture several
consecutive frames and check the character actually moves. A sign error made
everything moonwalk for hours because it was invisible in single screenshots.

Tell me when you disagree with an approach rather than just doing it.
