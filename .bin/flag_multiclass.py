#!/usr/bin/env python3
"""Thorne-EQ multi-class spike helper — flag spells usable by a class for testing.

Operator script (mutating, reversible). Enables the Phase 1 experiment from
`.docs/MULTI-CLASS-DESIGN.md`: temporarily grant a base class access to another
class's spells in `spells_new` (the `classes1..16` min-level columns), so you can
test whether the stock TAKP/Quarm client + Zeal will scribe/memorize/cast them.

Every grant is backed up to `.reports/flag_multiclass_<class>.json` so `revoke`
restores the exact prior values. This is a TEST scaffold, not the real system — the
production path is a server-side `CanUseSpell()` overlay behind a rule flag.

Commands:
  list   --class <name>                 Show spells the class can currently cast.
  check  --class <name> --spells <ids>  Show current min-level for those spells.
  grant  --class <name> --spells <ids> [--from <class>|--level N]
                                        Make those spells castable by the class.
  revoke --class <name>                 Restore the class's columns from backup.

Examples:
  python .bin/flag_multiclass.py grant --class Necromancer --spells 1..20 --from Magician
  python .bin/flag_multiclass.py list  --class Necromancer
  python .bin/flag_multiclass.py revoke --class Necromancer
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS = REPO_ROOT / ".reports"

# EQ class id -> name (spells_new.classes_<id>). 255 in a column = barred.
CLASSES = {
    1: "Warrior",
    2: "Cleric",
    3: "Paladin",
    4: "Ranger",
    5: "ShadowKnight",
    6: "Druid",
    7: "Monk",
    8: "Bard",
    9: "Rogue",
    10: "Shaman",
    11: "Necromancer",
    12: "Wizard",
    13: "Magician",
    14: "Enchanter",
    15: "Beastlord",
}
NAME_TO_ID = {v.lower(): k for k, v in CLASSES.items()}

try:
    from rich.console import Console

    say = Console().print
except Exception:  # noqa: BLE001

    def say(msg: str = "") -> None:
        for t in ("[bold]", "[/bold]", "[green]", "[/green]", "[red]", "[/red]", "[yellow]", "[/yellow]", "[dim]", "[/dim]"):
            msg = str(msg).replace(t, "")
        print(msg)


def _connect():
    try:
        import pymysql
    except ImportError:
        say("[red]pymysql not installed.[/red] Run: pip install -r requirements.txt")
        raise SystemExit(1)
    return pymysql.connect(
        host=os.environ.get("THORNE_EQ_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("THORNE_EQ_DB_PORT", "3306")),
        user=os.environ.get("THORNE_EQ_DB_USER", "root"),
        password=os.environ.get("THORNE_EQ_DB_PASSWORD", ""),
        database=os.environ.get("THORNE_EQ_DB_NAME", "quarm"),
        autocommit=True,
    )


def _class_id(name: str) -> int:
    key = name.strip().lower()
    if key.isdigit() and int(key) in CLASSES:
        return int(key)
    if key not in NAME_TO_ID:
        say(f"[red]unknown class:[/red] {name}. One of: {', '.join(CLASSES.values())}")
        raise SystemExit(1)
    return NAME_TO_ID[key]


def _parse_spells(spec: str) -> list[int]:
    """Accept '1,2,3', ranges '1..20', or a mix."""
    ids: list[int] = []
    for part in spec.replace(" ", "").split(","):
        if ".." in part:
            lo, hi = part.split("..")
            ids.extend(range(int(lo), int(hi) + 1))
        elif part:
            ids.append(int(part))
    return sorted(set(ids))


def cmd_list(args: argparse.Namespace) -> None:
    cid = _class_id(args.class_name)
    col = f"classes{cid}"
    con = _connect()
    with con.cursor() as cur:
        cur.execute(f"SELECT id, name, {col} FROM spells_new WHERE {col} > 0 AND {col} < 255 ORDER BY {col}, id LIMIT %s", (args.limit,))
        rows = cur.fetchall()
    say(f"[bold]{CLASSES[cid]}[/bold] can cast {len(rows)} (showing up to {args.limit}):")
    for sid, name, lvl in rows:
        say(f"  {sid:>5}  L{lvl:<3}  {name}")


def cmd_check(args: argparse.Namespace) -> None:
    cid = _class_id(args.class_name)
    col = f"classes{cid}"
    ids = _parse_spells(args.spells)
    con = _connect()
    with con.cursor() as cur:
        cur.execute(f"SELECT id, name, {col} FROM spells_new WHERE id IN ({','.join(['%s'] * len(ids))})", ids)
        rows = cur.fetchall()
    say(f"[bold]{CLASSES[cid]}[/bold] min-levels ({col}); 255 = barred:")
    for sid, name, lvl in rows:
        tag = "[red]barred[/red]" if lvl == 255 else f"[green]L{lvl}[/green]"
        say(f"  {sid:>5}  {tag:<16}  {name}")


def cmd_grant(args: argparse.Namespace) -> None:
    cid = _class_id(args.class_name)
    col = f"classes{cid}"
    ids = _parse_spells(args.spells)
    from_col = f"classes{_class_id(args.from_class)}" if args.from_class else None
    con = _connect()
    backup: dict[str, int] = {}
    with con.cursor() as cur:
        cols = f"id, name, {col}" + (f", {from_col}" if from_col else "")
        cur.execute(f"SELECT {cols} FROM spells_new WHERE id IN ({','.join(['%s'] * len(ids))})", ids)
        rows = cur.fetchall()
        changed = 0
        for row in rows:
            sid, name, cur_val = row[0], row[1], row[2]
            new_val = row[3] if from_col else args.level
            if from_col and new_val == 255:
                say(f"  [yellow]skip {sid} ({name}): source class can't cast it[/yellow]")
                continue
            backup[str(sid)] = cur_val
            cur.execute(f"UPDATE spells_new SET {col}=%s WHERE id=%s", (new_val, sid))
            say(f"  {sid:>5}  {name}: {cur_val} -> [green]{new_val}[/green]")
            changed += 1
    REPORTS.mkdir(parents=True, exist_ok=True)
    bpath = REPORTS / f"flag_multiclass_{CLASSES[cid].lower()}.json"
    prev = json.loads(bpath.read_text()) if bpath.exists() else {}
    prev.update(backup)
    bpath.write_text(json.dumps(prev, indent=2), encoding="utf-8")
    say(f"[green]granted[/green] {changed} spells to {CLASSES[cid]}. Backup: {bpath.relative_to(REPO_ROOT)}")
    say("[dim]Reminder: this is a client-behavior test scaffold; revoke when done.[/dim]")


def cmd_revoke(args: argparse.Namespace) -> None:
    cid = _class_id(args.class_name)
    col = f"classes{cid}"
    bpath = REPORTS / f"flag_multiclass_{CLASSES[cid].lower()}.json"
    if not bpath.exists():
        say(f"[yellow]no backup found for {CLASSES[cid]}[/yellow] ({bpath.name}); nothing to revoke.")
        return
    backup = json.loads(bpath.read_text())
    con = _connect()
    with con.cursor() as cur:
        for sid, val in backup.items():
            cur.execute(f"UPDATE spells_new SET {col}=%s WHERE id=%s", (val, int(sid)))
    bpath.unlink()
    say(f"[green]revoked[/green] {len(backup)} spells for {CLASSES[cid]} (restored original min-levels).")


def main() -> None:
    p = argparse.ArgumentParser(description="Thorne-EQ multi-class spike helper.")
    sub = p.add_subparsers(dest="command", required=True)
    for name, fn, needs_spells in (("list", cmd_list, False), ("check", cmd_check, True), ("grant", cmd_grant, True), ("revoke", cmd_revoke, False)):
        sp = sub.add_parser(name)
        sp.add_argument("--class", dest="class_name", required=True, help="class name or id (1-16)")
        if needs_spells or name == "grant":
            sp.add_argument("--spells", required=(name != "revoke"), help="ids: '1,2,3' or ranges '1..20'")
        if name == "list":
            sp.add_argument("--limit", type=int, default=40)
        if name == "grant":
            sp.add_argument("--from", dest="from_class", help="copy min-levels from this class")
            sp.add_argument("--level", type=int, default=1, help="min level to grant (if not --from)")
        sp.set_defaults(func=fn)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
