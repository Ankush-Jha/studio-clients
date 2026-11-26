# Golden judge (monthly, concept stage only)

Use this once a month on the strategist's concepts for the 5 briefs in `studio/evals/golden.jsonl`. The procedure is in `TESTS.md` (Golden creative set). The judge is a fresh Sonnet agent (`critic` type, or general-purpose with Sonnet) that did not write the concepts. It reads files only and never renders anything.

## Prompt (paste as the judge's task, one call per brief)

```
You are judging Studio concepts at the concept stage. You did not write them. Be strict and concrete.

Inputs (read them, nothing else):
- The brief and its mustContain list: line <ID> of $R/studio/evals/golden.jsonl
- The concepts: $R/studio/evals/golden/runs/<YYYY-MM>/<ID>/concepts.json
- The client kit: $R/kits/<client>/kit.json and voice.md
- The rubric: $R/studio/rubric/critic.md
- The client's recent pieces: $R/kits/<client>/history.json and $R/radar/clients.json (that client's "recent")

Steps:
1. For each concept (A, B, C), score the 9 concept-stage rubric lines below 1-5, each with one concrete reason
   that quotes the concept (hook text, beat, slide, device). Judge what is planned: the hook, the beats or slides,
   the device, the CTA, the facts used. Do not reward polish you cannot see.
2. Pick the best concept (highest mean; ties go to the higher Originality score).
3. For the best concept only, mark each mustContain item true or false, with the quote that proves it or "absent".
4. List hard stops for any concept (from the rubric's hard-stop list, applied to what the concept plans), e.g. an
   invented client fact, a planned rate without APR and term, an Ontario piece without the compliance line and not
   marked PROOF, another client's asset, a banned word.
5. Say in one line whether the three concepts are genuinely different (device, structure and style all differ).

Check every client fact the concepts use against kit.json. A fact that is not in the kit (licence, city detail,
years in business, review count, rate offer) is an invented fact: Truth = 1 and a hard stop.

Output only this JSON (no prose around it):
{"id":"<ID>","best":"A|B|C","distinct":true,
 "concepts":{"A":{"scores":{...},"reasons":{...}},"B":{...},"C":{...}},
 "scores":{ <the best concept's 9 scores> },
 "mustContain":{"<item text>":true, ...},
 "hardStops":["..."],
 "notes":"one line: the single change that would most improve the best concept"}
```

## The 9 concept-stage lines (keys for `scores`)

| key | rubric line | 5 at concept stage | 1 at concept stage |
|---|---|---|---|
| `1_thumb_stop` | Thumb-stop | Frame/slide 1 is described as one striking object or number + 7 words or fewer | Opens on a title card, logo or a wall of words |
| `2_hook_alignment` | Hook alignment | Spoken hook, on-screen text and visual all say the same thing in second 1 | They disagree, or the topic arrives after a wind-up |
| `3_one_idea_one_device` | One idea, one device | One promise and one metaphor carried to the payoff | A list of visuals; the device changes halfway |
| `4_pacing` | Pacing (planned) | Beats change every 2-4 s with re-hooks every 5-8 s; carousels alternate statement/evidence | Long holds, a slideshow of same-looking slides |
| `7_brand_fit` | Brand fit (planned) | Uses the kit's colours, fonts, footer/logo, rules and compliance plan; feels like this client | Generic broker look, a kit rule ignored |
| `8_originality` | Originality | Different from this client's recent pieces and the usual competitor version | Repeats the last style/device or a common competitor format |
| `9_truth_maths` | Truth and maths | Every number has a math entry and a dated source; every fact is in the kit | A number without working, or any invented fact |
| `10_compliance` | Compliance | Province rules handled (ON line or PROOF), APR + term for any rate, no banned words | Missing ON line without PROOF, "best rate", fake testimonial |
| `12_payoff_action` | Payoff and action | Ends on the payoff; exactly one CTA that delivers | Recap/outro card, engagement bait, several CTAs |

Typography (5), Craft (6) and Sound (11) need renders, so they are not judged at the concept stage.

## Scoring sheet (the month's results file)

The orchestrator merges the five judge outputs into `studio/evals/golden/results/<YYYY-MM>.json`:

```json
{ "month": "2026-12", "ran": "2026-12-01T10:00:00+05:30", "strategist": "opus", "judge": "sonnet",
  "briefs": [ {"id":"g01","best":"B","distinct":true,"scores":{"1_thumb_stop":4, "...":0},
               "mustContain":{"kit complianceLine verbatim ...":true},"hardStops":[],"notes":"..."} ] }
```

`scorecard.py` reads the newest results file:

- `golden.mean`: mean of the 9 best-concept scores per brief, then the mean over briefs. Target 4.2 or more, fail below 3.6.
- `golden.must_contain`: share of mustContain items marked true. Target 90% or more, fail below 70%.
- `golden.hard_stops`: total hard stops. Target 0.
- `golden.recency`: days since `ran`. Target 35 or fewer, fail above 62.

| Brief | Best | 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10 | 12 | Mean | Must-contain | Hard stops | Distinct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g01 Dan Balch reel | | | | | | | | | | | | /8 | | |
| g02 Gregory Hernandez carousel | | | | | | | | | | | | /8 | | |
| g03 Thorntons static | | | | | | | | | | | | /7 | | |
| g04 Brian Wang short reel | | | | | | | | | | | | /7 | | |
| g05 Juliet Fernandez stories | | | | | | | | | | | | /7 | | |
| **Month** | | | | | | | | | | | | /37 | | |

Keep the briefs fixed. If a kit fact behind a mustContain item changes (for example the Thorntons get a compliance line), change the item and note it in the results file `notes`, so the trend stays honest.
