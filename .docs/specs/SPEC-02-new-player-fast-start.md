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
- **Starter spell/tome satchel** for the class, level-band `1-20` (player scribes normally).
- **Tier-1 WR bags** so inventory isn't a problem.
- **Bind at the hub** + a **transport rune** (charge/cooldown) so travel isn't a wall.
- **Basic consumables:** food/water, reagents by class lane, a few stacks of ammo if relevant.

## 3. Design & approach

- Grant is **one-time per character**, tracked by a claim flag in `data_buckets` so it can't be
  re-farmed (idempotent, like a one-shot migration).
- Delivered by **item summon into a container** (a "Newcomer's Satchel") or direct grant on the
  first-login/enter-zone event — preserves the stock scribe/equip ritual.
- **Multi-class fast-start:** when a secondary is declared (SPEC-04 / the Tome flow), the same
  quartermaster can hand the matching class starter satchel so the new role is immediately usable.
- Everything behind a rule flag; values live in DB tables so they're tunable without a rebuild.

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

## 8. Why this pairs with SPEC-01

Once the multi-class spike proves the mechanic, fast-start makes **rolling a new hybrid**
frictionless — which is exactly the loop we want to playtest: declare, gear up in minutes,
go earn rested/AFK bonuses from day 1.
