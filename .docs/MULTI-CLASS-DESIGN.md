# Multi-Class Design (the crux)

> Consolidates the scattered multi-class thinking into one current-direction doc.
> Deep-dives live in `archive/ARCHITECTURE.md` (original capability model) and
> `DESIGN-SKILL-CAP-SYSTEM.md` (the optional Equalizer). Choices tracked in `DECISIONS.md`.

## The one thing that must work

Everything in Thorne-EQ hinges on one question: **can we give a character curated access
to another class's spells, in a way that is fun and playable, on the stock TAKP/Quarm
(Mac) client?** If yes, the rest is content and tuning. If no, nothing else matters.

## Grounded reality (from the EQMacEmu source)

Verified against `B:\SecretsOTheP\EQMacEmu`:

| Fact | Location | Consequence |
| --- | --- | --- |
| Class is a **single `uint8`**; no second-class exists | `zone/mob.h` `GetClass()` | Multi-class must be a **server overlay**, not a client-known second class |
| One central spell-eligibility check | `common/spdat.h::CanUseSpell(spellid, class, level)` | The single choke point to overlay |
| `spells_new.classes_1..16` = min level per class (255 = barred) | DB + `spdat.h` | Reuse existing per-class tables; no re-authoring spells |
| Per-character key/value store | `data_buckets` | Store declared classes / allocation with no schema change |
| Feature flags | `rule_values` (`RuleB/RuleI/RuleR`) | Stage safely, per-character or per-zone |
| Augments **absent/disabled** | `common/item_data.h` | "Socket a class into a slot" = build-from-scratch (avoid early) |
| Client is moddable via DLLs | Zeal `.asi`, akplus, classless (MQ) | Optional UX help, never core authority |

## Two models, unified

We had two overlapping ideas. They are the **same substrate at different richness**:

- **Declaration** (start here): you *are* your primary class plus a curated set of declared
  secondary classes. Eligibility = union of declared classes' existing tables.
- **Equalizer** (later): a point budget tunes *how far* each declared line progresses
  (native/secondary/tertiary caps). Additive on top of declaration. See
  `DESIGN-SKILL-CAP-SYSTEM.md`.

**Decision:** ship Declaration first (reuses everything, proves fun), add the Equalizer only
if the core loop wants more depth. (`DECISIONS.md` D2, A5.)

## The enforcement fork (the critical choice)

Where we enforce eligibility decides how much client help we need:

- **Cast-time (chosen, server-authoritative):** make secondary spells scribable in
  `spells_new`, then gate at cast in `CanUseSpell()`. Pure server, per-character, reversible.
  Risk: a barred spell might look scribable — mitigated with clear messaging.
- **Scribe-time (partly client-side):** the Mac `CSpellBookWnd` may refuse to scribe
  off-class spells. Per-character overlay here needs Zeal/akplus help.

**Decision (tentative):** cast-time authority; validate in **Phase 1** whether the stock
client even lets you scribe off-class spells. That test sets `DECISIONS.md` D6.

## Declaration model (Phase 2 target)

- **Primary class:** immutable identity anchor; sets floors you can never drop.
- **Declared secondaries:** earned, curated by a matrix (which primaries may take which
  secondaries — grants **and** prohibitions). Stored in `data_buckets`.
- **Resolver:** `CanUseSpell` returns eligible if *any* declared class qualifies at the
  character's level, AND the line is not hard-forbidden for that primary.
- **Interface:** a clicky **"Tome of the {Class}"** item declares/activates a secondary
  (`EVENT_ITEM_CLICK`). The "backpack of tomes" is flavor; extra bags/quests = more slots.

## The swap-lock (hard requirement)

Role swaps must never happen mid-combat. All checks are cheap and server-side; layer them:

| Lock | Mechanism |
| --- | --- |
| Out-of-combat | reject if `InCombat()` / recent aggro |
| Safe location | zone allowlist (Bazaar/Nexus) **or** proximity to a "Soul Shrine" NPC |
| Ritual channel | short, interruptible cast to re-attune |
| Cooldown | `data_buckets` TTL between swaps |

**Leaning:** out-of-combat + safe-location + short ritual + cooldown, with the **Nexus** as
the consolidated hub (re-attune + blessings + travel). (`DECISIONS.md` D3, D4.)

## Playability enablers (Phase 3 — why it's fun, not just possible)

A 2-3 hybrid group needs sustain and baseline buffs or it can't function:

- Rule-driven regen (anti-sitting), sustain as earned affinity perks (Death=leech,
  Nature=regen) — `zone/client_mods.cpp` `LevelRegen`/`CalcManaRegen`.
- Nexus blessing NPC (MGB-style) + open travel to remove hard class dependencies.
- Longer buff durations; pet auto-attack + hold/guard for small-group/AFK-safe camps.

These make hybridization feel **earned** and keep it **curated**, not classless.

## Phase 1 test plan (do this first)

1. Anchor + one secondary (proposal: Necromancer + Magician).
2. Temporarily set a few Magician spells usable by Necro in `spells_new`.
3. Observe on the stock client + Zeal: can you **scribe**? **memorize**? **cast**?
4. Add the real `CanUseSpell()` override behind a `rule_values` flag.
5. Record the enforcement answer here and in `DECISIONS.md` (D6).

**Exit:** a Necromancer casts a normally-barred Magician spell, gated server-side, toggled
by a flag — and we know whether scribe-time needs any client-DLL help.
