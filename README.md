# Ship small apps with Claude

A field-tested playbook for building and shipping **small, installable apps** — offline-first
web apps (PWAs) that you can wrap into real **Android/iOS store apps** — with **Claude Code** as
your pair-programmer.

It's the distilled "what worked / what we'd warn you about" from actually shipping one to
production: the architecture, the QA discipline that stops embarrassing bugs, the release
pipeline, and the **store + legal gotchas nobody tells you about** (yes, including the one where
the Play Store can publish your **home address**).

> This is a *guide + templates*, not a framework. No build step, no lock-in. Copy what helps.

---

## Who this is for
- Solo devs, freelancers, and small teams building a focused tool (tracker, flashcards, utility…).
- People using **Claude Code** (or any AI coding agent) who want a repo their agent can *read and follow*.
- Anyone who's been burned by "it worked in my browser but broke in the app."

## The 60-second pitch of the approach
1. **Build offline-first, no framework, no build step.** One folder of HTML/CSS/JS + `localStorage`.
   It runs from a file, installs as a PWA, and works on a plane.
2. **Wrap it for the stores with Capacitor** *only when you need to* (push, share targets, store presence).
3. **Gate every release with an executable check** — because *"passes in the browser ≠ works in the native WebView."*
4. **Treat the AI agent as a teammate** with a written brief (`CLAUDE.md`), reusable skills, and a
   session-handoff doc so it picks up where it left off.

---

## How to use this with Claude (the point)
1. **Copy `CLAUDE.md`** (the template here) into your new project and fill in the placeholders.
   Claude Code reads this file automatically and treats it as the project's rules.
2. Skim the **`docs/`** — they're written to be read by *you and your agent*. Tell Claude:
   > "Read `docs/` and `CLAUDE.md`, then help me scaffold the app described there."
3. Copy the **`templates/`** you want (the QA gate, the session-handoff doc) and adapt them.
4. Ship. Then keep `SESSION-STATE.md` updated so the next session (human or AI) starts oriented.

## What's inside
| Path | What it gives you |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | A fill-in-the-blanks project brief your AI agent follows |
| [`docs/01-architecture.md`](docs/01-architecture.md) | The no-build, offline-first, single-folder architecture |
| [`docs/02-qa-and-webview-gotchas.md`](docs/02-qa-and-webview-gotchas.md) | The executable gate + the "breaks only in the native app" inventory |
| [`docs/03-release-and-app-stores.md`](docs/03-release-and-app-stores.md) | Release pipeline + Play/App Store gotchas (timelines, the address issue) |
| [`docs/04-working-with-claude.md`](docs/04-working-with-claude.md) | Briefs, skills, session handoffs, working agreements |
| [`templates/qa_regression.py`](templates/qa_regression.py) | A regression-gate skeleton (Playwright) to adapt |
| [`templates/SESSION-STATE.md`](templates/SESSION-STATE.md) | A session-handoff doc template |

---

## The single most important habit
**Run an automated regression check before every store build, and verify the network/device paths
on a real device — not just in a desktop browser.** Most "it broke in production" bugs are things
that silently no-op inside the native WebView (downloads, share, clipboard, notifications) and look
perfectly fine in Chrome. See [`docs/02`](docs/02-qa-and-webview-gotchas.md).

## License
MIT — see [LICENSE](LICENSE). Use it, fork it, no attribution required (but appreciated).

*Built from real shipping experience with Claude Code. Placeholders mark where your specifics go.*
