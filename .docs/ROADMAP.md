# Thorne-EQ Master Roadmap

> Single source of truth for **how we get from nothing running to a proven multi-class
> playstyle**. Supersedes the scope-only `archive/ROADMAP-v0.1.0.md`.
> Companion docs: `DECISIONS.md` (choices), `BACKLOG.md` (itemized wants),
> `MULTI-CLASS-DESIGN.md` (the crux design).

## Guiding principle

**Prove the multi-class system and its playability before anything else.** Sustain,
loot, travel, AA, GM tiers, and Diablo-style polish are all secondary. If we can't make
a curated multi-class character *fun and playable* on the TAKP/Quarm client, none of the
bells and whistles matter. Every phase ships in a small, testable chunk behind a feature
flag, with an explicit **exit test**.

## Phase map (at a glance)

| Phase | Name | Goal | Status |
| ---: | --- | --- | --- |
| 0 | Baseline Bring-up | Server builds & runs; client connects | In progress |
| 1 | Multi-Class Spike | Prove cast-time cross-class access works on this client | Next |
| 2 | Declaration MVP | Earned secondary classes via item, combat-locked swap | Planned |
| 3 | Playability Tuning | Make a 2-3 hybrid group actually fun & sustainable | Planned |
| 4 | Casual Enablers | Low-pop QoL: bags, xp/AA, drops, GM tiers, AFK | Planned |
| 5 | Equalizer Layer | Optional point-buy caps/tiers on top of declaration | Optional |
| 6+ | Bells & Whistles | Diablo affixes, AA trees, Zeal UI, archetypes | Icebox |

---

## Phase 0 — Baseline Bring-up (in progress)

Get an unmodified Secrets/EQMacEmu server building and running, with the `C:\TEQ` client
connecting through Zeal. No gameplay changes yet.

- [x] Fork `SecretsOTheP/EQMacEmu` + `quests`; clone to `server/`, `quests/`, `maps/`
- [x] Locate in-repo Quarm DB dump (`quarm_2026-03-20`) — matches live Quarm
- [ ] Stand up MariaDB (portable, due to Windows service-temp issue) + import DB
- [ ] Seed a GM login account (auto-create enabled)
- [ ] Build server (VS 2026 MSVC, RelWithDebInfo)
- [ ] Write `eqemu_config.json` (localhost, gitignored); run login/world/zone
- [ ] Point `C:\TEQ\eqhost.txt` -> `127.0.0.1`; stage Zeal + eqw + Thorne-UI

**Exit test:** log in, create a character, zone in, `/zeal version` works.

---

## Phase 1 — Multi-Class Spike (the de-risking test)

The single cheapest experiment that answers the make-or-break question:
**can the server grant cross-class spell use at cast time on the stock client + Zeal, or
do we need a client DLL patch for scribing?**

- [ ] Pick a test anchor + one secondary (proposal: Necromancer + Magician) — see `DECISIONS.md` D1
- [ ] Temporarily flag a handful of Magician spells usable in `spells_new` for the anchor
- [ ] Observe: can the client **scribe** them? **memorize**? **cast**? (server logs + in-game)
- [ ] Add a minimal server override in `CanUseSpell()` (behind a rule flag) as the real path
- [ ] Record findings in `MULTI-CLASS-DESIGN.md` (enforcement decision D6)

**Exit test:** a Necromancer casts a normally-barred Magician spell, gated entirely
server-side, toggled by a `rule_values` flag. We know definitively whether scribe-time
needs Zeal/akplus help.

**Why first:** everything in Phase 2+ assumes the answer. Cheap to run, high information.

---

## Phase 2 — Declaration MVP

Turn the spike into a real, data-driven, curated system — no cap math yet.

- [ ] `data_buckets`-backed "declared classes" per character (primary immutable + N secondary)
- [ ] Curated class matrix table: which secondaries each primary may take (grants + prohibitions)
- [ ] `CanUseSpell()` overlay = eligible if any declared class qualifies AND not hard-forbidden
- [ ] Clicky "Tome of the {Class}" item to declare/activate a secondary (quest-granted)
- [ ] **Swap-lock**: reject role change while in combat; require safe zone or Soul Shrine
- [ ] Feature flag + per-character enable for safe testing

**Exit test:** a character declares a secondary via item, scribes/casts its spells within
curated limits, and cannot swap mid-combat.

---

## Phase 3 — Playability Tuning (find the fun)

The heart of the project: make a **2-3 hybrid group** cover roles a raid normally needs,
without collapsing role identity. Iterative; driven by playtest feel.

- [ ] Rule-driven regen: high out-of-combat recovery + modest in-combat (anti-sitting)
- [ ] Sustain as earned affinity perks (Death=leech, Nature=regen)
- [ ] Longer buff durations (rule multiplier) to cut re-buff downtime
- [ ] Nexus blessing NPC (MGB-style baseline buffs) so groups aren't hard-gated on cleric/enchanter
- [ ] Open travel (spires/translocators/clicky stones)
- [ ] Pet auto-attack + hold/guard tuning for small-group and AFK-safe camps
- [ ] Playtest: can a Necro + one hybrid clear content tuned for a bigger group?

**Exit test:** a small hybrid group has a fun, sustainable loop; roles feel earned, not trivial.

---

## Phase 4 — Casual Enablers (low-pop quality of life)

Cheap, high-satisfaction wins for a small population. Mostly data/rule changes.

- [ ] Bigger bags + more weight reduction; better starting gear
- [ ] XP/AA rate tuning; buffed quest xp/rewards
- [ ] Better low-level static drops (kill "always Rusty")
- [ ] AFK xp/AA farming support (auto-combat, pet guard)
- [ ] Tiered GM roles for trusted friends (respawn named, trigger quests, restricted powers)

**Exit test:** a new casual character reaches mid-game noticeably faster, with less grind friction.

---

## Phase 5 — Equalizer Layer (optional depth)

Only if the Declaration MVP proves fun and wants more expression: layer the point-buy
"Attunement" caps/tiers (see `DESIGN-SKILL-CAP-SYSTEM.md`) on top of the same choke points.

- [ ] Point budget by level (`data_buckets`), native/secondary/tertiary tiers
- [ ] `skill_caps` overlay for per-channel cap deltas
- [ ] Re-spec via consumable (RIFT-style)

**Exit test:** players meaningfully trade off channels; builds feel distinct without going classless.

---

## Phase 6+ — Bells & Whistles / Icebox

Deferred until the core loop is proven. Tracked in `BACKLOG.md`.

- Diablo-style random item affixes + rarity colors (large build; augments absent)
- Expanded AA trees (THJ-style), verify Quarm coverage first
- Named archetype presets (Warden of Ash, etc.)
- Zeal custom "Attunement" panel + gauges/labels
- Deeper world/travel and endgame (Planes-focused) content

---

## How we work each phase

1. Pick the smallest slice with a clear exit test.
2. Put it behind a `rule_values` flag; enable per-character or per-zone first.
3. Playtest, capture metrics/notes, decide: iterate, ship wider, or revert.
4. Update `DECISIONS.md` and `BACKLOG.md` as choices are made.
5. Keep changes forward-migratable; never an irreversible global change in one step.
