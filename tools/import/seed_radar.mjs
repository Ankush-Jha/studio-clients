#!/usr/bin/env node
// Build radar/accounts.json and radar/posts.jsonl (source "landscape") from the content-desk research files.
// Reads only. Item dates are the item's own date; never the fetch time.
import fs from 'node:fs';
import path from 'node:path';
import { CD, ACCOUNTS, readAccounts, writeAccounts, readPosts, writePosts, upsert, blankPost, postId, platformOf, normUrl, ytId, num, isMain, recomputeOutliers } from './lib.mjs';

const RES = path.join(CD, 'research');
const jread = (f) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return null; } };
const runDirs = () => { try { return fs.readdirSync(path.join(CD, 'runs'), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort(); } catch { return []; } };

function handleOf(a) {
  let h = a.handle;
  if (h && typeof h === 'object') h = h.handle || h.instagram || h.value || Object.values(h).find((v) => typeof v === 'string') || null;
  if (typeof h === 'string' && h) return h;
  const m = (a.url || '').match(/(?:youtube\.com|tiktok\.com|instagram\.com)\/(@?[\w.-]+|channel\/[\w-]+)/);
  if (m && !/^(channel|watch)$/.test(m[1])) return m[1].replace('channel/', '');
  if (m) return m[1].replace('channel/', '');
  try { return new URL(a.url).hostname.replace(/^www\./, ''); } catch { return null; }
}
function followersText(a) {
  const f = a.followers;
  if (!f) return '';
  if (typeof f === 'object') return Object.values(f).filter((v) => typeof v === 'string').join('; ');
  return String(f);
}

export async function seed({ force = false } = {}) {
  const files = [path.join(RES, 'landscape_2026-11-19.json'), path.join(RES, 'landscape_merged.json'), path.join(RES, 'landscape_tt_yt.json'), path.join(RES, 'landscape_ig_fb.json'), path.join(RES, 'landscape_industry.json')];
  const accMap = new Map();
  for (const f of files) {
    const j = jread(f); if (!j?.accounts) continue;
    for (const a of j.accounts) if (!accMap.has(a.id)) accMap.set(a.id, a);
  }
  const existing = readAccounts();
  const have = new Map(existing.map((a) => [a.id, a]));
  for (const a of accMap.values()) {
    if (have.has(a.id)) continue; // never overwrite manual edits / API-resolved fields
    have.set(a.id, {
      id: a.id, name: a.name, handle: handleOf(a), platform: a.platform, url: a.url, region: a.region || '', type: a.type || '',
      followers: followersText(a), watchFor: [...(a.pillars || []), ...(a.formats || [])], source: 'landscape', active: true,
    });
  }
  const accounts = [...have.values()];
  writeAccounts(accounts);

  // ---- posts ----
  const posts = readPosts();
  const stats = { added: 0, updated: 0 };
  const add = (rec) => { const r = upsert(posts, rec); stats[r]++; };
  const isConcrete = (u) => {
    let x; try { x = new URL(u); } catch { return false; }
    if (/(^|\.)(x|twitter|reddit|threads)\.(com|net)$/i.test(x.hostname)) return false; // not collected: platform enum has no X/Reddit
    const p = platformOf(u);
    if (p === 'youtube') return !!ytId(u);
    if (p === 'tiktok') return /\/video\/\d+/.test(x.pathname);
    if (p === 'instagram') return /\/(p|reel|reels|tv)\/[\w-]+/.test(x.pathname);
    if (p === 'facebook' || p === 'linkedin') return /\/(posts|videos|reel|watch|permalink|feed\/update|pulse)/.test(x.pathname) || x.searchParams.has('story_fbid');
    return x.pathname.replace(/\/+$/, '').length > 1; // web: not a bare homepage
  };
  const fmtOf = (u) => {
    const p = platformOf(u);
    if (p === 'youtube') return /\/shorts\//.test(u) ? 'short' : 'video';
    if (p === 'tiktok') return 'video';
    if (p === 'instagram') return /\/reel/.test(u) ? 'reel' : 'image';
    if (p === 'web') return 'article';
    return null;
  };
  const accByHandle = (u) => {
    const m = u.match(/tiktok\.com\/(@[\w.]+)\//i) || u.match(/youtube\.com\/(@[\w.-]+)/i);
    if (!m) return null;
    return accounts.find((a) => a.handle && a.handle.toLowerCase() === m[1].toLowerCase())?.id || null;
  };
  const ytAccount = new Map(); // video url -> account id (from raw_video)
  const mk = (o) => {
    const url = o.url;
    const rec = blankPost({ url, account: o.account || accByHandle(url) || ytAccount.get(normUrl(url)) || null, date: o.date || null, format: fmtOf(url),
      caption: o.caption || '', hook: o.hook || '', metrics: o.metrics || {}, outlier: o.outlier ?? null, source: 'landscape', confidence: 'check' });
    if (o.outlier != null) rec.outlierBasis = 'stated';
    if (o.title) rec.title = o.title;
    return rec;
  };

  // 1. raw_video.json from every run (old to new, so the newest views win)
  for (const d of runDirs()) {
    const rv = jread(path.join(CD, 'runs', d, 'raw_video.json')); if (!rv) continue;
    for (const ch of rv.channels || []) for (const u of ch.uploads || []) {
      if (!u.url) continue;
      ytAccount.set(normUrl(u.url), ch.id);
      add(mk({ url: u.url, account: ch.id, date: u.date, title: u.title, caption: u.title, hook: u.title, metrics: { views: num(u.views) } }));
    }
    for (const u of rv.topVideos || []) if (u.url) add(mk({ url: u.url, date: u.date, title: u.title, caption: u.title, hook: u.title, metrics: { views: num(u.views) } }));
  }

  // 2. landscape files (research + runs): standout items, then pattern evidence
  const lfiles = [];
  for (const f of fs.readdirSync(RES).filter((n) => /^landscape.*\.json$/.test(n))) lfiles.push(path.join(RES, f));
  for (const d of runDirs()) for (const f of fs.existsSync(path.join(CD, 'runs', d)) ? fs.readdirSync(path.join(CD, 'runs', d)).filter((n) => /^landscape.*\.json$/.test(n)) : []) lfiles.push(path.join(CD, 'runs', d, f));
  lfiles.sort((a, b) => (path.basename(a).match(/\d{4}-\d\d-\d\d/)?.[0] || '0').localeCompare(path.basename(b).match(/\d{4}-\d\d-\d\d/)?.[0] || '0'));
  for (const f of lfiles) {
    const j = jread(f); if (!j) continue;
    for (const a of j.accounts || []) for (const s of a.standout || []) {
      if (!s.url || !isConcrete(s.url)) continue;
      const what = s.what || '';
      const mult = what.match(/(\d+(?:\.\d+)?)\s*x\b(?!\d)/i);
      const views = s.views != null ? num(s.views) : (what.match(/([\d,.]+\s*[KkMm]?)\s+views/) ? num(what.match(/([\d,.]+\s*[KkMm]?)\s+views/)[1]) : null);
      const q = what.match(/"([^"]{4,120})"|“([^”]{4,120})”|(?:^|[\s(])['‘]([^'’]{4,120}?)['’](?=[\s.,:;)?!]|$)/); const qt = q ? (q[1] || q[2] || q[3]) : '';
      add(mk({ url: s.url, account: a.id, date: s.date, caption: what, hook: qt, metrics: views != null ? { views } : {}, outlier: mult ? parseFloat(mult[1]) : null, title: platformOf(s.url) === 'web' ? undefined : (qt || undefined) }));
    }
    for (const p of j.patterns || []) for (const u of p.evidence || []) {
      if (typeof u !== 'string' || !/^https?:/.test(u) || !isConcrete(u)) continue;
      add(mk({ url: u, caption: '', hook: '' }));
    }
  }

  // 3. sweep: any other concrete YouTube/TikTok/Instagram post URL in research + run json files
  const sweepFiles = fs.readdirSync(RES).filter((n) => n.endsWith('.json')).map((n) => path.join(RES, n));
  for (const d of runDirs()) for (const n of fs.readdirSync(path.join(CD, 'runs', d))) if (/^(raw_|research_|landscape_|browser_|weekly_).*\.json$/.test(n)) sweepFiles.push(path.join(CD, 'runs', d, n));
  const re = /https?:\/\/(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)[\w-]{6,}|youtu\.be\/[\w-]{6,}|tiktok\.com\/@[\w.]+\/video\/\d+|instagram\.com\/(?:p|reel)\/[\w-]+)/g;
  for (const f of sweepFiles) {
    let txt; try { txt = fs.readFileSync(f, 'utf8'); } catch { continue; }
    for (const u of new Set(txt.match(re) || [])) add(mk({ url: u }));
  }
  // drop YouTube/TikTok posts with no date and no title? keep: oEmbed adds title; date stays null (unknown)
  recomputeOutliers(posts);
  writePosts(posts);
  return { accounts: accounts.length, posts: posts.length, ...stats };
}

if (isMain(import.meta)) seed().then((r) => console.log(JSON.stringify(r)));
