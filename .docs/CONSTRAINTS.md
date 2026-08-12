# Thorne-EQ Constraints & Boundaries

## Purpose

This document captures the non-negotiable technical realities that shape all server-side design in `thorne-eq`.

## Primary Constraint: EQ Client Contract

The EverQuest client defines hard assumptions around:

- class identity presentation,
- spellbook/spell gem interaction expectations,
- packet formats and state transitions,
- UI affordances for abilities and roles.

### Implication

We must design hybrid systems that are:

- **server-authoritative**,
- **client-compatible**,
- **incrementally applied**.

## Constraint Categories

## 1) Class & Spell Eligibility

- Client-visible class semantics exist, even if server rules add overlays.
- Some eligibility behavior may require server-side reinterpretation rather than client mutation.
- Avoid designs that require broad client patching for baseline gameplay.

## 2) UI/UX Expectations

- Players still operate through classic EQ interaction models.
- Any advanced capability should map to familiar EQ verbs where possible.
- If new states are introduced, they should degrade gracefully without custom UI dependency.

## 3) Balance Risk

- Cross-class spell access can collapse role boundaries if unrestricted.
- We must limit via:

  - spell-family whitelists,
  - progression gates,
  - role penalties/tradeoffs,
  - cooldown/resource controls.

## 4) Data & Migration Safety

- Schema changes must be reversible or forward-migratable.
- Prototype flags should isolate hybrid systems from legacy rule sets.
- Existing characters/content should remain valid under disabled feature flags.

## 5) Operational Safety

- Rollouts must support:

  - per-character testing,
  - per-zone or per-rule-set enabling,
  - rapid rollback paths.

## Zeal / Extension Position

**Updated posture (2026-08-11):** approved client DLLs are a **permitted enhancement layer**,
not forbidden. Zeal (CoastalRedwood `zeal.asi`), akplus, and MacroQuest-style tools may be
used. The only hard line is **no full client rewrite**.

- **Server-authoritative always** — core progression, unlocks, and eligibility run server-side.
- Client DLLs provide **UX and convenience** (custom windows, gauges, readouts), never authority.
- Server behavior must remain coherent for a stock client path (DLLs optional, not required).

## Design Rule of Thumb

If a feature requires the client to fundamentally understand a new class system, it is likely too aggressive for initial milestones.

Prefer:

- server-side unlocks,
- selective spell-family allowance,
- explicit progression milestones,
- messaging and tooling that explains state clearly.
