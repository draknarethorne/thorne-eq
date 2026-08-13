# Thorne-EQ Decision Log

> Tracks **what's been decided** (with rationale) and **what's still open**. Open decisions
> are the gating questions for the roadmap. Update this as choices are locked in.
> Companion: `ROADMAP.md`, `BACKLOG.md`, `MULTI-CLASS-DESIGN.md`.

## Decided

| # | Decision | Rationale | Date |
| --- | --- | --- | --- |
| A1 | **Fork-first source intake**: fork `SecretsOTheP/EQMacEmu` + `quests`, clone locally, track `upstream` | Quarm-adjacent baseline, clean upstream sync, custom work isolated | 2026-08-11 |
| A2 | **DB baseline = latest Quarm dump** (`quarm_2026-03-20`) over Al'Kabor | Goal is to mirror the live Quarm build | 2026-08-11 |
| A3 | **Client posture softened**: server-authoritative always, but approved client DLLs (Zeal, akplus, classless/MQ for dev) are permitted; only a *full client rewrite* is off-limits | User wants Zeal + is fine with DLLs; only a full reimplementation is too costly | 2026-08-11 |
| A4 | **Enforce eligibility at cast time, server-side** (tentative — validate in Phase 1) | Pure server authority, no client dependency, fully per-character, reversible | 2026-08-11 |
| A5 | **Declaration before Equalizer**: start with curated multi-class declaration; add point-buy caps later | Smallest slice that reuses all existing spell tables; proves fun first | 2026-08-11 |
| A6 | **Interface = clicky "Tome" item**; backpack is flavor wrapper | Fits stock client via `EVENT_ITEM_CLICK`; no custom UI required | 2026-08-11 |
| A7 | **Anti-mid-combat swap is required**: role swaps locked in combat | Explicit user requirement | 2026-08-11 |
| A8 | **Repo layout**: `server/`, `quests/`, `maps/` nested in `C:\Thorne-EQ`, gitignored; forks tracked independently | User is comfortable with it; keeps docs repo clean | 2026-08-11 |
| A9 | **Portable MariaDB 10.3** instead of MSI | MSI fails on this machine (broken service-account temp); portable runs as user | 2026-08-11 |
| A10 | **Identity = anti-EverGrind**: cut wasted-time (travel, sitting, restock, faction-by-1); keep earned tension (dangerous pulls, contested camps, milestones) | The differentiator vs stock EQ; also self-describing so docs stay light | 2026-08-12 |
| A11 | **Two-meter meta layer**: Renown (permanent contribution) + Momentum (volatile streak, resets on death); neither costs gear or lifetime progress | Makes "playing matters + death matters" without cruelty | 2026-08-12 |
| A12 | **Active-participation gate on meta rewards**: AFK levels to 50, but Renown/Momentum accrue only with player actions (pet auto-attack doesn't count) | Protects the reward/economy curve from AFK inflation | 2026-08-12 |
| A13 | **Easy-to-50, earned-after**: smooth AFK-friendly climb to 50; deliberate steepening past 50 | Time-to-fun without trivializing endgame | 2026-08-12 |
| A14 | **Humane death**: keep items; sting via XP debt + Momentum loss + short recovery; corpse-to-bind/relocate fixes deep-CR misery | Death matters without punishing deep-dungeon runs | 2026-08-12 |
| A15 | **Anti-grind base tweaks**: cap-aware run-speed floor; Gate-for-all via Soulbinder + rune (effect, not class spell); kill-based faction alongside existing quests | Attack the biggest time-wasters, classic-client-clean | 2026-08-12 |
| A16 | **Discoverability = chat-first**: Herald NPC + Adventurer's Handbook (in-game patch notes) + one out-of-game delta page; reuse existing Quarm/TAKP quest refs | No new wiki to maintain; prefer self-announcing changes | 2026-08-12 |
| A17 | **Multi-class is design-validated (THJ), not yet client-validated**: keep the Phase 1 spike to prove Mac/Quarm scribe/memorize/cast of server-granted cross-class spells | THJ ran on a modern client; the classic-client mechanics remain the real unknown | 2026-08-12 |
| A18 | **Rested/Offline XP+AA is the preferred progression path**: a capped pool accrues while logged off, all characters benefit, consumed by playing (kill multiplier), monthly-reset to prevent banking a year offline; in-game pet-AFK demoted to optional/secondary | Friendlier than leaving a client running; rewards every character; abuse-bounded | 2026-08-12 |

## Open (need a decision)

| # | Question | Options | Leaning | Blocks |
| --- | --- | --- | --- | --- |
| D1 | First test anchor + secondaries | (a) Necro + Mage + Enchanter (b) Warrior + Cleric + Druid | (a) for Phase 1 spike; (b) stresses heal-balance | Phase 1 |
| D2 | Declaration richness at start | Fixed multi-declare vs Equalizer from day one | Fixed-first | Phase 2 |
| D3 | Swap-lock recipe | Strict Bazaar-only vs out-of-combat + safe-zone/Soul-Shrine + ritual channel + cooldown | Layered (OOC + shrine) | Phase 2 |
| D4 | Re-attune location | Single Nexus hub (re-attune + blessings + travel) vs distributed Soul Shrines | Nexus hub | Phase 2/3 |
| D5 | Regen model | OOC-burst + modest combat baseline (all) vs affinity-perk leech only | Baseline + affinity perks | Phase 3 |
| D6 | Scribe-time enforcement | Cast-time only vs add Zeal/akplus scribe patch | Decide after Phase 1 test | Phase 1 |
| D7 | Max secondary classes + tier depth | 2 vs 3 secondaries; how deep each line goes | TBD after playtest | Phase 2/5 |
| D8 | Level/cap target | 60 vs beyond | TBD | Phase 3+ |
| D9 | MariaDB long-term | Portable vs Windows service (after temp fix) vs Docker | Portable now, revisit on C: drive swap | low stakes |
| D10 | Death sting mix | XP-debt vs Momentum-loss vs durability weighting | Momentum-loss primary; light XP debt | Phase 3/4 |
| D11 | Renown curve shape + caps | linear vs tiered; per-day caps; loot vs XP weighting | tiered + daily cap | Phase 4 |
| D12 | Momentum detail | step size, decay, which titles/buffs, armor-tier downgrade | TBD after playtest | Phase 4 |
| D13 | Meta activation timing | activate after multi-class MVP vs run parallel early | schema early, activate Phase 4 | Phase 2/4 |
| D14 | Rested accrual tuning | pool size/cap, reset cadence (monthly?), per-char vs account pool, Renown scaling, consume-rate multiplier | monthly cap + per-char + play-to-consume | Phase 3/4 |

## Recently resolved technical facts (not decisions, but settled)

- EQMacEmu fork has **no submodules** (`LOCAL-SETUP` previously said otherwise).
- Dependencies auto-fetch on MSVC via `cmake/DependencyHelperMSVC.cmake`.
- Central spell-eligibility choke point: `common/spdat.h::CanUseSpell(spellid, class, level)`.
- Per-character state store: `data_buckets`; feature flags: `rule_values` (`RuleB/RuleI/RuleR`).
- Regen is computed in `zone/client_mods.cpp` (`LevelRegen`, `CalcManaRegen`) — mostly hardcoded,
  candidate to make rule-driven.
- Augments are **absent/disabled** in this codebase (affects any "socket a class" idea).
