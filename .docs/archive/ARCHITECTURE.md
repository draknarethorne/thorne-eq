# Thorne-EQ Hybrid Capability Architecture (Draft)

> **Current direction lives in `.docs/MULTI-CLASS-DESIGN.md`** (grounded in the server source).
> This draft is the conceptual capability-resolver model it builds on.

## Goal

Enable curated multi-class-like progression while preserving EQ client compatibility and server operational safety.

## Core Concepts

## 1) Base Class (Immutable Identity Anchor)

- Character retains a canonical base class identity.
- Base class determines foundational progression and baseline permissions.

## 2) Affinity Tracks (Earned Secondary Domains)

- Affinity tracks represent controlled access to non-base-class domains.
- Example tracks: `Nature`, `Death`, `Protection`, `Tactics`, etc.
- Tracks are levelled/unlocked by milestones, achievements, or content gates.

## 3) Spell Family Whitelists

- Spells are grouped into server-defined families.
- Access is granted by `base class + affinity threshold + feature flags`.
- This avoids broad classless access while enabling archetype expression.

## 4) Archetype Profiles

- Archetypes are named presets built from affinity combinations.
- Example: warrior-focused profile with selective druid/necromancer lines.
- Archetypes define both grants and prohibitions.

## 5) Capability Resolver (Server-Side)

- Runtime resolver computes whether a character can use a spell/ability.
- Inputs:

  - base class,
  - active affinities,
  - progression milestones,
  - zone/server rules,
  - feature flags.

## Suggested Data Model (Conceptual)

- `character_affinity_progress`
  - character_id
  - affinity_id
  - rank
  - unlocked_at

- `spell_family`
  - spell_id
  - family_id
  - family_tag

- `archetype_profile`
  - profile_id
  - name
  - description
  - enabled

- `archetype_profile_grants`
  - profile_id
  - affinity_id / spell_family_id
  - min_rank

- `archetype_profile_limits`
  - profile_id
  - forbidden_family_id
  - condition

- `feature_flags`
  - flag_key
  - scope
  - enabled

## Enforcement Points (Server)

1. Learn/mem rules validation
2. Cast-time permission checks
3. Item click/scroll invocation checks
4. NPC script-driven grants and revocations
5. Zone or ruleset-level overrides

## Balance Levers

- Family-by-family access control
- Rank thresholds for stronger lines
- Opportunity cost (slower progression, reduced caps, or maintenance costs)
- Cooldown/resource penalties for off-domain power
- Hard prohibition lists to protect class fantasy boundaries

## Incremental Delivery Strategy

1. Start with one prototype archetype profile.
2. Enable only on test scope/ruleset.
3. Capture metrics:
   - power deltas,
   - group composition impacts,
   - spell usage distribution,
   - player friction points.
4. Iterate before broadening access.

## Non-Goals (Early Milestones)

- Fully classless systems
- Massive client UI rewrites
- Irreversible global rebalance in one patch
