# Local Setup — Windows + Visual Studio 2026

This is your ground-zero, first-time setup for building and running the Thorne-EQ server
(EQMacEmu / Quarm lineage) on Windows. It assumes you are new to C++ server builds but
comfortable with tooling. Take it one section at a time.

> Note on source code: you have NOT imported the server code into this repo yet.
> See `.docs/TRANSITION-TO-SERVER-CODE.md` for the fork-vs-import decision. The steps
> below use a working clone of your chosen upstream (recommended: your fork of
> `SecretsOTheP/EQMacEmu`).

---

## 0) What you're building (mental model)

The server is several cooperating processes that share one MariaDB database:

- `loginserver` — handles account login and server list.
- `world` — the world/server hub; character select, zone routing.
- `zone` — runs zones and gameplay (you'll run one or more).
- `ucs` — chat/mail service.
- `queryserv` — logging/analytics service.
- `shared_memory` — loads shared game data into memory-mapped files.

The EQ **client** connects to `loginserver`, then `world`, then a `zone`.

---

## 1) Install the toolchain

### 1a) Visual Studio 2026 (C++)

You already have VS 2026. Ensure these components are installed
(Visual Studio Installer → Modify):

- **Workload:** Desktop development with C++
- Included/verify:
  - MSVC C++ build tools (latest v14x)
  - Windows 11 SDK (latest)
  - C++ CMake tools for Windows
  - C++ ATL (optional but handy)
  - C++ AddressSanitizer (optional, for debugging)

### 1b) Git

- Install Git for Windows: <https://git-scm.com/download/win>
- Confirm: `git --version`

### 1c) CMake

- VS bundles CMake, but a standalone install is fine too (>= 3.12):
  <https://cmake.org/download/>
- Confirm: `cmake --version`

> Dependencies (Boost, MySQL/MariaDB connector, ZLIB, OpenSSL, Lua51, LuaJit) are
> **fetched automatically by MSVC** via `cmake/DependencyHelperMSVC.cmake`. You do NOT
> need to install those by hand for a Windows/MSVC build.

---

## 2) Install the database (MariaDB 10.3.x)

Al'Kabor/EQMac targets MariaDB 10.3.x specifically.

1. Download MariaDB 10.3 (x64): <https://mariadb.org/download/>
2. During install:
   - Set a **root password** you will remember (used later in config).
   - Enable "Use UTF8 as default server's character set" if prompted.
   - Keep the default service name/port (`3306`).
3. Confirm the service is running (Windows Services → `MariaDB`).
4. Optional GUI: install **HeidiSQL** (bundled with MariaDB) to browse the DB.

Create an empty database (via HeidiSQL or CLI):

```sql
CREATE DATABASE eqmac CHARACTER SET utf8;
```

---

## 3) Install scripting runtime (Perl + Lua)

- **Strawberry Perl (x64)** — needed for quest scripting:
  <https://strawberryperl.com/>
  - Confirm: `perl -v`
- Lua support is provided through the build's fetched dependencies; no separate
  install is required for a basic build.

---

## 4) Get the server source

Replace `<your-fork>` with your fork once created (recommended path in
`.docs/TRANSITION-TO-SERVER-CODE.md`). If you have not forked yet, you can clone
upstream directly to start.

```bash
# From a code folder, e.g. C:\Code
git clone https://github.com/<your-fork>/EQMacEmu.git server-src
cd server-src

# Pull in required submodules (very important)
git submodule update --init --recursive
```

Related content repositories (clone near the server, per upstream README):

- Quests: `SecretsOTheP/quests` (or `EQMacEmu/quests`)
- Maps: `EQMacEmu/Maps`
- Database dump: `utils/sql/database_full` inside the server source

---

## 5) Configure + build with CMake (MSVC)

### Option A — Open folder in Visual Studio (easiest)

1. Visual Studio 2026 → **Open a local folder** → select `server-src`.
2. VS detects `CMakeLists.txt` and starts configuring.
3. Wait for dependency auto-fetch + CMake configure to finish (first run is slow).
4. Select configuration **RelWithDebInfo**, target **x64**.
5. Build → Build All.

### Option B — Command line

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --config RelWithDebInfo
```

Build outputs (server executables) land under the build output directory
(e.g. `build/bin/` depending on configuration).

> If configure fails: verify the C++ workload, CMake >= 3.12, and that submodules
> were initialized. Then delete `build/` and reconfigure.

---

## 6) Server configuration

1. Copy the sample config to `eqemu_config.json` in your run directory.
2. Set database connection:
   - host: `127.0.0.1`
   - port: `3306`
   - username: `root` (or a dedicated user)
   - password: your MariaDB root password
   - database: `eqmac`
3. Set world `shortname`/`longname` (your server's identity).

> Keep real passwords out of git. Use a local config that is gitignored.

---

## 7) Import the database

From the server source `utils/sql/database_full` (or the linked DB dump):

1. Unzip the dump if compressed.
2. Import all provided `.sql` files into the `eqmac` database (HeidiSQL: File → Load SQL,
   or CLI `mysql -u root -p eqmac < file.sql`).
3. Run any required update/patch SQL noted in the upstream README.

---

## 8) Maps and quests

- Point the server to the maps and quests directories (per upstream config/paths).
- Typical layout keeps `maps/` and `quests/` next to the server binaries/config.

---

## 9) First run (start order)

Start processes in this order (each in its own terminal, or via provided scripts):

1. `shared_memory` (loads shared data)
2. `loginserver`
3. `world`
4. `zone` (one instance; you can launch more later)
5. `ucs` and `queryserv` (optional at first)

Watch each console for successful DB connection and "ready" messages.

---

## 10) Connect the EQ client

1. Use a TAKP/Quarm-compatible client install (separate from your normal play install).
2. Edit `eqhost.txt` to point at your local login server (e.g. `127.0.0.1:5998`
   or the port your login server uses).
3. Launch the client, log in (local login can auto-create accounts if configured),
   select your server, create a character, and enter a zone.

---

## 11) Make yourself a GM (optional, for testing)

- After logging in once, set your account status to `255` in the `account` table
  (HeidiSQL), then `/camp` and log back in for GM commands.

---

## Troubleshooting quick hits

- **CMake configure fails** → C++ workload missing, CMake < 3.12, or submodules not
  initialized. Fix, delete `build/`, reconfigure.
- **Linker errors** → dependency auto-fetch incomplete; clean build and reconfigure.
- **DB connection refused** → MariaDB service down or wrong credentials in
  `eqemu_config.json`.
- **Quests not firing** → Strawberry Perl x64 not on PATH, or wrong quests path.
- **Client can't see server** → login server not running, wrong `eqhost.txt`, or port
  mismatch.

---

## What to do in the morning (suggested first session)

1. Decide fork vs import (`.docs/TRANSITION-TO-SERVER-CODE.md`).
2. Fork `SecretsOTheP/EQMacEmu`, clone, init submodules.
3. Get a clean baseline build (no gameplay changes yet).
4. Stand up MariaDB + import DB, run the server, connect once.
5. Only then start `.docs/ARCHITECTURE.md` prototype work.

You've got this — same craftsmanship you brought to Thorne-UI, now on the server side.
