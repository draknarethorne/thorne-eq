# Research — Multi-Class EQ Projects

> Living notes on how other EverQuest emu projects implement multi-classing, to learn from
> and borrow. Captured per the "script/save everything" principle. Deep code analysis is
> staged as a follow-up (clone THJ as a reference and grep it). Companion: `RESEARCH-CLIENT.md`
> (client architecture), `RESEARCH-PLAYABILITY-SYSTEMS.md` (non-multiclass tuning).

## Sources (confirmed)

| Project | What it is | Source / link | Client | Server base | Multiclass model |
| --- | --- | --- | --- | --- | --- |
| **The Heroes' Journey (THJ)** | Multiclass progression server; the project this repo's vision cites | **Open source: `firestormalpha/TheHeroesJourneyServer`** (branch `staging`, ~138 MB) | RoF2 | EQEmu (older fork) | Fixed 3-class combos (560 total) |
| **PerkyCrew** | Solo/duo-friendly; "multiclass-style AA choices", Rebirth, custom end-game | perkycrewserver.com (server; source not confirmed) | RoF2 | EQEmu derivative | AA choices + Rebirth respec |
| **Ascendant** | EQEmu progression server (community-maintained, March 2026) | **Open source: `Ascendant-EQ-Emu/Ascendant-Server`** (GitHub) | RoF2 | SecretsOTheP/Server fork | Undocumented (likely not a focus) |
| **EQ Classless 3.0** | Classless on the **Mac client** — already on disk | `B:\SecretsOTheP\classless-dll` (MQ2-style client DLL) | Mac/TAKP | EQMacEmu | True classless (any-class-casts-anything) |

## Early takeaways (from public info)

- **THJ multiclass = a fixed 3-class combo** chosen by the player (e.g. `clr/rog/sk`,
  `clr/mnk/xx`), not free-form classless. This matches our **"curated, not classless"** pillar
  — a strong validation of the declaration-first direction.
- THJ leans heavily on **AA** for cross-class power and QoL ("op hammer pet", etc.), and is
  **solo/duo tuned** — same north star as ours (small groups do big content).
- **PerkyCrew** frames multiclass as **AA choices + Rebirth** (a prestige/respec loop) rather
  than raw class stacking — a lighter-weight model worth comparing to our Equalizer (Phase 5).
- **Client difference matters:** THJ/PerkyCrew/Ascendant are **RoF2**; we started **Mac/TAKP**.
  Their UI-driven mechanics (custom windows, pet bags) may not port — but their **server-side**
  class/spell/AA handling is the transferable part. Cross-check against EQ Classless 3.0
  (`B:\SecretsOTheP\classless-dll`), which is our on-client precedent.
- **IP/legal note:** THJ hit Daybreak legal action (settled 2026, $3.5M damages); Quarm
  returned under an agreement. Keep Thorne-EQ private/personal and IP-careful. See
  `DECISIONS.md` for legal safety model.

---

## Server fork strategy (Phase 0-2 critical decision)

### Why server choice matters

Your choice of **EQEmu server base** locks in:
1. **Protocol support** — which client(s) you can use
2. **Multiclass feasibility** — code maturity, how much you build from scratch
3. **Long-term maintenance** — how often upstream changes affect your codebase
4. **Feature ceiling** — what Phase 4-5 features are possible (e.g., Renown UI, Equalizer panels)

### The three contenders

| Fork | Base EQEmu | Maturity | Multiclass support | Active | Best for |
| --- | --- | --- | --- | --- | --- |
| **SecretsOTheP/Server** | RoF2-capable mainline | High (2025 updates) | ❌ None yet | Yes (bleeding-edge) | Modern servers, rich feature space, development velocity |
| **SecretsOTheP/EQMacEmu** | TAKP/Mac lineage | Medium (niche) | ❌ None yet | Yes (maintained) | TAKP-only servers, era-accurate gameplay |
| **Official EQEmu** | Broadest base | Very high (stable) | ❌ None yet | Yes (conservative) | Maximum stability, largest community, slowest feature adoption |
| **THJ (firestormalpha)** | EQEmu (older fork) | High (live-tested) | ✅ Full tri-class bitmask | No (server shutdown 2025) | **Study reference** (architecture proven), **not for production** |

### Recommendation: Staged fork strategy

**Phase 0-1: Validate on EQMacEmu (you're already here)**
- Server: SecretsOTheP/EQMacEmu (your current choice)
- Client: TAKP/Mac
- Why: Validate multiclass concept on constrained, known platform
- Risk: None (reversible, isolated)
- Outcome: Prove Phase 1 spike works; answer DECISIONS.md D6 (scribe-time enforcement)

**Phase 2 boundary: Switch to SecretsOTheP/Server + RoF2**
- Server: SecretsOTheP/Server (RoF2-capable)
- Client: RoF2 (from Internet Archive, patched for EQEmu)
- Why: Rich feature space (Phase 4 Renown/Momentum UI, Phase 5 Equalizer), native window support
- Effort: ~2-3 weeks porting multiclass logic from EQMacEmu → SecretsOTheP/Server (same architecture, different opcode layer)
- Risk: Medium (new codebase), mitigated by dual-track Phase 1 validation
- Outcome: Shipping platform for Phase 2+ with full feature ceiling

**Phase 6+ (optional): Add TAKP support**
- If demand warrants, add dual-protocol support (TAKP + RoF2 in same server)
- But: Only after core loop is proven on RoF2
- Complexity: High (opcode juggling, testing both paths); not worth early investment

---

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

### Ascendant — community fork, unknown multiclass (if any)

Ascendant-Server was created March 2026, is community-maintained, but does **not publicly document** 
a multiclass system. May be a "vanilla-plus" progression server (solo/duo tuned, no multiclass). 
Useful for studying solo/duo balance tuning (Phase 3), not multiclass architecture.

---

## Our adaptation (unique to Thorne-EQ)

Borrow THJ's **bitmask-overlay** mechanism, keep our **curated declaration** design:

1. Store **declared classes** as a bitmask in `data_buckets` (primary class always set; secondaries
   earned + curated by a matrix). Not a client-known second class (client stays single-class primary).
2. Add `GetClassesBits()` / `HasClass()` to `Mob`/`Client` (port THJ's helpers).
3. Overlay **cast-time** eligibility in `CanUseSpell()`/spell scribe: usable if **any declared class**
   qualifies, using that class's min-level → **spell chains preserved**. `AND NOT` hard-forbidden.
4. Gate behind a `rule_values` flag (our `MulticlassingEnabled`); watch AA-timer deconfliction.
5. Later (Phase 5): the Equalizer point-buy tunes *how far* each declared line goes (tiers/caps).

**Net:** THJ proves the exact architecture works server-side; we implement a curated, declaration-
gated version (not free-form tri-class). Server base choice (Phase 2 pivot to SecretsOTheP/Server)
enables UI-rich Phase 4-5 features that THJ's RoF2-only design already supports.

---

## Verified code extraction (diff pass, 2026-08-12)

Ran a THJ-vs-EQEmu-upstream comparison (`B:\FirestormAlpha\TheHeroesJourneyServer` vs
`B:\EQEmu\EQEmu`, saved under `.reports/thj_diff/`). **Method caveat:** THJ forked an
**older** EQEmu (note the GPLv2→v3 relicense, `#pragma once` vs `#ifndef`, include-path
refactor in current upstream), so whole-file diffs are dominated by **fork-age drift**, not
multiclass logic (`mob.h` = 588, `client.h` = 732 diff lines, mostly noise). The reliable
method is **symbol-targeted extraction** — and we port to our chosen base **by logic, not by patch**
(each fork diverges differently).

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
  single-class bit → **identical to stock behavior when disabled**.
- **Declaration API:** `AddExtraClass()` / `RemoveExtraClass()` (`client.cpp:14461+`). Caps at
  **3 classes total** (`class_count > 2` → reject) — the curated ceiling. NPC-callable.
- **Class range:** THJ loops `Class::Warrior .. Class::Berserker` (**1..16**). Mac/Quarm has
  **no Berserker** — our loop is **1..15** (Beastlord). Porting delta on EQMacEmu; on SecretsOTheP/Server
  (RoF2-based), loop is **1..16** (matches THJ).

**Spell eligibility overlay** (`zone/spells.cpp:1303`, and `common/spdat.cpp:1012` for the
min-level helper) — verified: iterate the character's set class bits and take the **lowest**
`spells[spell_id].classes[class_id-1]` among them. A Necro+Mage casts a Mage spell at the
**Mage** min-level. **Spell chains preserved** — confirmed, exactly our goal.

### Storage decision for Thorne-EQ (answers "store it uniquely + efficiently")

THJ reuses `m_pp.classes` — a **client-synced PlayerProfile field**. On the **Mac client** the
PP struct is fixed and client-authoritative; repurposing a field risks desync and violates
the "T0-T2 only" rule for client authority. **Our approach:** keep the declared bitmask **purely
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

---

## Phase 1 port checklist (Phase 0-1, on current EQMacEmu base)

1. `common/ruletypes.h`: add `RULE_BOOL(Custom, MulticlassingEnabled, false, ...)` (default
   **off** — safer than THJ's `true`).
2. `common/classes.*`: confirm `GetPlayerClassBit()` exists (stock); add `GetPlayerClassIDByName()`
   if we want NPC name→id (THJ helper).
3. `Client::GetClassesBits()` overlay reading the **server-side** store (not `m_pp`), rule-gated
   with single-class fallback; loop **1..15** (TAKP class range).
4. `Mob::HasClass(class, bitmask=0)` helper.
5. Spell-eligibility overlay at the equivalent of `spells.cpp:1303` — lowest min-level
   among declared classes; **and NOT** hard-forbidden by our curated matrix.
6. Declaration entry point (curated/gated `AddExtraClass` equivalent), driven by an NPC per
   design — not char-create.

**Gate:** do NOT start until the **stock, unmodified** server is verified running and a client
login test passes.

---

## Phase 2 migration checklist (Phase 2 boundary, switching to SecretsOTheP/Server + RoF2)

After Phase 1 spike is validated on EQMacEmu/TAKP:

1. **Fork SecretsOTheP/Server** as your Phase 2+ base
   - Clone to `server/` in your repo (parallel to current EQMacEmu work)
   - Do NOT delete EQMacEmu fork yet (keep as reference)

2. **Port multiclass logic from EQMacEmu → SecretsOTheP/Server**
   - Copy the same steps from Phase 1 checklist, adapted to SecretsOTheP/Server codebase
   - Most changes are identical (same class/spell/AA architecture)
   - Differences: opcode paths, rule system details (RoF2 has slightly different rule scope)
   - Estimate: 2-3 weeks of careful porting

3. **Switch client** to RoF2
   - Download from Internet Archive, extract, patch for EQEmu (see `RESEARCH-CLIENT.md`)
   - Test connection to your new SecretsOTheP/Server instance
   - Verify multiclass spike test (Necro + Mage) works on RoF2 (should be identical)

4. **Begin Declaration matrix + Phase 2 design**
   - Build curated class combination rules (which secondaries available for each primary)
   - Design NPC "Tome of the {Class}" item questline
   - Implement swap-lock logic (out-of-combat, safe-zone, cooldown)
   - All on SecretsOTheP/Server base

---

## Multi-pet implications (sibling to multiclass)

Multiclass and multi-pet are **orthogonal but related**:
- **Multiclass:** character has spell access from multiple classes
- **Multi-pet:** character can summon/control multiple pets simultaneously

### THJ's multi-pet approach

THJ allowed **stacking summons** from different classes (e.g., Mage swarm + Necro undead + Enchanter pet)
but still enforced the single controllable pet model (`GetPet()` = one active, others are timed/auto).

### Thorne-EQ's innovation opportunity

Instead of just stacking timed summons (THJ's approach), consider a **tiered companion system**:
- **Primary pet:** fully controllable (guard, follow, attack, hold, passive)
- **Secondary helpers:** timed summoned pets (Fire Elementals, skeletons, etc.), auto-cast/auto-attack
- **Tertiary wards:** static-location helpers (Earth elemental on ground, healing ward)
- **Pet tiers gated by class declaration:** Mage gets more elementals, Enchanter gets nukes/charm, Necro gets undead swarm

This is **unique to Thorne-EQ** (not THJ's model) and leverages multiclass declaration to offer deeper
pet/companion play than vanilla or THJ.

**Storage:** Pet state lives in `data_buckets` per character, with `active_pet_id`, `summoned_pets[]`, `wards[]`.
**Casting:** Each pet has separate memory pool (not shared with player mana).
**Control:** Primary pet gets all commands; secondaries auto-attack/cast only.

---

## Legal safety model for Thorne-EQ

**Key decision: Use THJ as a reference, not a codebase fork**

1. **Study THJ** (architecture, design patterns, code organization)
2. **Implement independently** on your chosen server base (EQMacEmu Phase 1 → SecretsOTheP/Server Phase 2)
3. **Diverge intentionally** with curated Declaration (not free-form tri-class), multi-pet tiers, Renown/Momentum/Death meta

**Why this protects you:**
- You're not shipping THJ's code (only inspired by it)
- You're not replicating THJ's tri-class power fantasy (your design is differentiated)
- You're building on open-source EQEmu (established legal precedent: personal, non-commercial servers OK)
- You're kept private/non-commercial (zero legal risk surface)

See `DECISIONS.md` for the full legal safety framework.

---

## References & resources

- **THJ Server:** https://github.com/firestormalpha/TheHeroesJourneyServer (branch `staging`)
- **Ascendant Server:** https://github.com/Ascendant-EQ-Emu/Ascendant-Server (community fork)
- **SecretsOTheP/Server:** https://github.com/SecretsOTheP/Server (RoF2-capable mainline)
- **SecretsOTheP/EQMacEmu:** https://github.com/SecretsOTheP/EQMacEmu (TAKP-only)
- **Official EQEmu:** https://github.com/EQEmu/Server (stable, conservative)
- **EQEmu Opcodes:** https://github.com/EQEmu/Server/tree/master/opcodes (protocol definitions)
- **Packet Wiki:** https://wiki.eqemulator.org/p=opcode:opcode_reference2 (struct references)
