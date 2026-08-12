#!/usr/bin/env python3
"""Thorne-EQ server control — assemble the run directory and drive the process chain.

Operator script (mutating). Turns the multi-step "assemble run dir + start four
processes in order" dance into single commands. Windows-focused (uses directory
junctions + tasklist/taskkill), degrades with clear messages elsewhere.

Layout it assumes (all under the repo root, C:\\Thorne-EQ):
  server/   EQMacEmu fork (build output in server/build/bin/RelWithDebInfo)
  quests/   quests fork            maps/   map data
  mariadb/  portable MariaDB       .tmp/logs/  process logs (git-ignored)

Commands:
  mariadb            Start portable MariaDB in the foreground (Ctrl+C to stop).
  assemble           Build/refresh the run directory (idempotent, safe to re-run).
  start [procs...]   Start processes in order (default: shared_memory loginserver world zone).
  stop               Stop all Thorne-EQ server processes.
  status             Show which processes/ports are up.

Examples:
  python .bin/control_server.py assemble
  python .bin/control_server.py start
  python .bin/control_server.py status
  python .bin/control_server.py stop
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_DIR = REPO_ROOT / "server"
RUN_DIR = SERVER_DIR / "build" / "bin" / "RelWithDebInfo"
MARIADB_DIR = REPO_ROOT / "mariadb"
MAPS_DIR = REPO_ROOT / "maps"
QUESTS_DIR = REPO_ROOT / "quests"
LOG_DIR = REPO_ROOT / ".tmp" / "logs"

# Start order matters: shared_memory populates the memory-mapped files the rest read.
# Zones boot via eqlaunch (a launcher pool) named below, not standalone zone.exe.
LAUNCHER_NAME = "dynzone1"
PROCESS_ORDER = ["shared_memory", "loginserver", "world", "eqlaunch"]
OPTIONAL_PROCS = ["ucs", "queryserv"]
ALL_PROCS = ["shared_memory", "loginserver", "world", "eqlaunch", "zone", "ucs", "queryserv"]

IS_WINDOWS = sys.platform.startswith("win")

try:
    from rich.console import Console

    _c = Console()

    def say(msg: str) -> None:
        _c.print(msg)
except Exception:  # noqa: BLE001 - rich is optional

    def say(msg: str) -> None:
        # Strip simple rich markup if rich is unavailable.
        for tag in ("[bold]", "[/bold]", "[green]", "[/green]", "[red]", "[/red]", "[yellow]", "[/yellow]", "[dim]", "[/dim]"):
            msg = msg.replace(tag, "")
        print(msg)


def _die(msg: str) -> None:
    say(f"[red]error:[/red] {msg}")
    raise SystemExit(1)


def _junction(link: Path, target: Path) -> None:
    """Create a Windows directory junction (no admin needed). Copy fallback elsewhere."""
    if link.exists():
        return
    if not target.exists():
        say(f"[yellow]skip:[/yellow] junction target missing: {target}")
        return
    if IS_WINDOWS:
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=False, capture_output=True)
    else:
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            shutil.copytree(target, link)
    say(f"  linked {link.name} -> {target}")


def cmd_assemble(_args: argparse.Namespace) -> None:
    """Populate the run directory so the binaries find configs, assets, maps, quests."""
    if not RUN_DIR.exists():
        _die(f"run dir not found (build first): {RUN_DIR}")
    say(f"[bold]Assembling run directory[/bold]  {RUN_DIR}")

    # Configs
    for name in ("eqemu_config.json", "login.json"):
        src = SERVER_DIR / name
        if src.exists():
            shutil.copy2(src, RUN_DIR / name)
            say(f"  config {name}")
        else:
            say(f"[yellow]  missing config {name} (create it in server/)[/yellow]")

    # Assets: opcodes + patches
    opcodes_dst = RUN_DIR / "assets" / "opcodes"
    patches_dst = RUN_DIR / "assets" / "patches"
    opcodes_dst.mkdir(parents=True, exist_ok=True)
    patches_dst.mkdir(parents=True, exist_ok=True)
    patch_src = SERVER_DIR / "utils" / "patches"
    if patch_src.exists():
        for conf in patch_src.glob("*.conf"):
            shutil.copy2(conf, opcodes_dst / conf.name)
            shutil.copy2(conf, patches_dst / conf.name)
        for extra in patch_src.glob("patch_*"):
            shutil.copy2(extra, patches_dst / extra.name)
        say("  copied opcodes + patches")
    # Login opcodes live next to the loginserver working dir.
    login_util = SERVER_DIR / "loginserver" / "login_util"
    if login_util.exists():
        for conf in login_util.glob("*.conf"):
            shutil.copy2(conf, RUN_DIR / conf.name)
        say("  copied login opcodes")

    # Runtime dirs + junctions
    (RUN_DIR / "shared").mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    _junction(RUN_DIR / "Maps", MAPS_DIR)
    _junction(RUN_DIR / "quests", QUESTS_DIR)

    # Runtime DLLs the vcpkg applocal.ps1 post-build step fails to copy on this box:
    # vcpkg dependency DLLs + project-built lib DLLs (e.g. zlib-ng, which zone.exe needs).
    dll_files = list((SERVER_DIR / "vcpkg" / "vcpkg-export-x64" / "installed" / "x64-windows" / "bin").glob("*.dll"))
    dll_files += [p for p in (SERVER_DIR / "build" / "libs").rglob("*.dll") if "RelWithDebInfo" in p.parts]
    for dll in dll_files:
        shutil.copy2(dll, RUN_DIR / dll.name)
    if dll_files:
        say(f"  copied {len(dll_files)} runtime DLLs (vcpkg + built libs)")

    say("[green]assemble complete.[/green] Next: python .bin/control_server.py start")


def _running() -> dict[str, list[int]]:
    """Return {process_name: [pids]} for our server exes via tasklist."""
    if not IS_WINDOWS:
        return {}
    found: dict[str, list[int]] = {}
    out = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) < 2:
            continue
        image = parts[0].strip('"').lower()
        for proc in ALL_PROCS:
            if image == f"{proc}.exe":
                found.setdefault(proc, []).append(int(parts[1]))
    return found


def cmd_start(args: argparse.Namespace) -> None:
    procs = args.procs or PROCESS_ORDER
    if not RUN_DIR.exists():
        _die(f"run dir not found (build + assemble first): {RUN_DIR}")
    if not (RUN_DIR / "eqemu_config.json").exists():
        say("[yellow]run dir not assembled; running assemble first...[/yellow]")
        cmd_assemble(args)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    say(f"[bold]Starting[/bold] {', '.join(procs)}")
    for proc in procs:
        exe = RUN_DIR / f"{proc}.exe"
        if not exe.exists():
            say(f"[yellow]skip {proc}: {exe.name} not built[/yellow]")
            continue
        log = LOG_DIR / f"{proc}.log"
        if proc == "shared_memory":
            # One-shot loader: MUST fully populate shared/ before world/zone start.
            say("  running [green]shared_memory[/green] to completion (loads items/spells)...")
            with open(log, "w", encoding="utf-8") as fh:
                subprocess.run([str(exe)], cwd=str(RUN_DIR), stdout=fh, stderr=subprocess.STDOUT)
            say("  shared_memory done.")
            continue
        flags = 0
        if IS_WINDOWS:
            flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008  # DETACHED_PROCESS
        cmd = [str(exe), LAUNCHER_NAME] if proc == "eqlaunch" else [str(exe)]
        with open(log, "w", encoding="utf-8") as fh:
            subprocess.Popen(cmd, cwd=str(RUN_DIR), stdout=fh, stderr=subprocess.STDOUT, creationflags=flags)
        say(f"  started [green]{proc}[/green]  -> {log.relative_to(REPO_ROOT)}")
        time.sleep(1.5)
    say("[green]start issued.[/green] Check: python .bin/control_server.py status")


def cmd_stop(_args: argparse.Namespace) -> None:
    if not IS_WINDOWS:
        _die("stop is implemented for Windows (taskkill).")
    running = _running()
    if not running:
        say("nothing running.")
        return
    for proc, pids in running.items():
        for pid in pids:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
        say(f"  stopped {proc} ({len(pids)})")
    say("[green]stopped.[/green]")


def cmd_status(_args: argparse.Namespace) -> None:
    running = _running()
    say("[bold]Thorne-EQ status[/bold]")
    # MariaDB
    mariadb_up = any(p.lower() == "mysqld.exe" for p in _tasklist_images())
    say(f"  MariaDB (mysqld) : {'[green]UP[/green]' if mariadb_up else '[red]down[/red]'}")
    for proc in ALL_PROCS:
        pids = running.get(proc, [])
        state = f"[green]UP[/green] pid {pids[0]}" if pids else "[dim]down[/dim]"
        say(f"  {proc:<14} : {state}")


def _tasklist_images() -> list[str]:
    if not IS_WINDOWS:
        return []
    out = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True).stdout
    return [line.split('","')[0].strip('"') for line in out.splitlines() if line]


def cmd_mariadb(_args: argparse.Namespace) -> None:
    mysqld = MARIADB_DIR / "bin" / "mysqld.exe"
    my_ini = MARIADB_DIR / "my.ini"
    if not mysqld.exists():
        _die(f"mysqld not found: {mysqld}")
    say(f"[bold]Starting MariaDB[/bold] (Ctrl+C to stop)\n  {mysqld}")
    subprocess.run([str(mysqld), f"--defaults-file={my_ini}", "--console"], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Thorne-EQ server control.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("mariadb", help="Start portable MariaDB (foreground).").set_defaults(func=cmd_mariadb)
    sub.add_parser("assemble", help="Assemble/refresh the run directory.").set_defaults(func=cmd_assemble)
    p_start = sub.add_parser("start", help="Start the server process chain.")
    p_start.add_argument("procs", nargs="*", help=f"processes (default: {' '.join(PROCESS_ORDER)})")
    p_start.set_defaults(func=cmd_start)
    sub.add_parser("stop", help="Stop all server processes.").set_defaults(func=cmd_stop)
    sub.add_parser("status", help="Show process/port status.").set_defaults(func=cmd_status)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
