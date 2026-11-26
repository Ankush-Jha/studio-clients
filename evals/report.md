# Eval dry run (intake readiness)

Generated 2026-11-19T23:56:58+05:30 by `studio/evals/run_evals.py`. No model usage, no renders: kit, routing and gate lookups only.

**20 briefs: 10 pass, 10 warn, 0 blocked.** Readiness: 15 ready, 4 proof-only, 1 group (per-client below), 0 blocked.

| id | client | format | engine | verdict | readiness | why |
|---|---|---|---|---|---|---|
| e01 | dan-balch | carousel | stills | **pass** | ready |  |
| e02 | keaton-thornton-jim-thornton | graphic-reel | films | **warn** | proof-only | complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6) |
| e03 | keith-crossland-dustin-moss | static | stills | **warn** | proof-only | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on every piece; 1 asset(s) need user confirmation before use: logo-2.png |
| e04 | gregory-hernandez | carousel | stills | **pass** | ready |  |
| e05 | raoul-hunt | short-reel | motion | **pass** | ready |  |
| e06 | krystian-catala | carousel | stills | **pass** | ready |  |
| e07 | brian-wang | footage-reel | face-reels | **warn** | ready | no client photo (brand-only piece; no person shown); no logo file (+1) |
| e08 | group:2 | carousel | stills | **warn** | group | ariana-learoux: proof-only (complianceLine null); borrowise: proof-only (complianceLine null) |
| e09 | nav-utppal | cover | stills | **warn** | ready | 1 asset(s) need user confirmation before use: logo-2.png |
| e10 | jim-decoste | gif | motion | **warn** | ready | no client photo (brand-only piece; no person shown) |
| e11 | rahul-vinod | graphic-reel | films | **warn** | ready | 1 asset(s) need user confirmation before use: image60-mmg-badges.png |
| e12 | vittorio-oliverio | static | stills | **warn** | proof-only | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on every piece |
| e13 | akshat-chauhan | story | stills | **pass** | ready |  |
| e14 | sahil-rihani | carousel | stills | **pass** | ready |  |
| e15 | amit-khurana | graphic-reel | films | **pass** | ready |  |
| e16 | georges-madi | animated-carousel | hyperframes | **pass** | ready |  |
| e17 | borrowise | short-reel | motion | **warn** | proof-only | complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6); no client photo (brand-only piece; no person shown) |
| e18 | dan-balch | carousel | stills | **pass** | ready |  |
| e19 | ranjit-singh | carousel | stills | **pass** | ready |  |
| e20 | michael-marini | graphic-reel | films | **warn** | ready | no client photo (brand-only piece; no person shown); no logo file (+1) |

## Per brief

### e01: carousel for Dan Balch about renewing in 2027
- Verdict **pass** / ready. Client: `dan-balch` (matched dan balch, Dan Balch, dan). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Dan Balch, London ON, group 4, completeness 1.0, video=True, languages ['en'].
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: Ontario compliance line present -> gate+kit/kit+checker
  - judgement: London-specific angle -> critic
  - checkable: 8-10 slides, slide 2 second hook -> gate

### e02: graphic reel for the Thorntons on what a reverse mortgage is, 45 s
- Verdict **warn** / proof-only. Client: `keaton-thornton-jim-thornton` (matched thornton). Format: graphic-reel.
- Engine: `films`  (alternatives: hyperframes, motion); adapter ok, engine home found.
- Kit: Keaton Thornton & Jim Thornton, Brantford ON, group 1, completeness 0.857, video=False, languages ['en'].
- PROOF-ONLY: complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6)
- note: kit missing fields: complianceLine, socials
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Kit rules that apply: [never] 3 Nov - Please stop using 'best rates' in all future posts. I have already made the change | [outro] Always use Jim's Outro for Reels
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: never says 'best rates' -> gate
  - checkable: Jim's outro used on the reel -> kit+critic
  - judgement: Brantford fact used -> critic

### e03: static for Keith Crossland & Dustin Moss: Edmonton month-end market numbers
- Verdict **warn** / proof-only. Client: `keith-crossland-dustin-moss` (matched Keith Crossland & Dustin Moss, keith, crossland). Format: static.
- Engine: `stills`  (alternatives: custom-html); adapter ok, engine home found.
- Kit: Keith Crossland & Dustin Moss, Edmonton AB, group 1, completeness 0.857, video=False, languages ['en'].
- PROOF-ONLY: complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on every piece
- warn: 1 asset(s) need user confirmation before use: logo-2.png
- note: kit missing fields: complianceLine, agent.licence
- Kit rules that apply: [hashtags] Sep 5, 2025 - Please don't hashtag Mortgageontario as we don't work there.
- Expect items (3 checkable, 0 judgement, 0 kit gaps):
  - checkable: Edmonton numbers only -> checker
  - checkable: no #Mortgageontario -> gate/kit+checker
  - checkable: sourced and dated figures -> checker

### e04: carousel for Gregory Hernandez on first-time buyer incentives
- Verdict **pass** / ready. Client: `gregory-hernandez` (matched gregory hernandez, Gregory Hernandez, gregory). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Gregory Hernandez, Montreal QC, group 1, completeness 0.929, video=False, languages ['en', 'fr'].
- note: QC/French client: French version required in script `fr`
- note: kit missing fields: agent.licence
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: French version provided -> kit+checker
  - checkable: Quebec rules, not Ontario -> kit+checker
  - judgement: Orbis brand -> critic

### e05: short reel for Raoul Hunt, one-number punch about a 0.25% rate move on $500K
- Verdict **pass** / ready. Client: `raoul-hunt` (matched raoul hunt, Raoul Hunt, raoul). Format: short-reel.
- Engine: `motion`  (alternatives: hyperframes, films); adapter ok, engine home found.
- Kit: Raoul Hunt, None None, group None, completeness 0.714, video=False, languages ['en'].
- note: kit missing fields: stills (no roster style assigned; needs a group first), agent.licence, city, province, group
- note: no group assigned (batch and weekly plans skip this client)
- note: 2 expect item(s) are judgement only (critic, no coded check)
- Expect items (1 checkable, 2 judgement, 0 kit gaps):
  - checkable: math checked: about $67-70/month on 25-yr amortizing -> checker
  - judgement: rounded in voice, exact on screen -> critic
  - judgement: Ottawa angle -> critic

### e06: carousel for Krystian Catala: private second mortgage costs explained
- Verdict **pass** / ready. Client: `krystian-catala` (matched krystian catala, Krystian Catala, krystian). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Krystian Catala, None ON, group None, completeness 0.786, video=None, languages ['en'].
- note: kit missing fields: video (footage reels allowed?), stills (no roster style assigned; needs a group first), city, group, socials
- note: no group assigned (batch and weekly plans skip this client)
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - judgement: Greenbrix brand + DLC lockup -> critic
  - checkable: 3-line FSRA footer every slide -> gate+kit/gate
  - checkable: placeholders for unknown fees stay visible -> kit+critic

### e07: footage reel for brian-wang from a supplied talking-head clip
- Verdict **warn** / ready. Client: `brian-wang` (matched brian wang, Brian Wang, brian). Format: footage-reel.
- Engine: `face-reels`  (alternatives: hyperframes, films); adapter ok, engine home found.
- Kit: Brian Wang, Toronto ON, group None, completeness 0.692, video=True, languages ['en'].
- warn: no client photo (brand-only piece; no person shown)
- warn: no logo file
- warn: footage reel needs a supplied clip; face-reels pipeline not yet run end to end (UNVERIFIED, see face-reels.md Status)
- note: kit missing fields: standalone logo file (logo exists only inside the brand card), standalone photo (photo exists only inside the brand card), assets.photo, stills (no roster style assigned; needs a group first), group, socials
- note: no group assigned (batch and weekly plans skip this client)
- note: face-reels client folder missing: `new_client.py` creates it from kit facts; also needs the supplied clip
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Kit rules that apply: [scope] Not a mortgage broker: wealth coach / life insurance advisor. Never use mortgage-broker co | [scope] Footage reels allowed. | [outro] Reels end on his brand card with 'For information only. Not investment advice.'
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: every spoken word kept -> gate
  - judgement: brand card at end with disclaimer -> critic
  - checkable: captions in his words -> gate

### e08: carousel for group 2 on the Dec 9 Bank of Canada decision
- Verdict **warn** / group. Client: `group:2` (8 clients in group 2). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- warn: ariana-learoux: proof-only (complianceLine null)
- warn: borrowise: proof-only (complianceLine null)
- note: group 2: 6 ready, 2 proof-only, 0 blocked of 8
- note: batch: one job per client, distinct style each (tools/batch_plan.py)
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Group members: akshat-chauhan (ready), al-manji (ready), amit-khurana (ready), ariana-learoux (proof-only), borrowise (proof-only), juliet-fernandez (ready), karven-wu (ready), rahul-vinod (ready)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: one job per client -> producer
  - judgement: each client's hook and visual differ -> critic
  - checkable: near-dup check clean across siblings -> variety+neardup

### e09: cover for Nav Utppal's next reel: 'Your renewal letter is a negotiation'
- Verdict **warn** / ready. Client: `nav-utppal` (matched nav utppal, Nav Utppal, nav). Format: cover.
- Engine: `stills` --format story (or the engine that made the reel: poster.jpg) (alternatives: films); adapter ok, engine home found.
- Kit: Nav Utppal, Toronto ON, group 3, completeness 1.0, video=True, languages ['en'].
- warn: 1 asset(s) need user confirmation before use: logo-2.png
- note: kit missing fields: agent.title
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: headline in centre 3:4 band -> gate
  - checkable: 6 words or fewer -> gate
  - judgement: Next Mortgage/FIDES brand -> critic

### e10: GIF for Jim DeCoste: Bank of Canada reminder Dec 9
- Verdict **warn** / ready. Client: `jim-decoste` (matched jim decoste, Jim DeCoste, jim). Format: gif.
- Engine: `motion` --gif (alternatives: hyperframes); adapter ok, engine home found.
- Kit: Jim DeCoste, Antigonish NS, group 1, completeness 0.923, video=False, languages ['en'].
- warn: no client photo (brand-only piece; no person shown)
- note: kit missing fields: socials
- Expect items (3 checkable, 0 judgement, 0 kit gaps):
  - checkable: loops -> gate
  - checkable: Nova Scotia (no Ontario rule), DLC franchise line -> kit+checker
  - checkable: under 8 s -> gate

### e11: graphic reel for Rahul Vinod for newcomers to Canada, Moncton
- Verdict **warn** / ready. Client: `rahul-vinod` (matched rahul vinod, Rahul Vinod, rahul). Format: graphic-reel.
- Engine: `films`  (alternatives: hyperframes, motion); adapter ok, engine home found.
- Kit: Rahul Vinod, Moncton NB, group 2, completeness 1.0, video=False, languages ['en'].
- warn: 1 asset(s) need user confirmation before use: image60-mmg-badges.png
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: newcomer specifics sourced -> checker
  - checkable: New Brunswick context -> kit+checker
  - judgement: consider Hindi/Malayalam audience only if kit says -> critic

### e12: static for Vittorio Oliverio: HELOC interest-only explained
- Verdict **warn** / proof-only. Client: `vittorio-oliverio` (matched vittorio oliverio, Vittorio Oliverio, vittorio). Format: static.
- Engine: `stills`  (alternatives: custom-html); adapter ok, engine home found.
- Kit: Vittorio Oliverio, Lethbridge AB, group None, completeness 0.714, video=None, languages ['en'].
- PROOF-ONLY: complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on every piece
- note: kit missing fields: video (footage reels allowed?), associate footers for Cara, Marty/Marry, Clarke, Karen, Kim, David (only Vittorio's footer exists), stills (no roster style assigned; needs a group first), complianceLine, brokerage.licence, agent.licence, group
- note: no group assigned (batch and weekly plans skip this client)
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Kit rules that apply: [hashtags] Hashtags: #MortgageBroker #CenterProfessionalMortgageGroup #Cpmg | [rotation] Use alternate associates on alternate days in the footer for the posts. | [footer] For every associate use the phone number 403.380.4413 so the number is used and remembered | [rotation] 15 July 2025 - Remove David from the posts for 4 weeks. Use Kim, Marty, Cara, Vittorio; pu | [rotation] 28 July 2025 - Skip David for a month; focus on Marty, Cara, Vittorio, Kim for August. In  | [footer] 12 September 2025 - Use footers for Cara, Marry, Clarke, Karen, Vittorio.
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: footer associate rotation respected -> gate+kit
  - judgement: 403.380.4413 used -> critic
  - checkable: HELOC +0.25% ≈ $21/month per $100K -> checker

### e13: story frames for Akshat Chauhan: 3 questions to ask before you sign a renewal
- Verdict **pass** / ready. Client: `akshat-chauhan` (matched akshat chauhan, Akshat Chauhan, akshat). Format: story.
- Engine: `stills` --format story (still) / motion (loop) (alternatives: hyperframes); adapter ok, engine home found.
- Kit: Akshat Chauhan, Calgary AB, group 2, completeness 0.857, video=False, languages ['en'].
- note: kit missing fields: agent.licence, socials
- note: 2 expect item(s) are judgement only (critic, no coded check)
- Expect items (1 checkable, 2 judgement, 0 kit gaps):
  - judgement: Calgary angle -> critic
  - checkable: story safe zones -> gate
  - judgement: one action -> critic

### e14: carousel for Sahil Rihani about self-employed mortgage approval
- Verdict **pass** / ready. Client: `sahil-rihani` (matched sahil rihani, Sahil Rihani, sahil). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Sahil Rihani, Vaughan ON, group 1, completeness 1.0, video=False, languages ['en'].
- note: 2 expect item(s) are judgement only (critic, no coded check)
- Expect items (1 checkable, 2 judgement, 0 kit gaps):
  - judgement: Vaughan angle -> critic
  - checkable: no guarantees language -> gate
  - judgement: illustrative labels -> critic

### e15: graphic reel for Amit Khurana on fixed vs variable, 50 s
- Verdict **pass** / ready. Client: `amit-khurana` (matched amit khurana, Amit Khurana, amit). Format: graphic-reel.
- Engine: `films`  (alternatives: hyperframes, motion); adapter ok, engine home found.
- Kit: Amit Khurana, Toronto ON, group 2, completeness 1.0, video=False, languages ['en'].
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: style not used by Amit before -> variety+neardup
  - judgement: both outcomes shown, no rate prediction -> critic
  - checkable: Centum brokerage line -> gate+kit

### e16: animated carousel for Georges Madi: refinancing to consolidate debt
- Verdict **pass** / ready. Client: `georges-madi` (matched georges madi, Georges Madi, georges). Format: animated-carousel.
- Engine: `hyperframes` animated slides (alternatives: stills); adapter ok, engine home found.
- Kit: Georges Madi, Montreal QC, group 4, completeness 0.857, video=True, languages ['en', 'fr'].
- note: QC/French client: French version required in script `fr`
- note: kit missing fields: brokerage.licence, socials
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: French version -> kit+checker
  - checkable: Quebec -> kit+checker
  - judgement: debt still exists stated honestly -> critic

### e17: short reel for Borrowise (no photo, brand only) on comparing lenders
- Verdict **warn** / proof-only. Client: `borrowise` (matched borrowise, Borrowise, borrowise). Format: short-reel.
- Engine: `motion`  (alternatives: hyperframes, films); adapter ok, engine home found.
- Kit: Borrowise, None ON, group 2, completeness 0.692, video=False, languages ['en'].
- PROOF-ONLY: complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6)
- warn: no client photo (brand-only piece; no person shown)
- note: kit missing fields: agent.title, contact.phones, complianceLine, brokerage.name, brokerage.licence, city
- note: 3 expect item(s) are judgement only (critic, no coded check)
- Expect items (0 checkable, 3 judgement, 0 kit gaps):
  - judgement: no person shown -> critic
  - judgement: Borrowise brand -> critic
  - judgement: no named-lender comparison without label -> critic

### e18: idea:nightly-2026-11-19-g4-2
- Verdict **pass** / ready. Client: `dan-balch` (from idea target). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Dan Balch, London ON, group 4, completeness 1.0, video=True, languages ['en'].
- Expect items (3 checkable, 0 judgement, 0 kit gaps):
  - checkable: uses the nightly idea as one concept -> producer
  - checkable: client and group from the idea -> producer
  - checkable: math re-checked -> checker

### e19: carousel for Ranjit Singh on buying a pre-construction condo in the GTA
- Verdict **pass** / ready. Client: `ranjit-singh` (matched ranjit singh, Ranjit Singh, ranjit). Format: carousel.
- Engine: `stills`  (alternatives: custom-html, hyperframes); adapter ok, engine home found.
- Kit: Ranjit Singh, None ON, group None, completeness 0.786, video=None, languages ['en'].
- note: kit missing fields: video (footage reels allowed?), agent.title, stills (no roster style assigned; needs a group first), city, group, socials
- note: no group assigned (batch and weekly plans skip this client)
- note: 1 expect item(s) are judgement only (critic, no coded check)
- Expect items (2 checkable, 1 judgement, 0 kit gaps):
  - checkable: AKAL brokerage + LIC#10845 -> gate+kit
  - checkable: GTA facts sourced -> checker
  - judgement: no investment-return promises -> critic

### e20: graphic reel for Michael Marini on mortgage renewal shock, Toronto
- Verdict **warn** / ready. Client: `michael-marini` (matched michael marini, Michael Marini, michael). Format: graphic-reel.
- Engine: `films`  (alternatives: hyperframes, motion); adapter ok, engine home found.
- Kit: Michael Marini, Toronto ON, group 1, completeness 0.923, video=False, languages ['en'].
- warn: no client photo (brand-only piece; no person shown)
- warn: no logo file
- warn: 1 asset(s) need user confirmation before use: logo.png
- note: kit missing fields: assets.logos
- Expect items (3 checkable, 0 judgement, 0 kit gaps):
  - checkable: different style than other Toronto clients this week -> variety+neardup
  - checkable: logo pending confirmation not used until confirmed -> kit+critic
  - checkable: Toronto numbers dated -> checker

## Clients: production readiness (all kits)

Still = carousel/static, Reel = graphic reel, Footage = face/footage reel. `proof-only` = complianceLine null on an Ontario or unknown-province kit.

| client | prov | grp | still | reel | footage | main reasons |
|---|---|---|---|---|---|---|
| abbas | ON | 3 | blocked | proof-only | proof-only | no footer image in kit assets: every still carries the footer band; complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6) |
| adrian-biccum | ON | 3 | proof-only | proof-only | proof-only | complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6) |
| akaalinder-dhaliwal | None | 3 | blocked | proof-only | proof-only | no footer image in kit assets: every still carries the footer band; complianceLine is null and province is unknown (treated as Ontario): proof-only (O |
| akshat-chauhan | AB | 2 | ready | ready | blocked |  |
| al-manji | ON | 2 | ready | ready | blocked |  |
| amit-khurana | ON | 2 | ready | ready | blocked |  |
| anil-lakhiya | None | None | proof-only | proof-only | proof-only | complianceLine is null and province is unknown (treated as Ontario): proof-only (O. Reg. 188/08 s.6) |
| ariana-learoux | AB | 2 | proof-only | proof-only | blocked | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on e |
| borrowise | ON | 2 | proof-only | proof-only | blocked | complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6) |
| brian-wang | ON | None | ready | ready | ready |  |
| byran-peters | ON | 4 | ready | ready | ready |  |
| dan-balch | ON | 4 | ready | ready | ready |  |
| gaurav-makhija | ON | 4 | ready | ready | ready |  |
| georges-madi | QC | 4 | ready | ready | ready |  |
| gregory-hernandez | QC | 1 | ready | ready | blocked |  |
| jalal-khan | BC | 4 | ready | ready | ready |  |
| jim-decoste | NS | 1 | ready | ready | blocked |  |
| juliet-fernandez | BC | 2 | ready | ready | blocked |  |
| karven-wu | ON | 2 | ready | ready | blocked |  |
| keaton-thornton-jim-thornton | ON | 1 | proof-only | proof-only | blocked | complianceLine is null and province is ON: proof-only (O. Reg. 188/08 s.6) |
| keith-crossland-dustin-moss | AB | 1 | proof-only | proof-only | blocked | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on e |
| krystian-catala | ON | None | ready | ready | ready |  |
| kulbhushan-narang | ON | None | ready | ready | ready |  |
| michael-marini | ON | 1 | ready | ready | blocked |  |
| nav-utppal | ON | 3 | ready | ready | ready |  |
| rahul-vinod | NB | 2 | ready | ready | blocked |  |
| ranjit-singh | ON | None | ready | ready | ready |  |
| raoul-hunt | None | None | ready | ready | blocked |  |
| robert-cheszes | None | None | ready | ready | ready |  |
| sahil-rihani | ON | 1 | ready | ready | blocked |  |
| scott-brouke | AB | 1 | proof-only | proof-only | blocked | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on e |
| vittorio-oliverio | AB | None | proof-only | proof-only | proof-only | complianceLine is null (AB): no Ontario rule, but the 19 Nov Keith/Dustin job (AB) was also labelled PROOF and the brokerage line is still needed on e |
| wise-equity | None | None | ready | ready | blocked |  |

Clients ready for stills and reels: 23 of 33; proof-only: 8; blocked for stills: 2.
