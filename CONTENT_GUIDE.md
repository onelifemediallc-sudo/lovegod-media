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
- Reels: include the line "Scripture quotations taken from the NASB (New American Standard Bible), Copyright © 1995 by The Lockman Foundation. Used by permission. All rights reserved. lockman.org" in the video.

## Verse count (Lockman 1,000-verse limit)
- Log every NASB verse posted in `verse-log.csv` (date, reference, number of verses, post time).
- Count each **different** verse once toward the total. Reusing a verse already logged adds 0.
- Show today's count and the running total at the top of every preview.
- At **900+** total, flag it clearly at the top of the preview so Dustin can decide (ask Lockman, reuse posted verses, or switch new verses to KJV/WEB). At 1,000, stop adding new NASB verses until he decides.

## Daily mix at 8 posts/day (Oct 25 – Nov 7, 2026; Eastern time)
Times are based on Metricool's best-time data for the Page (peaks around 10 AM–12 PM and 4–6 PM; weakest before 7 AM and after 9 PM).
| Time | Type |
|---|---|
| 8:00 AM | Verse graphic |
| 10:00 AM | **Morning reel** — "start your day" verse, upbeat music |
| 11:00 AM | Text post (no image) — short reflection ending in a question or prompt |
| 12:00 PM | Verse graphic |
| 3:00 PM | Engagement graphic (fill in the blank, "Type AMEN if…", this-or-that) |
| 5:00 PM | Verse graphic |
| 6:00 PM | Humor or relatable church-life graphic (kind, never mocking) |
| 8:00 PM | **Night reel** — peaceful / rest / trust verse, calm music |

- Goal right now: reach new people who want faith content. Reels for discovery; captions built to be shared ("Share this with someone who…", "Tag a friend who…").
- Once a week (Sundays), check Metricool's getBestTimeToPostByNetwork (facebook, America/New_York) and the Page's post analytics. If the best hours have clearly shifted, adjust the times and tell Dustin.

## Volume plan (Dustin's decision, Oct 24, 2026)
- **8 posts/day for the first 30 days: Oct 25 – Nov 23, 2026.** Use the 8-post schedule above. Do not increase volume on your own.
- **Nov 23 run: 30-day evaluation.** In that morning's preview message, include a short 30-day report from Metricool analytics and the Professional Dashboard if available: total reach/views, followers gained, best and worst post types, best times, and earnings if visible. Then recommend whether to move toward 20 posts/day. Dustin decides; keep 8/day until he says otherwise.
- Dustin's goal: eventually 20 posts/day, earning $20–$40/day at first, with $100/day as the long-term target. The test window is 60 days.
- If Dustin approves more posts, use this mix as a guide:

| Posts/day | Reels | Verse graphics | Text | Engagement | Humor | Prayer prompt |
|---|---|---|---|---|---|---|
| 12 | 2 | 4 | 2 | 2 | 1 | 1 |
| 16 | 3 | 5 | 3 | 2 | 2 | 1 |
| 20 | 3 | 6 | 4 | 3 | 2 | 2 |

- For 8/day use the exact times in the 8-post table. For 12+/day (only after Dustin approves), spread posts between 7:00 AM and 10:00 PM, putting more of them in the peak windows (about 9 AM–1 PM and 3–7 PM) and fewer early or late; reels around 10 AM, 1 PM (when there are 3) and 8 PM; don't put two verse graphics back to back; keep humor in the evening.
- Prayer prompt = a graphic or text post inviting people to share prayer requests or pray for something specific (no verse needed).
- Keep about half of each day non-verse to avoid repetitive, mass-produced patterns and to slow the NASB verse count. Reusing popular verses already in verse-log.csv (with a new caption and design wording) adds 0 to the count; do this regularly at 16–20 posts/day.
- Each week, include a one-line reach/engagement trend in the preview message (Metricool analytics), so Dustin can see how the ramp is landing.
- Goal right now: reach new people who want faith content. Reels for discovery; captions built to be shared ("Share this with someone who…", "Tag a friend who…").

## Reels
- Make with `tools/reel.py` → `make(scenes, ref, music, out)`: 1080x1920, 15 seconds, 2–3 scenes, verse text in yellow Lora on teal, white reference, "Love God." and the NASB notice built in.
- Use explicit line breaks (`\n`) so lines break naturally; check frames so no single word sits alone on a line.
- Music: rotate the original tracks in `tools/` (`music_morning_15s.wav` for morning reels; `music_night_15s.wav` for night reels; `music_hope_15s.wav` and `worship_bed_15s.wav` to vary). Never use copyrighted music.
- Save as `media/YYYY-MM-DD/r1.mp4` (morning) and `r2.mp4` (night).
- Schedule with `facebookData` `{"type":"REEL","title":"<short title | reference>"}` and the video URL in `media`.
- Never use the same verse twice in one day across reels and graphics.
- Vary verses, topics and prompts day to day. Never repeat a caption. Avoid near-identical posts (Meta penalizes repetitive, mass-produced content).
- Every post should invite engagement (comment, share, tag, type a word).
- No made-up statistics, no fake engagement numbers on graphics, no real people's names.

## Approval rule (Dustin's decision, Oct 26, 2026)
- **Nothing goes to Metricool until Dustin confirms.** Each run builds tomorrow's posts and a preview, then waits for his reply.
- Approval = a clear OK such as "post it", "approved" or "fine to post". Then schedule all posts and log the verses.
- Changes requested → redo them, republish the preview, and ask again. "Cancel tomorrow" → schedule nothing.
- No reply → nothing posts that day, and those verses are not logged.
- Reading Metricool analytics (Sunday trend, best times, Nov 23 report) is fine without approval.

## Daily workflow (scheduled run at about 7:45 AM Eastern)
1. Read this guide and `verse-log.csv`.
2. Plan tomorrow's posts using the Volume plan (8/day unless Dustin has approved more); look up each verse's NASB 1995 wording.
3. Make the graphics with `tools/brand.py` and the two reels with `tools/reel.py`; save to `media/YYYY-MM-DD/` (tomorrow's date), e.g. `media/2026-10-26/p1.png`, `r1.mp4`, plus `r1.jpg`/`r2.jpg` poster frames.
4. Commit and push to `main`. Image links: `https://raw.githubusercontent.com/onelifemediallc-sudo/lovegod-media/main/media/YYYY-MM-DD/pN.png`. Check each link returns 200.
5. Publish the preview page (based on `tools/preview_template.html`) marked "Not scheduled yet: waiting for your OK", showing every post in time order with graphic, caption, time, tomorrow's verse count and the running total including tomorrow. Notify Dustin that it's ready and won't post until he confirms.
6. **Wait for Dustin's approval.** Do not schedule anything before it.
7. After approval: schedule each post in Metricool (brand/blog id `7633380`, timezone `America/New_York`, network `facebook`, `facebookData.type` = `POST`, `autoPublish` true; reels as `REEL` with the poster as `videoThumbnailUrl`) for tomorrow at its time. Then append the day's verses to `verse-log.csv`, commit and push, and confirm to Dustin.
8. If Dustin asks for changes after scheduling, update or delete those posts in Metricool (and the graphic/log) and confirm.

## Dustin's own reels
- Dustin will sometimes record reels of himself (a verse thought, a prayer, a testimony). These are the page's most valuable content.
- If he sends one for a given day, write the caption, schedule it, and use it in place of that day's automated reel (morning or night, whichever fits) instead of adding an extra reel. Mark it "Dustin's reel" in the preview.
- If he posts one himself directly on Facebook, keep the automated schedule as is.
