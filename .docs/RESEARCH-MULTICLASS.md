# Research — Multi-Class EQ Projects

> Living notes on how other EverQuest emu projects implement multi-classing, to learn from
> and borrow. Captured per the "script/save everything" principle. Deep code analysis is
> staged as a follow-up (clone THJ as a reference and grep it).

## Sources (confirmed)

| Project | What it is | Source / link | Client |
| --- | --- | --- | --- |
| **The Heroes' Journey (THJ)** | Multiclass progression server; the project this repo's vision cites | **Open source: `firestormalpha/TheHeroesJourneyServer`** (branch `staging`, ~138 MB) | RoF2 |
| **PerkyCrew** | Solo/duo-friendly; "multiclass-style AA choices", Rebirth, custom end-game | perkycrewserver.com (server; source not confirmed) | RoF2 |
| **Ascendant** | EQEmu progression server (mentioned alongside) | (to confirm) | RoF2 |
| **EQ Classless 3.0** | Classless on the **Mac client** — already on disk | `B:\SecretsOTheP\classless-dll` (MQ2-style client DLL) | Mac/TAKP |

## Early takeaways (from public info)

- **THJ multiclass = a fixed 3-class combo** chosen by the player (e.g. `clr/rog/sk`,
  `clr/mnk/xx`), not free-form classless. This matches our **"curated, not classless"** pillar
  — a strong validation of the declaration-first direction.
- THJ leans heavily on **AA** for cross-class power and QoL ("op hammer pet", etc.), and is
  **solo/duo tuned** — same north star as ours (small groups do big content).
- **PerkyCrew** frames multiclass as **AA choices + Rebirth** (a prestige/respec loop) rather
  than raw class stacking — a lighter-weight model worth comparing to our Equalizer (Phase 5).
- **Client difference matters:** THJ/PerkyCrew/Ascendant are **RoF2**; we are **Mac/TAKP**.
  Their UI-driven mechanics (custom windows, pet bags) may not port — but their **server-side**
  class/spell/AA handling is the transferable part. Cross-check against EQ Classless 3.0
  (`B:\SecretsOTheP\classless-dll`), which is our on-client precedent.
- **IP/legal note:** several emu servers (incl. THJ) hit Daybreak legal action in 2025; Quarm
  returned under an agreement. Keep Thorne-EQ private/personal and IP-careful.

## Findings — how they actually do it (from cloned source)

Reference clones on `B:` (org = top-level dir, matching the existing convention):
`B:\FirestormAlpha\TheHeroesJourneyServer` (THJ), `B:\SecretsOTheP\classless3` (EQ Classless 3.0),
`B:\SecretsOTheP\eq-core-dll`.

### THJ — class **bitmask** overlay (this is our blueprint)

THJ makes a character *be* multiple classes via a **class bitmask**, and overlays it at every
place the code used to check a single `GetClass()`:

- **Storage:** a per-character class bitmask kept in a data value (guild code reads
  `SELECT db.value AS class_bitmask`) — i.e. the `data_buckets` pattern.
- **Helpers** (`zone/mob.h`, `zone/client.cpp:14452`): `uint32 GetClassesBits()` and
  `bool HasClass(uint8 class, uint32 bitmask=0)`. `GetPlayerClassBit(class_id)` -> the bit.
- **Spell eligibility** (`zone/spells.cpp:1303`): iterate the character's class bits; for a
  spell, take the **lowest `spells[id].classes[class_id-1]` among the classes they have**.
  This **preserves the per-class spell chains** (a Necro+Mage casts a Mage spell at the Mage
  min-level) — exactly the goal. No classless bypass.
- **Items / AA / skills:** `IsEquipable(race, GetClassesBits())`, AA checks
  `(ability->classes >> 1) & GetClassesBits()`, etc. — the bitmask replaces the single class.
- **Feature-flagged:** `RuleB(Custom, MulticlassingEnabled)` (+ `UseDynamicAATimers` to
  deconflict multiclass AA timers, and `ServerAuthStats`).
- **Curated:** THJ ships fixed 3-class combos, not free-form — matches "curated, not classless".

### classless3 — the anti-pattern (what NOT to do)

EQ Classless 3.0 (our Mac lineage) adds a `CLASSLESS` class = **17** (`common/classes.h`) and
**bypasses** class restrictions where `GetClass() != CLASSLESS`. Its `CanUseSpell` is stock/
unused. That's a blanket "any class casts anything" — the classless model we explicitly reject.
Useful only as a map of the same choke points (item `Classes` bitmask, `spells[].classes[]`).

## Our adaptation (unique to Thorne-EQ)

Borrow THJ's **bitmask-overlay** mechanism, keep our **curated declaration** design:

1. Store **declared classes** as a bitmask in `data_buckets` (primary class always set; secondaries
   earned + curated by a matrix). Not a client-known second class (Mac client stays single-class).
2. Add `GetClassesBits()` / `HasClass()` to `Mob`/`Client` (port THJ's helpers to EQMacEmu).
3. Overlay **cast-time** eligibility in `CanUseSpell`/spell scribe: usable if **any declared class**
   qualifies, using that class's min-level -> **spell chains preserved**. `AND NOT` hard-forbidden.
4. Gate behind a `rule_values` flag (our `MulticlassingEnabled`); watch AA-timer deconfliction.
5. Later (Phase 5): the Equalizer point-buy tunes *how far* each declared line goes (tiers/caps).

**Net:** THJ proves the exact architecture works server-side; we implement a curated, declaration-
gated version on the Mac lineage (where classless3 shows the same choke points). Ascendant /
PerkyCrew are closed-source (no repos) — treated as design inspiration only (AA-choices + Rebirth).

## Verified code extraction (diff pass, 2026-08-12)

Ran a THJ-vs-EQEmu-upstream comparison (`B:\FirestormAlpha\TheHeroesJourneyServer` vs
`B:\EQEmu\EQEmu`, saved under `.reports/thj_diff/`). **Method caveat:** THJ forked an
**older** EQEmu (note the GPLv2->v3 relicense, `#pragma once` vs `#ifndef`, include-path
refactor in current upstream), so whole-file diffs are dominated by **fork-age drift**, not
multiclass logic (`mob.h` = 588, `client.h` = 732 diff lines, mostly noise). The reliable
method is **symbol-targeted extraction** — and we port to EQMacEmu **by logic, not by patch**
(EQMacEmu diverges again).

**`Client::GetClassesBits()`** (`zone/client.cpp:14452`) — verified body:

```cpp
uint32 Client::GetClassesBits() const {
    if (RuleB(Custom, MulticlassingEnabled))
        return m_pp.classes;                    // live per-char bitmask
    else
        return GetPlayerClassBit(m_pp.class_);  // stock single-class fallback
}
```

- **Storage (THJ):** the bitmask lives in `m_pp.classes` (a PlayerProfile `uint32`) **and** a
  `GestaltClasses` data_bucket (`SetBucket("GestaltClasses", ...)`). Rule-off returns the
  single-class bit -> **identical to stock behavior when disabled**.
- **Declaration API:** `AddExtraClass()` / `RemoveExtraClass()` (`client.cpp:14461+`). Caps at
  **3 classes total** (`class_count > 2` -> reject) — the curated ceiling. NPC-callable.
- **Class range:** THJ loops `Class::Warrior .. Class::Berserker` (**1..16**). Mac/Quarm has
  **no Berserker** — our loop is **1..15** (Beastlord). Porting delta.

**Spell eligibility overlay** (`zone/spells.cpp:1303`, and `common/spdat.cpp:1012` for the
min-level helper) — verified: iterate the character's set class bits and take the **lowest**
`spells[spell_id].classes[class_id-1]` among them. A Necro+Mage casts a Mage spell at the
**Mage** min-level. **Spell chains preserved** — confirmed, exactly our goal.

### Storage decision for Thorne-EQ (answers "store it uniquely + efficiently")

THJ reuses `m_pp.classes` — a **client-synced PlayerProfile field**. On the **Mac client** the
PP struct is fixed and client-authoritative; repurposing a field risks desync and violates our
`CLIENT-STRATEGY.md` "T0-T2 only" rule. **Our approach:** keep the declared bitmask **purely
server-side** and have `GetClassesBits()` read it there, never touching the client PP:

- **Option A (portable, THJ-style):** `data_buckets` key (e.g. `thorne.classes`) — schema-change-
  free, rebuild-portable, but string-typed and one row per key.
- **Option B (unique + queryable):** a dedicated `thorne_character_build` table
  (`char_id`, `class_bits`, `primary_class`, affinity/allocation columns) — one row per
  character, integer-typed, JOIN-friendly for future Equalizer/affinity queries; costs a
  tracked migration in `db/bootstrap/`.
- **Leaning:** start with **A** for the Phase 1 spike (fast, reversible), migrate to **B** when
  affinity + Equalizer need real columns. Either way, `GetClassesBits()` is the single read
  point, so the storage swap is internal. (Tracked in `BACKLOG.md` parking lot.)

### Phase 1 port checklist (EQMacEmu, when unblocked)

1. `common/ruletypes.h`: add `RULE_BOOL(Custom, MulticlassingEnabled, false, ...)` (default
   **off** — safer than THJ's `true`).
2. `common/classes.*`: confirm `GetPlayerClassBit()` exists (stock); add `GetPlayerClassIDByName()`
   if we want NPC name->id (THJ helper).
3. `Client::GetClassesBits()` overlay reading the **server-side** store (not `m_pp`), rule-gated
   with single-class fallback; loop **1..15**.
4. `Mob::HasClass(class, bitmask=0)` helper.
5. Spell-eligibility overlay at EQMacEmu's equivalent of `spells.cpp:1303` — lowest min-level
   among declared classes; **and NOT** hard-forbidden by our curated matrix.
6. Declaration entry point (curated/gated `AddExtraClass` equivalent), driven by an NPC per
   `CLIENT-STRATEGY.md` — not char-create.

**Gate:** do NOT start until the **stock, unmodified** server is verified running and a client
login test passes.
