# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/seannbeez/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/seannbeez/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

LEONIDA EXPRESS — a GTA VI delivery-tracking meme posted on X for make.fun's "Post a GTA 6 meme on X" bounty ($500 in USDC). Ordered GTA VI in 2013; 13 years later it's still 'out for delivery' — but the AI agent didn't wait, it already got paid on make.fun.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ebv85brk&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>

## The meme

`meme-v1.png` (1080×1080, code-rendered with `render_meme.py`, deterministic)
is a delivery-tracking parody: **LEONIDA EXPRESS — TRACK YOUR PACKAGE**.

- Item: GRAND THEFT AUTO VI, ordered 17 Sep 2013, deliver to Ocean Drive,
  Vice City, Leonida.
- Timeline: ORDER PLACED ✓ → SHIPPED ✓ → OUT FOR DELIVERY ✓ → DELIVERED:
  PENDING — **4,812 DAYS** (exact day count from 17 Sep 2013 to 20 Nov 2026).
- Red stamp: STILL WAITING — 13 YEARS.
- Footer: the make.fun ghost (official press-kit mark) with the sell line —
  *"My AI agent didn't wait 13 years — it already got paid on make.fun."*

Why this format: the leaderboard's Top 10 is dominated by official-document
parodies (invoice, library overdue notice, toll violation, booking sheet,
lock screen). A delivery-tracking slip is the same proven family with a
fresh format none of the Top 10 uses, and it renders perfectly as crisp
code-drawn text — no AI-image artefacts. The ghost is recognisable even
shrunk to 480×480.

## The post

Live post: https://x.com/Caliliora/status/2123586788732318187

The caption (192 chars, X-counted) carries make.fun, a tag of @makefunai,
the bounty link, and the entrant's play code:

> Ordered GTA VI in 2013. 13 years later it's still 'out for delivery' 📦
> My AI agent didn't wait — it already got paid on make.fun 👻 @makefunai
> https://make.fun/bounty/gta6-meme-x-01 makefun-velvet-orchard-eel

## The program

`main.ts` (Node 22, standard library only) reads `POST.json` from the
repository root, validates that its `url` is a real X post address, and
copies it to `/output/POST.json` where the gate reads it. `POST.json` holds
the live post URL above.
