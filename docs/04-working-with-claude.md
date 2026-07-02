# 04 · Working with Claude Code (or any AI coding agent)

The agent is a teammate. Teammates do their best work with a **written brief, reusable playbooks, and a
handoff doc.** This is the lightweight system that made it productive instead of chaotic.

## 1. Give it a brief: `CLAUDE.md`
Claude Code reads `CLAUDE.md` automatically and treats it as the rules of the repo. Keep it **short and
current**. It should contain:
- **What the app is** (one line) and **where files live**.
- **Working agreements** — the non-negotiables (see below).
- **How to run and test** locally, and **how to run the gate**.
- **Scope** — and explicitly what the app is *not* (stops scope creep).

A fill-in template is in [`../CLAUDE.md`](../CLAUDE.md).

## 2. Working agreements that paid off
- **Never claim "done" without a passing test run.** This single rule prevents most regressions.
- **A browser pass ≠ the native app.** Verify device/network/system paths on a real device; **prove the
  data landed** (don't trust "no error").
- **Run the regression gate automatically before any build** — don't make the human ask.
- **Agree on the approach first** — one sentence, then wait for go-ahead. Cheap, avoids big wrong turns.
- **Spec before code for anything complex.** For a big feature, write the problem, the edge cases, and
  what's explicitly *out of scope* first, then let the agent plan against it. Small fixes skip this — but
  complex work built straight from a vague ask is exactly where rework hides.
- **You can't outsource direction.** The agent builds whatever you point it at — vague in, vague out.
  Deciding what you actually want (and debating it when you have an opinion) is *your* job; that's where
  the real thinking is, and it's the part that stays yours.
- **Bump the cache version after every change.**
- **Commit locally; pushing/deploying/store-uploading is human-gated.** The agent preps; you pull the trigger.
- **Bundle changes; don't deploy per tiny edit** (saves build minutes and noise).

## 3. Reusable skills / playbooks
Capture repeatable procedures as **skills** the agent can invoke — e.g. a **QA gate** runbook, a
**security review** checklist, a **release** procedure, a **legal/privacy** review. Each is just a
markdown playbook with: when to use it, the steps/checklist, and the output format. Benefits:
- Consistency (the security review checks the same things every time).
- You can run **adversarial / multi-angle reviews** (architecture, security, QA, legal) before building
  anything risky — and merge the findings.

A starter `qa-gate` skill folder is under [`../templates/.claude/skills/`](../templates/.claude/skills/).

## 4. The session-handoff doc: `SESSION-STATE.md`
AI sessions are stateless across days. A living **"read this first"** doc means every session — human or
AI — starts oriented instead of re-deriving context. Keep at the top:
- **What's shipped / live** (versions on web vs. the store).
- **What's in flight** (unpushed commits, pending builds).
- **What's next** + any **open decisions** waiting on you.
- **Backlog** of small fixes with enough detail to act cold.

Template: [`../templates/SESSION-STATE.md`](../templates/SESSION-STATE.md).

## 5. Verify, then trust
Have the agent **show its work**: run the gate and paste the verdict, screenshot the change, read the row
back from the server. "It should work" is not "it works." The whole system above exists to make
*verification cheap and automatic*, so "done" actually means done.

## 6. Let the gate teach the agent
When a bug slips through, don't just fix it — **add an assertion to the gate** so it can't return. Over
time your gate encodes everything that ever bit you, and the agent inherits that hard-won caution for free.

## 7. Use the right tool for the right job (incl. design)
The coding agent is great at logic, structure, and shipping discipline — it's not always the fastest way
to *design*. A pattern that works well: use an **AI design / mockup tool** (or a designer) to generate and
polish a **design system** — a coherent set of colors, type, spacing, and components — then **port the
tokens** into your no-build app as CSS variables (`--bg`, `--accent`, …) and have the coding agent wire
them in. You get a considered visual language without hand-tuning hex codes one screen at a time. Keep the
*tokens* as the single source of truth so design and code never drift. (Capture your own tool choices and
prompts in a doc in your repo so the next session reuses them.)

---

### A good first prompt to your agent
Run this from your **new app folder** (after you've copied in `CLAUDE.md` + `templates/` and filled the
placeholders). The `docs/` are reference — point the agent at this repo to read them, but you don't copy
them into your app.
> "Read my `CLAUDE.md`, and read the `docs/` in the ship-small-apps-with-claude playbook for context.
> Then propose a one-paragraph plan to scaffold the app described in `CLAUDE.md` — the single-folder
> offline-first structure, a service worker (with the cache-busting done right), a manifest, and a stub
> regression gate. Wait for my go-ahead before writing code."

---
[← 03 Release & app stores](03-release-and-app-stores.md) · **04 Working with Claude** · [README](../README.md)
