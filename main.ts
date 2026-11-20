// gta6-meme-x-01 entry — "LEONIDA EXPRESS" (Node 22, standard library only).
//
// The entry is the X post itself: a GTA 6 meme (a delivery-tracking parody —
// GTA VI ordered 17 Sep 2013, still "out for delivery" 4,812 days later),
// posted from a public X account with make.fun / @makefunai and the entrant's
// play code in its text. The house reads the post from X (first picture,
// then text) and hands it to the judge.
//
// This program's only job is to hand the post's address to the grader: it
// reads POST.json from the repository root and copies it to /output/POST.json,
// refusing clearly if the address is missing, malformed, or still the
// placeholder. Nothing this program writes is judged — the post is.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// A real X post address: https://x.com/<handle>/status/<digits>.
// (twitter.com is the same post under its old host; accept it too.)
const POST_URL = /^https:\/\/(x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/[0-9]+$/;

function fail(message: string): never {
  console.error(`POST.json rejected: ${message}`);
  process.exit(1);
}

const postPath = join(BOT_DIR, "POST.json");
let raw: string;
try {
  raw = readFileSync(postPath, "utf8");
} catch (err) {
  fail(`cannot be read from ${postPath}: ${(err as Error).message}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(raw!);
} catch (err) {
  fail(`is not valid JSON: ${(err as Error).message}`);
}

if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  fail("must be a JSON object with a \"url\" field.");
}
const url = (parsed as Record<string, unknown>).url;
if (typeof url !== "string" || url.length === 0) {
  fail("has no \"url\" string field.");
}
if (!POST_URL.test(url)) {
  fail(`"${url}" is not an X post address (expected https://x.com/<handle>/status/<id>).`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(postPath, join(OUTPUT_DIR, "POST.json"));
} catch (err) {
  fail(`could not be copied to ${OUTPUT_DIR}: ${(err as Error).message}`);
}
console.log(`POST.json handed in: ${url}`);
