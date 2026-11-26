#!/usr/bin/env python3
"""Seed (re-runnable) the Studio library from past work. Read-only on sources.
Writes: library/cards/*.json, library/thumbs/*.jpg, library/index.jsonl, library/hashes.json,
        library/client-history.json, library/README.md
Hand-curated fields live in studio/tools/library_seed_notes.json.
Run: studio/.venv/bin/python studio/tools/seed_library.py
"""
import json, os, glob, subprocess, re, sys, tempfile, shutil, collections
from pathlib import Path
from PIL import Image
import imagehash

R = Path('.')
GR = R / 'graphic reels'
LIB = R / 'library'
HOME = Path.home()
NOTES = json.load(open(R / 'studio/tools/library_seed_notes.json'))
CLIENT_ALIAS = {'georges': 'georges-madi', 'keaton-jim-thornton': 'keaton-thornton-jim-thornton'}
GENERIC_CLIENTS = {'client-a', 'client-b'}
MAX_FRAMES = 8


def ex(p):
    return Path(os.path.expanduser(str(p)))


def absr(p):
    p = ex(p)
    return str(p if p.is_absolute() else GR / p)


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height,r_frame_rate:format=duration', '-of', 'json', str(path)],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    s = d['streams'][0]
    n, den = s['r_frame_rate'].split('/')
    fps = round(int(n) / int(den), 2)
    return round(float(d['format']['duration']), 2), (int(fps) if fps == int(fps) else fps), f"{s['width']}x{s['height']}"


def mtime_date(p):
    import datetime
    return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()


def make_thumb(src_img, cid):
    im = Image.open(src_img).convert('RGB')
    w = 480
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    dst = LIB / 'thumbs' / f'{cid}.jpg'
    im.save(dst, quality=84, optimize=True)
    return dst


def video_frames(video, dur, tmp):
    paths = []
    for i in range(MAX_FRAMES):
        t = dur * (i + 0.5) / MAX_FRAMES
        f = Path(tmp) / f'f{i}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(video), '-frames:v', '1',
                        '-vf', 'scale=270:-2', str(f)], check=True)
        if f.exists():
            paths.append((round(t, 2), f))
    return paths


def hash_img(p):
    im = Image.open(p).convert('RGB')
    return {'phash': str(imagehash.phash(im)), 'dhash': str(imagehash.dhash(im))}


def poster_frame(video, dur, dst):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{dur*0.25:.3f}', '-i', str(video), '-frames:v', '1', str(dst)], check=True)


def base_card(cid):
    return {"id": cid, "title": "", "clients": [], "generic": True, "date": "", "format": "", "engine": "", "style": "",
            "lengthS": None, "fps": None, "size": "", "voice": None, "music": None, "topic": "", "tags": [], "hook": "",
            "logline": "", "structure": "", "device": "", "rejectedStyles": [], "rejectedStructures": [],
            "files": {"final": "", "poster": "", "thumb": f"library/thumbs/{cid}.jpg", "treatment": "", "project": ""},
            "status": "delivered", "feedback": [], "performance": None, "lessons": [], "source": "seed"}


cards, hashes, missing = [], {}, []
tmp = tempfile.mkdtemp()

# ---------------------------------------------------------------- reels
for cid, n in NOTES['reels'].items():
    c = base_card(cid)
    proj = GR / n['project']
    final = ex(n['final']) if str(n['final']).startswith('~') else (GR / n['final'])
    if not final.exists():
        missing.append(f'{cid}: {final}')
        continue
    dur, fps, size = probe(final)
    poster = absr(n['poster']) if n.get('poster') else ''
    c.update({k: n[k] for k in ('title', 'clients', 'generic', 'format', 'engine', 'style', 'voice', 'music', 'topic', 'tags',
                                'hook', 'logline', 'structure', 'device', 'rejectedStyles', 'rejectedStructures', 'lessons')})
    c['hookPattern'] = n.get('hookPattern', '')
    c['date'] = mtime_date(final)
    c['lengthS'], c['fps'], c['size'] = dur, fps, size
    tr = n.get('treatment') or f"{n['project']}/TREATMENT.md"
    c['files'].update({'final': str(final), 'poster': poster, 'treatment': absr(tr), 'project': str(proj)})
    if n.get('alt'):
        c['files']['alt'] = [str(ex(a)) if a.startswith('~') else str(GR / a) for a in n['alt']]
    src = poster if poster and os.path.exists(poster) else None
    if not src:
        src = os.path.join(tmp, cid + '_poster.jpg')
        poster_frame(final, dur, src)
        c['files']['poster'] = ''
    make_thumb(src, cid)
    fr = video_frames(final, dur, tempfile.mkdtemp(dir=tmp))
    hashes[cid] = {'kind': 'video', 'thumb': hash_img(LIB / 'thumbs' / f'{cid}.jpg'),
                   'frames': [dict(t=t, **hash_img(f)) for t, f in fr]}
    cards.append(c)

# ---------------------------------------------------------------- greenbrix carousels
gb = GR / 'clients/greenbrix'
GN = NOTES['greenbrix']
import csv
plan = {r['ID']: r for r in csv.DictReader(open(gb / 'plan.csv'))}
HOOK_OVERRIDE = {'C5': 'The money is coming. The deadline came first.', 'C6': '4 investment deals banks pass on. We look at them.'}
for k in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']:
    cid = f'greenbrix-{k.lower()}'
    row, n = plan[k], GN[k]
    c = base_card(cid)
    slides = sorted((gb / 'FINAL' / k).glob(f'{k}-*.png'))
    if not slides:
        slides = sorted((gb / k / 'out').glob(f'{k}-*.png'))
    if not slides:
        missing.append(cid)
        continue
    w, h = Image.open(slides[0]).size
    caption = (gb / 'FINAL' / k / 'caption.txt')
    c.update({'title': f"Greenbrix {k}: {row['Title']}", 'clients': [GN['client']], 'generic': False, 'date': GN['date'],
              'format': 'carousel', 'engine': 'custom-html', 'style': 'greenbrix-brick-objects', 'size': f'{w}x{h}',
              'topic': f"{row['Focus area']}: {row['Title']}",
              'tags': ['greenbrix', 'private-lending', 'ontario', 'carousel', 'seamless-join', 'brick-motif'] + [t.strip().lower().replace(' ', '-') for t in row['Focus area'].split(';')[:2]],
              'hook': HOOK_OVERRIDE.get(k, row['Slide 1 (cover)']), 'hookPattern': 'list-promise' if re.match(r'^\d', row['Title']) or re.match(r'^\d', row['Slide 1 (cover)']) else 'claim-statement',
              'logline': f"Seven-slide Greenbrix Capital carousel for Krystian Catala: {row['Title']}.",
              'structure': n['structure'], 'device': n['device'], 'rejectedStructures': n.get('rejectedStructures', []), 'lessons': n['lessons'],
              'voice': None, 'music': None})
    c['slides'] = len(slides)
    c['files'].update({'final': str(gb / 'FINAL' / k), 'poster': str(slides[0]), 'treatment': str(gb / k / 'NOTES.md'),
                       'project': str(gb / k)})
    if caption.exists():
        c['files']['caption'] = str(caption)
    make_thumb(slides[0], cid)
    hashes[cid] = {'kind': 'carousel', 'thumb': hash_img(LIB / 'thumbs' / f'{cid}.jpg'),
                   'frames': [dict(n=i + 1, **hash_img(s)) for i, s in enumerate(slides[:MAX_FRAMES])]}
    cards.append(c)

# ---------------------------------------------------------------- statics (broker-stills proofs)
so = GR / 'content-desk/statics/out'
sty_dir = GR / 'content-desk/statics/library'
sty = {}
for sj in sty_dir.glob('*/style.json'):
    d = json.load(open(sj))
    sty[d['slug']] = d
seen = set()
for mf in sorted(so.glob('**/manifest.json')):
    d = json.load(open(mf))
    cdir = mf.parent
    slug = d['client']
    clients = [] if slug in GENERIC_CLIENTS else [CLIENT_ALIAS.get(slug, slug)]
    spec = d['id']
    style = d.get('style') or f"legacy-{d.get('family', 'unknown')}"
    fmt = d.get('format') or 'feed'
    cid = f"{spec}--{style}--{fmt}--{slug}"
    if cid in seen:
        cid += '-2'
    seen.add(cid)
    slides = sorted(cdir.glob('[0-9][0-9].jpg'))
    if not slides:
        missing.append(cid)
        continue
    w, h = Image.open(slides[0]).size
    n_slides = len(d.get('slides', slides))
    cover = d['slides'][0] if d.get('slides') else {}
    runs = [r for r in cover.get('runs', []) if r.get('role') == 'display']
    hook = max(runs, key=lambda r: len(r['text']))['text'] if runs else d['title']
    meta = sty.get(d.get('style') or '', {})
    c = base_card(cid)
    c.update({'title': f"{d['title']} [{style}, {fmt}, {slug}]", 'clients': clients, 'generic': slug in GENERIC_CLIENTS or not clients,
              'date': (d.get('renderedAt') or '')[:10], 'format': 'carousel' if n_slides > 1 else 'static', 'engine': 'broker-stills',
              'style': style, 'size': f'{w}x{h}', 'topic': d['title'], 'status': 'draft',
              'tags': ['broker-stills', spec, style, f'{fmt}-format'] + ([f"group-{d['group']}"] if d.get('group') else []),
              'hook': hook, 'hookPattern': '',
              'logline': f"Proof render of spec '{spec}' in the {meta.get('name', style)} style for {d.get('clientName') or slug}, {fmt} format ({n_slides} slide{'s' if n_slides > 1 else ''}).",
              'structure': f"{n_slides} slide(s), {w}x{h} ({fmt}); slide types: " + ', '.join(s.get('type', '') for s in d.get('slides', [])[:10]),
              'device': meta.get('summary') or f"early broker-stills family '{d.get('family', '?')}' layout with placeholder client {slug}",
              'voice': None, 'music': None,
              'lessons': (['Compliance fields still placeholders (agent name, title, brokerage, licence) in this proof: ' + ', '.join(d['compliance']['missing'])]
                          if d.get('compliance', {}).get('missing') else [])})
    c['slides'] = n_slides
    c['files'].update({'final': str(cdir), 'poster': str(slides[0]), 'project': str(GR / 'content-desk/statics')})
    c['files']['treatment'] = str(GR / 'content-desk/statics' / d['spec']) if d.get('spec') else ''
    make_thumb(slides[0], cid)
    hashes[cid] = {'kind': 'static', 'thumb': hash_img(LIB / 'thumbs' / f'{cid}.jpg'),
                   'frames': [dict(n=i + 1, **hash_img(s)) for i, s in enumerate(slides[:MAX_FRAMES])]}
    cards.append(c)

# ---------------------------------------------------------------- motion test renders
mo = GR / 'content-desk/motion/out'
MD = NOTES['motionDevices']
TITLE = "Paul's HELOC: $7,800 paid, still owes $150,000"
for mp4 in sorted(mo.glob('**/*.mp4')):
    rel = mp4.relative_to(mo)
    if rel.parts[0].startswith('_'):
        continue
    man = mp4.with_suffix('.manifest.json')
    if not man.exists():
        man = mp4.parent / (mp4.stem + '.manifest.json')
    d = json.load(open(man)) if man.exists() else {}
    tpl = d.get('template')
    if not tpl:  # opuscar/game-show has no manifest
        tpl = {'game-show': 'oc-game-show'}.get(rel.parts[1] if rel.parts[0] == 'opuscar' else '', '')
    client = (d.get('client') or {}).get('id') if isinstance(d.get('client'), dict) else None
    client = client or rel.stem.split('.')[0] if rel.parts[0] in ('directions', 'opuscar') else client or rel.parts[-2]
    client_slug = CLIENT_ALIAS.get(client, client)
    cid = 'motion--' + '--'.join(p.replace('.mp4', '') for p in rel.parts)
    dur, fps, size = probe(mp4)
    poster = mp4.with_suffix('.poster.jpg')
    src = str(poster) if poster.exists() else None
    if not src:
        src = os.path.join(tmp, cid + '.jpg')
        poster_frame(mp4, dur, src)
    c = base_card(cid)
    c.update({'title': f"{d.get('title', 'HELOC interest-only')} [{tpl}, {client_slug}]", 'clients': [client_slug], 'generic': False,
              'date': (d.get('renderedAt') or mtime_date(mp4))[:10], 'format': 'short-reel', 'engine': 'motion', 'style': tpl,
              'lengthS': dur, 'fps': fps, 'size': size, 'status': 'draft',
              'topic': 'Interest-only HELOC: the payment moves, the balance does not',
              'tags': ['motion-template-test', tpl, 'heloc', 'interest-only'], 'hook': TITLE, 'hookPattern': 'number-stuck',
              'logline': f"Template test render of '{tpl}' on the heloc-paul data block for {client_slug}: $150,000 balance, 12 payments of $650 = $7,800, balance unchanged.",
              'structure': 'Looping 12-15s HTML/GSAP motion piece rendered frame by frame in Chromium; no voiceover; loops to frame 1.',
              'device': MD.get(tpl, ''), 'voice': None, 'music': 'synthesised SFX only (cue-timed)',
              'lessons': ['Test render of a motion template, not a delivered piece; compliance placeholders (agent name, licence) were still open.']})
    c['files'].update({'final': str(mp4), 'poster': src if poster.exists() else '', 'project': str(GR / 'content-desk/motion')})
    make_thumb(src, cid)
    fr = video_frames(mp4, dur, tempfile.mkdtemp(dir=tmp))
    hashes[cid] = {'kind': 'video', 'thumb': hash_img(LIB / 'thumbs' / f'{cid}.jpg'), 'frames': [dict(t=t, **hash_img(f)) for t, f in fr]}
    cards.append(c)

# ---------------------------------------------------------------- write
for old in (LIB / 'cards').glob('*.json'):
    old.unlink()
cards.sort(key=lambda c: (c['date'], c['id']))
with open(LIB / 'index.jsonl', 'w') as ix:
    for c in cards:
        json.dump(c, open(LIB / 'cards' / f"{c['id']}.json", 'w'), indent=1, ensure_ascii=False)
        ix.write(json.dumps(c, ensure_ascii=False) + '\n')
json.dump(hashes, open(LIB / 'hashes.json', 'w'), indent=0)
hist = collections.defaultdict(list)
for c in cards:
    for cl in c['clients']:
        hist[cl].append(c['id'])
json.dump(dict(sorted(hist.items())), open(LIB / 'client-history.json', 'w'), indent=1)

# README
def cnt(key, f=lambda c: True):
    return collections.Counter(c[key] for c in cards if f(c))
def table(counter):
    return '\n'.join(f'| {k} | {v} |' for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])))
reels = [c for c in cards if c['format'] in ('graphic-reel', 'short-reel')]
readme = f"""# Studio library

Past work indexed for retrieval as exemplars and for variety checks. {len(cards)} cards.
Rebuild with `studio/.venv/bin/python studio/tools/seed_library.py` (read-only on sources; hand-extracted fields live in `studio/tools/library_seed_notes.json`).

## Layout
- `cards/<id>.json`: one card per piece (schema in `studio/SPEC.md`, Library card). Seed extras: `hookPattern`, `slides`, `files.alt`, `files.caption`.
- `thumbs/<id>.jpg`: 480 px wide thumbnails (poster.jpg when present, else the first slide, else a frame at 25%).
- `index.jsonl`: every card, one per line.
- `hashes.json`: pHash + dHash of each thumb and of up to {MAX_FRAMES} evenly spaced frames per video (or every slide, max {MAX_FRAMES}) for near-duplicate checks.
- `client-history.json`: `{{client slug: [card ids]}}`. Generic broker reels have no client; `self` is the agency owner's own reels.
- `feedback.jsonl`, `lessons-pending.md`: written by the gates later, not by the seed.

## Counts
Seed pieces with a real delivered/approved final are `delivered`; broker-stills proofs and motion template tests are `draft`.

| Format | Cards |
|---|---|
{table(cnt('format'))}

| Engine | Cards |
|---|---|
{table(cnt('engine'))}

| Status | Cards |
|---|---|
{table(cnt('status'))}

| Style | Cards |
|---|---|
{table(cnt('style'))}

## Notes
- Formats: `graphic-reel` = fully animated reel, `short-reel` = reel built around speaker/client footage or a short motion piece, `carousel` = multi-slide feed set, `static` = single image.
- Statics are one card per (spec, style, format, client). Drafts are proofs, never posted; `variety.py` ignores drafts.
- Reels from before the research (heloc-rules, mortgage-insurance, keep-your-rate) carry PLAYBOOK lessons in `lessons`.
- Finals missing: {', '.join(missing) if missing else 'none'}.
"""
open(LIB / 'README.md', 'w').write(readme)
shutil.rmtree(tmp, ignore_errors=True)
print(len(cards), 'cards; missing:', missing)
