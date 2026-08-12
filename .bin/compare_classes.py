#!/usr/bin/env python3
"""Thorne-EQ class/spell analyzer — plan the multi-class tests with real data.

Read-only (auditor). Answers the questions we need before Phase 1:
  * Which spells could a base class gain from a secondary class? (grant candidates)
  * How big is each class's spell list? (the landscape)
  * What do two classes already share?

Reads `spells_new.classes1..16` (min level per class; 0/255 = cannot cast) from the
live DB. Connection via THORNE_EQ_DB_* env vars (defaults root@127.0.0.1 / quarm).

Commands:
  summary                                   Castable-spell counts for all 16 classes.
  candidates --base <cls> --secondary <cls> Spells the secondary can cast but the base cannot.
  shared     --a <cls> --b <cls>            Spells both classes can cast.

Examples:
  python .bin/compare_classes.py summary
  python .bin/compare_classes.py candidates --base Necromancer --secondary Magician --maxlevel 20
"""

from __future__ import annotations

import argparse
import os

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
    from rich.table import Table

    _c = Console()
    _HAVE_RICH = True
except Exception:  # noqa: BLE001
    _HAVE_RICH = False

    def _print(msg: str = "") -> None:
        print(msg)


def _say(msg: str = "") -> None:
    if _HAVE_RICH:
        _c.print(msg)
    else:
        for t in ("[bold]", "[/bold]", "[green]", "[/green]", "[dim]", "[/dim]"):
            msg = str(msg).replace(t, "")
        print(msg)


def _connect():
    try:
        import pymysql
    except ImportError:
        _say("pymysql not installed. Run: pip install -r requirements.txt")
        raise SystemExit(1)
    return pymysql.connect(
        host=os.environ.get("THORNE_EQ_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("THORNE_EQ_DB_PORT", "3306")),
        user=os.environ.get("THORNE_EQ_DB_USER", "root"),
        password=os.environ.get("THORNE_EQ_DB_PASSWORD", ""),
        database=os.environ.get("THORNE_EQ_DB_NAME", "quarm"),
        autocommit=True,
    )


def _cid(name: str) -> int:
    key = name.strip().lower()
    if key.isdigit() and int(key) in CLASSES:
        return int(key)
    if key not in NAME_TO_ID:
        _say(f"unknown class: {name}. One of: {', '.join(CLASSES.values())}")
        raise SystemExit(1)
    return NAME_TO_ID[key]


def _castable(col: str) -> str:
    return f"({col} > 0 AND {col} < 255)"


def cmd_summary(_args: argparse.Namespace) -> None:
    con = _connect()
    counts: dict[int, int] = {}
    with con.cursor() as cur:
        for cid in CLASSES:
            cur.execute(f"SELECT COUNT(*) FROM spells_new WHERE {_castable(f'classes{cid}')}")
            counts[cid] = cur.fetchone()[0]
    if _HAVE_RICH:
        table = Table(title="Castable spells per class")
        table.add_column("Class")
        table.add_column("Spells", justify="right")
        for cid, name in CLASSES.items():
            table.add_row(name, str(counts[cid]))
        _c.print(table)
    else:
        for cid, name in CLASSES.items():
            print(f"  {name:<14} {counts[cid]:>5}")


def cmd_candidates(args: argparse.Namespace) -> None:
    base, sec = _cid(args.base), _cid(args.secondary)
    bcol, scol = f"classes{base}", f"classes{sec}"
    where = f"{_castable(scol)} AND NOT {_castable(bcol)}"
    if args.maxlevel:
        where += f" AND {scol} <= {args.maxlevel}"
    con = _connect()
    with con.cursor() as cur:
        cur.execute(f"SELECT id, name, {scol} FROM spells_new WHERE {where} ORDER BY {scol}, id LIMIT %s", (args.limit,))
        rows = cur.fetchall()
        cur.execute(f"SELECT COUNT(*) FROM spells_new WHERE {where}")
        total = cur.fetchone()[0]
    _say(f"[bold]{CLASSES[sec]} -> {CLASSES[base]}[/bold] grant candidates: {total} total (showing {len(rows)})")
    for sid, name, lvl in rows:
        _say(f"  {sid:>5}  L{lvl:<3}  {name}")
    _say(f"[dim]Test with: flag_multiclass.py grant --class {CLASSES[base]} --secondary-note {CLASSES[sec]} --spells <ids> --from {CLASSES[sec]}[/dim]")


def cmd_shared(args: argparse.Namespace) -> None:
    a, b = _cid(args.a), _cid(args.b)
    where = f"{_castable(f'classes{a}')} AND {_castable(f'classes{b}')}"
    con = _connect()
    with con.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM spells_new WHERE {where}")
        total = cur.fetchone()[0]
    _say(f"[bold]{CLASSES[a]}[/bold] and [bold]{CLASSES[b]}[/bold] share [green]{total}[/green] castable spells.")


def main() -> None:
    p = argparse.ArgumentParser(description="Thorne-EQ class/spell analyzer.")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("summary", help="Castable-spell counts per class.").set_defaults(func=cmd_summary)
    pc = sub.add_parser("candidates", help="Spells a secondary class could grant a base class.")
    pc.add_argument("--base", required=True, help="base/anchor class")
    pc.add_argument("--secondary", required=True, help="secondary class to borrow from")
    pc.add_argument("--maxlevel", type=int, help="only spells up to this level")
    pc.add_argument("--limit", type=int, default=40)
    pc.set_defaults(func=cmd_candidates)
    ps = sub.add_parser("shared", help="Spells both classes can cast.")
    ps.add_argument("--a", required=True)
    ps.add_argument("--b", required=True)
    ps.set_defaults(func=cmd_shared)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
