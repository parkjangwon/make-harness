#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
mode="${MAKE_HARNESS_HOOK_MODE:-strict}"

# Summary line shapes emitted by this hook:
# [make-harness] audit: pass
# [make-harness] done-gate: pass
# [make-harness] sensitive-change: pass

if [[ "$mode" == "off" ]]; then
  echo "[make-harness] hook mode=off, skipping harness checks"
  exit 0
fi

run_or_handle() {
  local label="$1"
  shift

  if "$@"; then
    echo "[make-harness] ${label}: pass"
    return 0
  fi

  if [[ "$mode" == "warn" ]]; then
    echo "[make-harness] ${label}: warn (continuing because MAKE_HARNESS_HOOK_MODE=warn)"
    return 0
  fi

  echo "[make-harness] ${label}: fail"
  return 1
}

run_or_handle "audit" python3 "$repo_root/tools/audit-harness.py" "$repo_root"
run_or_handle "done-gate" python3 "$repo_root/tools/check-harness-done.py" "$repo_root"

mapfile -t staged_files < <(git diff --cached --name-only --diff-filter=ACMR)
if [[ ${#staged_files[@]} -eq 0 ]]; then
  echo "[make-harness] sensitive-change: pass (no staged files)"
  exit 0
fi

if python3 "$repo_root/tools/check-sensitive-change.py" "$repo_root" --paths "${staged_files[@]}"; then
  echo "[make-harness] sensitive-change: pass"
  exit 0
fi

if [[ "$mode" == "warn" ]]; then
  echo "[make-harness] sensitive-change: warn (continuing because MAKE_HARNESS_HOOK_MODE=warn)"
  exit 0
fi

echo "[make-harness] sensitive-change: fail"
echo "[make-harness] review the staged diff, confirm the sensitive change, or relax the relevant rule_strengths if the project truly wants a softer default"
exit 1
