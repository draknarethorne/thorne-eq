# Design — The Attunement System (Point-Buy Skill/Spell Cap "Equalizer")

> Status: **Ideation / captured vision** (not yet implemented). This document exists to
> preserve and sharpen the core idea so an Architect + Server session can execute it.

## The Big Idea

Break the mold of EQ's fixed single-class system without becoming a classless free-for-all.

Instead of picking one rigid class, a character has a **primary identity** plus a
**budget of points** they allocate across **cap channels** — like a graphic-equalizer /
multi-point star. Where you raise the sliders defines which skills, spell lines, and
spell tiers you can access. Raising one channel means you can't max another. The budget
grows as you level, giving you increasing control over your build.

**Goal:** let a small group of **2-3 hybrid adventurers** cover the roles that normally
require a full raid — while preserving classic EQ feel and role tradeoffs.

## What it is NOT

- Not single-class rigidity.
- Not "all classes can cast everything."
- Not a fixed 3-class combo.

## What it IS

- A **point-buy cap system** layered on top of EQ's existing skill/spell constructs.
- A **primary class anchor** that sets floors (and identity) you can't drop below.
- A **tradeoff economy**: points spent raising casting caps are points not spent on melee.
- **Server-authoritative**, client-compatible, and ideally adjusted through **items/potions**
  rather than a custom UI.

## Inspirations (and what we borrow)

- **Rift (souls / respec / points)** — flexible allocation and re-spec agency.
- **Ultima Online / Asheron's Call** — use/earn-based skill advancement, soft caps.
- **Diablo** — build identity through selective investment.
- **Hero's Journey EQ** — deeper class fantasy on an EQ base.

Borrow: point allocation, cap tradeoffs, re-spec, and progression-driven control.
Avoid: full classlessness and anything requiring EQ client rewrites.

## Core Model

## 1) Primary Identity (Anchor)

- Character keeps a canonical base class (e.g., Necromancer).
- The anchor defines:
  - **floor caps** (things you can never reduce — a warrior keeps core melee floors),
  - baseline identity and starting channel weights,
  - which channels are "native" (cheaper) vs "foreign" (costlier).

## 2) Cap Channels (the Equalizer sliders)

- A channel = a tunable cap on a skill or spell line, e.g.:
  - Melee channels: 1H/2H, defense, dual wield, etc.
  - Casting channels: Necromancy(Death), Conjuration(Elemental/Summoning),
    Alteration(Healing), Evocation(Nuke), Abjuration(Wards), etc.
- Each channel has a **current cap** and a **max reachable cap** (gated by anchor + tier).
- Raising a channel's cap costs **Attunement Points**.

## 3) Attunement Points (the budget)

- Earned on level-up (like stat/skill points) — increasing control as you grow.
- Total budget is finite → **you cannot max everything**.
- Re-spec possible (cost/cooldown TBD) to support experimentation (Rift-like).

## 4) Access Tiers (how far a foreign line can go)

- **Primary line** (native): full progression.
- **Secondary lines** (e.g., Necro branching into Magician/Elementalist): high but capped.
- **Tertiary lines** (e.g., a little Druid/Cleric healing): limited tier, higher point cost.
- Anchor class determines which tiers are reachable for which lines (curated matrix).

## 5) Adjustment Interface (fits EQ client)

- Prefer **consumable items / potions / tomes** to spend or re-allocate points:
  - "Tome of Attunement" grants/points,
  - "Elixir of Reweaving" triggers a re-spec,
  - vendor/quest turn-ins to buy/sell channel investment.
- This avoids a custom UI dependency and rides EQ's existing item-click/turn-in flows.
- Zeal/extensions may add optional readouts, but are not required.

## How This Maps to EQ Server Constructs (already ~80% there)

The fundamentals largely exist in the EQEmu/EQMac schema — we're unlocking and layering,
not inventing from scratch.

- **`skill_caps`** (class, skill, level → cap): the primary lever for per-skill caps.
  - We overlay a per-character delta driven by allocated points.
- **`spells_new`** class columns (`classes_1..16` = min level per class; `255` = barred):
  - Spell-line access is already class-gated by min level; we reinterpret eligibility
    server-side based on the character's channel investment + tier, not just base class.
- **`character_skills`**: learned skill values (bounded by effective cap).
- **`rule_values`**: feature flags / global toggles for staged rollout.
- **`data_buckets`** (per-character key/values): store allocation state and channel caps.
- **`char_create_*` / race-class stat defaults**: precedent that caps/defaults are
  already data-driven — we extend that philosophy to a spendable budget.

### The key server insight

EQ already computes an **effective cap** per skill and an **eligibility** per spell.
The Attunement System injects a **per-character modifier layer** into those two
decisions:

```text
effective_skill_cap(char, skill, level)
  = base_skill_cap(class, skill, level)         # existing skill_caps
  + attunement_channel_bonus(char, skill)       # NEW: point-buy overlay
  clamped to [class_floor, tier_max]

spell_is_usable(char, spell)
  = base_class_eligible(spell, class, level)    # existing spells_new gating
  OR attunement_line_unlocked(char, spell_line, tier)   # NEW: curated overlay
  AND NOT hard_forbidden(spell_line, char)      # protect fantasy boundaries
```

## Balance Levers (to prevent collapse)

- Finite point budget + floor caps + tier ceilings.
- Foreign lines cost more points than native lines.
- Optional resource/cooldown penalties for off-anchor power.
- Hard prohibition list (some lines never open to some anchors).
- Small-group power should feel earned, not trivializing.

## Open Questions (to resolve in ideation)

- Exact channel taxonomy (map EQ skills + spell lines to channels).
- Point budget curve by level (how fast control grows).
- Re-spec cost/cooldown and whether it's item-gated.
- Which lines are tertiary-capped vs fully barred per anchor.
- How healing access is limited so 2-3 group play is strong but not god-mode.

## First Prototype Slice (proposed)

1. Pick one anchor (Necromancer).
2. Define 3 channels: `Death (native)`, `Elemental (secondary)`, `Healing (tertiary)`.
3. Implement point budget in `data_buckets`; overlay `skill_caps` + spell eligibility.
4. Gate everything behind a `rule_values` feature flag.
5. Drive allocation with a single test item ("Tome of Attunement").
6. Measure: can a Necro+X duo clear content tuned for a larger group without breaking roles?

## Related Docs

- `.docs/MULTI-CLASS-DESIGN.md` — current crux design (this Equalizer is its Phase 5 layer).
- `.docs/ROADMAP.md` — master phased plan.
- `.docs/CONSTRAINTS.md` — client/server boundaries.
