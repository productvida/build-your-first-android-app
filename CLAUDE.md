# <YOUR_APP_NAME> — Project brief for the AI agent

> This file is read automatically by Claude Code. It's the source of truth for how to work in this
> repo. Keep it short and current. Replace every `<PLACEHOLDER>`. Delete guidance you don't need.

## What this is
<ONE-LINE DESCRIPTION — e.g. "An offline-first PWA for <doing X>. No backend, no account. Also
packaged as an Android app via Capacitor (appId `com.<you>.<app>`).">

## Where things live
```
<app>/            ← the app: index.html, app.js, app.css, sw.js, manifest.json, bundled data
<app>/index.html  ← entry point
scripts/          ← qa_regression.py (the gate), release pipeline
android/          ← Capacitor project — GITIGNORED, regenerated via `npx cap sync android`
.claude/skills/   ← reusable agent playbooks (qa, security, release)
SESSION-STATE.md  ← current status / handoff — read this FIRST
```

## Working agreements (the rules)
- **Never claim a change works without a passing test run.** Run the regression gate before saying "done".
- **A desktop-browser pass does NOT verify the native app.** Anything touching the network, device, or
  system (downloads, share, clipboard, notifications, back button, CSP) behaves differently inside the
  Capacitor WebView. Verify those on a real device, and for network calls **prove the data actually
  landed** — "no error thrown" is meaningless when errors are swallowed.
- **The regression gate is an executable gate, run it automatically.** `<command to run the gate>` must
  pass before any store build. Do this without being asked.
- **Bump the service-worker cache version after every code change** (so users get the update).
- **Agree on the approach before building.** One sentence on the plan, then wait for go-ahead.
- **Commit locally; push/deploy and store-upload only when asked.** Those are human-gated.
- **Keep `SESSION-STATE.md` current** so the next session starts oriented.
- **Syntax-check before testing** (e.g. `node -c app.js`).

## How to run / test locally
```
<how to serve the app locally — e.g. a tiny static server on an ephemeral port>
<how to run the gate — e.g. python scripts/qa_regression.py  → must print PASS>
```

## Stack & constraints
- No framework, no build step, vanilla JS. Data in `localStorage`; large reference data bundled as JSON.
- Offline-first: a service worker caches the shell + data.
- Native features via Capacitor plugins (only the ones you actually need).

## Positioning / scope (one line, keep it honest)
<WHAT THIS APP IS — AND WHAT IT IS NOT. Saying "not X" keeps scope from creeping.>
