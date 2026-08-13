# SPEC-01 — Multi-Class Spike

> **Status:** Draft · **Phase:** 1 · **Authority for:** the make-or-break client question.
> Companion: `MULTI-CLASS-DESIGN.md`, `RESEARCH-MULTICLASS.md`, `DECISIONS.md` (D1, D6, A4, A17).

## 1. Purpose

Prove the single thesis everything else depends on: **can the server grant cross-class spell
use at cast time on the stock Mac/Quarm client + Zeal, or do we need a client-side scribe
patch?** THJ design-validated the *idea* on a modern client; this validates the *mechanics*
on ours.

## 2. MVP expression

One anchor class gains a handful of a second class's spells, gated entirely server-side by a
rule flag. No declaration UI, no matrix, no caps — just the raw client-mechanics test.

- Anchor: **Necromancer**. Secondary: **Magician** (67 grantable spells ≤ L20 already identified;
  e.g. Burst of Flame 93, Flare 310, Burn 94, Summon Dagger 311).

## 3. Design & approach

- Add a server-side eligibility overlay at the central choke point so a Necro is treated as
  eligible for the whitelisted Magician spells.
- **Eligibility rule:** use the **lowest** `min-level` among the character's eligible class bits
  → preserves spell chains (Necro+Mage casts the Mage spell at the Mage min-level).
- **Storage:** the eligible-class bitmask lives **server-side only** (`data_buckets`), never in
  `m_pp.classes` (Mac client PP desync risk — see A-level decision).
- Everything behind `RuleB(Custom, MulticlassingEnabled)` (or equivalent), per-character enable.

## 4. Data & code seams

- Central eligibility: `common/spdat.h::CanUseSpell(spellid, class, level)` (overlay here).
- Class-bit read point: a single `GetClassesBits()`-style accessor reading the `data_buckets` value.
- Spell table: `spells_new` (`classes1..15`; `255` = barred) — either flag entries or, preferably,
  leave the table stock and do the allow in the overlay.
- Feature flag: `rule_values`. Per-char state: `data_buckets`.
- Observation: server logs + in-game client behavior (scribe / memorize / cast).

## 5. Acceptance test

A Necromancer, with the rule flag on and the Mage bit set in `data_buckets`:

1. can **scribe** a whitelisted Magician spell into the spellbook, **or** we learn scribe needs
   Zeal/akplus help (records the answer to D6);
2. can **memorize** it to a gem;
3. can **cast** it successfully, resisted/landed like a normal spell;
4. with the flag **off**, none of the above is possible (clean gate).

Pass = cross-class cast works, gated purely server-side, toggled by one rule flag.

## 6. Rollback

Set the rule flag off (and/or clear the `data_buckets` value). Stock characters and the stock
spell tables are untouched, so there is zero residue.

## 7. Open questions

- **D6:** does scribe-time need a Zeal/akplus assist, or is cast-time overlay enough?
- **D1:** confirm Necro+Mage as the spike pair (vs a heal-stressing pair later).
- Does the Mac client show/allow a gem for a spell its class normally can't scribe?

## 8. Why this is first

Every Phase 2+ design assumes the answer. It is the cheapest, highest-information experiment
in the whole project.
