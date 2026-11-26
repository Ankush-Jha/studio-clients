# Learnings: Orbis Mortgage Group

## 2026-11-12, Reel 01 "Minimum payments"
- Client rejected v1 graphics as generic (repeated panel look, fake card numbers, bouncy pops, off-brand font/colours).
- v3 approved direction: premium private-bank look, Inter + gold #d4b225 + navy #111634, a different asset type for every beat (statement document, notification, chart, gauge, flow, fork, calendar, bars, DM composer), soft sound design, background audio low.
- Captions intentionally left in the old bold Montserrat style at the client's request; revisit.
- B-roll was five Higgsfield clips matched to cue points by content (generation order unknown).
- Open items: confirm Instagram handle and Level 2 wording; confirm compliance review path.
- Toolchain gotcha: ffmpeg 9.0.2 deadlocks at end of render when B-roll overlays and a PNG-sequence overlay share one filter graph. Render in two passes and always use a timeout.
- Reference build lives in reels/2026-11-12_reel01-minimum-payments/ (build/overlay_v3.html is the style reference).

## 2026-11-12, Reel 02 "Home equity debt consolidation" (stage 1 built)
- Raw clip: WhatsApp-compressed 576x1024 (soft when scaled to 1080x1920). Ask the client for the ORIGINAL camera file next time.
- The clip started with ~2 s of silence (-58 dB); whisper.cpp's plain word times were wrong there. Use `--dtw small.en -nfa` token alignment plus measured audio energy (tools/plan_cut.py does this).
- ASR ambiguity: "interest cost" vs "costs" - used "costs" via build/corrections.json. NEEDS the client/user to confirm by ear.
- Beats used six asset families (paper-cut house + card stack + stamp, identity badge, UI toggle, hand-drawn flow, typographic emphasis, house + padlock, plan document, chat thread) and a tone dim during the risk passage.
- On-screen text QA found "Active now" in the chat UI: implies availability the client never claimed; remove.
- Pending for the full-potential pass: words-behind-the-speaker beat (needs BiRefNet matte), voice enhancement, "Active now" removal.
