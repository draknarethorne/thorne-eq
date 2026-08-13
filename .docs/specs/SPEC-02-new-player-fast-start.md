# SPEC-02 — New Player Fast-Start

> **Status:** Draft · **Phase:** 1/2 · **Low-hanging fruit, high value.**
> Companion: `BACKLOG.md` (Playability & Sustain, Progression & AA), `DECISIONS.md`.

## 1. Purpose

Kill the day-one runaround. A brand-new character should be **combat-functional within
minutes with no external twink** — no begging for plat, armor, or spells. Starting a *new
multi-class* character should be just as fast, so experimentation is cheap and the rested/AFK
bonus starts earning from day 1.

## 2. MVP expression

A one-time, per-character **starter boon** granted at first login (or claimed from a hub
"Herald/Quartermaster" NPC), scaled to the character's class. Purely server-side + data-driven.

Contents (bounded — practical, not raid-grade):

- **Starter plat** (bounded) + a small **bank seed** cushion.
- **Class-appropriate starter armor + primary weapon** (functional, not BiS).
- **Spell access via an on-demand Grimoire clicky** (not a carried satchel of all 1-20 spells) — see Section 3a.
- **Tier-1 WR bags** so inventory isn't a problem.
- **Bind at the hub** + a **transport rune** (charge/cooldown) so travel isn't a wall.
- **Reagents by class lane** + a few stacks of ammo if relevant. **Food/water are optional** (stat-boost only, not required) — see Section 3b.

## 3. Design & approach

- Grant is **one-time per character**, tracked by a claim flag in `data_buckets` so it can't be
  re-farmed (idempotent, like a one-shot migration).
- Delivered by **item summon into a container** (a "Newcomer's Satchel") or direct grant on the
  first-login/enter-zone event — preserves the stock scribe/equip ritual.
- **Multi-class fast-start:** when a secondary is declared (SPEC-04 / the Tome flow), the same
  quartermaster can hand the matching class starter kit so the new role is immediately usable.
- Everything behind a rule flag; values live in DB tables so they're tunable without a rebuild.

### 3a. Spell delivery — on-demand, not a carried satchel

Problem: carrying every 1-20 spell is clutter, and running back to a vendor mid-hunt breaks flow.

**Model (preferred): a Grimoire clicky/draught** the player uses when they level.

- On use (out of combat), it **summons only the spells newly available** to that class at the
  current level (and any earlier ones not yet scribed) into a small container; the player scribes
  normally, preserving the ritual, **in the field**.
- **Charge economy:** a charge is **consumed only if it actually delivered spells** — leveling
  into a "no new spell" level is a no-op (no charge spent, "nothing new to learn" message).
- Class-whitelisted; hard-gated to the character's current level (never future spells).

**Alternative (simpler): a reusable, level-gated clicky** with no charge accounting — click any
time to pull newly-eligible spells; if none, it just says so. Trades the charge flavor for less
bookkeeping. (Open question O-1.)

**Realistic seam:** a **quest-scripted item** (Perl/Lua `EVENT_ITEM_CLICK`) is needed for the
"only consume on delivery" logic, because stock item charges always decrement on click. The
script checks level + class, diffs against already-scribed spells (or a `data_buckets`
last-delivered-level marker), summons the missing scrolls, and decides whether to spend a charge.

### 3b. Food & water — optional, not required

Remove the survival tax: **no starvation/thirst penalty**, so players never carry food/water
just to function. Food/water become **optional stat-boost consumables** (buff-food), kept for
players who want the edge.

**Realistic seam:** disable the hunger/thirst penalty (rule-driven in the zone consume/stamina
path, `m_pp.hunger_level` / `thirst_level`), and add buff-food items as the opt-in upgrade.

## 4. Data & code seams

- Trigger: quest engine `EVENT_ENTERZONE` / first-login, or NPC `EVENT_SAY` / `EVENT_ITEM` claim.
- Items: standard `items` rows; containers via item summon-into-bag effects.
- Claim state: `data_buckets` (`fast_start_claimed` per character/class).
- Feature flag + per-class kit tables: `rule_values` + a small custom/`data_buckets`-backed table.
- Bind/rune: standard bind mechanic + a charge clicky item.

## 5. Acceptance test

A freshly created character, on first login with the flag on:

1. receives (or claims from the Herald) a class-appropriate kit;
2. can equip armor + weapon, scribe the starter spells, fill bags, and is bound at the hub;
3. has enough plat/consumables to leave town and fight **without any other player's help**;
4. the grant **cannot** be claimed twice (flag holds);
5. declaring a secondary class yields its matching starter satchel just as fast.

Pass = time-to-functional-character drops from "needs a twink" to "a few minutes, self-served."

## 6. Rollback

Disable the rule flag; existing characters keep what they already claimed, new ones simply get
nothing extra. No schema damage; claim flags are inert when the feature is off.

## 7. Open questions

- Exact **plat amount** and **bank seed** (bound to avoid inflation — see economy guardrails).
- **Kit contents per class** (armor/weapon/spell list per class + level band).
- **Per-account vs per-character** subsidy (e.g., first character fully free, alts lighter?).
- Grant-on-login vs NPC-claim (claim is more discoverable and self-announcing).
- **O-1:** spell delivery = charged draught (consume-on-delivery, needs quest script) vs a
  reusable level-gated clicky (simpler)?
- Spells-per-level varies — confirm delivery diffs correctly against already-scribed spells.
- Food/water penalty removal: global vs a per-test toggle rule.

## 8. Why this pairs with SPEC-01

Once the multi-class spike proves the mechanic, fast-start makes **rolling a new hybrid**
frictionless — which is exactly the loop we want to playtest: declare, gear up in minutes,
go earn rested/AFK bonuses from day 1.
