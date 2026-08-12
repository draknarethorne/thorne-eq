#!/usr/bin/env python3
"""Thorne-EQ database operator — import, reset, backup, and admin the Quarm DB.

Operator script (mutating). Encodes the import quirks learned during bring-up so a
fresh database is one command:
  * rename dump files whose names contain ':' (Windows can't open them)
  * strip the MariaDB sandbox-mode header the 10.3 client rejects
  * import by piping each file (batch mode), not the client `SOURCE` command

Connection defaults come from server/eqemu_config.json when present, else root@127.0.0.1
with no password (the portable MariaDB default). Override with flags or THORNE_EQ_DB_*.

Commands:
  status                       Show DB up + table/spell/item/zone counts.
  import --dump <path>         Import a Quarm dump (.tar.gz or extracted dir) into --database.
  reset  --yes                 Drop + recreate the database (destructive).
  backup [--out <file>]        mysqldump the database into .reports/.
  gm --account <name>          Set account.status (default 255 = full GM).
  query "<sql>"                Run a SQL statement and print rows.

Examples:
  python .bin/manage_database.py status
  python .bin/manage_database.py import --dump server/utils/sql/database_full/quarm_2026-03-20-09_37.tar.gz
  python .bin/manage_database.py gm --account Draknare
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARIADB_BIN = REPO_ROOT / "mariadb" / "bin"
MY_INI = REPO_ROOT / "mariadb" / "my.ini"
CONFIG = REPO_ROOT / "server" / "eqemu_config.json"
REPORTS = REPO_ROOT / ".reports"
BOOTSTRAP_DIR = REPO_ROOT / "db" / "bootstrap"
CONFIG_DIR = REPO_ROOT / "config"
# Template -> live-file rendering for `bootstrap` (real files stay gitignored; templates tracked).
CONFIG_RENDER = {
    CONFIG_DIR / "mariadb.template.ini": REPO_ROOT / "mariadb" / "my.ini",
    CONFIG_DIR / "eqemu_config.template.json": REPO_ROOT / "server" / "eqemu_config.json",
    CONFIG_DIR / "login.template.json": REPO_ROOT / "server" / "login.json",
}

try:
    from rich.console import Console

    _c = Console()
    say = _c.print
except Exception:  # noqa: BLE001

    def say(msg: str = "") -> None:
        for tag in ("[bold]", "[/bold]", "[green]", "[/green]", "[red]", "[/red]", "[yellow]", "[/yellow]", "[dim]", "[/dim]"):
            msg = str(msg).replace(tag, "")
        print(msg)


def _conn_info(args: argparse.Namespace) -> dict:
    """Resolve DB connection: flags > env > eqemu_config.json > portable defaults."""
    info = {"host": "127.0.0.1", "port": "3306", "user": "root", "password": "", "db": "quarm"}
    if CONFIG.exists():
        try:
            cfg = json.loads(CONFIG.read_text(encoding="utf-8")).get("server", {}).get("database", {})
            info.update({k: str(cfg[k]) for k in ("host", "port", "db") if k in cfg})
        except Exception:  # noqa: BLE001 - config is best-effort
            pass
    info["host"] = os.environ.get("THORNE_EQ_DB_HOST", info["host"])
    info["user"] = args.user or os.environ.get("THORNE_EQ_DB_USER", "root")
    info["password"] = args.password if args.password is not None else os.environ.get("THORNE_EQ_DB_PASSWORD", "")
    info["db"] = args.database or info["db"]
    return info


def _mysql_argv(info: dict, database: str | None = None) -> list[str]:
    exe = MARIADB_BIN / "mysql.exe"
    argv = [str(exe), f"--defaults-file={MY_INI}", "-h", info["host"], "-P", info["port"], "-u", info["user"]]
    if info["password"]:
        argv.append(f"-p{info['password']}")
    if database:
        argv.append(database)
    return argv


def _run_sql(info: dict, sql: str, database: str | None = None) -> str:
    argv = _mysql_argv(info, database) + ["-e", sql]
    res = subprocess.run(argv, capture_output=True, text=True)
    if res.returncode != 0:
        say(f"[red]SQL error:[/red] {res.stderr.strip()}")
    return res.stdout


def cmd_status(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    say(f"[bold]Database status[/bold]  {info['user']}@{info['host']}:{info['port']} / {info['db']}")
    out = _run_sql(
        info,
        "SELECT "
        "(SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()) AS tables,"
        "(SELECT COUNT(*) FROM spells_new) AS spells,"
        "(SELECT COUNT(*) FROM items) AS items,"
        "(SELECT COUNT(*) FROM zone) AS zones;",
        info["db"],
    )
    say(out.strip() or "[yellow]no output (is MariaDB running? try control_server.py mariadb)[/yellow]")


def _prepare_dump(dump: Path) -> Path:
    """Return a directory of import-ready .sql files (extract + sanitize as needed)."""
    if dump.is_dir():
        work = dump
    else:
        work = Path(tempfile.mkdtemp(prefix="thorne_dump_"))
        say(f"  extracting {dump.name} ...")
        with tarfile.open(dump, "r:gz") as tf:
            tf.extractall(work)
    # Rename ':' in filenames; strip sandbox-mode header lines.
    for f in list(work.rglob("*.sql")):
        if ":" in f.name:
            nf = f.with_name(f.name.replace(":", "_"))
            f.rename(nf)
            f = nf
        text = f.read_text(encoding="utf-8", errors="ignore")
        cleaned = re.sub(r"^.*enable the sandbox mode.*\n", "", text, flags=re.MULTILINE)
        if cleaned != text:
            f.write_text(cleaned, encoding="utf-8")
    return work


def cmd_import(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    dump = Path(args.dump)
    if not dump.exists():
        say(f"[red]dump not found:[/red] {dump}")
        raise SystemExit(1)
    work = _prepare_dump(dump)
    say(f"[bold]Importing[/bold] into `{info['db']}` from {work}")
    _run_sql(info, f"CREATE DATABASE IF NOT EXISTS {info['db']} CHARACTER SET utf8;")
    # Import content first, then player_tables, then login_tables (per dump readme).
    order = ["quarm", "alkabor", "player_tables", "login_tables", "data_tables"]
    files = sorted(work.glob("*.sql"), key=lambda p: next((i for i, k in enumerate(order) if p.name.startswith(k)), 99))
    for f in files:
        if f.name.startswith("drop_system"):
            continue
        say(f"  {f.name} ...")
        with open(f, "rb") as fh:
            res = subprocess.run(_mysql_argv(info, info["db"]), stdin=fh, capture_output=True, text=True)
        if res.returncode != 0:
            say(f"[red]  failed:[/red] {res.stderr.strip()[:200]}")
            raise SystemExit(1)
    say("[green]import complete.[/green]")
    cmd_status(args)


def cmd_reset(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    if not args.yes:
        say(f"[red]refusing to drop `{info['db']}` without --yes[/red]")
        raise SystemExit(1)
    _run_sql(info, f"DROP DATABASE IF EXISTS {info['db']}; CREATE DATABASE {info['db']} CHARACTER SET utf8;")
    say(f"[green]reset `{info['db']}`.[/green] Re-import with: manage_database.py import --dump <path>")


def cmd_backup(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    REPORTS.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else REPORTS / f"{info['db']}_{datetime.now():%Y%m%d_%H%M%S}.sql"
    dump_exe = MARIADB_BIN / "mysqldump.exe"
    argv = [str(dump_exe), f"--defaults-file={MY_INI}", "-h", info["host"], "-P", info["port"], "-u", info["user"]]
    if info["password"]:
        argv.append(f"-p{info['password']}")
    argv.append(info["db"])
    say(f"[bold]Backing up[/bold] `{info['db']}` -> {out}")
    with open(out, "w", encoding="utf-8") as fh:
        res = subprocess.run(argv, stdout=fh, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        say(f"[red]backup failed:[/red] {res.stderr.strip()[:200]}")
        raise SystemExit(1)
    say(f"[green]backup written[/green] ({out.stat().st_size // 1024} KB)")


def cmd_gm(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    status = args.status
    _run_sql(info, f"UPDATE account SET status={status} WHERE name='{args.account}';", info["db"])
    out = _run_sql(info, f"SELECT name, status FROM account WHERE name='{args.account}';", info["db"])
    say(f"[green]set GM[/green] status={status} for '{args.account}':\n{out.strip()}")


def cmd_query(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    say(_run_sql(info, args.sql, info["db"]).rstrip())


def cmd_repair(args: argparse.Namespace) -> None:
    info = _conn_info(args)
    exe = MARIADB_BIN / "mysqlcheck.exe"
    argv = [str(exe), f"--defaults-file={MY_INI}", "-h", info["host"], "-P", info["port"], "-u", info["user"]]
    if info["password"]:
        argv.append(f"-p{info['password']}")
    argv += ["--auto-repair", "--databases", "mysql", info["db"]]
    say(f"[bold]Repairing[/bold] mysql + {info['db']} (auto-repair crashed tables)...")
    res = subprocess.run(argv, capture_output=True, text=True)
    bad = [ln for ln in res.stdout.splitlines() if ln.strip() and "OK" not in ln]
    say("\n".join(bad[-20:]) if bad else "[green]all tables OK.[/green]")


def cmd_bootstrap(args: argparse.Namespace) -> None:
    """Fresh-DB setup: render config templates + apply custom bootstrap SQL (users, launcher)."""
    info = _conn_info(args)
    say("[bold]Rendering config templates[/bold]")
    for tmpl, dest in CONFIG_RENDER.items():
        if not tmpl.exists():
            say(f"[yellow]  missing template {tmpl.name}[/yellow]")
            continue
        if dest.exists() and not args.force:
            say(f"[dim]  keep existing {dest.name} (use --force to overwrite)[/dim]")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmpl, dest)
        say(f"  {tmpl.name} -> {dest}")
    say("[bold]Applying bootstrap SQL[/bold]")
    for sql in sorted(BOOTSTRAP_DIR.glob("*.sql")):
        db = None if "user" in sql.name.lower() else info["db"]
        say(f"  {sql.name} [{db or 'server'}]")
        with open(sql, "rb") as fh:
            res = subprocess.run(_mysql_argv(info, db), stdin=fh, capture_output=True, text=True)
        if res.returncode != 0:
            say(f"[red]    failed:[/red] {res.stderr.strip()[:200]}")
            raise SystemExit(1)
    say("[green]bootstrap complete.[/green] Next: python .bin/control_server.py start")


def main() -> None:
    p = argparse.ArgumentParser(description="Thorne-EQ database operator.")
    p.add_argument("--database", help="database name (default: from config or 'quarm')")
    p.add_argument("--user", help="db user (default: root)")
    p.add_argument("--password", help="db password (default: empty / env THORNE_EQ_DB_PASSWORD)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show DB counts.").set_defaults(func=cmd_status)
    pi = sub.add_parser("import", help="Import a dump.")
    pi.add_argument("--dump", required=True, help=".tar.gz or extracted dump dir")
    pi.set_defaults(func=cmd_import)
    pr = sub.add_parser("reset", help="Drop + recreate the DB (destructive).")
    pr.add_argument("--yes", action="store_true", help="confirm the drop")
    pr.set_defaults(func=cmd_reset)
    pb = sub.add_parser("backup", help="mysqldump the DB into .reports/.")
    pb.add_argument("--out", help="output file path")
    pb.set_defaults(func=cmd_backup)
    pg = sub.add_parser("gm", help="Set account.status (GM level).")
    pg.add_argument("--account", required=True, help="account name")
    pg.add_argument("--status", type=int, default=255, help="status level (default 255)")
    pg.set_defaults(func=cmd_gm)
    pq = sub.add_parser("query", help="Run a SQL statement.")
    pq.add_argument("sql", help="SQL to execute")
    pq.set_defaults(func=cmd_query)
    sub.add_parser("repair", help="Auto-repair crashed MyISAM/Aria tables.").set_defaults(func=cmd_repair)
    pbo = sub.add_parser("bootstrap", help="Render config templates + apply custom bootstrap SQL (users, launcher).")
    pbo.add_argument("--force", action="store_true", help="overwrite existing config files")
    pbo.set_defaults(func=cmd_bootstrap)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
