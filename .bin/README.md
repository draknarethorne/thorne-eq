# Thorne-EQ Tooling (`.bin`)

Automation and analysis scripts for the server-side project. Mirrors the Thorne-UI
philosophy: **auditors (read-only) first, operators (mutating) second**, with outputs
written to `.tmp/` and `.reports/` (git-ignored), never treated as source of truth.

> Naming: snake_case `verb_noun.py`. Every Python tool has a matching `.bat` launcher
> (prefers the `.venv` Python) so you can run it from a plain Windows shell.

## Setup

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt        REM runtime deps
.venv\Scripts\python -m pip install -r requirements-dev.txt    REM + lint/format tooling
```

Requirements and `pyproject.toml` live at the **repo root** (Thorne-UI convention).

## Scripts

| Script (`.py` + `.bat`) | Type | Purpose |
| --- | --- | --- |
| `check_environment.ps1` / `.sh` | read-only | Toolchain readiness (Git, CMake, VS C++, MariaDB, Perl, Python). |
| `control_server` | operator | Assemble the run dir + start/stop/status the process chain; start MariaDB. |
| `manage_database` | operator | Import/reset/backup the DB, set GM status, run queries. |
| `compare_classes` | read-only | Class spell landscape + multi-class grant candidates. |
| `flag_multiclass` | operator | Grant/revoke a class's access to spells for the Phase 1 test (reversible). |
| `schema_explore` | read-only | Inspect key tables from a SQL dump dir or a live DB. |

### control_server — the server orchestrator

```bat
control_server.bat mariadb      REM start portable MariaDB (foreground)
control_server.bat assemble     REM link Maps/quests, copy configs+assets into the run dir
control_server.bat start        REM shared_memory -> loginserver -> world -> zone
control_server.bat status       REM what's up
control_server.bat stop         REM stop all server processes
```

### manage_database — DB operator

```bat
manage_database.bat status
manage_database.bat import --dump server\utils\sql\database_full\quarm_<date>.tar.gz
manage_database.bat bootstrap          REM render config templates + apply custom SQL (users, launcher)
manage_database.bat repair             REM auto-repair crashed MyISAM/Aria tables
manage_database.bat backup
manage_database.bat gm --account <name>            REM set account.status = 255
```

### Rebuild from scratch (the recipe)

The custom pieces that aren't in the upstream dump live in the hub and are applied by script:

- `config/*.template.*` -> rendered to `mariadb/my.ini`, `server/eqemu_config.json`, `server/login.json`
- `db/bootstrap/*.sql` -> the `eq` DB user + the zone `launcher` tables

```bat
manage_database.bat import --dump <latest quarm dump>   REM load content
manage_database.bat bootstrap --force                   REM users + launcher + configs
control_server.bat start                                REM run it
```

### compare_classes — plan the tests

```bat
compare_classes.bat summary
compare_classes.bat candidates --base Necromancer --secondary Magician --maxlevel 20
```

### flag_multiclass — Phase 1 spike (reversible)

```bat
flag_multiclass.bat grant  --class Necromancer --spells 50,93,310 --from Magician
flag_multiclass.bat list   --class Necromancer
flag_multiclass.bat revoke --class Necromancer     REM restores original min-levels
```

## DB connection

Scripts default to `root@127.0.0.1:3306` / db `quarm` (portable MariaDB). Override with
`--user/--password/--database` or `THORNE_EQ_DB_{HOST,PORT,USER,PASSWORD,NAME}`.

## Why these tables matter (multi-class levers)

- `spells_new` — `classes1..15` min-level gating; the spell-line access lever (255 = barred).
- `skill_caps` — per-class/skill/level caps; the "equalizer" lever (Phase 5).
- `rule_values` — feature flags for staged rollout.
- `data_buckets` — per-character declaration/allocation state.

See `.docs/MULTI-CLASS-DESIGN.md` and `.docs/ROADMAP.md` for the design these tools support.

## Conventions

- Read-only auditors are safe anytime; operators mutate — read their `--help` first.
- Never commit secrets; pass DB passwords via env vars, not files.
- Treat `.tmp/` and `.reports/` as disposable artifacts.
