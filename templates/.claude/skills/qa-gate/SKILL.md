---
name: qa-gate
description: Run the regression gate and the on-device checklist before any store build. Use before building or shipping, after any change touching network/device/system paths, or when asked to verify a release is safe.
---

# QA Gate

A reusable runbook so "is it safe to ship?" is answered the same way every time.

> Copy this into your repo at `.claude/skills/qa-gate/SKILL.md`. Add sibling skills the same way
> (e.g. `security-review`, `release`, `legal-review`) — each is a markdown playbook.

## When to use
- Before any store build or deploy.
- After any change touching the network, device, or system (downloads, share, clipboard,
  notifications, back button, deep links, CSP, auth).
- Whenever the human asks "is this safe to ship?"

## Steps
1. **Syntax-check** the changed files (e.g. `node -c app.js`).
2. **Run the executable gate:** `<command, e.g. python scripts/qa_regression.py>`. It must print
   `VERDICT: PASS`. If it fails, fix and re-run — do not proceed.
3. **Bump the service-worker cache version** if code changed.
4. **For network calls, prove the data landed** — read the row/file back independently. A 200 (or "no
   error") is not proof.
5. **On-device pass (the gate can't do this):** on a real phone, verify the WebView-divergent paths that
   this change could touch — downloads/share, notifications firing, the back button/gesture, deep links,
   TTS/audio. See `docs/02`.
6. **Add a new assertion to the gate** for anything that bit you, so it can't return.

## Output
Report: the gate verdict (paste it), what was checked on-device, and any new assertions added. If you
sampled/skipped anything, say so explicitly — don't let a green check imply coverage you didn't run.

> Reminder: a desktop-browser pass does NOT verify the native app. The two most expensive bug classes
> are (a) silently-failing WebView APIs and (b) swallowed network errors. This gate exists to catch both.
