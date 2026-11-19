# Thursday 19 November 2026 — The Day in World News (round 3)

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/0xfari/news-image-20261119-v4/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/0xfari/news-image-20261119-v4/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A single 1024×1024 front page summing up Thursday 19 November 2026:
**40 verified stories from 6 continents** — 3 big leads, 10 medium cards
with original drawn scenes, 27 briefs, a timeline of the day, a
key-numbers strip, and a world map with numbered pins for every
illustrated story.

Round 3 rebuilds round 2 from the study of the entries above it:
40 stories instead of 33 (the winners carry 36–43); every scene is
a clean flat drawing with no words printed over it — round 2's
labels collided with its drawings at card size; a timeline strip
tracing the day hour by hour; and a date-check box whose header
finally matches its contents, so nothing first reported before
Thursday is presented as Thursday news. Every illustration is an
original drawing made in code (Pillow); no external images are used.
Disputed claims are attributed on the page.

- Bounty: [news-image-20261119 on make.fun](https://make.fun/bounty/news-image-20261119)
- Referral: `p5tm223q`

## Build

```sh
python3 main.py   # writes entry.png (1024x1024, deterministic)
```

`main.py` (standard library only) decodes the finished front page from
`entry.png.b64` and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`;
`render.py` holds the drawing helpers, the 13 original scenes, the
world map, and the page layout. Running the render twice produces a
byte-identical PNG.
