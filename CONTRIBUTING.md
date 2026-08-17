# Contributing

This playbook is a collection of **scars** — things that actually went wrong shipping a small app to
Google Play, written down so the next person doesn't pay for them twice. That shapes what belongs here.

## What makes a good contribution

**A specific thing that bit you, and what you'd do instead.** The bar is:

- ✅ **It happened.** You hit it on a real build, a real store submission, or a real device.
- ✅ **It was not obvious.** If the official docs say it plainly, link them instead of restating.
- ✅ **It has a concrete fix**, ideally a code snippet or a command someone can run.
- ✅ **It says how you'd verify** the fix — especially if a normal test cannot see the bug.

Anti-patterns for this repo:

- ❌ Generic best practice with no incident behind it ("write tests", "use TypeScript").
- ❌ Framework advocacy. This is deliberately no-build-step and no-lock-in.
- ❌ A wall of text where a table row would do.

## The most valuable contribution of all

**A gotcha where the normal test suite structurally cannot see the bug.** Those are the ones that cost
days. If you have one, say *why* the test can't see it — that reasoning is the useful part.

## How to contribute

1. Open an issue first for anything substantial, using the templates — it saves you writing something
   that's already covered elsewhere in the docs.
2. Small corrections: PR directly.
3. Put your change in the doc it belongs to (`docs/01`–`04`), and **add a line to
   [CHANGELOG.md](CHANGELOG.md)** under `[Unreleased]` so readers can see what's new.
4. If your fix is code, prefer a runnable snippet over prose.

## Style

- Lead with the failure, then the fix. People scan for the symptom they're seeing.
- Keep the "what this saves you" spirit: cost first, mechanism second.
- Tables for platform/behaviour differences, prose for reasoning.
- Link between docs rather than repeating.
- Mark uncertainty honestly. "We think, unverified" is more useful than false confidence — several
  entries here exist because someone was confident and wrong.

## Not accepting

Additions that require a backend, an account, or a build step to follow. The whole premise is that a
single-folder, offline-first app can reach a store, and the guidance has to stay usable at that scale.
