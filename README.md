# Build your first Android app

[![Docs](https://img.shields.io/badge/docs-4%20guides-blue)](docs/)
[![Changelog](https://img.shields.io/badge/changelog-keep%20a%20changelog-orange)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **What's new?** See the [CHANGELOG](CHANGELOG.md) or the [Releases](https://github.com/productvida/build-your-first-android-app/releases).
> Want to add a scar of your own? [CONTRIBUTING.md](CONTRIBUTING.md).

A field-tested playbook for building and shipping **small, installable apps** — offline-first
web apps (PWAs) that you can wrap into real **Android/iOS store apps** — with **Claude Code** as
your pair-programmer.

It's the distilled "what worked / what we'd warn you about" from actually shipping one to
production: the architecture, the QA discipline that stops embarrassing bugs, the release
pipeline, and the **store + legal gotchas nobody tells you about** (yes, including the one where
the Play Store can publish your **home address**).

> This is a *guide + templates*, not a framework. No build step, no lock-in. Copy what helps.

## What this saves you
- 🏠 **Publishing your home address.** An *individual* Google Play account can show your personal address
  publicly on the listing. → [doc 03](docs/03-release-and-app-stores.md#part-b--google-play-gotchas)
- ⏳ **A two-week surprise.** New Play accounts must run a closed test (historically ~12 testers / ~14
  days) *before* you can even apply for production. → [doc 03](docs/03-release-and-app-stores.md#-the-timelines-that-surprise-people)
- 🐛 **"Works in my browser, dead on the phone."** Downloads, share, clipboard, notifications and more
  silently behave differently in the native WebView. → [doc 02](docs/02-qa-and-webview-gotchas.md)
- 🔙 **Back closing your whole app.** Chrome on Android **silently skips** history entries you pushed
  without user activation, and one edge swipe reaches your app **twice**. Cost us five wrong fixes.
  → [doc 02](docs/02-qa-and-webview-gotchas.md#the-back-navigation-trap-the-one-that-cost-us-five-attempts)
- 🔢 **Burning version numbers.** Play consumes a `versionCode` **on upload, permanently** — even for
  internal testing, even if you discard it. Upload to **internal testing first**, test the real signed
  build yourself, then promote. → [doc 03](docs/03-release-and-app-stores.md#-upload-to-internal-testing-first-then-promote)
- 📐 **The edge-to-edge advisory that won't go away.** Upgrading your status-bar plugin does **not** clear
  it; the deprecated calls are still in the bytecode. → [doc 03](docs/03-release-and-app-stores.md)
- 🚦 **A green gate that was actually red.** We piped our test gate into `grep` — and `grep` exits 0 when
  it finds the word "FAIL", so a failing build shipped. → [doc 04](docs/04-working-with-claude.md)
- 💾 **Silent data loss.** localStorage isn't durable (iOS evicts it after ~7 days of non-use) — ship an
  export/backup *if the data's worth keeping*. → [doc 01](docs/01-architecture.md)
- 🔒 **Privacy by default.** No backend = no sign-up, no account, nothing collected — the simplest, most
  honest privacy story. → [doc 01](docs/01-architecture.md)
- 🔗 **Sharing without a server.** Put the whole payload in the link/QR and decode it client-side — a
  share/growth loop with no backend, no accounts, no PII. → [doc 01](docs/01-architecture.md#sharing-without-a-backend-the-link-is-the-database)
- 🤖 **Reinventing the agent workflow every session.** A brief, skills, and a handoff doc. → [doc 04](docs/04-working-with-claude.md)

---

## Quickstart (5 minutes)
```bash
# 1. Get the playbook
git clone https://github.com/productvida/build-your-first-android-app.git

# 2. Start your app from the templates (the docs/ stay here as reference — you don't copy them)
mkdir my-app && cd my-app
cp ../build-your-first-android-app/CLAUDE.md .
cp ../build-your-first-android-app/templates/SESSION-STATE.md .
mkdir -p scripts && cp ../build-your-first-android-app/templates/qa_regression.py scripts/
mkdir -p .claude/skills && cp -r ../build-your-first-android-app/templates/.claude/skills/qa-gate .claude/skills/
```
3. **Fill in the `<PLACEHOLDERS>`** in `CLAUDE.md` (app name, one-line scope, file paths).
4. **Open Claude Code in `my-app/` and paste the first prompt:**
   > "Read my `CLAUDE.md`, and read the `docs/` in the build-your-first-android-app playbook for context.
   > Then propose a one-paragraph plan to scaffold the app — single-folder offline-first structure, a
   > service worker (cache-busting done right), a manifest, and a stub regression gate. Wait for my
   > go-ahead before writing code."
5. Build → **run the gate** → ship. Keep `SESSION-STATE.md` current so the next session starts oriented.

> **Placeholder convention:** anything in `<ANGLE_BRACKETS>` is a placeholder — search the repo for `<`
> and replace or delete it before you ship. Nothing in angle brackets should survive into your real project.

**In a hurry?** Read [doc 02](docs/02-qa-and-webview-gotchas.md) — it's the one that saves you from
shipping embarrassing bugs.

---

## The 60-second pitch of the approach
1. **Build offline-first, no framework, no build step.** One folder of HTML/CSS/JS + `localStorage`.
   It runs from a file, installs as a PWA, and works on a plane.
2. **Wrap it for the stores with Capacitor** *only when you need to* (push, share targets, store presence).
3. **Gate every release with an executable check** — because *"passes in the browser ≠ works in the native WebView."*
4. **Treat the AI agent as a teammate** with a written brief (`CLAUDE.md`), reusable skills, and a
   session-handoff doc so it picks up where it left off.

## What's inside

**📖 Read these (reference — you don't copy them):**
| Doc | What it gives you |
|---|---|
| [`docs/01-architecture.md`](docs/01-architecture.md) | The no-build, offline-first, single-folder architecture (+ the storage/backup traps) |
| [`docs/02-qa-and-webview-gotchas.md`](docs/02-qa-and-webview-gotchas.md) | The executable gate + the "breaks only in the native app" inventory |
| [`docs/03-release-and-app-stores.md`](docs/03-release-and-app-stores.md) | Release pipeline + Play/App Store gotchas (timelines, the address issue, legal) |
| [`docs/04-working-with-claude.md`](docs/04-working-with-claude.md) | Briefs, skills, session handoffs, working agreements |

*Read in order: Architecture → QA → Release → Working with Claude.*

**📋 Copy these into your project (then fill the `<PLACEHOLDERS>`):**
| File | What it is |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | A fill-in-the-blanks project brief your AI agent follows automatically |
| [`templates/qa_regression.py`](templates/qa_regression.py) | A regression-gate skeleton (Playwright) to adapt |
| [`templates/SESSION-STATE.md`](templates/SESSION-STATE.md) | A "read this first" session-handoff doc |
| [`templates/.claude/skills/qa-gate/`](templates/.claude/skills/qa-gate/) | A reusable "is it safe to ship?" agent skill (→ `.claude/skills/`) |

---

## The single most important habit
**Run an automated regression check before every store build, and verify the network/device paths
on a real device — not just in a desktop browser.** Most "it broke in production" bugs are things
that silently no-op inside the native WebView (downloads, share, clipboard, notifications) and look
perfectly fine in Chrome. See [`docs/02`](docs/02-qa-and-webview-gotchas.md).

## Contributing
Found a gotcha we missed — a new WebView trap, a store-policy change, a footgun? **Issues and PRs
welcome.** A living gotchas doc is only as good as the scars people add to it.

## License
MIT — see [LICENSE](LICENSE). Use it, fork it, no attribution required (but appreciated).

*Built from real shipping experience with Claude Code. Placeholders mark where your specifics go.*
