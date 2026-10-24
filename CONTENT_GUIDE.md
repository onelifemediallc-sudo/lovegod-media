# Love God. — Daily Content Guide

This is the rulebook for the daily posting run. Follow it exactly.

## The page
- Facebook Page name: **Love God.** (a Christian / Bible page, formerly a gamer page, ~2,500 followers)
- Category: Digital Creator. In Facebook's Content Monetization program.
- Owner: Dustin. Goal: earn from Facebook through reach and engagement.
- Tone: warm, encouraging, broadly Christian (not tied to one denomination). Original writing only.

## Brand look (every graphic)
- Size: 1080 x 1080 PNG.
- Background: solid teal `#51B5A9`. No gradient, no vignette, no pictures.
- Main text: yellow `#F8E34C`, font **Lora** (weight 600). No drop shadow, no outline.
- Verse reference: white `#FFFFFF`, Poppins Medium, all caps, under a short white line. Example: `ISAIAH 41:10a (NASB)`.
- Signature: "Love God." in yellow Lora at the bottom center.
- Use `tools/brand.py` → `card(lines, out, ref=..., size=...)`. Keep at least ~90px side margins; shrink `size` for long verses.

## Bible version: NASB 1995 only
- Never quote from memory. Look up every verse's exact NASB 1995 wording online (for example biblehub.com/<book>/<ch>-<v>.htm, the "NASB 1995" line) before using it.
- Normal capitalization is fine where the NASB prints Old Testament quotes in caps.
- Partial verse → mark it, e.g. `Isaiah 41:10a`.
- Every verse graphic shows `(NASB)` in the reference. Every verse post caption ends with `Scripture: NASB · Lockman.org`.
- Every verse post needs an **original caption longer than the verse** (reflection, encouragement, prayer or question).
- Reels (not yet in use): include the line "Scripture quotations taken from the NASB (New American Standard Bible), Copyright © 1995 by The Lockman Foundation. Used by permission. All rights reserved. lockman.org" in the video.

## Verse count (Lockman 1,000-verse limit)
- Log every NASB verse posted in `verse-log.csv` (date, reference, number of verses, post time).
- Count each **different** verse once toward the total. Reusing a verse already logged adds 0.
- Show today's count and the running total at the top of every preview.
- At **900+** total, flag it clearly at the top of the preview so Dustin can decide (ask Lockman, reuse posted verses, or switch new verses to KJV/WEB). At 1,000, stop adding new NASB verses until he decides.

## Daily mix (start: 6 posts/day, Eastern time)
| Time | Type |
|---|---|
| 6:00 AM | Verse graphic |
| 9:00 AM | Text post (no image) — short reflection ending in a question or prompt |
| 12:00 PM | Verse graphic |
| 3:00 PM | Engagement graphic (fill in the blank, "Type AMEN if…", this-or-that) |
| 6:00 PM | Verse graphic |
| 9:00 PM | Humor or relatable church-life graphic (kind, never mocking) |

- No reels in the first month.
- Vary verses, topics and prompts day to day. Never repeat a caption. Avoid near-identical posts (Meta penalizes repetitive, mass-produced content).
- Every post should invite engagement (comment, share, tag, type a word).
- No made-up statistics, no fake engagement numbers on graphics, no real people's names.

## Daily workflow (scheduled run at 8:00 AM Eastern)
1. Read this guide and `verse-log.csv`.
2. Plan tomorrow's 6 posts; look up each verse's NASB 1995 wording.
3. Make the graphics with `tools/brand.py`; save to `media/YYYY-MM-DD/` (tomorrow's date), e.g. `media/2026-10-26/p1.png`.
4. Commit and push to `main`. Image links: `https://raw.githubusercontent.com/onelifemediallc-sudo/lovegod-media/main/media/YYYY-MM-DD/pN.png`. Check each link returns 200 before scheduling.
5. Schedule each post in Metricool (brand/blog id `7633380`, timezone `America/New_York`, network `facebook`, `facebookData.type` = `POST`, `autoPublish` true) for tomorrow at its time.
6. Append the day's verses to `verse-log.csv`, commit and push.
7. Publish the preview page (based on `tools/preview_template.html`) showing every post in time order with graphic, caption, time, today's verse count and running total, and send it to Dustin.
8. Posts go out automatically. If Dustin asks for changes during the day, update or delete those posts in Metricool (and the graphic/log) and confirm.
