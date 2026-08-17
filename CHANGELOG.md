# Changelog

All notable changes to this playbook are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) loosely — a **minor** bump means new guidance, a **patch**
means corrections and clarifications.

Every entry below came from actually shipping an app to Google Play, not from reading docs.

## [Unreleased]

## [1.0.0] — 2026-08-17

Renamed from `ship-small-apps-with-claude` to **`build-your-first-android-app`**, because that is what
people are actually searching for when they need this. The old URL redirects.
_(The approach still wraps to iOS — see doc 03 Part C — but the hard-won material is Play Store.)_

### Added
- **[doc 02] The back-navigation trap** — the half nobody documents, and the single most expensive lesson
  so far (**five wrong fixes** on a real device):
  - `pushState` **without user activation** is marked *skippable* by Chrome on Android, so re-arming
    inside a `popstate` handler silently breaks back. Fix: **one entry per layer, pushed at open time**.
  - On Android **one edge swipe reaches your app twice** (your `touchend` *and* the browser's back), so a
    single gesture closes two layers. De-dupe on **state, never a timer** — and register exactly one back
    path per platform.
  - **Why a headless-browser test cannot see it**: the intervention is activation-based and does not apply
    to synthetic navigation. Assert the *structural* property instead.
- **[doc 03] Upload to internal testing FIRST, then promote.** Instant, installs the real signed build on
  your own device, and you promote the artifact you already tested.
- **[doc 03] A `versionCode` is burned ON UPLOAD, permanently** — even for internal testing, even if you
  discard the draft. Every device-test cycle costs a code.
- **[doc 03] The edge-to-edge advisory (targetSdk 35+): upgrading your status-bar plugin does NOT clear
  it.** The deprecated calls remain in the bytecode. Remove the plugin, call `EdgeToEdge.enable()`, and
  verify with a `dex` scan. Includes two follow-on scars: call it **after** `super.onCreate()` when your
  framework swaps the Activity theme, and disable framework inset handling if you already use
  `env(safe-area-inset-*)`.
- **[doc 03] Don't advertise a new `versionCode` on the web before the build is live on Play** — your
  update check will point real users at a build that does not exist.
- **[doc 03] Put an Android emulator in the loop** (Play Store system image = real Chrome), with an honest
  statement of what it does *not* cover: OEM battery optimisation, real TTS voices, touch latency.
- **[doc 04] Make the gate structural, not disciplinary** — and the failure that prompted it: a build that
  **failed** the gate reached production because the gate was piped into `grep`, and **`grep` exits 0 when
  it finds the word "FAIL"**. Never pipe your gate; check the **exit code**.
- **[doc 04] Verify the agent's claims about your own codebase** — an adversarial review found five
  factual errors in one plan, each a `grep` away, including a named function that existed but was the
  wrong one.
- **[doc 04] Debug logs must outlive the crash they diagnose** — `sessionStorage` dies with the tab, so it
  only ever shows the steps *before* the failure. Use `localStorage`, opt-in, and remove it after.
- **`templates/install-git-hooks.sh`** — a pre-push hook that runs your gate by exit code, with a
  `SKIP_GATE=1` escape hatch and an automatic skip for docs-only pushes.
- **CHANGELOG.md, CONTRIBUTING.md, and issue templates**, so additions are visible and contributable.

### Changed
- README retitled, badges added, and a pointer to the changelog and releases.

## [0.3.0] — 2026-08-14

### Added
- Read the **native plugin's own source** before believing a plugin change works — traced end-to-end.
  A reminder "exact alarm" fix shipped without the Doze `allowWhileIdle` flag and was deferred overnight.
- **Never `git add -A` in a release script** — it sweeps in unrelated untracked files.

## [0.2.0] — 2026-07-02

### Added
- Lessons from shipping v1.1.x: **accountless sharing** (the link is the database), independent-agent
  review, entity/liability and consent gotchas, and spec-before-code.

## [0.1.0] — 2026-06-25

### Added
- Initial playbook and templates: architecture, QA and WebView gotchas, release and app stores, working
  with Claude. Privacy-by-default framing, backup guidance, and a note on using the right design tool.

[Unreleased]: https://github.com/productvida/build-your-first-android-app/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/productvida/build-your-first-android-app/releases/tag/v1.0.0
