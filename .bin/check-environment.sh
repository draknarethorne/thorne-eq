#!/usr/bin/env bash
# Thorne-EQ local build environment readiness check (Bash / Git Bash / WSL).
# Read-only. Probes for Git, CMake (>=3.12), MariaDB client, Perl, Python.
# Note: Visual Studio detection is best-effort here; use check-environment.ps1
# on Windows for accurate VS C++ workload detection.

set -u

pass=0
fail=0

check() {
  local name="$1"; local required="$2"; local cmd="$3"; local hint="$4"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    ver="$("$cmd" --version 2>/dev/null | head -n1)"
    printf '  [ OK ]      %-22s %s\n' "$name" "$ver"
    pass=$((pass+1))
  else
    if [[ "$required" == "yes" ]]; then
      printf '  [MISSING]   %-22s %s\n' "$name" "$hint"
      fail=$((fail+1))
    else
      printf '  [optional]  %-22s %s\n' "$name" "$hint"
    fi
  fi
}

echo ""
echo "  Thorne-EQ Environment Readiness (bash)"
echo "  ======================================"

check "Git"        yes git    "https://git-scm.com/download/win"
check "CMake"      yes cmake  "https://cmake.org/download/ (>=3.12)"
check "MariaDB cli" yes mysql "https://mariadb.org/download/ (10.3.x)"
check "Perl"       yes perl   "https://strawberryperl.com/"
check "Python"     no  python "https://www.python.org/downloads/"

echo ""
if [[ "$fail" -gt 0 ]]; then
  echo "  Missing $fail required component(s). See hints above."
  echo "  On Windows, also run: pwsh -File .bin/check-environment.ps1"
  exit 1
else
  echo "  All required CLI components present."
  echo "  On Windows, confirm VS C++ via: pwsh -File .bin/check-environment.ps1"
  exit 0
fi
