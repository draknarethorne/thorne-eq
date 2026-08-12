# Local Setup — Windows + Visual Studio 2026

This is your ground-zero, first-time setup for building and running the Thorne-EQ server
(EQMacEmu / Quarm lineage) on Windows. It assumes you are new to C++ server builds but
comfortable with tooling. Take it one section at a time.

> **VERIFIED 2026-08-11 — the baseline now builds and runs.** Key corrections vs the
> original draft: this fork has **no git submodules**; MariaDB should be run **portable**
> (the MSI can fail on some Windows setups); CMake needs `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`.
> Folder layout: `C:\Thorne-EQ\{server,quests,maps,mariadb}` + client at `C:\TEQ`.
> The `.docs/` companions `DECISIONS.md`, `ROADMAP.md`, `MULTI-CLASS-DESIGN.md` carry the plan.
>
> **Now scripted:** the day-to-day flow (start MariaDB, assemble the run dir, start/stop/
> shutdown the process chain, import/bootstrap the DB) is automated by `.bin/control_server`
> and `.bin/manage_database`. This guide remains the ground-truth explanation of *what*
> those scripts do; the live database is named **`quarm`**.

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

> Dependencies (Boost, MariaDB connector, ZLIB, OpenSSL, LuaJit, libsodium, mbedTLS) are
> **fetched automatically via vcpkg** at CMake-configure time. You do NOT install them by
> hand. (MySQL and Lua51 report MISSING but the build uses MariaDB + LuaJIT instead — fine.)

---

## 2) Install the database (MariaDB 10.3 — portable recommended)

EQMacEmu targets MariaDB 10.3. **The MSI installer can fail** on some Windows setups with
`InnoDB: Unable to create temporary file; errno: 0` (broken Windows service-account temp
dir). **Use the portable ZIP** and run it as your user instead:

1. Download the portable ZIP:
   <https://archive.mariadb.org/mariadb-10.3.39/winx64-packages/mariadb-10.3.39-winx64.zip>
2. During install:
   - Set a **root password** you will remember (used later in config).
   - Enable "Use UTF8 as default server's character set" if prompted.
   - Keep the default service name/port (`3306`).
3. Confirm the service is running (Windows Services → `MariaDB`).
4. Optional GUI: install **HeidiSQL** (bundled with MariaDB) to browse the DB.

Create an empty database (via HeidiSQL or CLI):

```sql
CREATE DATABASE quarm CHARACTER SET utf8;
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

> If configure fails with `Compatibility with CMake < 3.5 has been removed` (vendored
> `submodules/libuv`), add `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`. If the build errors only on a
> post-build `applocal.ps1` / `powershell ... exited with code 9009` step, the code already
> built — just copy `vcpkg/vcpkg-export-x64/installed/x64-windows/bin/*.dll` next to the exes.

---

## 6) Server configuration

1. Copy the sample config to `eqemu_config.json` in your run directory.
2. Set database connection:
   - host: `127.0.0.1`
   - port: `3306`
   - username: `root` (or a dedicated user)
   - password: your MariaDB root password
   - database: `quarm`
3. Set world `shortname`/`longname` (your server's identity).

> Keep real passwords out of git. Use a local config that is gitignored.

---

## 7) Import the database

From the server source `utils/sql/database_full` (or the linked DB dump):

1. Unzip the dump if compressed.
2. Import all provided `.sql` files into the `quarm` database (HeidiSQL: File → Load SQL,
   or CLI `mysql -u root -p quarm < file.sql`). In practice, use
   `manage_database.bat import --dump <dump>`, which handles the Quarm dump quirks.
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

- **CMake configure fails** → add `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`; verify the C++
  workload. Delete `build/` and reconfigure.
- **Linker errors** → dependency auto-fetch incomplete; clean build and reconfigure.
- **DB connection refused** → MariaDB service down or wrong credentials in
  `eqemu_config.json`.
- **Quests not firing** → Strawberry Perl x64 not on PATH, or wrong quests path.
- **Client can't see server** → login server not running, wrong `eqhost.txt`, or port
  mismatch.

---

## Next steps

The baseline builds and connects to the DB. See `.docs/ROADMAP.md` for the phased plan; the
next gameplay step is the Phase 1 multi-class cast-time spike in `.docs/MULTI-CLASS-DESIGN.md`.
