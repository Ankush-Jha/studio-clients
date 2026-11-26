# Greenbrix Capital: carousel brief (shared by every carousel agent)

Client: **Greenbrix Capital**, a private-lending mortgage brokerage in Ontario. It's an independently owned and operated franchise of Dominion Lending Centres. The face of the brand is **Krystian Catala, Broker & President**.

Audience: Ontario homeowners and investors the banks turned down or can't serve fast enough, such as business owners, rebuilders, people facing power of sale, bridge-loan needs and investors. The tone is calm, expert, no-judgment and plain-spoken. Never salesy, never desperate.

## Format
- Instagram feed carousel, **1080×1350 (4:5)**, 7 slides, PNG.
- In the profile grid, Instagram shows a **3:4 crop** of the cover: x 34–1046. Keep every cover word inside x 60–1020.
- Slide 1 must stop the scroll on its own, and every slide gives a reason to swipe.

## Brand (from the logo)
- Colours:
  - deep green `#0B2E1B` / `#124127`
  - brand green `#1F6A37`
  - lime `#86C64F` (logo `#79B94A`)
  - charcoal `#505052`
  - paper `#F2F4EC`
  - The logo's brick cluster uses a dark-green-to-lime horizontal gradient. That brick motif is the brand's signature device.
- Type, all OFL, in `content-desk/statics/fonts/`:
  - Young Serif for headlines (it echoes the GREENBRIX wordmark);
  - Instrument Sans for body;
  - Geist Mono for numbers and labels.
  - You may add one more OFL face from that folder if your concept needs it. Maximum 2–3 families per carousel.
- Logos, in `clients/greenbrix/assets/`, **all transparent; never put a box or plate behind a logo**:
  - `logo-t.png` (for light backgrounds);
  - `logo-light.png` (white wordmark, for dark backgrounds);
  - `logo-dlc-light.png` (Greenbrix plus "Powered by Dominion Lending Centres" lockup, for dark backgrounds);
  - `logo-dlc-t.png` (the same lockup for light backgrounds).
  - The DLC blue box is part of DLC's own logo. Keep it as it is.
- Headshot: `assets/headshot-cut.png`, Krystian with the background removed (transparent PNG). The original is `headshot.jpg`.

## Compliance (Ontario, FSRA): every slide carries this 3-line footer (added Nov 17 at the user's request)
Krystian Catala, Mortgage Broker · Lic. #M12001607 / Greenbrix Capital · Brokerage Lic. #13645 / Independently owned & operated franchise of Dominion Lending Centres.
Any slide showing an interest rate also needs the term, plus a note that the APR including fees is higher (see C2).

- Brokerage line, small and quiet but readable (20 px or larger), on every slide or at least on the cover and the CTA slide: "Greenbrix Capital · Independently owned & operated franchise of Dominion Lending Centres · Lic. #13645".
- On the CTA slide:
  - "Krystian Catala, Broker & President · Mortgage Broker Lic. #M12001607"
  - phone "416.460.2215 or DM".
- These licence numbers come from Greenbrix's own About page, found via search on Nov 17. Keep them exactly as written.
- No guarantees ("approved", "we fund everyone"). Say "we look at…", "can", "may".
- Placeholders the client must supply, like `[X% to Y%]` or `[How Greenbrix charges]`, stay visible as obvious yellow placeholder tags. Never invent rates or fees.
- Every number must match the plan; recheck the math with python.

## Quality bar (the user said earlier versions looked "cheap, dull, stale, basic, everything the same")
- Premium financial-brand quality: think a top agency's work for a modern lender. Strong hierarchy, generous but intentional space, real depth (layers, soft shadows, texture or grain), and one signature visual device per carousel.
- Covers need the person or a striking object, plus 10 words or fewer. Make a number or object the hero where it fits.
- No AI-template look: no glassmorphism, no purple, no generic emoji icons, no centred-everything layouts, no clip-art. Draw everything in code (HTML/CSS/SVG; three.js if you need it). No AI-generated images.
- Copy: sharpen the client's script into short, specific, human lines. Keep every fact. No AI-tell phrasing; see `~/.claude/skills/humanizer/SKILL.md`. Avoid "it's not X, it's Y".
- Read `content-desk/research/visual_brief_for_stills.md` for the rules.

## Inputs
- Client plan: `clients/greenbrix/plan.csv` (your carousel's row).
- Previous attempt, for reference only (you may change everything): `clients/greenbrix/build.mjs` and `clients/greenbrix/out/<ID>/`.
- Rendering:
  - playwright-core is in `content-desk/tools/node_modules`;
  - sharp, satori, three, GSAP, icons and more are in `content-desk/toolchain/node_modules` (see its README).

## Process and deliverable (budget-aware: one build, then at most 2 refinement passes)
1. Work only in `clients/greenbrix/<ID>/` with your own `build.mjs`. Don't touch other carousels' folders or the shared assets.
2. Render all 7 slides to `clients/greenbrix/<ID>/out/<ID>-1.png` … `<ID>-7.png`, plus `contact.jpg`.
3. Look at every slide at full size yourself (Read the PNG). Check for:
   - text overflow or collisions;
   - anything cut off;
   - a logo with a background behind it;
   - weak hierarchy;
   - a cover that wouldn't stop a thumb in the 3:4 grid crop.

   Fix and re-render, at most 2 passes.
4. Write `clients/greenbrix/<ID>/caption.txt`: the client's caption, tightened, with 3–5 hashtags. Write `NOTES.md` with the concept, the placeholders still to fill and anything to verify.

Final message: the concept in one line, the paths, and anything the client must supply.
