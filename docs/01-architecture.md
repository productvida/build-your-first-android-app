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

> **When one file stops scaling:** "one `app.js`" is great to start, not forever. Past roughly **1–2k
> lines**, or when two features no longer fit in your head at once, split into a few plain `<script>`
> files or ES modules — **still no build step**. Don't let "one file is fine" become "one file forever."

## State & data
- **User data lives in `localStorage`** as JSON. Wrap it in a tiny `store.get/set` helper with try/catch.
- **Snapshot, don't reference.** When the user "saves" something derived from bundled data, copy the
  fields you need into their record. Later edits to the bundled data then can't corrupt old records.
- **Large reference data is bundled as JSON** and loaded once at boot (and cached by the SW). For big
  files, show a tiny loader while it parses — and keep the payload modest (a multi-MB JSON parsed at boot
  janks low-end phones; compress or lazy-load).
- Keep a **migration step** in your load function for when your data shape changes (e.g. rename a field).

> ⚠️ **localStorage is NOT durable storage — plan for loss.**
> - It's **~5 MB per origin** and **synchronous**; writes **throw** when you hit quota (so the "snapshot
>   into every record" habit above can blow up — catch it and surface the failure).
> - **iOS (WKWebView/Safari) evicts it after ~7 days of non-use**, and OS storage pressure can wipe it.
>   For a daily-use offline app, that means **users can lose their data**.
> - **Match the backup to the stakes — it's not always needed.** If losing the data would genuinely upset
>   the user (lessons they built, a journal, anything irreplaceable), **ship an export/import early**
>   (download a JSON, restore from it) — it's your backup story, migration path, and recovery when storage
>   is wiped. For a **throwaway or easily-recreated** utility (a calculator, a one-off converter), skip it.
> - When you outgrow a few MB or need structured/large data, **graduate to IndexedDB**.

## Offline-first (the service worker)
- Cache the shell (`index.html`, `app.js`, `app.css`, `manifest.json`) + your data file on install.
- **Bump a `CACHE` version constant on every change** and delete old caches on `activate`.
- **A version bump alone does NOT guarantee users get the update.** Two more things are required, and
  forgetting them is the #1 "my PWA won't update" footgun:
  1. **Serve `sw.js` with `Cache-Control: no-cache`** (never long-lived) — otherwise the browser's HTTP
     cache hands back the *old* service worker and users are stuck indefinitely.
  2. **Call `self.skipWaiting()` on install and `clients.claim()` on activate** (or prompt the user to
     reload), so the new worker takes over promptly instead of waiting for every tab to close.

## Rendering
- A single `render()` that rebuilds the screen from state is fine to start.
- For **frequent** interactions (toggles, deletes, drags), do **targeted DOM updates** instead of a full
  re-render — full re-renders cause flicker and lose scroll/focus.
- Keep design values as **CSS variables** (`--bg`, `--accent`, …) so theming is one place.
- **Never build DOM from untrusted strings with `innerHTML`.** Treat any **imported, shared, or
  user-entered** data as hostile — render it with `textContent`/`createElement`, or escape it. Importing a
  backup file or a shared item and `innerHTML`-ing its fields is a classic **stored-XSS** hole. (Add
  "import a malformed/hostile file" to your test habits — see `docs/02`.)

## Privacy by default (a feature, not an afterthought)
With this architecture, **the default is that you collect nothing** — **no sign-up, no account, no email,
no personal data ever leaves the device.** That's the strongest, simplest privacy story you can have (and
the easiest to be honest about in a privacy policy). Say it plainly in-app and in your store listing —
"no account, your data stays on your device" is a real differentiator. You only take on data collection,
and its obligations, **when you deliberately add a backend** (below) — so don't, until you must.

## When to add a backend (resist at first)
Start with **zero backend**. Everything local = no accounts, no privacy surface, no server bill, instant.
Add a backend only when a feature *requires* it (sync across devices, sharing between users, etc.).
When you do, keep it **optional and additive** — the app must still work offline without an account.
Treat that as the biggest architectural change you'll make and design it deliberately (and review the
security of any access-control / row-level rules — see `docs/02`).

## Sharing without a backend (the link *is* the database)
"Let two people share a thing" sounds like it needs a server. Often it doesn't. **Put the whole payload in
the URL `#fragment` and decode it client-side** — the link (and its QR) *is* the data. A tiny static page
renders a preview for people who don't have the app yet; people who do get it imported locally. Zero
hosting, zero accounts, **no personal data, and you never become a host of user content** (a real legal
line — see `docs/03`). The craft that makes it solid:
- **Nothing leaks.** The `#fragment` is never sent to the server — but a page can still read it, so
  **strip it with `history.replaceState` the instant you've decoded it**, and keep third-party analytics
  *off* that page. Then shared content truly never leaves the device.
- **One decoder, byte-identical**, shared by the app and the preview page — so a per-store app build and a
  per-push web page can't drift into "can't read each other's links." Version the payload (`v=1`) and
  evolve it **additive-only** (consumers ignore unknown keys).
- **Send only what can't be rebuilt.** Ship the user's edits/corrections verbatim; re-derive anything that
  comes from bundled data (e.g. dictionary defaults) on the other side. Smaller links, no lost corrections.
- **Fitting a QR:** compress (DEFLATE) and encode in the QR's **alphanumeric** alphabet (a URL-safe base
  like Base43) — roughly ~20% more capacity than base64-in-a-byte-stream. Anything that still won't fit →
  fall back to a **link only** (links carry any size); never emit an unscannable QR.

Reach for a real backend only when the feature *fundamentally* needs shared server state — multi-device
sync, revoke-after-send, per-recipient tracking — not just "exchange a thing between two devices."

## The principle
> Optimize for *changeability* and *shippability*, not for how impressive the stack looks.
> A boring, legible app you can ship and verify beats a clever one you can't.

---
[README](../README.md) · **01 Architecture** · [02 QA & WebView →](02-qa-and-webview-gotchas.md)
