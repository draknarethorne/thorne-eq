# Copilot Instructions — Thorne-EQ

## Project identity

Thorne-EQ is the **server-side** companion to Thorne-UI. It targets a custom, Quarm-compatible EverQuest server built from the EQMacEmu (Al'Kabor) lineage, with a long-term goal of **curated, server-authoritative hybrid class progression** inspired by UO, Diablo, Asheron's Call, and Hero's Journey — while staying compatible with the classic EQ client.

- Maintainer alias: **Draknare Thorne**
- Companion repo: `draknarethorne/thorne-ui` (client UI, TAKP Quarm)
- This repo: `draknarethorne/thorne-eq` (server behavior, content, rules)

## Codebase reality (once server code is imported)

- Language: **C++20** (server core), Perl + Lua (quests/scripting), SQL (MariaDB schema).
- Build system: **CMake** (>= 3.12).
- Toolchain: **Visual Studio 2026 (MSVC, Desktop C++ workload)** on Windows.
- Dependencies on MSVC are auto-fetched via `cmake/DependencyHelperMSVC.cmake`
  (Boost, MySQL/MariaDB connector, ZLIB, OpenSSL, Lua51, LuaJit).
- Database: **MariaDB 10.3.x** (Al'Kabor-era compatibility).
- Server processes: `loginserver`, `world`, `zone`, `ucs`, `queryserv`, `shared_memory`.

## Guiding principles

1. **Server-authoritative.** Progression, unlocks, and restrictions are enforced server-side.
2. **Client-compatible.** Do not require broad EQ client rewrites. Zeal/extensions are optional UX, not core authority.
3. **Curated, not classless.** Hybrid capability comes from earned affinities and whitelisted spell families — never "all classes cast everything."
4. **Reversible + flagged.** Prefer feature flags, staged rollouts, and forward-migratable schema changes.
5. **Era respect.** Preserve TAKP/Quarm tone and role clarity.

## Working conventions

- Docs live in `.docs/` (hidden from tooling noise, uppercase-hyphen filenames).
- Agent definitions live in `.github/agents/`.
- Use Conventional Commits: `feat|fix|docs|chore|refactor|build(scope): summary`.
- Scope examples: `zone`, `world`, `spells`, `db`, `affinity`, `archetype`, `build`, `docs`, `repo`.
- Keep changes small and testable; document rule decisions in plain language before implementing.

## Source-of-truth order

`VERSION` → `README.md` → `.docs/ROADMAP-*.md` → `.docs/ARCHITECTURE.md` → `.docs/CONSTRAINTS.md`.
If in doubt, trust the running server + upstream code, then update docs to match.

## Safety

- Never push force to shared branches without explicit confirmation.
- Never commit secrets (DB passwords, tokens) — use local config files ignored by git.
- Validate builds after dependency or CMake changes.
