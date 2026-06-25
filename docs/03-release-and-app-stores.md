# 03 · Releasing + the app-store gotchas nobody warns you about

Two parts: a **repeatable release pipeline**, and the **store realities** that cost people days (and
sometimes their privacy) because they found out too late.

> ⚠️ Store policies change constantly. Everything below is "what to check," not legal advice —
> **verify the current policy** on the Google Play / Apple developer sites before you rely on it.

---

## Part A — A repeatable release pipeline
Make releasing a **single boring script**, not a hand-run ritual you get wrong at midnight. The pipeline
should, in order:

1. **Bump the version in every place it lives, consistently.** A web/Capacitor app usually has the
   version in *three* spots: the web app (a JS constant + a `version.json`), and the native build file
   (`versionName` + an integer `versionCode` that must increase every upload). Keep them in lockstep.
2. **Require a human-written changelog entry first** — the script should refuse to build without it
   (the agent shouldn't invent release notes).
3. **Bump the service-worker cache version.**
4. **Sync the web assets into the native project** (`npx cap sync`).
5. **Run the regression gate — and ABORT the build if it fails.**
6. **Build + sign** the release artifact.
7. **Verify the artifact is actually signed**, then drop it somewhere obvious.
8. **Print the remaining HUMAN steps** — and stop. The script should **never** push git or upload to a
   store on its own. Those stay human-gated.

A skeleton is in [`../templates/`](../templates). Keep signing keys **out of the repo** (see `.gitignore`)
and document where they live separately.

### Web vs. app drift
Your **website/PWA auto-deploys** on push; your **store app only updates per build**. So the web is
often *ahead* of the shipped app. That's fine — just **track it** (in `SESSION-STATE.md`) and make sure
behavioral changes live in the folder that gets bundled into the app, so the next build catches up.

---

## Part B — Google Play gotchas

### 🏠 The big one: your personal/home address can be shown publicly
Google requires a verified developer identity and **displays developer contact details on the store
listing**. If you register as an **individual**, the address you provide can end up **publicly visible**
on your app's listing — for a freelancer working from home, that's your **home address on the internet**.

What to do:
- Consider registering as an **organization** (needs a D-U-N-S number) so a **business** name/address is
  shown instead of your personal one.
- Or use a **business address / virtual mailbox / PO-box-style address** you're comfortable being public.
- Decide this **before** you publish — changing developer identity later is painful.
- **Verify the exact current rules** (who-sees-what changes); this is the single most-overlooked privacy
  trap for solo publishers.

### ⏳ The timelines that surprise people
- **New personal developer accounts** must run a **closed test with a minimum number of testers
  (commonly ~12) for ~14 continuous days** *before* you can even apply for production access. That's a
  two-week gate **before** your first public launch — plan for it; recruit testers early.
- **Identity verification** of a new developer account can take days.
- **App review** ranges from hours to several days, and is typically **slowest on your first submission**
  and after big changes. Don't schedule a launch announcement for "the day I upload."
- **`versionCode` must strictly increase** every upload, or the upload is rejected.

### 📋 Data Safety form (must be accurate)
Play makes you declare what data you collect/share and why. **It must match reality** — if you later add
analytics, accounts, or email, **re-file it**. A false declaration is an enforcement/removal risk on your
only distribution channel. Keep it in sync with your privacy policy.

### 🗑️ Account/data deletion
If your app has accounts, Play requires a **working data-deletion path** (often a public URL). Build the
"delete my account/data" mechanism *before* you ship accounts, not after.

---

## Part C — Apple App Store (if/when you go there)
- A **paid developer program** membership is required; **Sign in with Apple** may be required if you offer
  any third-party/social login.
- Review tends to be stricter; "thin" wrapper apps and anything that looks like a website-in-a-box get
  scrutiny — make it feel like a real app (offline, native affordances).
- Same address/identity considerations apply for individuals vs. organizations.

---

## Part D — Privacy & legal hygiene (cheap insurance)
- **Collect as little as possible.** "Everything stays on the device" is the strongest, simplest privacy
  story — and a real asset if you're ever acquired (no data-liability mess).
- **Your privacy policy must match what the app actually does — today.** If you use *any* analytics, a
  feedback form, or third-party hosting, **disclose it** (name the processors, the data, the basis). The
  #1 legal risk for small apps is a policy that *misrepresents* (e.g. "we collect nothing" while running
  session-replay analytics).
- **In the EU**, analytics that set identifiers generally need **consent**; personal data has obligations
  (lawful basis, access, **deletion**, processor agreements, EU data residency). Email-only + magic-link
  is a clean, minimal posture if you must collect anything.
- **Attribution:** if you bundle open-data/dictionaries/assets under licenses like CC BY-SA, put a
  **user-visible credit** somewhere (about screen / policy).
- **User-generated content** that's shared to others needs **Terms of Service** (rights warranty, a
  takedown path, liability disclaimer) — get a lawyer for that and for any children's-audience question.
- **Anything material — a privacy policy rewrite, a ToS, children's-data handling — get a qualified
  lawyer to sign off.** AI is great for spotting issues and drafting; it is not your lawyer.
