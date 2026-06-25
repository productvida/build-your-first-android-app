# 02 · QA: the executable gate + the "only breaks in the app" inventory

This is the doc that saves you from shipping embarrassing bugs. **Read it twice.**

## The core lesson
> **Passing in a desktop browser does NOT mean it works in the native app.**

A wrapped web app runs inside a **WebView** (Android System WebView / iOS WKWebView), not Chrome. A
pile of web APIs **silently no-op or behave differently** there. They look perfect in your dev browser
and dead on a real phone — and you won't see it unless you test on a device.

## The WebView-divergent inventory (verify each on a real device)
| Web API / behavior | What goes wrong in the native WebView |
|---|---|
| `<a download>` / blob downloads | Usually does **nothing**. Write the file with a native filesystem plugin, then share it or save to a user folder. *(The highest-value row — this one bites everyone.)* |
| Web Share / `navigator.share` | May be missing or limited. Use the Capacitor Share plugin. |
| Clipboard | **Write** (`writeText`) usually works on a user gesture; **read** is the unreliable one — provide a fallback. |
| Speech synthesis / audio | Support **varies** — Android System WebView generally has `speechSynthesis`; **iOS WKWebView is the weak/async one** (voices load late). Test on-device or use a TTS plugin. |
| Notifications | Web Notifications don't fire reliably; use local-notification plugins (and request OS permission). |
| Back button / gesture | The hardware/gesture back may bypass web history and exit the app. Intercept it natively. |
| `fetch` + CSP | Your Content-Security-Policy applies in the WebView too — a missing host **silently blocks** requests. |
| `display-mode: standalone` / install prompts | Detecting "installed" differs; `beforeinstallprompt` never fires on iOS and some browsers, and won't fire once the app is already installed — don't show an "install me" hint based on its absence. |

**Rule of thumb:** if it touches the **network, the device, or the system**, assume it differs in the
WebView until you've seen it work on a phone.

## "Prove the data landed"
For any network call, **"no error was thrown" is worthless** — many failures are swallowed (CSP blocks,
`no-cors` requests, wrong access rules). Verify the *effect*: read the row back, confirm the file exists,
assert the item actually appears. If you can't observe the result, you haven't verified it.

## The executable gate (run before every store build)
Keep a single script that drives the **real app in a real browser** and asserts the core flows still
work. Make it print a clear `VERDICT: PASS` / `FAIL`, and **run it automatically before any build** —
put that in your `CLAUDE.md` working agreements so the agent does it without being asked.

A good gate mixes:
- **Static checks** on the source — but make them *real*, not vibes. `"download" in source` only proves a
  substring exists, not that the download is correctly guarded; that's a heuristic, **not** verification.
  Prefer asserting actual structure, and label any heuristic as a heuristic. (The skeleton's static
  examples are deliberately marked this way.)
- **Live checks** in a headless browser (boot the app, exercise the main loop, assert outcomes).
- **A real round-trip** for anything that writes to a server (insert → read it back).

A skeleton you can adapt is in [`../templates/qa_regression.py`](../templates/qa_regression.py).

**Every finding that bites you should become a new assertion in the gate** — that's how the gate gets
smarter than you are and stops the same class of bug from returning.

## Catch errors in production (you have no console on a user's phone)
A no-backend app still fails in the field — and swallowed errors (the villain above) are invisible there.
Add a global `window.onerror` + `unhandledrejection` handler that **surfaces failures to the user**
(a toast, a retry) and optionally a privacy-respecting, opt-in error log. Otherwise "it just didn't work"
is all you'll ever hear.

## The on-device pass (the part the gate can't do)
Before you trust a store build, do a **manual pass on a physical device** for exactly the
WebView-divergent things above: downloads/share, notifications firing, the back button, deep links,
TTS/audio, importing a backup. The gate runs a desktop browser and *structurally cannot* see these.

## Multi-angle review (optional but powerful)
For anything risky (a new backend, auth, sharing user content), review the design from several lenses
*before building*: **architecture, security, QA, and legal**. With an AI agent you can run each as a
separate focused pass and merge the findings. The security one alone routinely catches real holes (e.g. an
over-permissive **access-control rule** that exposes everyone's data, or a public client key doing
privileged things).

## Don't silently cap coverage
If a check samples, truncates, or skips something, **say so** in the output (and prefer a *failing*
"not configured yet" check over a silent skip). A green check that quietly tested 3 of 50 cases — or
nothing at all — reads as "all good" when it isn't.

---
[← 01 Architecture](01-architecture.md) · **02 QA & WebView** · [03 Release & app stores →](03-release-and-app-stores.md)
