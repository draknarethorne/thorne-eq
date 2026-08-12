# Thorne-EQ Backlog

> Every "want" thrown into the bucket, itemized so we can decide and prioritize.
> **Priority**: MVP (needed to prove the core) · Soon · Later · Icebox (deferred).
> **Src**: inspiration source. **Phase**: target roadmap phase. See `ROADMAP.md`.

## Multi-Class Core (the crux — must prove first)

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Cast-time cross-class eligibility overlay | — | MVP | 1 | `CanUseSpell()` override behind flag |
| Declared secondary classes via item | THJ | MVP | 2 | `data_buckets`; primary immutable |
| Curated class matrix (grants + prohibitions) | — | MVP | 2 | Data table; protects fantasy |
| Role swap between fights, combat-locked | RIFT | MVP | 2 | OOC + safe location |
| Affinity tracks (Nature/Death/Protection/...) | AC/UO | Soon | 3/5 | Also gate sustain perks |
| Equalizer point-buy caps/tiers | RIFT souls | Later | 5 | Additive on declaration |
| Named archetype presets (e.g. Warden of Ash) | Diablo | Later | 6 | Curated starting blends |
| Re-spec via consumable | RIFT | Later | 5 | Cost/cooldown |

## Playability & Sustain (make the small group fun)

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Rule-driven regen (anti-sitting) | Diablo/RIFT | Soon | 3 | Edit `LevelRegen`/`CalcManaRegen` -> rules |
| On-kill / on-hit leech (earned) | Diablo | Soon | 3 | Death-affinity perk |
| Longer buff durations | — | Soon | 3 | Rule multiplier |
| Reagent-lite utility casting | QoL | Soon | 3 | Reduce pearl/bone-chip friction for baseline buffs/ports |
| Out-of-combat recovery clickies | Diablo/UO | Soon | 3 | Reusable bandages/food-tonics for downtime smoothing |
| Pet auto-attack + hold/guard tuning | THJ | Soon | 3/4 | Small-group + AFK-safe |
| Primary pet + swarm/ward companion model | THJ | Soon | 3/4 | Uses existing swarm-pet lane; avoids breaking the one-primary-pet client model |
| Multiple simultaneous pets (2-3 per controller) | THJ | Later | 4/5 | Small-group force-multiplier; needs pet-cap + control UX audit |
| Multi-pet command wheel / proxy commands | Zeal | Later | 5 | Needs a client assist layer because stock `/pet` assumes one primary pet |
| `/cast` from spellbook to build buff macros (no spellbar swap) | QoL | Later | 4 | Cast by spellbook slot so buffs run from a macro without memming; verify client `/cast` support |
| Saved buff-package macros | Zeal | Later | 5 | UI-assisted convenience layer over spellbook casting / clickies |
| 2-3 hybrid group content viability | — | MVP-of-fun | 3 | The key playtest |

## Pets & Companions

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Pet stance polish (guard/follow/taunt presets) | THJ | Soon | 3 | Mostly server logic + existing pet commands |
| Suspend-like storage for more pet archetypes | EQ live | Later | 4 | Current code has one `SuspendedMinion`; extending that is real work |
| Totem/ward pseudo-pets | Diablo | Soon | 3 | Use immobile or timed NPC helpers instead of full permanent pets |
| Treasure-goblin escort pet / mule pet | UO/Diablo | Icebox | 6 | Cute, but likely UI-heavy and messy for inventory ownership |
| Pet equipment simplification | QoL | Later | 5 | Either curated equipment slots or no-gear pets to avoid micromanagement |

## World & Travel

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Nexus blessing NPC (MGB-style) | Quarm | Soon | 3 | Baseline buffs; not raid-trivializing |
| Open travel (spires/translocators/stones) | — | Soon | 3 | Remove porter dependency |
| Consolidated Nexus hub | — | Soon | 3 | Re-attune + buffs + travel in one |
| Bazaar/Nexus attunement brokers | THJ (borrow) | Soon | 2/3 | Class declaration, role swap, respec, and affinity unlocks via NPC flows |
| Reagent vendors / exchange NPCs | QoL | Soon | 3 | Smooth friction for buffs, ports, pet toys, arrows |
| Daily or weekly bounty board | Diablo/UO | Later | 4 | Quest scripts + rotating targets + token payouts |
| Expedition-lite challenge rings | Diablo | Later | 5 | Ring an object, spawn a tuned wave, earn small-group rewards |
| Treasure courier / wandering merchant events | UO | Later | 5 | Time-window world events that feel alive without client changes |

## Loot & Items

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Better low-level static drops | Diablo | Later | 4 | Kill "always Rusty" feel |
| Bigger bags + weight reduction | QoL | Later | 4 | Trivial DB items |
| Giant-size 10-slot bag pass | QoL | Soon | 3 | Safe lane: `BagSlots` already supports 10; avoid inventing >10-slot client UI |
| Quest-supplied consumable packs | UO | Soon | 3 | Bundles of food, bandages, arrows, reagents, pet consumables |
| Global loot table pass for low/mid content | Diablo | Soon | 3/4 | Use `global_loot` + `lootsim` to add chase drops broadly |
| Ground supply caches / loot chests | UO | Soon | 4 | Reuse groundspawn/object flow for static or timed caches |
| Treasure-runner NPCs | Diablo | Later | 4 | Flee/aggro AI + juicy loottables; high fun-per-code |
| Self-found / character-bound chase items | Quarm | Later | 4 | Extend Quarm-style per-instance metadata where useful |
| Pre-authored pseudo-affix item families | Diablo | Later | 5 | Safer than true random stats; unique IDs preserve client compatibility |
| Random item affixes + rarity colors | Diablo | Icebox | 6 | Big build; augments absent |
| Tokenized item upgrading / tempering | Diablo | Later | 5 | Server-authoritative path around true randomized packets |
| Ground chest trap / lock variants | UO | Later | 5 | Turn caches into a small gameplay loop, not free vending |

## Progression & AA

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| XP/AA rate tuning | — | Later | 4 | Rules |
| AFK xp/AA farming support | — | Later | 4 | Auto-combat + pet guard |
| Expanded/opened AAs | THJ | Icebox | 6 | Verify Quarm coverage first |
| Equalizer-as-AA spend model | Diablo/RIFT | Later | 5/6 | Zeal could make it feel like AA spending without trusting the client |
| Attunement milestone quests | UO/AC | Soon | 3/4 | Unlock secondary perks through repeatable progression tasks |

## Admin / GM

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Tiered GM roles for friends | — | Later | 4 | `account.status` + `command_settings` |
| Buffed quest xp/rewards | — | Later | 4 | Quest scripts + rules |
| Loot simulation tooling pass | EQEmu | Soon | 3 | Build around existing `#lootsim` to validate custom drop economics |
| Live feature flags for experiments | — | Soon | 3 | `rule_values` + `data_buckets` + custom tables for reversible rollout |

## NPC Logic & World Simulation

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Smarter script-driven NPCs | UO | Soon | 3 | Quest events + buckets + timers before anything ML-shaped |
| Combat archetype packages | Diablo | Soon | 4 | Reusable melee/caster/summoner brains via aggro + spell choice tuning |
| Flee/retreat/assist behavior pass | EQEmu | Soon | 4 | Tune `CheckAggro`, flee logic, and special abilities for livelier fights |
| Bazaar/Nexus service personalities | UO | Soon | 3 | Merchants/attuners/clerks with persistent dialogue state |
| Procedural chatter from server state | AI-lite | Later | 5 | Rule-based templated lines keyed by zone, faction, and events |
| External AI dialogue sandbox | AI | Icebox | 6 | Flavor only, never authority or combat logic; requires strict guardrails |

## Client / UX (optional polish)

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Zeal "Attunement" panel + gauges | — | Later | 6 | `uifiles/zeal` custom window |
| Scribe-time UX via akplus/Zeal | — | Conditional | 1/6 | Only if Phase 1 shows client blocks scribing |
| Class declaration via NPC (post-creation), not char-create | THJ (borrow) | Soon | 2 | Avoid a custom char-create client; use a Bazaar/Nexus NPC flow. See `CLIENT-STRATEGY.md` |
| Equalizer allocation window with save/apply | Zeal | Later | 6 | Zeal already has writable options UI + `.ini` persistence |
| Build templates stored client-side, validated server-side | Zeal | Later | 6 | Client convenience only; server checks all costs/rules |
| Optional Thorne UI skin distribution | Zeal/Thorne-UI | Later | 6 | Ship XML/UI assets separately from core server changes |
| Thorne launcher / patcher | MMO ops | Icebox | 6 | Optional updater for `zeal.asi`, `uifiles`, and docs after base install |

## Data, Storage & Operations

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| `data_buckets` first, custom table later | THJ + Thorne | Soon | 2/5 | Fast spike path, then migrate to queryable build tables if needed |
| Keep gameplay code in repo-of-truth | — | Soon | 2 | Server source in `server/`, UI assets in UI repo, orchestration in hub |
| Hub-owned rebuild recipes | — | Soon | 2 | `.bin/`, `config/`, `db/bootstrap/` stay centralized for from-scratch rebuilds |
| Nested repo ignore hygiene | — | Soon | 2 | Prevent generated local config from appearing as accidental server work |

## Parking lot (raw ideas, undecided)

- Diablo-style loot beams / rarity SFX (client limits on Mac client — likely icebox).
- Endgame focus on Planes / later expansions instead of early grind.
- Larger inventory/QoL conveniences to "get rid of early-level grinds".
- Server-side storage "uniqueness": weigh a dedicated custom table (e.g. `thorne_character_build`)
  vs. reusing `data_buckets` for declared classes / affinity / allocation — schema-change-free
  and portable vs. more queryable/efficient. See `CLIENT-STRATEGY.md` + `MULTI-CLASS-DESIGN.md`.
- Multiple-pet control and `/cast`-from-spellbook macros both depend on a client-capability
  audit (Mac client + Zeal) before committing — see `CLIENT-STRATEGY.md`.
- Runtime external AI for combat brains is probably the wrong first move; script/state-machine
  NPC logic gives most of the flavor without latency, moderation, or determinism problems.
