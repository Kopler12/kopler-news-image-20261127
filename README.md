# The World Today — Friday 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Kopler12/kopler-news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Kopler12/kopler-news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up the world's news of **Friday 27 November 2026** — a
newspaper front page with the six stories that defined the day, drawn
programmatically with Python + Pillow (`render.py`) and shipped as `entry.png`.

## The six stories

1. **Middle East · Gaza** — Defence Minister Israel Katz warns a new Gaza
   operation is coming, one that could displace a million Palestinians, as
   aid agencies fear and the ceasefire frays.
2. **Europe · Ukraine** — Ukrainian drones strike a power plant at
   Nevinnomyssk in southern Russia, and a fertiliser plant in Stavropol too.
3. **Asia · North Korea** — Kim Jong Un promises an "irreversible" expansion
   of the nuclear arsenal and blames American hostility.
4. **Asia · Hong Kong** — Hong Kong marks a year since the Tai Po tower fire
   that killed 159 people.
5. **Asia · Bangladesh** — A day after a 36% minimum-wage rise, garment
   workers say it falls short and march again; police answer with tear gas.
6. **Americas · USA** — Wild weather delays flights and clogs highways as
   Americans head home for Thanksgiving.

Also today: the UN trade body votes to aid Palestine's economy; Iraq jails
eight French IS fighters for life; a blast at a Thai oil refinery injures
seven.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws the front page from scratch with Pillow; re-running it
reproduces `entry.png` byte for byte.
