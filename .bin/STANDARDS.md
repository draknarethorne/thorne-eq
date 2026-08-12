# Script Standards — Thorne-EQ

Conventions for every operational script in `.bin/`. The prime directive of this
repo is **rebuild-from-scratch**: nothing about the running server should exist
only in someone's head. Every setup, migration, and fix is a tracked, re-runnable
script. These standards keep that promise enforceable.

---

## Guiding Principles

1. **Rebuildable.** If a step can't be re-run from a clean checkout, it isn't done.
   Encode it in a script + tracked SQL/JSON/template, not a manual edit.
2. **Server-authoritative, reversible.** Prefer idempotent, one-shot, forward-
   migratable operations. Back up before you mutate (`.reports/*.json` snapshots).
3. **Discoverable.** A newcomer finds the right command from `--help` and
   `.bin/README.md` without reading source.
4. **Consistent.** Predictable naming, argument style, and output locations across
   every script.
5. **Safe by default.** No secrets in tracked files. Destructive commands
   (`reset`, `revoke`, `shutdown`) confirm intent or require an explicit flag.

---

## Naming & Pairing

| Rule | Convention | Example |
| ---- | ---------- | ------- |
| Script name | `verb_noun.py` (snake_case) | `manage_database.py`, `flag_multiclass.py` |
| Launcher | matching `.bat` next to every `.py` | `manage_database.bat` |
| Launcher behavior | prefer `.venv` Python, fall back to `python` | (see any `.bat`) |
| PowerShell/shell | `snake_case.ps1` / `.sh` | `check_environment.ps1` |
| Disposable output | `.tmp/` (scratch) and `.reports/` (kept artifacts) | `.reports/flag_multiclass_*.json` |

Both files ship together. A `.py` without its `.bat` is incomplete.

---

## Argument Style

All Python scripts use **`argparse` with subcommands** — this gives `--help` for
free at both levels and keeps a single script per domain (one operator, many verbs)
rather than a sprawl of one-off files.

```bash
manage_database.bat --help            # lists subcommands
manage_database.bat import --help     # options for one subcommand
```

- Every subcommand has a one-line `help=` string.
- Destructive verbs take an explicit guard (a `--yes`/`--force` flag or a typed
  confirmation) — never destroy on a bare invocation.
- Long-form `--flags` for anything optional; positionals only for the obvious
  primary argument.

---

## Classification & Documentation

### Simple scripts

Single purpose, read-only or low-risk, few options.

- **Documented in:** `.bin/README.md` (one entry + a quick example).
- **Examples:** `schema_explore.py` (read-only DB explorer),
  `check_environment.ps1` (readiness check).

```markdown
**schema_explore.py** — Read-only schema/table explorer.

​```bash
schema_explore.bat --db quarm --table spells_new
​```
For options: `schema_explore.bat --help`
```

### Complex scripts

Multiple workflows, subcommands, or workflow-critical. These carry real
operational knowledge (import quirks, launcher pool, DLL assembly).

- **Documented in:** a dedicated `.bin/<script_name>.md` **and** a summary entry in
  `.bin/README.md` that links to it.
- **Examples:** `control_server.py` (orchestrator: mariadb/assemble/start/stop/
  shutdown/status), `manage_database.py` (status/import/reset/backup/gm/query/
  repair/bootstrap), `compare_classes.py`, `flag_multiclass.py`.

Dedicated `.md` structure:

```markdown
# <script_name>.py

One-paragraph overview.

## Overview          — what it does, when to use it
## Quick Start       — the single most common command
## Subcommands       — each verb with options
## How It Works      — the non-obvious knowledge it encodes
## Troubleshooting   — known failure modes + fixes
```

---

## Encode the Knowledge, Not Just the Command

A script's real value is the hard-won detail it captures so we never rediscover it.
When a command exists only because of an environment quirk, **document the why** in
the script's `.md` (or a comment). Current examples worth preserving:

- `manage_database.py import` — strips MariaDB sandbox-header lines, pipes files
  (batch) instead of `SOURCE`, renames colon filenames.
- `control_server.py assemble` — copies `zlib-ng1.dll` from built libs because
  `zone.exe` needs it (world/login use plain `zlib1.dll`).
- `control_server.py start` — zones boot via the `eqlaunch` launcher pool
  (`dynzone1`), not standalone; `shared_memory` runs to completion first.
- `control_server.py shutdown` — graceful MariaDB stop via `mysqladmin` to avoid
  crashed MyISAM tables.

---

## Checklist for a New Script

- [ ] `verb_noun.py` + matching `.bat` launcher (prefers `.venv`).
- [ ] `argparse`; every subcommand has `help=`; `--help` verified.
- [ ] Destructive verbs guarded; mutations back up to `.reports/` first.
- [ ] Output goes to `.tmp/` or `.reports/` (both gitignored) — never scattered.
- [ ] No secrets; DB creds from env/local ignored config.
- [ ] Documented: simple → `README.md` entry; complex → dedicated `.md` + link.
- [ ] Idempotent / re-runnable from a clean checkout where feasible.
