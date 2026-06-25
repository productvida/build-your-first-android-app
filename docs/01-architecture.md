# 01 · Architecture: no build, offline-first, one folder

The whole bet: **the simplest thing that can possibly work, and keep working offline.** No framework,
no bundler, no transpile step. This is *liberating* for a small app and makes the AI agent far more
effective (it can reason about the whole thing).

## The shape
```
<app>/
  index.html        ← loads app.css + app.js, mounts into a single root element
  app.js            ← all the logic (vanilla JS, no modules build — one file is fine to start)
  app.css           ← all the styles (design tokens as CSS variables)
  sw.js             ← service worker: caches the shell + data for offline
  manifest.json     ← PWA manifest (name, icons, display: standalone)
  data.json         ← any bundled reference data (dictionary, presets…) shipped with the app
  icons/            ← app icons
```

## Why no build step
- **Edit → refresh → see it.** No watch process, no broken toolchain at 2am.
- **The agent can hold it all in its head.** One `app.js` it can read end-to-end beats a maze of modules.
- **It deploys as static files** — any static host (Netlify/Cloudflare/GitHub Pages) works for free.
- You can always *graduate* later. You rarely need to.

## State & data
- **User data lives in `localStorage`** as JSON. Wrap it in a tiny `store.get/set` helper with try/catch.
- **Snapshot, don't reference.** When the user "saves" something derived from bundled data, copy the
  fields you need into their record. Later edits to the bundled data then can't corrupt old records.
- **Large reference data is bundled as JSON** and loaded once at boot (and cached by the SW). For big
  files, show a tiny loader while it parses.
- Keep a **migration step** in your load function for when your data shape changes (e.g. rename a field).

## Offline-first (the service worker)
- Cache the shell (`index.html`, `app.js`, `app.css`, `manifest.json`) + your data file on install.
- **Bump a `CACHE` version constant on every change** and delete old caches on `activate` — otherwise
  users get stale code. (Put "bump the cache" in your `CLAUDE.md` working agreements so it's automatic.)
- Network-first or cache-first is your call; cache-first with a version bump is simplest for a static app.

## Rendering
- A single `render()` that rebuilds the screen from state is fine to start.
- For **frequent** interactions (toggles, deletes, drags), do **targeted DOM updates** instead of a full
  re-render — full re-renders cause flicker and lose scroll/focus.
- Keep design values as **CSS variables** (`--bg`, `--accent`, …) so theming is one place.

## When to add a backend (resist at first)
Start with **zero backend**. Everything local = no accounts, no privacy surface, no server bill, instant.
Add a backend only when a feature *requires* it (sync across devices, sharing between users, etc.).
When you do, keep it **optional and additive** — the app must still work offline without an account.
Treat that as the biggest architectural change you'll make and design it deliberately (and review the
security of any row-level access rules — see `docs/02`).

## The principle
> Optimize for *changeability* and *shippability*, not for how impressive the stack looks.
> A boring, legible app you can ship and verify beats a clever one you can't.
