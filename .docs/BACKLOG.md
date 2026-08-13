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
| Friends-and-family helper lane | UO | Later | 4 | Not GM power; a bounded assist mode for trusted private-server play |
| Starter class spell satchel | UO/EQ | Soon | 3 | Grant/sell all vendor-tier scrolls/tomes for a class up to a level band |
| Purchasable level-band spell sets | UO/EQ | Soon | 3/4 | e.g. 1-20, 21-40, 41-50 bundles so leveling never becomes a vendor crawl |
| Starter bank platinum seed | UO | Soon | 3 | One-time per character reserve cushion in bank to prevent early dead-ends; bounded and flag-tracked |
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
| Domestic / housed pet state | UO | Soon | 4 | Safe non-hostile house pets after release / conversion state |
| Stable claim one-at-a-time | UO | Later | 4 | QoL for pet-heavy players; avoid all-or-nothing retrieval |
| Suspend-like storage for more pet archetypes | EQ live | Later | 4 | Current code has one `SuspendedMinion`; extending that is real work |
| Totem/ward pseudo-pets | Diablo | Soon | 3 | Use immobile or timed NPC helpers instead of full permanent pets |
| Treasure-goblin escort pet / mule pet | UO/Diablo | Icebox | 6 | Cute, but likely UI-heavy and messy for inventory ownership |
| Pet equipment simplification | QoL | Later | 5 | Either curated equipment slots or no-gear pets to avoid micromanagement |

## Anti-EverGrind Time-Saver Pass (base tweaks to the biggest time-wasters)

> **Frame:** Thorne-EQ is classic EQ **minus the wasted-time tax** (running, sitting, restock,
> faction-by-1) while keeping earned tension (dangerous pulls, contested camps, milestones).
> Prefer **self-announcing** changes (felt in normal play) so docs stay minimal; reserve written
> docs for the invisible systems (attunement/multiclass). Every item ships behind a rollback flag.

| Item | Src | Priority | Phase | Self-announcing? | Notes |
| --- | --- | --- | --- | --- | --- |
| Base run-speed floor (cap-aware) | THJ/QoL | Soon | 3 | Yes (felt) | Raise base movement via rule; **respect client speed cap** or players warp; SoW/JBoots/Selo's still stack up to safe ceiling |
| Reduced med/downtime tax | Diablo/RIFT | Soon | 3 | Yes (felt) | Pairs with rule-driven regen; cut sitting hours without removing mana as a resource |
| Transport runes + Gate-for-all | THJ/EQ | Soon | 3 | Yes (vendor/NPC) | See World & Travel rows; kills cross-world running |
| Kill-based faction paths | THJ | Soon | 3/4 | Yes (faction msg) | See World & Travel row; ends grind-by-1 turn-in chores |
| Discoverability: Herald NPC + Adventurer's Handbook + delta page | UO/THJ | Soon | 2/3 | n/a | In-game first: hub Herald `/say` keywords + readable starter book = in-game patch notes; one out-of-game "What's Different" page; lean on existing Quarm/TAKP quest refs for everything unchanged |

## World & Travel

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Nexus blessing NPC (MGB-style) | Quarm | Soon | 3 | Baseline buffs; not raid-trivializing |
| Open travel (spires/translocators/stones) | — | Soon | 3 | Remove porter dependency |
| Consolidated Nexus hub | — | Soon | 3 | Re-attune + buffs + travel in one |
| Featherstone-style travel clicky | UO | Soon | 3 | Personal Nexus recall stone / potion with cooldown, ownership, and bind rules |
| Bazaar/Nexus attunement brokers | THJ (borrow) | Soon | 2/3 | Class declaration, role swap, respec, and affinity unlocks via NPC flows |
| Player-city style service hub | UO | Soon | 3 | One friendly city/Nexus hub that concentrates travel, vendors, quests, and reset services |
| Reagent vendors / exchange NPCs | QoL | Soon | 3 | Smooth friction for buffs, ports, pet toys, arrows |
| Transport runes (bind/hub/key-zone clickies) | THJ/EQ | Soon | 3 | Charge/cooldown clickies; gate by level/faction; self-announcing (on vendor) |
| Gate-for-all via Soulbinder + Gate rune | EQ | Soon | 3 | Grant the *effect* (NPC binds any class + rune returns to bind), not the class spell; classic-client-clean |
| Kill-based faction paths | THJ | Soon | 3/4 | Add faction to more mob kills via `npc_faction`; keep quests, widen paths (e.g. no 100x milk runs); self-announcing (faction message) |
| Daily or weekly bounty board | Diablo/UO | Later | 4 | Quest scripts + rotating targets + token payouts |
| Expedition-lite challenge rings | Diablo | Later | 5 | Ring an object, spawn a tuned wave, earn small-group rewards |
| Treasure courier / wandering merchant events | UO | Later | 5 | Time-window world events that feel alive without client changes |

## Loot & Items

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Better low-level static drops | Diablo | Later | 4 | Kill "always Rusty" feel |
| Bigger bags + weight reduction | QoL | Later | 4 | Trivial DB items |
| Giant-size 10-slot bag pass | QoL | Soon | 3 | Safe lane: `BagSlots` already supports 10; avoid inventing >10-slot client UI |
| Stack size 20 → 100 | QoL | Soon | 3 | Raise stackable `stacksize` in item data; **verify Mac/Quarm client renders 100-stacks** (client cap risk); big inventory-friction + bank-space win; self-announcing |
| Starter WR bag ladder (Tier 1/2/3) | UO/QoL | Soon | 3/4 | Journeyman-style progression: practical starter WR, then quest/faction upgrades; no premium endgame bypass |
| Quest-supplied consumable packs | UO | Soon | 3 | Bundles of food, bandages, arrows, reagents, pet consumables |
| House placable supply depot | UO | Soon | 4 | Refillable or charge-based house chest for baseline consumables/materials |
| Global loot table pass for low/mid content | Diablo | Soon | 3/4 | Use `global_loot` + `lootsim` to add chase drops broadly |
| Curated low/mid craft-access pass | UO | Soon | 4 | Expand practical artisan outputs for low-pop independence without handing out top-tier chase gear |
| Ground supply caches / loot chests | UO | Soon | 4 | Reuse groundspawn/object flow for static or timed caches |
| Treasure-runner NPCs | Diablo | Later | 4 | Flee/aggro AI + juicy loottables; high fun-per-code |
| Self-found / character-bound chase items | Quarm | Later | 4 | Extend Quarm-style per-instance metadata where useful |
| Pre-authored pseudo-affix item families | Diablo | Later | 5 | Safer than true random stats; unique IDs preserve client compatibility |
| Random item affixes + rarity colors | Diablo | Icebox | 6 | Big build; augments absent |
| Tokenized item upgrading / tempering | Diablo | Later | 5 | Server-authoritative path around true randomized packets |
| Ground chest trap / lock variants | UO | Later | 5 | Turn caches into a small gameplay loop, not free vending |

## Economy & Vendors (low-pop shard resilience)

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Pseudo-player vendor market v1 | UO | Soon | 3/4 | NPC stock of crafted/farmed staples to cover low-pop supply gaps (no raid BiS) |
| Vendor restock schedule + scarcity tags | UO | Soon | 4 | Rotating item pools with predictable windows so players can plan |
| Price band guardrails (floor/cap) | MMO ops | Soon | 4 | Prevent extreme inflation/deflation and easy arbitrage loops |
| Faction-based service discounts | EQ/UO | Later | 5 | Small economy identity without undermining core sinks |
| Sink pass for convenience economy | MMO ops | Soon | 4 | Travel permits, service fees, token rerolls to keep plat velocity healthy |
| Economy observability dashboard/logs | MMO ops | Later | 5 | Track plat faucets/sinks, staple availability, and exploit detection signals |
| Item policy tiers (protected/risky/volatile) | MMO ops | Later | 5 | Define clear loss/protection semantics for convenience items vs. high-value progression items |
| Guard/policy matrix framework | MMO ops | Soon | 4 | Centralize who/what/where/when/cost checks for convenience relaxations to prevent ad-hoc rule drift |
| Guard inversion regression suite | MMO ops | Soon | 4 | Add targeted tests for theft, loot eligibility, travel access, pet claims, and onboarding grants |
| Feature-flag + rollback standard for relaxations | MMO ops | Soon | 4 | Every permissive change ships with kill-switch and telemetry hook |

## Progression & AA

> **Pillar — "easy to 50, earned after":** the 1-50 climb should be smooth and AFK-friendly
> (THJ-style: park in a found spot, pets sustain vs blue/white spawns, wake up with XP/AA).
> Past 50 it steepens deliberately. "Finding the spot" is kept as earned knowledge, not friction.

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| XP/AA rate tuning (level-band curve) | — | Soon | 3/4 | Generous ≤50 via `rule_values`; steepen 50+; con-based XP keeps it blue/white only |
| AFK-to-50 grind loop (pillar) | THJ | Soon | 3/4 | Pet-sustained overnight XP/AA to 50; pet-present + leash + con gates; forbidden on yellow/red |
| Self-sustaining pet loop (resummon-on-death %) | THJ | Soon | 3/4 | Necro-style AA/spell proc that re-summons/raises a minion so the AFK loop survives a death — the keystone |
| Pet overnight survivability tuning | THJ | Soon | 3/4 | Pet self-heal/leech, taunt/hold, auto-attack so a lone/duo setup does not wipe to blue/white spawns |
| Post-50 difficulty ramp | — | Soon | 4 | 50→51 XP/AA multiplier drop + content out-scales a lone pet on purpose |
| Expanded/opened AAs | THJ | Icebox | 6 | **Mac-AA caveat**: classic Mac/Quarm client AA set is era-limited (Luclin/PoP-ish); audit coverage. Deliver THJ-style powers as spells/items/rules where AAs are unavailable |
| Equalizer-as-AA spend model | Diablo/RIFT | Later | 5/6 | Zeal could make it feel like AA spending without trusting the client |
| Attunement milestone quests | UO/AC | Soon | 3/4 | Unlock secondary perks through repeatable progression tasks |
| Starter boon package | UO | Soon | 3 | Better new-character inventory, travel, and recovery baseline |
| Optional direct-scribe convenience mode | EQ | Later | 5 | Only if scroll/tome bundles still feel too tedious after testing |

### AFK-to-50 guardrails

- **Enforcement**: con-based XP (blue/white only), leash radius, pet-present requirement, level-band XP rules.
- **Forbidden**: AFK viability on yellow/red, unattended named/loot-camp farming, unattended plat printing, AFK past the intended ceiling.
- **Balance levers**: resummon proc %, pet upkeep cost, leash size, 50→51 multiplier drop.
- **Rollback signals**: AFK-drop inflation, camps hollowing out, time-to-50 collapsing to trivial.

## Renown, Momentum & Death (foundation-first meta layer)

> **Foundation pillar — lay this early.** Two meters drive the "playing matters + death matters"
> loop. **Renown** is permanent contribution (how much you've played/built/killed/researched) and
> compounds into the reward curve. **Momentum** is a volatile kill streak that resets on death.
> Neither ever costs gear or lifetime progress. Rewards are delivered/announced via **chat**
> (login summary + event messages), no UI required.
>
> **Key gate:** AFK leveling is fine, but **Renown/Momentum accrue only for active participation**
> — pets killing while the player uses no skills does not build the meta rewards. So you can AFK to
> 50, but you earn veteran rewards by *playing* (and you skip the "kill 1000 BB gnolls for teeth" grind).

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Renown (permanent contribution meter) | THJ/Vet | Soon | 3/4 | `data_buckets` counters from kills (con-gated), quests, crafting/building, research, skill use; drives +XP/kill, better/more loot, titles, daily-reward tier |
| Momentum (volatile kill streak) | roguelike | Soon | 3/4 | Builds on death-free kills; escalating temp buffs + volatile title; **resets on death**; never touches gear/Renown |
| Renown reward curve | — | Soon | 3/4 | `rule_values` XP/loot modifiers keyed to Renown tier; higher tier = more/better loot + XP per kill |
| Permanent Renown titles | EQ titles | Soon | 4 | Milestone titles kept forever |
| Volatile Momentum titles + buffs | EQ titles | Soon | 4 | Held only while streak alive (e.g. "the Unbroken"); breaking the streak downgrades an auto-armor/ward tier |
| Active-participation gate | — | Soon | 3/4 | Stamp `last_active_action`; kill hook awards meta only if a player action (cast/melee/skill/AA/clicky/loot/pull) is within a rolling ~3-5 min window; pet auto-attack/pet spells do NOT count; short bio-break grace |
| Server-wide day buffs (earned) | THJ | Soon | 4 | Scheduled or community-goal-triggered +XP/+loot day buffs; social glue for low pop |
| Daily login rewards | MMO | Soon | 4 | Timestamp bucket on login; reward tier scales with Renown; granted + announced in chat |
| Chat-first comms | UO/THJ | Soon | 3 | Login summary (Renown tier, daily reward, Momentum state) + event messages (faction-on-kill, Renown ticks, streak milestones, streak lost); Zeal panel optional-later |

### Renown/Momentum guardrails

- **Enforcement**: active-participation gate on all meta rewards; con-gated kill contribution; per-day caps + diminishing returns on cheap kills.
- **Anti-abuse**: weight by active-actions-per-kill ratio so periodic-macro "activity" earns far less than real play; accept minor leakage (stakes are titles/buffs, not gear).
- **Forbidden**: meta buffs that trivialize named/raid; any gear loss on death; pay-to-win; AFK accrual of Renown/Momentum.
- **Balance levers**: Renown curve, Momentum step/decay, buff magnitudes, daily/server-goal thresholds, activity window + grace.
- **Rollback signals**: XP/loot inflation from Renown, streak-loss feeling too punishing, macro-spoofed activity accrual.

## Death, Risk & Recovery (make death matter without CR misery)

> **Frame:** keep items on you (THJ-style) and never force redoing a deep-dungeon corpse trek;
> put the sting into time/recovery/Momentum, not gear or lifetime progress.

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Keep items on death (default) | THJ | Soon | 3 | Corpses are never item prisons |
| XP debt (not delevel) | EQ-ish | Soon | 3/4 | Owe XP before gaining; light ≤50, real 50+ |
| Rez / recovery sickness | WoW | Soon | 4 | Short fading effectiveness debuff so death lands in the moment |
| Bloodstain / soul marker | Dark Souls | Later | 4/5 | Death drops unbanked XP/coin at the spot; reclaim to erase debt, or lose on next death; custom ground object w/ state |
| Corpse-to-bind / relocating corpse | EQ | Soon | 4 | Summon-to-bind or auto-relocate to zone-in after a timer — the deep-CR-misery fix |
| Gear durability + repair sink | WoW/Diablo | Later | 5 | Optional coin sink, not item loss; feeds economy sinks |
| Diminishing returns on rapid deaths | roguelike | Later | 5 | Anti-zerg so hard content stays hard |
| Momentum loss on death (cross-link) | roguelike | Soon | 3/4 | Primary death sting = losing the streak buff/title (see Renown/Momentum) |

## Admin / GM

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Tiered GM roles for friends | — | Later | 4 | `account.status` + `command_settings` |
| Buffed quest xp/rewards | — | Later | 4 | Quest scripts + rules |
| Loot simulation tooling pass | EQEmu | Soon | 3 | Build around existing `#lootsim` to validate custom drop economics |
| Live feature flags for experiments | — | Soon | 3 | `rule_values` + `data_buckets` + custom tables for reversible rollout |
| Activity / event log for players | UO | Later | 5 | Surface notable world events, kills, and service notices in a player-readable way |
| Operator diagnostics for service friction | MMO ops | Later | 5 | Add targeted logs/commands for stuck travel, claim, vendor, and onboarding support tickets |

## NPC Logic & World Simulation

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Smarter script-driven NPCs | UO | Soon | 3 | Quest events + buckets + timers before anything ML-shaped |
| Combat archetype packages | Diablo | Soon | 4 | Reusable melee/caster/summoner brains via aggro + spell choice tuning |
| Flee/retreat/assist behavior pass | EQEmu | Soon | 4 | Tune `CheckAggro`, flee logic, and special abilities for livelier fights |
| Bazaar/Nexus service personalities | UO | Soon | 3 | Merchants/attuners/clerks with persistent dialogue state |
| Vendor / service locator | UO | Later | 5 | World or hub UI/NPC that helps players find merchants and services quickly |
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
