#!/usr/bin/env python3
"""Thorne-EQ schema explorer.

Read-only analysis toolkit for the EQMac/Quarm server database. Mirrors the
Thorne-UI approach of scripting against the .sql to understand game data before
changing it.

Two modes:
  1) --sql-dir <dir>   Scan a directory of .sql dump files (no DB needed).
  2) --db              Connect to a live MariaDB (requires pymysql; reads
                       connection info from --host/--user/--password/--database
                       or the THORNE_EQ_DB_* environment variables).

Focus tables (the levers for the Attunement / cap system):
  - skill_caps      : class/skill/level -> cap    (the "equalizer" lever)
  - spells_new      : classes_1..16 min-level gating (spell-line access lever)
  - rule_values     : feature-flag toggles
  - data_buckets    : per-character state store

Outputs a JSON summary to .tmp/schema_report.json and prints a concise console
digest. Degrades gracefully with clear guidance if no source is available.

Usage:
  python .bin/schema_explore.py --sql-dir C:/Code/server-src/utils/sql/database_full
  python .bin/schema_explore.py --db --database eqmac --user root
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

TARGET_TABLES = ["skill_caps", "spells_new", "rule_values", "data_buckets"]

REPO_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = REPO_ROOT / ".tmp"


def _emit(report: dict) -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / "schema_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(REPO_ROOT)}")


def scan_sql_dir(sql_dir: Path) -> dict:
    """Scan .sql files for target CREATE TABLE definitions and row counts."""
    if not sql_dir.exists():
        return {"error": f"sql-dir not found: {sql_dir}"}

    files = sorted(sql_dir.rglob("*.sql"))
    report: dict = {"mode": "sql-dir", "source": str(sql_dir), "files": len(files), "tables": {}}
    if not files:
        report["warning"] = "No .sql files found. Point --sql-dir at the DB dump folder."
        return report

    create_re = {
        t: re.compile(rf"CREATE TABLE[^;]*`{t}`\s*\((.*?)\)\s*(ENGINE|;)", re.IGNORECASE | re.DOTALL)
        for t in TARGET_TABLES
    }
    insert_re = {t: re.compile(rf"INSERT INTO `{t}`", re.IGNORECASE) for t in TARGET_TABLES}
    col_re = re.compile(r"^\s*`([A-Za-z0-9_]+)`", re.MULTILINE)

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:  # noqa: BLE001
            report.setdefault("read_errors", []).append({"file": str(f), "error": str(exc)})
            continue
        for t in TARGET_TABLES:
            entry = report["tables"].setdefault(t, {"found_in": [], "columns": [], "insert_statements": 0})
            m = create_re[t].search(text)
            if m and not entry["columns"]:
                entry["columns"] = col_re.findall(m.group(1))
                entry["found_in"].append(f.name)
            entry["insert_statements"] += len(insert_re[t].findall(text))

    return report


def scan_live_db(args: argparse.Namespace) -> dict:
    """Connect to MariaDB and inspect target tables."""
    try:
        import pymysql  # type: ignore
    except ImportError:
        return {
            "error": "pymysql not installed. Run: pip install -r .bin/requirements.txt",
            "hint": "Or use --sql-dir mode which needs no DB driver.",
        }

    host = args.host or os.environ.get("THORNE_EQ_DB_HOST", "127.0.0.1")
    user = args.user or os.environ.get("THORNE_EQ_DB_USER", "root")
    password = args.password or os.environ.get("THORNE_EQ_DB_PASSWORD", "")
    database = args.database or os.environ.get("THORNE_EQ_DB_NAME", "eqmac")

    report: dict = {"mode": "db", "source": f"{user}@{host}/{database}", "tables": {}}
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
    except Exception as exc:  # noqa: BLE001
        report["error"] = f"DB connection failed: {exc}"
        return report

    try:
        with conn.cursor() as cur:
            for t in TARGET_TABLES:
                entry: dict = {"exists": False, "columns": [], "row_count": None}
                try:
                    cur.execute(
                        "SELECT COLUMN_NAME FROM information_schema.columns "
                        "WHERE table_schema=%s AND table_name=%s ORDER BY ORDINAL_POSITION",
                        (database, t),
                    )
                    cols = [r[0] for r in cur.fetchall()]
                    if cols:
                        entry["exists"] = True
                        entry["columns"] = cols
                        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
                        entry["row_count"] = cur.fetchone()[0]
                except Exception as exc:  # noqa: BLE001
                    entry["error"] = str(exc)
                report["tables"][t] = entry
    finally:
        conn.close()

    return report


def print_digest(report: dict) -> None:
    print("\n  Thorne-EQ Schema Explorer")
    print("  =========================")
    if report.get("error"):
        print(f"  ERROR: {report['error']}")
        if report.get("hint"):
            print(f"  HINT:  {report['hint']}")
        return
    if report.get("warning"):
        print(f"  NOTE: {report['warning']}")
    print(f"  Mode:   {report.get('mode')}")
    print(f"  Source: {report.get('source')}")
    print("")
    for t, entry in report.get("tables", {}).items():
        cols = entry.get("columns") or []
        detail = ""
        if "row_count" in entry and entry["row_count"] is not None:
            detail = f"rows={entry['row_count']}"
        elif "insert_statements" in entry:
            detail = f"insert_stmts={entry['insert_statements']}"
        status = "found" if (entry.get("exists") or cols) else "not found"
        print(f"  - {t:<14} [{status}] cols={len(cols)} {detail}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Thorne-EQ schema explorer (read-only).")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--sql-dir", type=Path, help="Directory containing .sql dump files.")
    src.add_argument("--db", action="store_true", help="Use a live MariaDB connection.")
    p.add_argument("--host")
    p.add_argument("--user")
    p.add_argument("--password")
    p.add_argument("--database")
    args = p.parse_args(argv)

    if args.sql_dir:
        report = scan_sql_dir(args.sql_dir)
    elif args.db:
        report = scan_live_db(args)
    else:
        print(__doc__)
        print("No source selected. Use --sql-dir <dir> or --db. Nothing to do.")
        return 2

    print_digest(report)
    _emit(report)
    return 0 if not report.get("error") else 1


if __name__ == "__main__":
    sys.exit(main())
