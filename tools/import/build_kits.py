#!/usr/bin/env python3
"""Build client kits for Studio.  Re-runnable.

Writes only inside $R/kits.  Reads (never writes) clients.json, assets/, the
content-desk seed/roster/token files, PLAYBOOK.md, Greenbrix BRIEF.md and the
FACE_REELS_AGENT Orbis client folder.

Run:  $R/studio/.venv/bin/python $R/studio/tools/build_kits.py
"""
import json, re, os, sys, colorsys, datetime
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans

R = Path(__file__).resolve().parents[2]
GR = R / "graphic reels"
KITS = R / "kits"
SEED = GR / "content-desk/seed/clients"
ROSTER = GR / "content-desk/statics/library/roster.json"
TOKDIR = GR / "content-desk/statics/tokens/clients"
FACE = Path("~/Desktop/FACE_REELS_AGENT/clients/orbis-mortgage-group")
NOW = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def jload(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return default

# --------------------------------------------------------------------------
# hand-written tables
# --------------------------------------------------------------------------
PROV_MAP = {"ON": "Ontario", "QC": "Quebec", "NS": "Nova Scotia", "NB": "New Brunswick",
            "AB": "Alberta", "BC": "British Columbia"}
PROV_REV = {v.lower(): k for k, v in PROV_MAP.items()}

# style -> (display, body, note).  Source: broker-stills/STYLES.md
STYLE_FONTS = {
    "swiss": ("Archivo", "Archivo", ""),
    "terminal": ("Martian Mono", "Martian Mono", ""),
    "bento": ("Mona Sans", "Mona Sans", ""),
    "magazine": ("Bodoni Moda", "Schibsted Grotesk", ""),
    "annotated": ("Familjen Grotesk", "Familjen Grotesk", "handwriting accent: Nanum Pen Script"),
    "cutout": ("Young Serif", "Rethink Sans", ""),
    "riso": ("Bricolage Grotesque", "Space Mono", ""),
    "bold-type": ("Big Shoulders", "Big Shoulders", ""),
    "isometric": ("Red Hat Display", "Red Hat Mono", ""),
    "paper-trail": ("Courier Prime", "IBM Plex Sans Condensed", ""),
    "broadsheet": ("Libre Franklin", "Newsreader", "nameplate: UnifrakturMaguntia"),
}
DEFAULT_FONTS = ("Inter", "Inter")

# Facts read visually from footer images (Read tool).  provenance: "footer image (read visually)"
FOOTER_READ = {
    "krystian-catala": {"brokerage_licence": "#13645"},
    "wise-equity": {"brokerage_licence": "#13463", "agent_licence": "M19002342",
                    "phones": ["(647) 955-7464"], "emails": ["info@wiseequity.ca"], "website": "wiseequity.ca"},
    "georges-madi": {"agent_licence": "#183107", "title": "Mortgage Broker"},
    "scott-brouke": {"title": "Mortgage Broker", "brokerage_name": "Paragon Mortgage Inc.",
                     "phones": ["403-598-1055"], "emails": ["Scott@yourbestmortgage.ca"], "website": "yourbestmortgage.ca"},
    "borrowise": {"emails": ["support@borrowise.ca"], "website": "www.borrowise.ca"},
    "michael-marini": {"title": "Mortgage Agent Level 2"},
    "amit-khurana": {"title": "Mortgage Agent Level 2"},
    "anil-lakhiya": {"brokerage_name": "Legacy Mortgage Group"},
    "sahil-rihani": {"brokerage_licence": "#13654"},
    "al-manji": {"brokerage_licence": "#12728"},
    "akshat-chauhan": {"title": "Mortgage broker"},
    "kulbhushan-narang": {"title": "Mortgage Agent Level 2"},
}
# Brokerage identity read visually from logo images (only used where the sheet/footers lack it)
LOGO_READ = {
    "amit-khurana": {"brokerage_name": "Centum Indigo Mortgages Corp.", "note": "logo prints 'Centum indigo mortgages Corp. Brokerage Number: #12141', matching the sheet licence"},
    "raoul-hunt": {"brokerage_name": "Tango Ontario", "brokerage_licence": "#13691", "note": "logo-2 prints 'tango ONTARIO LIC # 13691'; confirm this is Raoul's brokerage of record (sheet gives none)"},
    "juliet-fernandez": {"brokerage_name": "Mortgage Architects", "note": "logo reads Mortgage Architects; footer prints brokerage #12728, the same number the sheet lists for Mortgage Architects (Dan Balch, Akshat Chauhan)"},
    "al-manji": {"brokerage_name": "Mortgage Architects", "note": "one logo carries '6ix / Mortgage Architects'; footer number 12728 equals the Mortgage Architects brokerage number; confirm"},
}
LOGO_FLAGS = {
    "sahil-rihani": "Logo reads 'Keystone Financial Experts' with Dominion Lending Centres; authorised brokerage name for #13654 not confirmed.",
    "ariana-learoux": "Logo reads 'Brokers for Life' with Dominion Lending Centres; brokerage name and licence not confirmed.",
    "robert-cheszes": "Logo reads 'Brilliant Investor' (brand); brokerage of record not confirmed.",
    "adrian-biccum": "Logo reads 'Your Mortgage Minute' and his email domain is mfco.ca; brokerage of record not confirmed.",
    "byran-peters": "Logo reads 'The Mortgage Doctors' and his email domain is migroup.ca; brokerage name not confirmed (licence 13626 is on his footer).",
    "jalal-khan": "Logos read Mortgage Architects and Vancouver Mortgage Solutions; brokerage name and licence not confirmed.",
    "georges-madi": "Logo reads 'Xperto Equipe Heritage' and 'Centres hypothecaires Dominion National' (very small marks on a wide transparent canvas, may need a crop); brokerage name and licence not confirmed.",
    "anil-lakhiya": "Logo reads 'Always True Financial' with Legacy Mortgage Group.",
}

# extra flags from comparing footers to the sheet
FOOTER_FLAGS = {
    "keaton-thornton-jim-thornton": ["Keaton's footer prints 'License #10530'; the sheet gives M22000917 for Keaton. Confirm which is right."],
    "juliet-fernandez": ["Footer also shows Christine Saranilla (Mortgage Broker Alberta and Saskatchewan, brokerage #12728), who is not in the sheet.",
                         "Footer title 'Mortgage Broker Alberta & British columbia' differs from sheet 'Mortgage Agent Level 2'."],
    "al-manji": ["Footer prints 'License Number: 12728', the same number as the Mortgage Architects brokerage no.; recorded as brokerage licence, agent licence still unknown."],
    "anil-lakhiya": ["Footer website alwaystruefinancial.com differs from sheet website aklmortgagesandwealth.ca.",
                     "Brokerage name read from the footer image (Legacy Mortgage Group); licence numbers not shown anywhere."],
    "gaurav-makhija": ["Footer says 'powered by GNE Mortgages # 10394'; sheet says 'edan Mortgages #10394'. Footer also shows a second phone 647-906-2323.",
                       "Footer name reads 'Gaurav Vijay M'."],
    "nav-utppal": ["Footer carries a FIDES Mortgages logo; sheet says brokerage 'Next Mortgage'. Footer spells the name 'Nav Uppal'."],
    "karven-wu": ["Footer title reads 'Mortgage Specialist at BMO'; sheet says 'Mortgage Agent Level 1' with Caliber Mortgage Inc. & Dominion Lending Centers. Confirm which brand he posts under."],
    "jalal-khan": ["Sheet licence MB607231; footer prints MB6047231. Confirm."],
    "dan-balch": ["Footer phone (519) 438 7025 differs from sheet (519) 854 7025 (sheet says to confirm); sheet time zone 'Greenwich Mean Time' vs posting time in EST."],
    "akshat-chauhan": ["Footer phone +1 (587) 439-6786 differs from sheet (587) 830-3777."],
    "kulbhushan-narang": ["Footer spells the name 'Kulbhusan Narang'.",
                          "Brokerage name 'Orbis Mortgage Group' and title 'Mortgage Agent Level 2' are not in the sheet fields; taken from the footer image and FACE_REELS_AGENT (itself marked needs_confirmation)."],
    "gregory-hernandez": ["Sheet brokerage 'Orbis Mortgage'; FACE_REELS_AGENT lists the group as 'Orbis Mortgage Group'. Gregory's own licence is still to be confirmed with the client (sheet)."],
    "scott-brouke": ["Footer spells 'Scott Bourke' and shows a Paragon Mortgage Inc. logo."],
    "ariana-learoux": ["Footer and website spell 'Leroux'."],
    "jim-decoste": ["Sheet labels both 3000209 (NS) and 220044097 (NB) as broker licences; footer prints 'Lic #2021-3000209'. Which is brokerage vs individual is unconfirmed."],
}

# Special requests -> structured rules (hand-written so the result is exact)
RULES = {
    "keaton-thornton-jim-thornton": [
        {"kind": "never", "text": "3 Nov - Please stop using 'best rates' in all future posts. I have already made the change in this post.",
         "appliesTo": ["all"], "since": "3 Nov", "value": "best rates"},
        {"kind": "outro", "text": "Always use Jim's Outro for Reels",
         "appliesTo": ["reel", "graphic-reel", "short-reel", "footage-reel"], "since": "", "value": "jim"},
        {"kind": "footer", "text": "Use Keaton's footer for all the static posts.",
         "appliesTo": ["static", "carousel"], "since": "", "value": "keaton"},
    ],
    "keith-crossland-dustin-moss": [
        {"kind": "scope", "text": "Aug 16, 2025 - Month End Report: please provide numbers for Edmonton and surrounding area. We don't do work in Calgary so don't want to post for their market.",
         "appliesTo": ["month-end-report"], "since": "2025-08-16", "value": "Edmonton and surrounding area only; never Calgary"},
        {"kind": "hashtags", "text": "Sep 5, 2025 - Please don't hashtag Mortgageontario as we don't work there.",
         "appliesTo": ["all"], "since": "2025-09-05", "value": "never #Mortgageontario"},
    ],
    "vittorio-oliverio": [
        {"kind": "hashtags", "text": "Hashtags: #MortgageBroker #CenterProfessionalMortgageGroup #Cpmg",
         "appliesTo": ["all"], "since": "", "value": ["#MortgageBroker", "#CenterProfessionalMortgageGroup", "#Cpmg"]},
        {"kind": "rotation", "text": "Use alternate associates on alternate days in the footer for the posts.",
         "appliesTo": ["static", "carousel"], "since": "", "value": "alternate associates on alternate days"},
        {"kind": "footer", "text": "For every associate use the phone number 403.380.4413 so the number is used and remembered.",
         "appliesTo": ["all"], "since": "", "value": "403.380.4413"},
        {"kind": "rotation", "text": "15 July 2025 - Remove David from the posts for 4 weeks. Use Kim, Marty, Cara, Vittorio; put a hold on David and Clarke for 4 weeks.",
         "appliesTo": ["static", "carousel"], "since": "2025-07-15", "value": {"use": ["Kim", "Marty", "Cara", "Vittorio"], "hold": ["David", "Clarke"], "weeks": 4}},
        {"kind": "rotation", "text": "28 July 2025 - Skip David for a month; focus on Marty, Cara, Vittorio, Kim for August. In September add Clarke and Karen to the mix.",
         "appliesTo": ["static", "carousel"], "since": "2025-07-28", "value": {"skip": ["David"], "august": ["Marty", "Cara", "Vittorio", "Kim"], "september_add": ["Clarke", "Karen"]}},
        {"kind": "footer", "text": "12 September 2025 - Use footers for Cara, Marry, Clarke, Karen, Vittorio.",
         "appliesTo": ["static", "carousel"], "since": "2025-09-12", "value": ["Cara", "Marry", "Clarke", "Karen", "Vittorio"]},
    ],
    "brian-wang": [
        {"kind": "scope", "text": "Not a mortgage broker: wealth coach / life insurance advisor. Never use mortgage-broker copy or the mortgage compliance line.",
         "appliesTo": ["all"], "since": "", "value": "not a mortgage broker"},
        {"kind": "scope", "text": "Footage reels allowed.", "appliesTo": ["footage-reel"], "since": "", "value": "allowed"},
        {"kind": "outro", "text": "Reels end on his brand card with 'For information only. Not investment advice.'",
         "appliesTo": ["reel", "graphic-reel", "short-reel", "footage-reel"], "since": "", "value": "brand card + For information only. Not investment advice."},
    ],
}
RULE_FLAGS = {
    "vittorio-oliverio": [
        "Rotation requests overlap (15 Jul, 28 Jul, 12 Sep 2025); the 12 Sep 2025 request is the latest and does not list Kim. Sheet spells one associate 'Marry' (earlier 'Marty').",
        "Hashtag text reads '#CenterProfessionalMortgageGroup' but the brokerage is 'Centum professional Mortgage Group Inc.'; kept exactly as the client wrote it.",
    ],
}
RULE_MISSING = {
    "vittorio-oliverio": ["associate footers for Cara, Marty/Marry, Clarke, Karen, Kim, David (only Vittorio's footer exists)"],
}

SEED_DISPLAY_ALIAS_EXTRA = {}

EXTRAS = {
    "abbas": {"seed": "abbas", "note": "not in client sheet"},
    "akaalinder-dhaliwal": {"seed": "akaalinder-dhaliwal", "note": "not in client sheet"},
}

BANNED_PHRASES = ["That's not how it works", "Nobody tells you", "Here's the thing", "Let's dive in",
                  "may surprise you", "game-changer", "unlock", "dream home", "The point?", "Sound familiar?"]
BANNED_PATTERNS = ["\"It's not X, it's Y\" closers", "aphorism endings", "lists of three for rhythm", "em-dash asides"]
BANNED_COMPLIANCE = ["guaranteed approval", "guaranteed", "best rate", "lowest rate", "fear-mongering", "secret loophole"]

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def cap(name):
    return " ".join(w[:1].upper() + w[1:] for w in name.split())

def toks(s):
    return set(re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("&", " ")).split())

def norm_brokerage_lic(s):
    if not s:
        return None
    m = re.search(r"(\d[\d-]*)", s)
    return "#" + m.group(1) if m else s.strip()

def norm_agent_lic(s):
    if not s:
        return None
    s = s.strip()
    m = re.search(r"\b([A-Z]{1,2}\d{6,}|\d{6,})\b", s)
    return m.group(1) if m else s

def lic_disp(l):
    return l if l.startswith("#") or not l[0].isdigit() else l

def lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)

def hex_(rgb):
    return "#%02X%02X%02X" % tuple(int(round(x)) for x in rgb)

def unhex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def hsv(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in rgb))
    return h * 360, s, v

def dist(a, b):
    return float(np.linalg.norm(np.array(a, float) - np.array(b, float)))

def clusters(path, k=8, crop=None):
    """k-means on opaque pixels (5-bit quantised, weighted).  returns [(rgb, frac)] desc."""
    try:
        im = Image.open(R / path).convert("RGBA")
    except Exception:
        return []
    if crop:
        im = im.crop(crop)
    if im.width > 500:
        im = im.resize((500, max(1, int(im.height * 500 / im.width))), Image.BOX)
    a = np.asarray(im)
    px = a[a[..., 3] > 200][:, :3]
    if len(px) < 50:
        return []
    q = (px >> 3).astype(np.int32)
    key = q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2]
    uk, cnt = np.unique(key, return_counts=True)
    cent = np.stack([(uk // 1024) * 8 + 4, ((uk // 32) % 32) * 8 + 4, (uk % 32) * 8 + 4], axis=1).astype(float)
    kk = min(k, len(uk))
    km = KMeans(n_clusters=kk, n_init=4, random_state=0).fit(cent, sample_weight=cnt)
    w = np.zeros(kk)
    for lab, c in zip(km.labels_, cnt):
        w[lab] += c
    w = w / w.sum()
    out = sorted(((tuple(km.cluster_centers_[i]), float(w[i])) for i in range(kk)), key=lambda t: -t[1])
    return out

def non_neutral(rgb):
    h, s, v = hsv(rgb)
    if s < 0.25 or v > 0.95 or v < 0.14:
        return False
    if 8 <= h <= 32 and s < 0.7 and v > 0.4:   # skin-like
        return False
    return True

def pick_palette(cl, min_w=0.008):
    """distinct non-neutral colours ordered by weight."""
    out = []
    for rgb, w in cl:
        if w < min_w or not non_neutral(rgb):
            continue
        if any(dist(rgb, o[0]) < 50 for o in out):
            continue
        out.append((rgb, w))
    return out

def pick_ink(cl):
    c = [x for x in cl if x[1] >= 0.04] or cl
    if not c:
        return None
    ink = min(c, key=lambda t: lum(t[0]))[0]
    return ink if lum(ink) < 0.08 else None

def pick_paper(cl):
    c = [x for x in cl if x[1] >= 0.10 and lum(x[0]) > 0.7 and hsv(x[0])[1] < 0.2]
    return max(c, key=lambda t: t[1])[0] if c else None

def vivid_accent(path):
    """thin saturated bands (rules, stripes) on dark footers: k-means over vivid pixels only."""
    try:
        im = Image.open(R / path).convert("RGBA")
    except Exception:
        return None
    if im.width > 500:
        im = im.resize((500, max(1, int(im.height * 500 / im.width))), Image.BOX)
    a = np.asarray(im)
    px = a[a[..., 3] > 200][:, :3].astype(float)
    if len(px) < 200:
        return None
    mx, mn = px.max(1), px.min(1)
    v = mx / 255
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    sel = px[(sat >= 0.5) & (v >= 0.5)]
    sel = np.array([p_ for p_ in sel if non_neutral(tuple(p_))])
    if len(sel) < 0.003 * len(px):
        return None
    km = KMeans(n_clusters=min(3, len(sel)), n_init=3, random_state=0).fit(sel)
    cnt = np.bincount(km.labels_)
    return tuple(km.cluster_centers_[int(cnt.argmax())])

def extract_colors(footer, logos, crop=None):
    fc = clusters(footer, 8, crop) if footer else []
    lc = []
    for lp in logos:
        lc += clusters(lp, 6)
    lc = sorted(lc, key=lambda t: -t[1])
    fp = pick_palette(fc)
    lp_ = pick_palette(lc, 0.02)
    # accent: first bright candidate from footer
    acc = acc_src = None
    bright = [x for x in fp if hsv(x[0])[2] >= 0.30 and hsv(x[0])[1] >= 0.3]
    if bright and (bright[0][1] >= 0.005):
        acc, acc_src = bright[0][0], "footer"
    elif fp:
        acc, acc_src = fp[0][0], "footer"
    if acc is not None and hsv(acc)[2] < 0.3 and footer:
        va = vivid_accent(footer)
        if va is not None:
            fp = [(va, 0.01)] + fp
            acc, acc_src = va, "footer"
    if acc is None:
        b = [x for x in lp_ if hsv(x[0])[2] >= 0.35] or lp_
        if b:
            acc, acc_src = b[0][0], "logo"
    pal = []
    if acc is not None:
        pal.append((acc, acc_src))
        for src, lst in (("footer", fp), ("logo", lp_)):
            for rgb, w in lst:
                if len(pal) >= 3:
                    break
                if all(dist(rgb, p[0]) > 60 for p in pal):
                    pal.append((rgb, src))
    ink = pick_ink(fc) or pick_ink(lc)
    paper = pick_paper(fc) or pick_paper(lc)
    return {"palette": pal, "ink": ink, "paper": paper}

def logo_is_light(path):
    try:
        im = Image.open(R / path).convert("RGBA")
    except Exception:
        return False
    a = np.asarray(im.resize((120, max(1, int(im.height * 120 / im.width)))))
    m = a[..., 3] > 200
    if m.sum() < 30:
        return False
    return float(np.mean([lum(tuple(p)) for p in a[m][:, :3]])) > 0.6 and (a[..., 3] < 50).mean() > 0.1

def dtcg_color(hexv, source, provisional, extra=None):
    d = {"studio": {"source": source, "provisional": provisional}}
    if extra:
        d["studio"].update(extra)
    return {"$type": "color", "$value": hexv, "$extensions": d}

# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------
sheet = jload(R / "clients.json")["clients"]
prov = jload(R / "assets/_provenance.json")
roster = jload(ROSTER)["clients"]
seed = {p.stem: jload(p) for p in sorted(SEED.glob("*.json"))}
tokfiles = {p.stem: jload(p) for p in sorted(TOKDIR.glob("*.json"))}

# slug mapping seed -> sheet client by name tokens
def slug_of(c):
    return c["asset_folder"].strip("/").split("/")[-1]

seed_to_sheet = {}
for s, d in seed.items():
    st = toks(d["name"])
    cands = [c for c in sheet if st and st <= toks(c["name"])]
    if slug_of_match := [c for c in sheet if slug_of(c) == s]:
        cands = slug_of_match
    if len(cands) > 1:
        eq = [c for c in cands if toks(c["name"]) == st]
        cands = eq or cands
    seed_to_sheet[s] = slug_of(cands[0]) if len(cands) == 1 else None

sheet_to_seed = {}
for s, t in seed_to_sheet.items():
    if t:
        sheet_to_seed[t] = s

PLAYBOOK_OK = (GR / "PLAYBOOK.md").exists()
GB_BRIEF = GR / "clients/greenbrix/BRIEF.md"
face_client = jload(FACE / "client.json", {})
face_brand = jload(FACE / "brand/brand.json", {})
face_comp = jload(FACE / "compliance.json", {})

def provfiles(slug):
    return (prov.get("clients") or {}).get(slug, [])

def parse_location(loc, seedcity, seedprov):
    """returns city, province, region(extra), note"""
    if not loc:
        return None, None, None
    loc = re.sub(r"\(.*?\)", "", loc).strip()
    parts = [p.strip() for p in loc.split(",") if p.strip()]
    city = prov_ = region = None
    for p in parts:
        if p.lower() in PROV_REV:
            prov_ = PROV_REV[p.lower()]
    cities = [p for p in parts if p.lower() not in PROV_REV]
    if cities:
        if cities[0].upper() == "GTA":
            region = "GTA"
        else:
            city = cities[0]
    return city, prov_, region

# --------------------------------------------------------------------------
# build one kit
# --------------------------------------------------------------------------
KEYFIELDS = ["name", "city", "province", "group", "brokerage.name", "brokerage.licence",
             "agent.licence", "photo", "footer", "logo", "colours", "complianceLine"]

def build_kit(slug, c, seedslug, extra_note=None):
    P = {}          # provenance
    flags, missing, na = [], [], set()
    sd = seed.get(seedslug) if seedslug else None
    rs = roster.get(seedslug) if seedslug else None
    SHEET = "clients.json"
    k = {"id": slug, "aliases": [], "sheetId": c["id"] if c else None}
    if seedslug and seedslug != slug:
        k["aliases"].append(seedslug)
    if slug == "keaton-thornton-jim-thornton":
        k["aliases"] = sorted(set(k["aliases"]) | {"keaton-jim-thornton"})
    if slug == "georges-madi":
        k["aliases"] = sorted(set(k["aliases"]) | {"georges"})

    # name
    if c:
        k["name"] = cap(c["name"]); P["name"] = f"{SHEET} name"
        if k["name"] != c["name"]:
            pass
    else:
        k["name"] = sd["name"]; P["name"] = "content-desk seed roster"
    k["people"] = c["people"] if c and c["people"] else []
    if k["people"]:
        P["people"] = f"{SHEET} people"

    # city / province
    city = prov_ = region = None
    if c and c.get("location"):
        city, prov_, region = parse_location(c["location"], None, None)
        if city or prov_:
            P["city"] = f"{SHEET} location '{c['location']}'" if city else None
            P["province"] = f"{SHEET} location '{c['location']}'" if prov_ else None
    scity = (sd or {}).get("city") or (rs or {}).get("city") or None
    sprov = (sd or {}).get("province") or (rs or {}).get("province") or None
    if city and scity and city.lower() != scity.lower():
        flags.append(f"City conflict: sheet says '{city}', roster/seed says '{scity}'. Sheet used.")
    if prov_ and sprov and prov_ != sprov:
        flags.append(f"Province conflict: sheet says {prov_}, roster/seed says {sprov}. Sheet used.")
    if not city and scity:
        city = scity; P["city"] = "content-desk seed/roster"
    if not prov_ and sprov:
        prov_ = sprov; P["province"] = "content-desk seed/roster"
    if region and not city:
        k["region"] = region
    k["city"] = city; k["province"] = prov_
    k["region"] = region or ""
    # group
    grp = (sd or {}).get("group")
    if grp in (0, None):
        k["group"] = None
        flags.append("Group not assigned: no group in the calendar/roster. Assign one before rendering." if c or sd else "No group.")
    else:
        k["group"] = grp; P["group"] = "content-desk seed (calendar)"
        if rs and rs.get("group") != grp:
            flags.append(f"Group conflict: seed {grp} vs roster {rs.get('group')}.")
    if sd:
        for f in sd.get("flags") or []:
            flags.append("seed: " + f)
    if rs:
        for f in rs.get("flags") or []:
            if "seed: " + f not in flags:
                flags.append("roster: " + f)
    k["video"] = sd.get("video") if sd else None
    if sd:
        P["video"] = "content-desk seed"
    else:
        missing.append("video (footage reels allowed?)")
    langs = (sd or {}).get("languages") or (rs or {}).get("languages")
    if langs:
        k["languages"] = langs; P["languages"] = "content-desk seed/roster"
    else:
        k["languages"] = ["en"]; P["languages"] = "default (no source)"
        if prov_ == "QC":
            k["languages"] = ["en", "fr"]; P["languages"] = "rule: QC requires French"

    # brokerage / agent
    fr = FOOTER_READ.get(slug, {})
    FIMG = "footer image (read visually)"
    bname = c["brokerage_name"] if c else None
    if bname:
        P["brokerage.name"] = f"{SHEET} brokerage_name"
    bname = bname.strip() if bname else None
    if not bname and fr.get("brokerage_name"):
        bname = fr["brokerage_name"]; P["brokerage.name"] = FIMG
    blic = norm_brokerage_lic(c["brokerage_license_no"]) if c and c["brokerage_license_no"] else None
    if blic:
        P["brokerage.licence"] = f"{SHEET} brokerage_license_no"
    if not blic and fr.get("brokerage_licence"):
        blic = fr["brokerage_licence"]; P["brokerage.licence"] = FIMG + (" and sheet other_ids" if c and c.get("other_ids") else "")
    alic = norm_agent_lic(c["agent_license_no"]) if c and c["agent_license_no"] else None
    if alic:
        P["agent.licence"] = f"{SHEET} agent_license_no"
    if not alic and fr.get("agent_licence"):
        alic = fr["agent_licence"]; P["agent.licence"] = FIMG
    title = c["designation"] if c and c["designation"] else None
    if title:
        P["agent.title"] = f"{SHEET} designation"
    if not title and fr.get("title"):
        title = fr["title"]; P["agent.title"] = FIMG
    lr = LOGO_READ.get(slug, {})
    if lr.get("brokerage_name") and not bname:
        bname = lr["brokerage_name"]; P["brokerage.name"] = "logo image (read visually)"
    if lr.get("brokerage_licence") and not blic:
        blic = lr["brokerage_licence"]; P["brokerage.licence"] = "logo image (read visually)"
    aname = k["name"]
    # raw_client_details parse for licences the structured fields miss
    raw = (c or {}).get("raw_client_details") or ""
    if not alic and raw:
        m = re.findall(r"\b(M\d{8})\b", raw)
        if m:
            alic = m[0]; P["agent.licence"] = f"{SHEET} raw_client_details"
    # special cases
    if slug == "keaton-thornton-jim-thornton":
        ppl = k["people"]
        alic = " / ".join(f"{p['agent_license_no']} ({p['name'].split()[0]})" for p in ppl if p.get("agent_license_no"))
        P["agent.licence"] = f"{SHEET} people / raw_client_details"
        title = " / ".join(f"{p['designation']} ({p['name'].split()[0]})" for p in ppl)
        P["agent.title"] = f"{SHEET} people"
    if slug == "jim-decoste":
        blic = "#2021-3000209"; P["brokerage.licence"] = FIMG + "; sheet writes 'NS Broker License # 3000209'"
        alic = "NB 220044097"; P["agent.licence"] = f"{SHEET} agent_license_no ('NB Broker License # 220044097')"
        title = "Mortgage Owner / Mortgage Broker"; P["agent.title"] = f"{SHEET} designation + footer image"
    if slug == "rahul-vinod":
        blic = "#2021-3000208"
    if slug == "kulbhushan-narang" and not bname:
        bname = face_client.get("company", {}).get("legal_name"); P["brokerage.name"] = "FACE_REELS_AGENT/clients/orbis-mortgage-group/client.json company.legal_name + footer image"
    if slug == "krystian-catala":
        bname = "Greenbrix Capital"; P["brokerage.name"] = "graphic reels/clients/greenbrix/BRIEF.md"
        alic = "M12001607"; P["agent.licence"] = "graphic reels/clients/greenbrix/BRIEF.md (Greenbrix About page, found 17 Nov)"
        title = "Mortgage Broker"; P["agent.title"] = "graphic reels/clients/greenbrix/BRIEF.md ('Broker & President')"
        blic = "#13645"; P["brokerage.licence"] = "footer image (read visually) + BRIEF.md + sheet other_ids"
        k["province"] = "ON"; P["province"] = "graphic reels/clients/greenbrix/BRIEF.md (Ontario, FSRA)"
        prov_ = "ON"
    if slug == "brian-wang":
        pass
    if slug == "kulbhushan-narang":
        if not prov_:
            k["province"] = prov_ = "ON"; P["province"] = "FACE_REELS_AGENT client.json company.jurisdiction"
        if not k["city"]:
            k["city"] = "Vaughan"; P["city"] = "FACE_REELS_AGENT client.json company.office_address (21-7611 Pine Valley Dr, Vaughan, ON)"
    if slug == "ranjit-singh" and not prov_:
        k["province"] = prov_ = "ON"; P["province"] = f"{SHEET} location 'GTA' (Greater Toronto Area) + M-format Ontario licence"
        k["region"] = "GTA"
    if slug == "wise-equity" and not prov_:
        pass

    k["brokerage"] = {"name": bname, "licence": blic}
    k["agent"] = {"name": aname, "title": title or "", "licence": alic}
    if not title:
        missing.append("agent.title")

    # contact
    phones = list(c["phones"]) if c else []
    emails = list(c["emails"]) if c else []
    website = (c["website"] or "") if c else ""
    if phones or emails or website:
        P["contact"] = f"{SHEET} phones/emails/website"
    if fr.get("phones") and not phones:
        phones = fr["phones"]; P["contact"] = FIMG
    if fr.get("emails") and not emails:
        emails = fr["emails"]; P["contact"] = FIMG
    if fr.get("website") and not website:
        website = fr["website"]; P["contact"] = FIMG
    k["contact"] = {"phones": phones, "emails": emails, "website": website}
    if not phones: missing.append("contact.phones")
    if not emails: missing.append("contact.emails")
    if not website: missing.append("contact.website")

    k["services"] = c["services"] if c and c["services"] else []
    if k["services"]:
        P["services"] = f"{SHEET} services"
    else:
        missing.append("services")
    aud = (sd or {}).get("audience") or ""
    if slug == "kulbhushan-narang":
        aud = face_client.get("audience", ""); P["audience"] = "FACE_REELS_AGENT client.json audience (draft)"
    if slug == "krystian-catala":
        aud = "Ontario homeowners and investors the banks turned down or can't serve fast enough, such as business owners, rebuilders, people facing power of sale, bridge-loan needs and investors."
        P["audience"] = "graphic reels/clients/greenbrix/BRIEF.md"
    k["audience"] = aud
    if aud and "audience" not in P:
        P["audience"] = "content-desk seed"
    if not aud:
        missing.append("audience")

    k["postingMode"] = (c or {}).get("posting_mode") or ""
    k["postingTime"] = (c or {}).get("posting_time") or ""
    tz = (c or {}).get("time_zone") or ""
    k["timeZone"] = tz.split(" (")[0] if tz else ""
    if k["postingMode"] or k["postingTime"] or k["timeZone"]:
        P["posting"] = f"{SHEET} posting_mode/posting_time/time_zone"
    if tz and "IST" in tz:
        flags.append(f"Time zone note in sheet: '{tz}'.")
        k["timeZone"] = "EST"
    k["figma"] = (c or {}).get("figma_file") or ""
    if k["figma"]:
        P["figma"] = f"{SHEET} figma_file"

    # notes -> flags
    for n in (c or {}).get("notes") or []:
        flags.append("sheet note: " + n)
    if c and c.get("photo_notes"):
        flags.append("sheet photo note: " + c["photo_notes"])
    flags += FOOTER_FLAGS.get(slug, [])
    if slug in LOGO_READ:
        flags.append("Logo-derived brokerage facts: " + LOGO_READ[slug]["note"])
    if slug in LOGO_FLAGS:
        flags.append(LOGO_FLAGS[slug])
    flags += RULE_FLAGS.get(slug, [])
    if slug == "krystian-catala":
        flags.append("No group in the calendar/roster (sheet client with no group).") if False else None

    # rules
    rules = []
    for i, r in enumerate(RULES.get(slug, []), 1):
        rr = {"id": f"r{i}", "kind": r["kind"], "text": r["text"], "appliesTo": r["appliesTo"],
              "since": r.get("since", ""), "source": "sheet special_requests" if c and c["special_requests"] else "task brief"}
        if "value" in r:
            rr["value"] = r["value"]
        rules.append(rr)
    if c and c["special_requests"] and slug not in RULES:
        for i, t in enumerate(c["special_requests"], 1):   # safety net: unmapped requests become kind other
            rules.append({"id": f"r{i}", "kind": "other", "text": t, "appliesTo": ["all"], "since": "", "source": "sheet special_requests"})
    k["rules"] = rules
    if rules:
        P["rules"] = "sheet special_requests (hand-mapped)" if slug != "brian-wang" else "task brief"
    missing += RULE_MISSING.get(slug, [])

    # assets
    assets = {"photo": None, "footer": None, "footerAlt": None, "logos": [], "check": []}
    pf = provfiles(slug)
    for f in pf:
        path, kind, conf = f["file"], f["kind"], f["confidence"]
        if not (R / path).exists():
            continue
        if conf != "verified":
            assets["check"].append(path)
        if kind == "photo":
            if conf == "verified":
                assets["photo"] = path; P["photo"] = "assets/_provenance.json (verified)"
        elif kind == "footer":
            if conf != "verified":
                continue
            if assets["footer"] is None:
                assets["footer"] = path; P["footer"] = "assets/_provenance.json (verified)"
            else:
                assets["footerAlt"] = path; P["footerAlt"] = "assets/_provenance.json (verified)"
        elif kind == "logo":
            if conf == "verified":
                assets["logos"].append(path)
                P["logos"] = "assets/_provenance.json (verified)"
    if slug == "rahul-vinod":
        orphan = "assets/_unassigned/image60-mmg-badges.png"
        if (R / orphan).exists():
            assets["check"].append(orphan)
            flags.append("Orphan image 'Elite/Platinum badges + Maritime Mortgage Group logo' may belong to Rahul (Moncton NB); confirm.")
    for f in pf:
        if f["confidence"] != "verified":
            flags.append(f"Asset to confirm: {f['file']} ({f.get('note','')})")
    if c and c.get("photo_notes") and "doesnt want" in c["photo_notes"].lower().replace("'", ""):
        na.add("photo")
        P["photo"] = f"{SHEET} photo_notes: client doesn't want image assets"
        if slug == "wise-equity":
            assets["photo"] = None
    if slug == "krystian-catala":
        extra = GR / "clients/greenbrix/assets"
        k["brandRefs"] = [str((extra / n).relative_to(R)) for n in
                          ["logo-t.png", "logo-light.png", "logo-dlc-t.png", "logo-dlc-light.png", "logo.png", "logo-dlc.png", "headshot-cut.png", "headshot.jpg"]
                          if (extra / n).exists()] + [str(GB_BRIEF.relative_to(R))]
        k["extraLogos"] = {"light": str((extra / "logo-t.png").relative_to(R)), "dark": str((extra / "logo-light.png").relative_to(R)),
                           "dlcLight": str((extra / "logo-dlc-t.png").relative_to(R)), "dlcDark": str((extra / "logo-dlc-light.png").relative_to(R))}
    if slug == "brian-wang":
        card = "graphic reels/portfolio-failing/source/brand-card.png"
        assets["footer"] = card; P["footer"] = "graphic reels/portfolio-failing/source/brand-card.png (brand card; end card)"
        missing += ["standalone logo file (logo exists only inside the brand card)", "standalone photo (photo exists only inside the brand card)"]
        k["brandRefs"] = [card]
    if slug in ("kulbhushan-narang", "gregory-hernandez"):
        k["faceReelsClient"] = "orbis-mortgage-group"
        k["brandRefs"] = [str(FACE / "brand/brand.json"), str(FACE / "brand/logo.png"), str(FACE / "brand/logo_white.png"),
                          str(FACE / "compliance.json"), str(FACE / "client.json")]
        if slug == "kulbhushan-narang":
            flags.append("FACE_REELS_AGENT compliance.json (draft, not confirmed by Orbis/FSRA) requires on end card: M17000370, 13476, Orbis Mortgage Group and the disclaimer 'General information only, not financial advice. Options depend on your situation and are subject to lender approval (O.A.C.)'.")
    k["assets"] = assets
    if not assets["photo"] and "photo" not in na:
        missing.append("assets.photo")
    if not assets["footer"]: missing.append("assets.footer")
    if not assets["logos"] and not (slug == "brian-wang"):
        missing.append("assets.logos")

    # stills
    if rs and rs.get("primary"):
        k["stills"] = {"primary": rs["primary"], "secondary": rs.get("secondary"), "variant": rs.get("variant")}
        P["stills"] = "content-desk/statics/library/roster.json"
    else:
        k["stills"] = {"primary": None, "secondary": None, "variant": None}
        missing.append("stills (no roster style assigned; needs a group first)" if k["group"] is None else "stills")

    # compliance line
    parts = []
    if aname and k["agent"]["title"] and not k["people"]:
        parts.append(f"{aname}, {k['agent']['title']}")
    elif aname and not k["people"]:
        parts.append(aname)
    if alic and not k["people"]:
        parts.append("Lic. " + alic)
    if bname:
        parts.append(bname)
    if blic:
        parts.append("Brokerage Lic. " + blic)
    cl = " · ".join(parts)
    cline = None
    strict = (prov_ == "ON") or not prov_
    if slug == "brian-wang":
        cline = "Brian Wang, Wealth Coach / Life Insurance Advisor · Lic. #05089990 · Caliber Wealth Management"
        P["complianceLine"] = "task brief + brand card image (read visually)"
        flags.append("Not a mortgage broker; the Ontario mortgage-brokerage rule does not apply. Insurance/advice wording to be confirmed with the client. Required footer note: 'For information only. Not investment advice.'")
    elif strict:
        if bname and blic and (alic or k["people"] or True) and not k["people"]:
            cline = cl
        else:
            flags.append("Ontario: brokerage name + licence required before posting" if prov_ == "ON" else
                         "Province unknown; treated as Ontario-strict: brokerage name + licence required before posting")
            if k["people"] and bname and blic:
                cline = None
    else:
        known = [x for x in (alic, blic) if x]
        if known and parts:
            cline = cl
    if slug == "keaton-thornton-jim-thornton":
        cline = None
    if cline and slug != "brian-wang":
        P["complianceLine"] = "composed from sheet/footer facts above"
    k["complianceLine"] = cline
    if not cline:
        missing.append("complianceLine")
    if not bname: missing.append("brokerage.name")
    if not blic and slug != "brian-wang": missing.append("brokerage.licence")
    if not alic: missing.append("agent.licence")
    if slug == "brian-wang":
        na.add("brokerage.licence")
        k["brokerage"] = {"name": "Caliber Wealth Management", "licence": None}
        k["agent"] = {"name": "Brian Wang", "title": "Wealth Coach / Life Insurance Advisor", "licence": "#05089990"}
        P["brokerage.name"] = P["agent.title"] = P["agent.licence"] = "task brief + brand card image (read visually)"
        missing = [m for m in missing if m not in ("brokerage.name", "agent.licence", "brokerage.licence", "agent.title")]
        k["contact"] = {"phones": ["(437) 425-2600"], "emails": ["brian.wang@caliberwealthmanagement.ca"], "website": ""}
        P["contact"] = "task brief + brand card image"
        missing = [m for m in missing if not m.startswith("contact.phones") and not m.startswith("contact.emails")]
        k["services"] = []
    if not k["city"]: missing.append("city")
    if not k["province"]: missing.append("province")
    if k["group"] is None: missing.append("group")

    k["_prov"] = prov_
    k["_na"] = na
    k["_flags"] = flags
    k["_missing"] = missing
    k["_P"] = P
    return k


# --------------------------------------------------------------------------
# website facts (kits/<slug>/web.json, written by a separate agent)
# --------------------------------------------------------------------------
def _norm(x):
    return re.sub(r"[^a-z0-9]", "", (x or "").lower())

def _drop_missing(k, *prefixes):
    k["_missing"] = [m for m in k["_missing"] if not any(m.startswith(p_) for p_ in prefixes)]

def apply_web(k, web):
    """sheet facts win; website fills empties; conflicts become flags 'website says X'."""
    url = web.get("url") or ""
    src = f"website: {url}"
    P, flags = k["_P"], k["_flags"]
    k["_web"] = web
    # brokerage
    wb = web.get("brokerage") or {}
    if wb.get("name"):
        if not k["brokerage"]["name"]:
            k["brokerage"]["name"] = wb["name"]; P["brokerage.name"] = src; _drop_missing(k, "brokerage.name")
        elif _norm(wb["name"]) != _norm(k["brokerage"]["name"]):
            flags.append(f"website says brokerage name '{wb['name']}' (kit has '{k['brokerage']['name']}')")
    if wb.get("licence"):
        wl = norm_brokerage_lic(wb["licence"])
        if not k["brokerage"]["licence"]:
            k["brokerage"]["licence"] = wl; P["brokerage.licence"] = src; _drop_missing(k, "brokerage.licence")
        elif _norm(wl) not in _norm(k["brokerage"]["licence"]):
            flags.append(f"website says brokerage licence '{wb['licence']}' (kit has '{k['brokerage']['licence']}')")
    # agent licence / title from team or labelled licences
    nt = toks(k["name"])
    for m in web.get("team") or []:
        if m.get("name") and len(toks(m["name"]) & nt) >= 2:
            if m.get("licence"):
                if not k["agent"]["licence"]:
                    k["agent"]["licence"] = m["licence"]; P["agent.licence"] = src; _drop_missing(k, "agent.licence")
                elif _norm(m["licence"]) not in _norm(k["agent"]["licence"]):
                    flags.append(f"website says {m['name']} licence '{m['licence']}' (kit has '{k['agent']['licence']}')")
            if m.get("title"):
                if not k["agent"]["title"]:
                    k["agent"]["title"] = m["title"]; P["agent.title"] = src; _drop_missing(k, "agent.title")
                elif _norm(m["title"]) != _norm(k["agent"]["title"]):
                    flags.append(f"website says title '{m['title']}' (kit has '{k['agent']['title']}')")
            break
    for l in web.get("licences") or []:
        lab = (l.get("label") or "").lower()
        val = l.get("value")
        if val and not k["agent"]["licence"] and any(w in lab for w in ("agent", "broker licence", "individual", "mortgage broker")) and "brokerage" not in lab:
            k["agent"]["licence"] = val; P["agent.licence"] = f"{src} ({l.get('label')}, {l.get('where','')})"; _drop_missing(k, "agent.licence")
        elif val and not k["brokerage"]["licence"] and "brokerage" in lab:
            k["brokerage"]["licence"] = norm_brokerage_lic(val); P["brokerage.licence"] = f"{src} ({l.get('label')}, {l.get('where','')})"; _drop_missing(k, "brokerage.licence")
    # languages (seed/roster win)
    wl = [x for x in (web.get("languages") or [])]
    if wl:
        if P.get("languages", "").startswith("default") or P.get("languages", "").startswith("rule"):
            if "fr" in k["languages"] and "fr" not in [x.lower()[:2] for x in wl]:
                flags.append(f"website lists languages {wl}; QC rule keeps French required")
            else:
                k["languages"] = [x.lower()[:2] for x in wl]; P["languages"] = src
        elif sorted(x.lower()[:2] for x in wl) != sorted(k["languages"]):
            flags.append(f"website says languages {wl} (kit has {k['languages']})")
    # services
    if web.get("specialties"):
        if not k["services"]:
            k["services"] = list(web["specialties"]); P["services"] = src; _drop_missing(k, "services")
    # audience
    if not k["audience"] and (web.get("specialties") or web.get("serviceAreas")):
        bits = []
        if web.get("serviceAreas"): bits.append("Serves " + ", ".join(web["serviceAreas"]))
        if web.get("specialties"): bits.append("focus: " + ", ".join(web["specialties"]))
        k["audience"] = "; ".join(bits) + "."; P["audience"] = src + " (serviceAreas/specialties)"; _drop_missing(k, "audience")
    # contact
    c = k["contact"]
    for key, wk in (("phones", "phones"), ("emails", "emails")):
        wv = web.get(wk) or []
        if wv and not c[key]:
            c[key] = list(wv); P["contact"] = P.get("contact") or src; P[f"contact.{key}"] = src; _drop_missing(k, f"contact.{key}")
        elif wv and c[key]:
            have = {_norm(x) for x in c[key]}
            extra = [x for x in wv if _norm(x) not in have and _norm(x)[-10:] not in {h[-10:] for h in have}]
            if extra:
                flags.append(f"website says {key} {extra} (kit has {c[key]})")
    if url and not c["website"]:
        c["website"] = url; P["contact.website"] = src; _drop_missing(k, "contact.website")
    # bio / socials / extras
    soc = {a: b for a, b in (web.get("socials") or {}).items() if b}
    k["socials"] = soc
    k["bio"] = web.get("bio") or ""
    if soc: P["socials"] = src
    if k["bio"]: P["bio"] = src
    k["webBlock"] = {x: web.get(x) for x in ("url", "fetched", "tagline", "yearsInBusiness", "serviceAreas", "specialties",
                                              "bookingUrl", "testimonialsCount", "notes", "sources", "fonts", "logoUrls") if web.get(x)}
    for n in web.get("notes") or []:
        flags.append("website note: " + n)
    if not soc: k["_missing"].append("socials")
    if not k["bio"]: k["_missing"].append("bio")
    # recompute compliance line if it can now be built
    if not k["complianceLine"] and k["id"] != "keaton-thornton-jim-thornton" and not k["people"]:
        b, a, t = k["brokerage"], k["agent"], k["agent"]["title"]
        parts = [f"{k['name']}, {t}" if t else k["name"]]
        if a["licence"]: parts.append("Lic. " + a["licence"])
        if b["name"]: parts.append(b["name"])
        if b["licence"]: parts.append("Brokerage Lic. " + b["licence"])
        strict = (k["_prov"] == "ON") or not k["_prov"]
        if (strict and b["name"] and b["licence"]) or (not strict and (a["licence"] or b["licence"])):
            k["complianceLine"] = " · ".join(parts); P["complianceLine"] = "composed from sheet/footer/website facts"
            _drop_missing(k, "complianceLine")
            k["_flags"] = [f for f in k["_flags"] if not f.startswith("Ontario: brokerage name + licence") and not f.startswith("Province unknown; treated")]

# --------------------------------------------------------------------------
# colours + tokens
# --------------------------------------------------------------------------
def make_tokens(k, tokfile):
    slug = k["id"]
    A = k["assets"]
    conf = jload(KITS / slug / "confirm.json")
    ext_note = None
    palette = None
    colors = {}
    source = None
    provisional = True
    good = False
    # 1) confirmed
    cc = (conf or {}).get("colors") or (conf or {}).get("color") if conf else None
    if cc and isinstance(cc, dict) and (cc.get("accent") or {}):
        def gv(x):
            return x.get("$value") if isinstance(x, dict) else x
        colors = {n: gv(cc[n]) for n in ("accent", "accent2", "ink", "paper") if cc.get(n)}
        source, provisional, good = "confirmed", False, True
    # 2a) website brand colours (stronger than footer extraction)
    elif (k.get("_web") or {}).get("brandColors"):
        bc = [x.get("hex") for x in k["_web"]["brandColors"] if x.get("hex") and re.match(r"^#?[0-9A-Fa-f]{6}$", x["hex"])]
        bc = ["#" + x.lstrip("#").upper() for x in bc]
        nn = [x for x in bc if non_neutral(unhex(x))] or bc
        if nn:
            colors["accent"] = nn[0]
            for x in nn[1:]:
                if dist(unhex(x), unhex(nn[0])) > 60:
                    colors["accent2"] = x; break
            dk = [x for x in bc if lum(unhex(x)) < 0.08]
            if dk: colors["ink"] = min(dk, key=lambda x: lum(unhex(x)))
            lt = [x for x in bc if lum(unhex(x)) > 0.8]
            if lt: colors["paper"] = max(lt, key=lambda x: lum(unhex(x)))
            palette = bc[:3]
            source, good = "website", True
            ext_note = f"website brand colours: {k['_web'].get('url','')}"
    # 2) explicit brand data
    elif slug == "krystian-catala":
        colors = {"accent": "#1F6A37", "accent2": "#86C64F", "ink": "#0B2E1B", "paper": "#F2F4EC"}
        source, good = "brand", True
        ext_note = "graphic reels/clients/greenbrix/BRIEF.md (colours read from the logo by the Greenbrix brief)"
    elif slug == "kulbhushan-narang" and face_brand.get("colors"):
        fb = face_brand["colors"]
        colors = {"accent": fb["accent"], "accent2": fb["accent_light"], "ink": fb["primary"], "paper": fb["background_light"]}
        source, good = "brand", True
        ext_note = "FACE_REELS_AGENT orbis-mortgage-group brand.json (read from live site, no official guide)"
    elif slug == "brian-wang":
        cl = extract_colors("graphic reels/portfolio-failing/source/brand-card.png", [], (14, 0, 486, 747))
        pal = cl["palette"]
        if pal:
            colors = {"accent": hex_(pal[0][0])}
            if len(pal) > 1: colors["accent2"] = hex_(pal[1][0])
            if cl["ink"]: colors["ink"] = hex_(cl["ink"])
            if cl["paper"]: colors["paper"] = hex_(cl["paper"])
            palette = [hex_(p[0]) for p in pal]
            source, good = "brand-card", True
    else:
        footer = A["footer"]
        logos = A["logos"]
        if footer or logos:
            ex = extract_colors(footer, logos)
            pal = ex["palette"]
            if pal:
                colors["accent"] = hex_(pal[0][0])
                src_acc = pal[0][1]
                if len(pal) > 1:
                    colors["accent2"] = hex_(pal[1][0])
                if ex["ink"] is not None:
                    colors["ink"] = hex_(ex["ink"])
                if ex["paper"] is not None:
                    colors["paper"] = hex_(ex["paper"])
                palette = [hex_(p[0]) for p in pal]
                source, good = src_acc, True
                k["_srcs"] = {i: p[1] for i, p in enumerate(pal)}
    if not good:
        fb = None
        if tokfile and tokfile.get("color", {}).get("accent", {}).get("$value"):
            fb = tokfile["color"]["accent"]["$value"]
        if fb:
            colors["accent"] = fb; source = "tokens"
        else:
            colors["accent"] = "#1E40AF"; source = "default"
    # fill gaps
    srcs = k.get("_srcs", {})
    defaults = {"ink": "#111111", "paper": "#F5F2EA"}
    out = {}
    for n in ("accent", "accent2", "ink", "paper"):
        v = colors.get(n)
        s = source
        if v is None and n == "accent2":
            continue
        if v is None:
            v, s = defaults[n], "default"
        if n == "accent2" and srcs.get(1):
            s = srcs[1]
        if n in ("ink", "paper") and source == "website" and colors.get(n):
            s = "website"
        elif n in ("ink", "paper") and source in ("footer", "logo") and colors.get(n):
            s = "footer" if A["footer"] else "logo"
        out[n] = (v.upper(), s)
    paper_rgb = unhex(out["paper"][0])
    ratio = contrast(unhex(out["accent"][0]), paper_rgb)
    fonts = DEFAULT_FONTS
    fsrc = "default"
    fnote = ""
    st = k["stills"]["primary"]
    if slug == "krystian-catala":
        fonts = ("Young Serif", "Instrument Sans"); fsrc = "graphic reels/clients/greenbrix/BRIEF.md"; fnote = "numbers and labels: Geist Mono"
    elif st in STYLE_FONTS:
        fonts = STYLE_FONTS[st][:2]; fsrc = f"roster style '{st}' (STYLES.md)"; fnote = STYLE_FONTS[st][2]
    elif slug == "kulbhushan-narang" and face_brand.get("fonts"):
        fonts = ("Inter", "Inter"); fsrc = "FACE_REELS_AGENT brand.json (Inter)"
    tok = {"$description": "Studio tokens (W3C DTCG style). logo.light = file to place on light backgrounds; logo.dark = file to place on dark backgrounds. "
                           "All colours provisional until the Desk writes kits/<slug>/confirm.json.",
           "color": {}, "font": {}, "logo": {}}
    for n, (v, s) in out.items():
        extra = {"contrastVsPaper": ratio} if n == "accent" else None
        if n == "accent" and palette:
            extra = dict(extra or {}, palette=palette)
        if ext_note and n == "accent":
            extra = dict(extra or {}, note=ext_note)
        tok["color"][n] = dtcg_color(v, s, provisional if s not in ("default",) else True, extra)
    tok["font"]["display"] = {"$type": "fontFamily", "$value": fonts[0], "$extensions": {"studio": {"source": fsrc}}}
    tok["font"]["body"] = {"$type": "fontFamily", "$value": fonts[1], "$extensions": {"studio": {"source": fsrc, **({"note": fnote} if fnote else {})}}}
    if (k.get("_web") or {}).get("fonts"):
        tok["font"]["display"]["$extensions"]["studio"]["websiteFonts"] = k["_web"]["fonts"]
    if k["stills"]["secondary"] in STYLE_FONTS:
        s2 = STYLE_FONTS[k["stills"]["secondary"]]
        tok["font"]["display"]["$extensions"]["studio"]["secondaryStyleFonts"] = [s2[0], s2[1]]
    # logos
    logos = A["logos"]
    lt = dk = None
    if k.get("extraLogos"):
        lt, dk = k["extraLogos"]["light"], k["extraLogos"]["dark"]
    else:
        light = [l for l in logos if logo_is_light(l)]
        dark = [l for l in logos if l not in light]
        lt = (dark or logos or [None])[0]
        dk = (light or logos or [None])[0]
    tok["logo"]["light"] = {"$type": "asset", "$value": lt}
    tok["logo"]["dark"] = {"$type": "asset", "$value": dk}
    if len(logos) == 1 and not k.get("extraLogos"):
        tok["logo"]["light"]["$extensions"] = tok["logo"]["dark"]["$extensions"] = {"studio": {"note": "single logo file; variant for the other background not supplied"}}
    k["_colors"] = out
    k["_ratio"] = ratio
    k["_csrc"] = source
    k["_provisional"] = provisional
    # colours count as filled only for real sources
    k["_colours_filled"] = good
    return tok

# --------------------------------------------------------------------------
# voice, history, lessons
# --------------------------------------------------------------------------
def voice_md(k):
    L = [f"# Voice: {k['name']}", ""]
    L += ["## Tone",
          "- Peer tone, plain words, jargon defined. Authority comes from correct math, not claims (PLAYBOOK rule 5).",
          "- Show the working for every number; label numbers as illustrative and date any rate.",
          "- Conditional language for outcomes: 'may', 'depending on your situation', 'subject to approval'.", ""]
    if k["id"] == "brian-wang":
        L += ["- Wealth coaching and life insurance voice. Not a mortgage broker: no mortgage-broker copy.",
              "- Every reel ends on his brand card with: \"For information only. Not investment advice.\"", ""]
    L += ["## Audience", k["audience"] or "- Not on file (listed as missing).", ""]
    L += ["## Languages", "- " + ", ".join(k["languages"])]
    if k["province"] == "QC":
        L.append("- Quebec client: French is REQUIRED for every piece (English alongside where the roster says en + fr).")
    L.append("")
    L += ["## Services"] + (["- " + s for s in k["services"]] if k["services"] else ["- Not on file (listed as missing)."]) + [""]
    L += ["## Banned (house rules, PLAYBOOK)", "Phrases (never write):"] + [f"- \"{p}\"" for p in BANNED_PHRASES]
    L += ["", "Patterns:"] + [f"- {p}" for p in BANNED_PATTERNS]
    L += ["", "Compliance language: " + ", ".join(f'"{x}"' for x in BANNED_COMPLIANCE) + ".",
          "Negation hooks only when the myth is widespread and a number is attached. Never copy hook-template wording.",
          "Sameness is the biggest AI tell: this client's version needs its own angle, hook and visual device, with at least two facts from the profile (communities, languages, niche, location).", ""]
    L += ["## Client rules (from the client's own requests)"]
    if k["rules"]:
        for r in k["rules"]:
            ap = ", ".join(r["appliesTo"])
            since = f" (since {r['since']})" if r["since"] else ""
            L.append(f"- [{r['kind']}] {r['text']}  Applies to: {ap}{since}.")
    else:
        L.append("- None on file.")
    L += ["", "## Compliance line",
          k["complianceLine"] or "- NOT AVAILABLE: facts missing. Do not post until supplied."]
    if k["id"] in ("kulbhushan-narang",):
        L += ["", "Reference: FACE_REELS_AGENT/clients/orbis-mortgage-group/voice.md (draft: calm, plain-spoken, educational, Canadian English)."]
    if k["id"] == "krystian-catala":
        L += ["", "Reference: graphic reels/clients/greenbrix/BRIEF.md (calm, expert, no-judgment, plain-spoken; never salesy; 'we look at', 'can', 'may'; no guarantees)."]
    L.append("")
    return "\n".join(L)

def write_history(d):
    p = d / "history.json"
    cur = jload(p)
    if isinstance(cur, dict) and cur.get("pieces"):
        return "kept"
    p.write_text(json.dumps({"pieces": [], "lastStyle": (cur or {}).get("lastStyle") if isinstance(cur, dict) else None}, indent=2) + "\n")
    return "written"

def write_lessons(d, name):
    p = d / "lessons.md"
    if not p.exists():
        p.write_text(f"# Lessons: {name}\n\nApproved lessons for this client. Empty until the library agent / Desk adds some.\n")

# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    KITS.mkdir(exist_ok=True)
    kits = []
    used_seed = set()
    for c in sheet:
        s = slug_of(c)
        sdslug = sheet_to_seed.get(s)
        if sdslug:
            used_seed.add(sdslug)
        kits.append(build_kit(s, c, sdslug))
    for s, e in EXTRAS.items():
        k = build_kit(s, None, e["seed"])
        k["_flags"].insert(0, "not in client sheet")
        kits.append(k)
    # brian-wang
    bw = {"id": "brian-wang"}
    kb = build_kit_brian = None

    # build brian manually via build_kit with synthetic client record
    brian = {"id": None, "name": "Brian Wang", "people": [], "emails": ["brian.wang@caliberwealthmanagement.ca"],
             "phones": ["(437) 425-2600"], "website": "", "location": "Toronto, Ontario", "brokerage_name": "Caliber Wealth Management",
             "brokerage_license_no": None, "agent_license_no": "#05089990", "designation": "Wealth Coach / Life Insurance Advisor",
             "other_ids": [], "time_zone": None, "posting_time": None, "posting_mode": None, "services": [],
             "special_requests": [], "photo_notes": None, "figma_file": None, "notes": [], "raw_client_details": "", "asset_folder": ""}
    k = build_kit("brian-wang", brian, None)
    k["sheetId"] = None
    k["_flags"].insert(0, "not in client sheet (task brief + brand card)")
    k["video"] = True
    k["_P"]["video"] = "task brief (footage reels allowed)"
    k["_missing"] = [m for m in k["_missing"] if not m.startswith("video")]
    k["_P"]["city"] = k["_P"]["province"] = "task brief (Toronto)"
    k["_P"]["name"] = "task brief"
    k["group"] = None
    kits.append(k)
    # fix brian P entries produced from the synthetic sheet record
    for kk in kits:
        for key in list(kk["_P"]):
            if kk["id"] == "brian-wang" and kk["_P"][key].startswith("clients.json"):
                kk["_P"][key] = "task brief"

    index = []
    report_rows = []
    for k in kits:
        slug = k["id"]
        d = KITS / slug
        d.mkdir(parents=True, exist_ok=True)
        web = jload(d / "web.json")
        if isinstance(web, dict):
            apply_web(k, web)
        tokfile = tokfiles.get(slug) or tokfiles.get((k["aliases"] or [None])[0])
        tok = make_tokens(k, tokfile)
        # colours missing?
        if not k["_colours_filled"]:
            k["_missing"].append("brand colours (accent is a placeholder; supply or confirm)")
        if k["_ratio"] < 3:
            k["_flags"].append(f"Accent {k['_colors']['accent'][0]} has contrast {k['_ratio']}:1 against paper (<3:1); pair with ink.")
        # provenance entries for colours/fonts
        P = k["_P"]
        for n, (v, s) in k["_colors"].items():
            P[f"colors.{n}"] = f"{s} (tokens.json)" if s != "default" else "default (no source)"
        P["colors.contrast"] = "computed (WCAG) accent vs paper"
        P["fonts"] = tok["font"]["display"]["$extensions"]["studio"]["source"]
        # completeness
        flds = {
            "name": bool(k["name"]), "city": bool(k["city"]), "province": bool(k["province"]),
            "group": k["group"] is not None, "brokerage.name": bool(k["brokerage"]["name"]),
            "brokerage.licence": bool(k["brokerage"]["licence"]), "agent.licence": bool(k["agent"]["licence"]),
            "photo": bool(k["assets"]["photo"]), "footer": bool(k["assets"]["footer"]),
            "logo": bool(k["assets"]["logos"]) or (slug == "brian-wang" and False),
            "colours": bool(k["_colours_filled"]), "complianceLine": bool(k["complianceLine"]),
        }
        keyf = list(KEYFIELDS)
        if k.get("_web") is not None:
            flds["socials"] = bool(k.get("socials")); flds["bio"] = bool(k.get("bio"))
            keyf += ["socials", "bio"]
        den = [f for f in keyf if f not in k["_na"]]
        comp = round(sum(1 for f in den if flds[f]) / len(den), 3)
        # provenance sanity: every filled key field must have provenance
        for f, ok in flds.items():
            if ok and f in ("name", "city", "province", "group", "brokerage.name", "brokerage.licence", "agent.licence"):
                if f not in P:
                    P[f] = "derived (see flags)"
        for key in ("photo", "footer"):
            if flds[key] and key not in P:
                P[key] = "assets/_provenance.json"
        if flds["logo"] and "logos" not in P:
            P["logos"] = "assets/_provenance.json"
        if flds["complianceLine"] and "complianceLine" not in P:
            P["complianceLine"] = "composed"
        # strip empties from provenance, de-dup lists
        P = {a: b for a, b in P.items() if b}
        flags = list(dict.fromkeys(k["_flags"]))
        missing = list(dict.fromkeys(k["_missing"]))
        kit = {
            "id": slug, "aliases": k["aliases"], "sheetId": k["sheetId"], "name": k["name"], "people": k["people"],
            "city": k["city"], "province": k["province"], "region": k["region"],
            "group": k["group"], "video": k["video"], "languages": k["languages"],
            "brokerage": k["brokerage"], "agent": k["agent"], "contact": k["contact"],
            "services": k["services"], "audience": k["audience"], "postingMode": k["postingMode"],
            "postingTime": k["postingTime"], "timeZone": k["timeZone"], "figma": k["figma"],
            "complianceLine": k["complianceLine"], "rules": k["rules"], "assets": k["assets"],
            "stills": k["stills"], "missing": missing, "flags": flags, "provenance": P,
            "completeness": comp, "updated": NOW,
        }
        for extra in ("faceReelsClient", "brandRefs", "extraLogos", "socials", "bio", "webBlock"):
            if extra in k:
                kit[extra] = k[extra]
        if "webBlock" in kit:
            kit["web"] = kit.pop("webBlock")
        kit["colorsProvisional"] = k["_provisional"]
        (d / "kit.json").write_text(json.dumps(kit, indent=2, ensure_ascii=False) + "\n")
        (d / "tokens.json").write_text(json.dumps(tok, indent=2, ensure_ascii=False) + "\n")
        (d / "voice.md").write_text(voice_md(k))
        write_history(d)
        write_lessons(d, k["name"])
        index.append({"slug": slug, "name": k["name"], "city": k["city"], "province": k["province"],
                      "group": k["group"], "completeness": comp, "flags": flags})
        k["_kit"] = kit; k["_comp"] = comp; k["_flds"] = flds
    (KITS / "_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    write_report(kits)
    write_contact(kits)
    avg = sum(k["_comp"] for k in kits) / len(kits)
    print(f"kits: {len(kits)}  average completeness: {avg:.1%}")

# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def write_report(kits):
    L = ["# Kit report", "", f"Generated {NOW} by studio/tools/build_kits.py. {len(kits)} kits.", ""]
    avg = sum(k["_comp"] for k in kits) / len(kits)
    L += [f"Average completeness: **{avg:.0%}**. Completeness = share of name, city, province, group, brokerage name, brokerage licence, agent licence, photo, footer, logo, colours, compliance line that are filled (photo is excluded where the client declines images; brokerage licence is excluded for Brian Wang).", "",
          "| Client | Slug | Completeness | Missing | Flags | Assets to confirm |", "|---|---|---|---|---|---|"]
    def esc(s):
        return s.replace("|", "/").replace("\n", " ")
    for k in sorted(kits, key=lambda k: k["_comp"]):
        kit = k["_kit"]
        L.append("| {} | {} | {:.0%} | {} | {} | {} |".format(
            esc(kit["name"]), kit["id"], k["_comp"],
            esc("; ".join(kit["missing"])) or "-",
            esc(" ; ".join(kit["flags"])) or "-",
            esc(", ".join(kit["assets"]["check"])) or "-"))
    # what user must supply
    L += ["", "## What the user must supply", ""]
    def names(cond):
        return ", ".join(k["_kit"]["name"] for k in kits if cond(k))
    L.append("1. **Brokerage name and licence for Ontario clients** (a compliance line cannot be built without them): " +
             (names(lambda k: not k["_kit"]["complianceLine"] and (k["_prov"] == "ON" or not k["_prov"])) or "none") + ".")
    L.append("2. **Agent licence numbers** still missing (not in the sheet, raw details or footer image): " +
             (names(lambda k: not k["_kit"]["agent"]["licence"]) or "none") + ".")
    L.append("3. **Groups** (no group in the calendar or roster, so no still style yet): " +
             (names(lambda k: k["_kit"]["group"] is None) or "none") + ".")
    L.append("4. **Brand colours**: every colour is extracted from footers/logos and marked provisional until confirmed in the Desk. No colours at all (placeholder accent only): " +
             (names(lambda k: not k["_colours_filled"]) or "none") + ".")
    L.append("5. **Cities / provinces** missing: " + (names(lambda k: not k["_kit"]["city"] or not k["_kit"]["province"]) or "none") + ".")
    L.append("6. **Assets to confirm** (provenance 'check'): " +
             "; ".join(f"{k['_kit']['name']}: {', '.join(k['_kit']['assets']['check'])}" for k in kits if k["_kit"]["assets"]["check"]) + ".")
    L.append("7. **Data conflicts to resolve** (see Flags column): Karven Wu (Barrie vs Richmond Hill; BMO vs Caliber), Rahul Vinod (Moncton NB vs North York ON), Keaton Thornton (footer licence #10530 vs sheet M22000917), Jalal Khan (licence typo?), Gaurav Makhija (edan vs GNE Mortgages), Nav Utppal (Next Mortgage vs FIDES), Jim DeCoste (licence labels), phone differences for Dan Balch and Akshat Chauhan.")
    L.append("8. **Vittorio Oliverio**: footers for Cara, Marty/Marry, Clarke, Karen, Kim (and David on hold); only his own footer exists. Confirm the current rotation (12 Sep 2025 request lists Cara, Marry, Clarke, Karen, Vittorio).")
    L.append("9. **Brian Wang**: standalone logo and photo files (they only exist inside the brand card); confirm the compliance wording for an insurance/wealth advisor.")
    L.append("10. **Audience** is empty for nearly every client (no source); services are missing for: " + (names(lambda k: not k["_kit"]["services"]) or "none") + ".")
    (KITS / "REPORT.md").write_text("\n".join(L) + "\n")

# --------------------------------------------------------------------------
# contact sheet
# --------------------------------------------------------------------------
def font(sz, bold=False):
    for p in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        try:
            return ImageFont.truetype(p, sz, index=1 if bold and p.endswith(".ttc") else 0)
        except Exception:
            continue
    return ImageFont.load_default()

def fit(im, w, h, bg=(235, 235, 235)):
    im = im.convert("RGBA")
    s = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2), im)
    return canvas

def write_contact(kits):
    RH, W = 132, 2000
    f1, f2, f3 = font(20, True), font(14), font(12)
    img = Image.new("RGB", (W, 60 + RH * len(kits)), (250, 250, 250))
    dr = ImageDraw.Draw(img)
    dr.text((16, 18), "Studio kits: name, footer, logo(s), photo, extracted colours (provisional) - %d kits" % len(kits), font=font(22, True), fill=(20, 20, 20))
    for i, k in enumerate(kits):
        y = 60 + i * RH
        kit = k["_kit"]
        dr.rectangle([0, y, W, y + RH - 2], fill=(255, 255, 255) if i % 2 == 0 else (244, 244, 244))
        dr.text((12, y + 10), kit["name"], font=f1, fill=(10, 10, 10))
        dr.text((12, y + 38), kit["id"], font=f2, fill=(90, 90, 90))
        g = "group " + str(kit["group"]) if kit["group"] is not None else "no group"
        dr.text((12, y + 58), f"{g} | {kit['province'] or '?'} | {k['_comp']:.0%}", font=f2, fill=(90, 90, 90))
        if kit["flags"]:
            dr.text((12, y + 80), f"{len(kit['flags'])} flags, {len(kit['missing'])} missing", font=f3, fill=(170, 60, 40))
        x = 250
        A = kit["assets"]
        def put(path, w, h, bg=(220, 220, 220)):
            nonlocal x
            if path and (R / path).exists():
                try:
                    img.paste(fit(Image.open(R / path), w, h, bg), (x, y + 6))
                except Exception:
                    dr.rectangle([x, y + 6, x + w, y + 6 + h], outline=(200, 0, 0))
            else:
                dr.rectangle([x, y + 6, x + w, y + 6 + h], outline=(190, 190, 190))
                dr.text((x + 8, y + 6 + h // 2 - 6), "none", font=f3, fill=(170, 170, 170))
            x += w + 10
        bgf = (30, 30, 30)
        put(A["footer"], 760, RH - 14, bgf)
        put(A["photo"], 110, RH - 14, (205, 205, 205))
        lp = A["logos"][:2]
        for j in range(2):
            put(lp[j] if j < len(lp) else None, 150, RH - 14, (160, 160, 160))
        # swatches
        cols = k["_colors"]
        for n in ("accent", "accent2", "ink", "paper"):
            if n in cols:
                hx = cols[n][0]
                dr.rectangle([x, y + 8, x + 62, y + 70], fill=unhex(hx), outline=(120, 120, 120))
                dr.text((x, y + 74), hx, font=f3, fill=(40, 40, 40))
                dr.text((x, y + 90), n + ("*" if not k["_colours_filled"] else ""), font=f3, fill=(120, 120, 120))
            x += 70
    img.save(KITS / "_contact.jpg", quality=88)

if __name__ == "__main__":
    main()
