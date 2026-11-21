[![make.fun](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/sarzxy/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/sarzxy/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

# ORVENNA — The Sundial's Shadow

A travel poster for a place that isn't there, entered in
[The Poster for a Place That Isn't There](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
on [make.fun](https://make.fun).

**The place:** ORVENNA, a sunlit Mediterranean harbour town at midday —
white stucco houses with terracotta roofs, pink bougainvillea, café
tables on a stone plaza above a turquoise bay. One landmark: the great
golden sundial at the plaza's centre. The name is set huge across the
sunlit pavement, in the manner of the live leaderboard's top entries —
an invented place name in caps + one iconic landmark subtitle.

**How it is made:** the poster is a painterly artwork (bright midday
Mediterranean plaza, one golden sundial landmark, the name painted huge
across the pavement), checked by eye at full size. `main.py` ships
`entry.png` pinned by size + sha256 and copies it to `/output/entry.png`
(fully deterministic). `render.py` is the retired first procedural
draft and is no longer the source of `entry.png`.

Run `python3 main.py` to place it (or `OUTPUT_DIR=/tmp/out python3 main.py`).
