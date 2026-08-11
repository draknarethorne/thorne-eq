# Thorne-EQ Tooling (`.bin`)

Automation and analysis scripts for the server-side project. Mirrors the Thorne-UI
philosophy: **auditors (read-only) first, operators (mutating) second**, with outputs
written to `.tmp/` and `.reports/` (git-ignored), never treated as source of truth.

> Hidden with a `.` prefix so it stays out of the way; run scripts from the repo root.

## Environment

| Script | Type | Purpose |
| --- | --- | --- |
| `check-environment.ps1` | read-only | Windows readiness check (Git, CMake, VS C++, MariaDB, Perl, Python). |
| `check-environment.sh` | read-only | Bash readiness check for Git Bash / WSL. |

### Usage

```powershell
# PowerShell (recommended on Windows)
pwsh -File .bin/check-environment.ps1

# JSON output (for tooling)
pwsh -File .bin/check-environment.ps1 -Json
```

```bash
# Git Bash / WSL
bash .bin/check-environment.sh
```

## Data / Schema analysis

| Script | Type | Purpose |
| --- | --- | --- |
| `schema_explore.py` | read-only | Inspect key tables (`skill_caps`, `spells_new`, `rule_values`, `data_buckets`) from a SQL dump dir or a live MariaDB. |

### Schema explorer usage

```bash
# Scan a SQL dump directory (no database needed)
python .bin/schema_explore.py --sql-dir C:/Code/server-src/utils/sql/database_full

# Inspect a live database (needs: pip install -r .bin/requirements.txt)
python .bin/schema_explore.py --db --database eqmac --user root
```

Environment variables (used when flags are omitted in `--db` mode):

- `THORNE_EQ_DB_HOST` (default `127.0.0.1`)
- `THORNE_EQ_DB_USER` (default `root`)
- `THORNE_EQ_DB_PASSWORD`
- `THORNE_EQ_DB_NAME` (default `eqmac`)

Outputs: `.tmp/schema_report.json` plus a console digest.

## Why these tables matter (Attunement system levers)

- `skill_caps` — per-class/skill/level caps; the "equalizer" lever we overlay with points.
- `spells_new` — `classes_1..16` min-level gating; the spell-line access lever.
- `rule_values` — feature flags for staged rollout.
- `data_buckets` — per-character allocation state.

See `.docs/DESIGN-SKILL-CAP-SYSTEM.md` for the full design these tools support.

## Conventions

- Read-only scripts are safe to run anytime.
- Never commit secrets; pass DB passwords via env vars or prompts, not files.
- Treat `.tmp/` and `.reports/` as disposable QA artifacts.
