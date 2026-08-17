#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Install this project's git hooks. Run once per clone:  bash scripts/install-git-hooks.sh
#
# WHY THIS EXISTS: a build that FAILED the regression gate reached
# production. The gate ran, was correct, and printed VERDICT: FAIL — but it had been
# chained into the commit with `&&` after a `grep`, and **grep exits 0 when it finds
# the word "FAIL"**. So a failing gate read as success and the push went out.
#
# Your gate is only a gate if it cannot be forgotten. Discipline alone is not enough. This makes it structural: pushing without a passing gate is not possible
# by accident.
#
# `.git/hooks/` is NOT versioned by git, which is why this installer lives in the
# repo — a fresh clone has no hooks until someone runs it.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
mkdir -p .git/hooks

cat > .git/hooks/pre-push <<'HOOK'
#!/usr/bin/env bash
# Pre-push gate. Installed by scripts/install-git-hooks.sh — do not edit here.
#
# If every push to main deploys (Netlify/Vercel/Pages), the gate must run BEFORE the
# push, not after. Checked by EXIT CODE and nothing else: never pipe the gate into
# grep/tee/head — a pipeline reports the exit status of the LAST command, which is
# exactly how a failing build once shipped.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

if [ "${SKIP_GATE:-}" = "1" ]; then
  echo "⚠️  pre-push: SKIP_GATE=1 — gate bypassed deliberately."
  exit 0
fi
# Docs-only pushes don't need the browser gate (it takes minutes).
CHANGED="$(git diff --name-only @{push}..HEAD 2>/dev/null || git diff --name-only origin/main..HEAD 2>/dev/null || true)"
if [ -n "$CHANGED" ] && ! echo "$CHANGED" | grep -qE '^(<your-app>/|scripts/qa_regression\.py)'; then
  echo "✔ pre-push: no app or gate changes in this push — skipping the regression gate."
  exit 0
fi
if [ ! -x .venv/bin/python ]; then
  echo "✗ pre-push: .venv/bin/python missing — cannot run the gate. Fix the venv or use SKIP_GATE=1."
  exit 1
fi

echo "▶ pre-push: running the regression gate (this takes a couple of minutes)…"
LOG="$(mktemp)"
.venv/bin/python scripts/qa_regression.py > "$LOG" 2>&1
RC=$?                      # <- the ONLY thing that decides. Never grep for this.
if [ $RC -ne 0 ]; then
  echo "✗ GATE FAILED — push aborted. The gate must pass before anything ships."
  grep -E "FAIL" "$LOG" | head -20
  echo "  full log: $LOG"
  exit 1
fi
tail -1 "$LOG"
rm -f "$LOG"
echo "✔ pre-push: gate passed."
exit 0
HOOK

chmod +x .git/hooks/pre-push
echo "✔ installed .git/hooks/pre-push (gate by exit code; SKIP_GATE=1 to bypass deliberately)"
