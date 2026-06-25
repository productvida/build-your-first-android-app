#!/usr/bin/env python3
"""
Regression GATE skeleton — adapt to your app.

Goal: prove the core flows still work, in a REAL browser, before every store build.
Prints `VERDICT: PASS` / `VERDICT: FAIL`. Wire it into your release pipeline so the build
ABORTS on FAIL. Add an assertion for every bug that ever bit you.

Setup (once):
    python -m venv .venv && . .venv/bin/activate
    pip install playwright && playwright install chromium

Run:
    python scripts/qa_regression.py
"""
import http.server, threading, time, json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP  = ROOT / "<app>"                      # <-- folder that holds index.html / app.js
APPJS = (APP / "app.js").read_text()

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

# ── 1. STATIC checks on the source (fast, catch whole classes of bug) ──────────
# NOTE: substring presence is a HEURISTIC, not proof. "download" in source does not prove the
# download is correctly guarded — real verification is the live check + the on-device pass.
# Label heuristics honestly so a green run never implies coverage you didn't actually run.
check("[heuristic] source mentions a native-vs-web branch for downloads",
      "isNativePlatform" in APPJS and "download" in APPJS,
      "blob <a download> silently fails in the WebView — verify the native branch for real on a device")

# CSP must allow every external host the app calls (a missing one silently blocks fetch in the WebView).
# Make the "not configured yet" state VISIBLE — fail it rather than skipping silently.
csp = (APP / "index.html").read_text()
HOSTS = []  # <-- list every external host your app calls, e.g. ["api.example.com"]
if not HOSTS:
    check("CSP host check is configured", False, "list your hosts in HOSTS[] to enable this check")
for host in HOSTS:
    check(f"CSP allows {host}", host in csp, "a missing host silently blocks fetch in the WebView")

# No privileged/secret keys in the client (only public/anon keys may ship).
check("no obvious secret keys committed in the client",
      "service_role" not in APPJS and "secret_key" not in APPJS, "ship only public/anon keys client-side")

# ── 2. LIVE checks: drive the real app in a headless browser ───────────────────
import os
os.chdir(APP)
httpd = http.server.HTTPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.4)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="domcontentloaded")
        pg.wait_for_timeout(2000)              # let the app boot / parse bundled data
        check("no JS error on load", len(errs) == 0, "; ".join(errs))

        # --- your core-loop assertions go here ---
        # Example pattern: set state, render, assert the DOM/result.
        # ok = pg.evaluate("() => { /* exercise a flow */ return true; }")
        # check("core: <the main thing your app does> works", ok)

        # --- "prove the data landed" pattern (if you have a backend) ---
        # Insert a row via the app, then INDEPENDENTLY read it back and assert it exists.
        # A 200 response is NOT proof.

        b.close()
except Exception as e:
    check("in-app browser run", False, str(e))
finally:
    httpd.shutdown()

# ── 3. REPORT ──────────────────────────────────────────────────────────────────
print("\nREGRESSION GATE\n" + "=" * 40)
fails = 0
for name, ok, detail in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if (not ok and detail) else ""))
    fails += 0 if ok else 1
print("=" * 40)
if fails:
    print(f"VERDICT: FAIL ({fails} issue{'s' if fails != 1 else ''}) — DO NOT BUILD/SHIP")
    sys.exit(1)
print("VERDICT: PASS — safe to build")
