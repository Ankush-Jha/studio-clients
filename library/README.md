# Studio library

Past work indexed for retrieval as exemplars and for variety checks. 131 cards.
Seeded once from the agency's past work (importer in `studio/tools/import/`); new pieces are added by the librarian after each approved job.

## Layout
- `cards/<id>.json`: one card per piece (schema in `studio/SPEC.md`, Library card). Seed extras: `hookPattern`, `slides`, `files.alt`, `files.caption`.
- `thumbs/<id>.jpg`: 480 px wide thumbnails (poster.jpg when present, else the first slide, else a frame at 25%).
- `index.jsonl`: every card, one per line.
- `hashes.json`: pHash + dHash of each thumb and of up to 8 evenly spaced frames per video (or every slide, max 8) for near-duplicate checks.
- `client-history.json`: `{client slug: [card ids]}`. Generic broker reels have no client.
- `feedback.jsonl`, `lessons-pending.md`: written by the gates later, not by the seed.

## Counts
Seed pieces with a real delivered/approved final are `delivered`; stills proofs and motion template tests are `draft`.

| Format | Cards |
|---|---|
| static | 70 |
| carousel | 41 |
| short-reel | 13 |
| graphic-reel | 7 |

| Engine | Cards |
|---|---|
| stills | 105 |
| motion | 10 |
| films | 10 |
| custom-html | 6 |

| Status | Cards |
|---|---|
| draft | 115 |
| delivered | 16 |

| Style | Cards |
|---|---|
| bento | 11 |
| broadsheet | 10 |
| cutout | 10 |
| magazine | 10 |
| paper-trail | 9 |
| swiss | 9 |
| annotated | 8 |
| terminal | 8 |
| isometric | 7 |
| riso | 7 |
| bold-type | 6 |
| greenbrix-brick-objects | 6 |
| legacy-ledger | 4 |
| brick-toy | 2 |
| kinetic-hook | 2 |
| legacy-dossier | 2 |
| legacy-kitchen | 2 |
| legacy-riso | 2 |
| object-3d | 2 |
| phone-pov | 2 |
| pop-hook | 2 |
| crayon-book | 1 |
| isometric-picture-book | 1 |
| midcentury-toon | 1 |
| news-package | 1 |
| oc-game-show | 1 |
| oc-pop-art | 1 |
| pixel-rpg | 1 |
| swiss-motion | 1 |
| urban-sketch | 1 |
| vintage-collage | 1 |

## Notes
- Formats: `graphic-reel` = fully animated reel, `short-reel` = reel built around speaker/client footage or a short motion piece, `carousel` = multi-slide feed set, `static` = single image.
- Statics are one card per (spec, style, format, client). Drafts are proofs, never posted; `variety.py` ignores drafts.
- Reels from before the research (heloc-rules, mortgage-insurance, keep-your-rate) carry PLAYBOOK lessons in `lessons`.
- Finals missing: none.
