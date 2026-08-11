# Thorne-EQ

Server-side evolution project for TAKP/Quarm-era EverQuest gameplay, crafted to preserve classic client feel while enabling controlled, modernized progression systems.

## Vision

`thorne-eq` explores a **server-driven hybrid class model** inspired by the character agency of games like Ultima Online, Diablo, Asheron's Call, and Hero's Journey—while staying grounded in EverQuest client realities.

Core intent:

- Keep the EQ client as the canonical gameplay surface.
- Drive advanced progression from server-side rules, data, and scripts.
- Allow **curated cross-class spell access** (not unrestricted classless play).
- Support “identity blends” such as a **warrior-druid-necromancer** archetype through unlock paths, not free-for-all spell access.

## Design Pillars

1. **Era Respect First**
   - Preserve TAKP/Quarm tone and pacing where possible.
   - Add systems that feel native to classic EQ instead of replacing EQ’s identity.

2. **Server Authority**
   - Unlocks, restrictions, progression gates, and balancing are server-enforced.
   - Client remains mostly unchanged; optional enhancements via Zeal-compatible workflows.

3. **Curated Hybridization**
   - Hybrid capability comes from earned unlocks and affinity tracks.
   - Spell families are intentionally limited per archetype path.

4. **Progression Through Skills**
   - Character growth extends beyond base class leveling through controlled skill tracks.
   - Skill tracks influence allowed spell lines, utility verbs, and role specialization.

5. **Safety + Iteration**
   - Build in feature flags and staged rollouts.
   - Ship in small increments with measurable impact.

## What This Is (and Is Not)

### This is

- A server-side framework and content strategy for advanced class capability systems.
- A long-term project plan built around Quarm-specific compatibility.
- A place to prototype lock/unlock progression and affinity-driven spell access.

### This is not

- A full rewrite of EQ class design.
- Unrestricted “all classes can cast everything.”
- A replacement for client constraints—those constraints are design inputs.

## Initial Scope

- Define a **Class Affinity Matrix** (what cross-class lines are ever allowed).
- Define **Unlock Tokens / Milestones** for hybrid capability progression.
- Implement first prototype archetype path:
  - Example: `Warrior -> Warden of Ash (warrior+druid+necromancer facets)`
- Enforce spell eligibility server-side based on:
  - class baseline,
  - unlocked affinities,
  - restricted spell-family flags,
  - progression milestones.

## Technical Strategy (High-Level)

- Base code target: Quarm-aligned server lineage (`SecretsOTheP/EQMacEmu` likely reference point).
- Keep compatibility with existing EQ client packet/behavior boundaries.
- Use server rules + database flags + scripts to:
  - gate abilities,
  - remap eligibility,
  - tune power curves,
  - preserve role clarity.
- Use Zeal/extensions where helpful, but avoid hard dependency for core progression logic.

## Repository Layout

- `.docs/CONSTRAINTS.md` — hard boundaries from EQ client + practical server implications.
- `.docs/ARCHITECTURE.md` — proposed system architecture for hybrid class capability.
- `.docs/ROADMAP-v0.1.0.md` — first milestone implementation roadmap.
- `.docs/LOCAL-SETUP-WINDOWS.md` — ground-zero Windows + Visual Studio 2026 build guide.
- `.docs/TRANSITION-TO-SERVER-CODE.md` — source intake (fork vs import) decision + kickoff.
- `.github/agents/` — server-side agent modes (Server, Architect, Build).
- `.github/copilot-instructions.md` — repo-wide working conventions.

## Getting Started

1. Read `.docs/LOCAL-SETUP-WINDOWS.md` for the full first-time build walkthrough.
2. Use `.docs/TRANSITION-TO-SERVER-CODE.md` to decide how to fork/import the server code.
3. Aim for a clean baseline build before starting hybrid-class prototype work.

## Working Agreement

- Start conservative, test often, avoid irreversible schema choices.
- Favor toggles and backward-compatible migration paths.
- Document every rule decision in plain language before implementation.

## Status

- **Phase:** Foundation / Planning
- **Version:** `0.1.0-dev`
- **Maintainer:** Draknare Thorne
