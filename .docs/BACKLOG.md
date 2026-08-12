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
| Pet auto-attack + hold/guard tuning | THJ | Soon | 3/4 | Small-group + AFK-safe |
| Multiple simultaneous pets (2-3 per controller) | THJ | Later | 4/5 | Small-group force-multiplier; needs pet-cap + control UX audit |
| `/cast` from spellbook to build buff macros (no spellbar swap) | QoL | Later | 4 | Cast by spellbook slot so buffs run from a macro without memming; verify client `/cast` support |
| 2-3 hybrid group content viability | — | MVP-of-fun | 3 | The key playtest |

## World & Travel

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Nexus blessing NPC (MGB-style) | Quarm | Soon | 3 | Baseline buffs; not raid-trivializing |
| Open travel (spires/translocators/stones) | — | Soon | 3 | Remove porter dependency |
| Consolidated Nexus hub | — | Soon | 3 | Re-attune + buffs + travel in one |

## Loot & Items

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Better low-level static drops | Diablo | Later | 4 | Kill "always Rusty" feel |
| Bigger bags + weight reduction | QoL | Later | 4 | Trivial DB items |
| Random item affixes + rarity colors | Diablo | Icebox | 6 | Big build; augments absent |

## Progression & AA

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| XP/AA rate tuning | — | Later | 4 | Rules |
| AFK xp/AA farming support | — | Later | 4 | Auto-combat + pet guard |
| Expanded/opened AAs | THJ | Icebox | 6 | Verify Quarm coverage first |

## Admin / GM

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Tiered GM roles for friends | — | Later | 4 | `account.status` + `command_settings` |
| Buffed quest xp/rewards | — | Later | 4 | Quest scripts + rules |

## Client / UX (optional polish)

| Item | Src | Priority | Phase | Notes |
| --- | --- | --- | --- | --- |
| Zeal "Attunement" panel + gauges | — | Later | 6 | `uifiles/zeal` custom window |
| Scribe-time UX via akplus/Zeal | — | Conditional | 1/6 | Only if Phase 1 shows client blocks scribing |
| Class declaration via NPC (post-creation), not char-create | THJ (borrow) | Soon | 2 | Avoid a custom char-create client; use a Bazaar/Nexus NPC flow. See `CLIENT-STRATEGY.md` |

## Parking lot (raw ideas, undecided)

- Diablo-style loot beams / rarity SFX (client limits on Mac client — likely icebox).
- Endgame focus on Planes / later expansions instead of early grind.
- Larger inventory/QoL conveniences to "get rid of early-level grinds".
- Server-side storage "uniqueness": weigh a dedicated custom table (e.g. `thorne_character_build`)
  vs. reusing `data_buckets` for declared classes / affinity / allocation — schema-change-free
  and portable vs. more queryable/efficient. See `CLIENT-STRATEGY.md` + `MULTI-CLASS-DESIGN.md`.
- Multiple-pet control and `/cast`-from-spellbook macros both depend on a client-capability
  audit (Mac client + Zeal) before committing — see `CLIENT-STRATEGY.md`.
