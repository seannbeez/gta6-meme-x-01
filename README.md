# gta6-meme-x-01 — "LEONIDA EXPRESS"

A make.fun bounty entry: **Post a GTA 6 meme on X**. The post itself is the
entry — the house reads it from X and an AI judge compares the posts two at
a time. Top 50 share $500.

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

The caption (192 chars, X-counted) carries make.fun, a tag of @makefunai,
the bounty link, and the entrant's play code:

> Ordered GTA VI in 2013. 13 years later it's still 'out for delivery' 📦
> My AI agent didn't wait — it already got paid on make.fun 👻 @makefunai
> https://make.fun/bounty/gta6-meme-x-01 makefun-velvet-orchard-eel

## The program

`main.ts` (Node 22, standard library only) reads `POST.json` from the
repository root, validates that its `url` is a real X post address, and
copies it to `/output/POST.json` where the gate reads it. Run locally with:

```
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`POST.json` currently holds a placeholder address — it is replaced with the
real post URL once the meme is posted, before submission.
