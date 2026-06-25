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
| `<a download>` / blob downloads | Often does nothing. Use the native filesystem + share, or write to a user folder. |
| Web Share / `navigator.share` | May be missing or limited. Use the Capacitor Share plugin. |
| Clipboard (`navigator.clipboard`) | Can silently fail. Provide a fallback / use a plugin. |
| Speech synthesis / audio | The Web Speech API is often absent. Use a TTS plugin. |
| Notifications | Web Notifications don't fire reliably; use local-notification plugins (and request OS permission). |
| Back button / gesture | The hardware/gesture back may bypass web history and exit the app. Intercept it natively. |
| `fetch` + CSP | Your Content-Security-Policy applies in the WebView too — a missing host silently blocks requests. |
| `display-mode: standalone` | Detecting "installed" differs; some install prompts (`beforeinstallprompt`) never fire on iOS / some browsers. |

**Rule of thumb:** if it touches the **network, the device, or the system**, assume it differs in the
WebView until you've seen it work on a phone.

## "Prove the data landed"
For any network call, **"no error was thrown" is worthless** — many failures are swallowed (CSP blocks,
`no-cors` requests, wrong RLS). Verify the *effect*: read the row back, confirm the file exists, assert
the item actually appears. If you can't observe the result, you haven't verified it.

## The executable gate (run before every store build)
Keep a single script that drives the **real app in a real browser** and asserts the core flows still
work. Make it print a clear `VERDICT: PASS` / `FAIL`, and **run it automatically before any build** —
put that in your `CLAUDE.md` working agreements so the agent does it without being asked.

A good gate mixes:
- **Static checks** on the source (e.g. "the download path is guarded by a native branch", "the CSP
  includes every host we call", "no secret keys are present").
- **Live checks** in a headless browser (boot the app, exercise the main loop, assert outcomes).
- **A real round-trip** for anything that writes to a server (insert → read it back).

A skeleton you can adapt is in [`../templates/qa_regression.py`](../templates/qa_regression.py).

**Every finding that bites you should become a new assertion in the gate** — that's how the gate gets
smarter than you are and stops the same class of bug from returning.

## The on-device pass (the part the gate can't do)
Before you trust a store build, do a **manual pass on a physical device** for exactly the
WebView-divergent things above: downloads/share, notifications firing, the back button, deep links,
TTS/audio. The gate runs a desktop browser and *structurally cannot* see these.

## Multi-angle review (optional but powerful)
For anything risky (a new backend, auth, sharing user content), it pays to review the design from
several lenses *before building*: **architecture, security, QA, and legal**. With an AI agent you can
literally run each as a separate focused pass and merge the findings. The security one alone routinely
catches real holes (e.g. an over-permissive database read rule that exposes everyone's data).

## Don't silently cap coverage
If a check samples, truncates, or skips something, **say so** in the output. A green check that quietly
tested 3 of 50 cases reads as "all good" when it isn't.
