# Research — Playability Systems That Fit the Needle

> Goal: identify systems that improve small-group self-sufficiency while staying
> **server-authoritative** and **Mac-client-compatible**. This is the shortlist of
> ideas that look like they can actually work, with the likely code seam and the
> main constraint.

## Feasibility legend

- **Green** — mostly server-side; low client risk.
- **Yellow** — feasible, but needs targeted client/Zeal validation.
- **Red** — possible long-term, but expensive or risky enough to avoid early.

## Feature threads

| Feature thread | Fit | Likely seam | Constraint / note |
| --- | --- | --- | --- |
| Attunement NPCs in Bazaar/Nexus | Green | `quests/*` (`EVENT_SAY`, `EVENT_ITEM`), `data_buckets`, rules | Cleanest path for class declaration, role swap, respec |
| Primary pet + swarm/ward companions | Green | `zone/aa.cpp`, `Mob::SpellProcess()`, pet spell lanes | Preserves one-primary-pet client assumption |
| Bigger bags / better WR | Green | DB item rows, `common/item_data.h` | `BagSlots` are fixed to **2/4/6/8/10**; do not invent 12+ slot bags |
| Low/mid global loot refresh | Green | `zone/loot.cpp`, global loot, `#lootsim` | Great fun-per-effort, easy to A/B test |
| Ground supply caches / loot chests | Green | `zone/inventory.cpp`, `CreateGroundObject`, ground spawns | Static/timed object interactions are already supported |
| Treasure-runner NPCs | Green | `aggro`, flee logic, special abilities, custom loottables | High flavor without client changes |
| Quest-supplied consumable packs | Green | quests + DB items | Smooths solo/small-group friction immediately |
| Smarter rule-based NPC behavior | Green | `aggro.cpp`, `attack.cpp`, `hate_list.cpp`, quest timers | Better first step than external AI |
| Equalizer UI with apply/save | Yellow | Zeal `ui_options.cpp`, `zeal_settings`, custom XML | Zeal already supports writable options + `.ini` persistence |
| Spellbook `/cast` buff macros | Yellow | Client command layer / Zeal command hooks | Needs proof that cast-by-book-slot is practical |
| Multiple permanent pets | Yellow/Red | `GetPet()`, single `PetID`, pet command flow | Current model is deeply single-primary-pet |
| Random item affixes on live items | Red | item packets / item schema / client display | Better to fake this with pre-authored item families early |
| Runtime AI-driven NPC dialogue/combat | Red | external service boundary | Flavor only if ever; never server authority early |
| Thorne patcher / launcher | Yellow/Red | separate utility / installer | Better as optional later distribution layer |

## RunUO / Featherstone case study (2026-08-12 diff passes)

The strongest proof-of-fun reference is not a public server at all — it is the
old `C:\RunUO\Development` tree compared against `C:\RunUO\UO2.3\2.3` and the
older `C:\RunUO\Base` scripts. That comparison shows a consistent design pattern:

- reduce repetitive gather friction,
- improve small-group independence,
- add travel convenience,
- preserve danger while softening grind,
- and move quality-of-life into world objects, quests, and NPC services.

### Concrete systems confirmed in the code

- **Placable refillable supply infrastructure**
  - `Scripts/Customs/Featherstone/SupplyChest.cs`
  - `Scripts/Customs/Featherstone/FeatherContainer.cs`
  - The chest is not just loot. It is a **movable house object** that fills with
    huge stacks of crafting/gathering supplies, has upgrade states, and either
    **resets** or **deletes** on a timer depending on state.
- **Personal travel stone / city recall item**
  - `Scripts/Customs/HomeStone.cs`
  - Ownership, markable home location, cooldown, blessed item semantics.
  - `ServerInfo.cs` also confirms every new player got a **Featherstone** travel item.
- **Player-city hub conversion**
  - `Scripts/Customs/Decorate Magincia.cs`
  - `Data/Magincia/*`
  - Release notes explicitly say Magincia references were changed over to Featherstone
    and that world decoration/buildings/vegetation were added.
- **Pet-friendly quality-of-life**
  - Release notes confirm: domestic-pet state after release, non-domestic cleanup,
    reduced aggro on taming, increased taming range, single-pet claim from stables,
    follower counting fixes, and young-player pet-heal allowances.
- **Quest + loot smoothing**
  - Release notes confirm unique drops on quest monsters, custom Featherstone quests,
    updates to random quest-giver equipment, better chest contents, and boosted early
    inventory/gold for new characters.
- **Player-visible service UI / social QoL**
  - `ServerInfo.cs` advertises global chat, activity logs, server status, vendor-finder
    travel, and `[Where]` location visibility for all players.

### Important caveat

I **did not yet find** a dedicated `Moderator` access level or a single obvious
"take less damage / super-powered pets" switch. `Development/Source/Mobile.cs`
still exposes the standard enum (`Player`, `Counselor`, `GameMaster`, `Seer`,
`Administrator`, `Developer`, `Owner`). The friendly-play outcomes may instead be
distributed across:

- young-player/account logic,
- follower/pet-slot tuning,
- pet behavior changes,
- loot/progression smoothing,
- spell and duration adjustments,
- and content/hub conveniences.

If we want the exact implementation, the next pass should be a purpose-built diff of
`Development/Source` against the closest original RunUO source snapshot.

## Broader diff scan — shared-file hotspots

To catch the "small adaptations everywhere" pattern, I also compared the **shared**
script files between `C:\RunUO\UO2.3\2.3\Scripts` and `C:\RunUO\Development\Scripts`.
There are **1106 changed shared files**, which confirms this was not only a custom-folder
story; you also edited lots of stock behavior in place.

### Highest-signal shared-file hotspots

- `Mobiles/PlayerMobile.cs`
- `Misc/CharacterCreation.cs`
- `Items/Misc/Teleporter.cs`
- `Items/Misc/Corpses/Corpse.cs`
- `Misc/Loot.cs` and `Misc/LootPack.cs`
- `Mobiles/Vendors/BaseVendor.cs` and many vendor/mobile files
- `Skills/AnimalTaming.cs`
- `Mobiles/Vendors/NPC/AnimalTrainer.cs`
- `Spells/Base/SpellHelper.cs`
- `Misc/AOS.cs`
- `Engines/CannedEvil/ChampionSpawn.cs`
- `Engines/Spawner/Spawner.cs`
- `Items/Skill Items/Magical/Spellbook.cs`

### What that likely means for Thorne-EQ

The Featherstone philosophy was distributed through the whole game loop:

- **starting state** (`CharacterCreation.cs`)
- **travel and movement convenience** (`Teleporter.cs`)
- **pet / tame / stable friendliness** (`AnimalTaming.cs`, `AnimalTrainer.cs`)
- **loot and reward pacing** (`Loot.cs`, `LootPack.cs`, chest systems)
- **combat feel and survivability** (`AOS.cs`, `SpellHelper.cs`, weapon/armor bases)
- **service discoverability and vendor friendliness** (`BaseVendor.cs`, player-vendor UI)

That is the direct analogue for Thorne-EQ: if we want it to feel great for friends and a
small group, we should expect to tune **many small seams**, not chase a single silver bullet.

## Platinum pass synthesis (hotspot-by-hotspot)

The focused report at `.tmp/runuo_platinum_pass.txt` reinforces the same conclusion,
but with clearer implementation patterns we can port to EQ immediately.

### What changed most in RunUO and why it matters

- `Mobiles/PlayerMobile.cs` (very high churn)
  - Heavy pet/follower quality-of-life and inventory/economy touchpoints.
  - Suggests that "friendly shard" feel came from many player-loop adjustments,
    not one privileged role toggle.
- `Misc/CharacterCreation.cs`
  - Explicit front-loading: big starter cash/bank injections, travel helpers,
    and pre-packed progression convenience.
- `Mobiles/Vendors/BaseVendor.cs`
  - Vendor behavior tuned toward availability and practical trading outcomes.
- `Mobiles/Vendors/NPC/AnimalTrainer.cs` + `Skills/AnimalTaming.cs`
  - Pet-capacity, claim flow, taming friction, and stable economics were all tuned.
- `Misc/LootPack.cs` + `ChampionSpawn.cs`
  - Reward frequency and payout pacing shifted to reduce dead-time and increase momentum.

### High-confidence patterns to copy (not code, just design intent)

1. **Front-load onboarding without trivializing progression**
   - RunUO used aggressive starter grants (huge gold/bank checks). For EQ, use a
     bounded equivalent: meaningful startup capital + practical supplies, not raid-grade power.
2. **Move friction from routine actions to optional goals**
   - Spell access, travel, pet management, and restocking should be easy.
   - Long-tail prestige should remain in quests, camps, and social objectives.
3. **Treat vendors/NPCs as service infrastructure**
   - A low-pop shard needs NPC systems that partially emulate missing player economy.
4. **Favor reversible economic levers**
   - Adjust with tables/rules and scheduled NPC inventories, not hardcoded one-way gifts.

### Anti-patterns to avoid in EQ

- Do **not** copy extreme raw-currency starts (e.g., giant direct bank grants) 1:1.
- Do **not** bypass class identity with universal spell access shortcuts.
- Do **not** rely on client-side authority for anything economic or progression-critical.

## EQ translation pack from the platinum pass

### A) Starter economy kit (server-side, data-driven)

Implement at character onboarding NPC (or first-login claim):

- **Starter coin grant**: enough for spells/food/basic tools through early bands.
- **Bank seed**: a smaller reserve cushion to reduce early failure spirals.
- **Starter supplies**: food/water, bandages/reagents by class lane, basic ammo.
- **Travel starter**: cooldown-limited Nexus recall consumable or charge item.

Balance levers:

- one-time per character,
- optional account-age rules,
- claim-flag in `data_buckets`,
- per-class and per-level-band values from DB tables.

### B) WR bag ladder (practical, not luxury)

Use the user-requested stepped model as the baseline shape:

- **Tier 1** (newbie): modest WR + practical slots.
- **Tier 2** (journeyman): improved WR from early quests/faction.
- **Tier 3** (specialist): high WR but still effort-gated.

Implementation posture:

- stay within stock bag slot constraints,
- gate upgrades via achievements/quest completions,
- keep top-end prestige bags outside starter lane.

### C) Spell set bundles (class + level band)

From the `CharacterCreation.cs` pattern, EQ equivalent should be:

- purchasable class bundles (`1-20`, `21-40`, `41-50`) as satchels/tomes,
- optional subsidized pricing for first character per account,
- strict class whitelist for contents.

This preserves the spell-chain ritual (scribe/use) while removing vendor crawl overhead.

### D) Pseudo-player vendor economy (for low-pop reality)

Define a curated NPC market layer that simulates player supply for baseline goods:

- rotating inventory pools for crafted staples,
- dynamic restock timers,
- price bands with caps/floors,
- optional faction discounts,
- sink hooks (fees, repair, reroll tokens, travel permits).

Guardrails:

- no best-in-slot raid items,
- no infinite arbitrage loops,
- no bypass of attunement/progression gates.

### E) Pet helper quality lane

Instead of true multi-primary pets now:

- increase convenience via stances, claim flow, and summon-helper lanes,
- improve survivability/command responsiveness,
- keep one-primary-pet authority model intact.

## Recommended staged rollout (platinum-derived)

1. **Immediate**: starter economy kit, Tier 1 WR bags, spell bundles `1-20`, travel consumable.
2. **Soon**: Tier 2 bag path, spell bundles `21-40/41-50`, vendor market v1, pet QoL pass.
3. **Later**: market dynamic pricing v2, Tier 3 specialist bags, advanced helper summons.

Rollback conditions:

- inflation spike beyond target range,
- major vendor-arbitrage exploit,
- starter kits measurably suppressing early-zone engagement.

Success metrics:

- time-to-functional-character (spells, supplies, movement) drops significantly,
- early retention and session length improve,
- platinum velocity remains within configured bounds,
- no reduction in class identity compliance checks.

## Adaptation concept catalog — what was actually changed (the gems)

This is the payoff of the analysis: the concrete Featherstone changes, what each one
*accomplishes*, and whether the **concept** carries to Thorne-EQ. Two kinds of change
matter — new systems you authored, and small edits to stock code that are easy to miss
but carry real gameplay weight.

### A. New systems authored (dev-only files)

| System | What the code does | EQ concept | Verdict |
| --- | --- | --- | --- |
| Supply chest (`SupplyChest`, `FeatherContainer`, `FeatherChest`) | Placeable object that refills bulk gather/craft supplies; timed reset/delete | Renewable supply depot / house cache to kill restock grind | Adapt |
| Home stone (`HomeStone`) | Personal bind + recall item; ownership, cooldown, blessed | Personal Nexus-recall clicky with cooldown/bind rules | Adopt |
| Elementalist spell line (`FrostBolt`, `FrostNova`, custom spellbook/scroll/gump) | Whole custom spell school + book/scribe UI | Curated custom spell family gated by class/affinity | Adapt |
| Featherstone service NPCs (Banker, Greeter, Guard, Quester, Ranger, Vendor, PrinceScott) | Named hub NPCs providing bank, greet, guard, quests, vending | NPC-driven service hub (attunement broker, quartermaster, clerk) | Adopt |
| Ops/logging engines (`AccountLog`, `ActivityLog`, `ChatLog`, `Logs`, `LogRoller`, `ServerInfo`) | Structured logs, activity feed, server-status readout | Operator observability + player-facing service notices | Adapt |
| Starter/gift items (`Gifts/*`, `SupplyBags`, `Stones`, `WebStone`) | Seasonal grants, starter bags, utility stones | Starter boon package + utility clickies | Adapt |

> Note: the large `Customs/Mondain's Legacy` (834), `Xml Spawner` (94), and `Neruns Distro` (46)
> trees are **imported distributions**, not authored design — treat as baseline, not intent.

### B. Small adaptations to stock code (easily-missed, high-impact)

| Area | Change (before → after) | What it accomplishes | EQ concept | Verdict |
| --- | --- | --- | --- | --- |
| Field spell durations | FireField `15→35`, PoisonField `3→15`, ParalyzeField `3.0→6.0`, VengefulSpirit `+10→+25` | Longer control/DoT windows help small groups | Rule-tuned spell durations for group viability | Adapt |
| Summon follower cost | `ControlSlots 2→1`; follower checks `+2→+1` across SummonCreature/Kirin/elementals/BladeSpirits/EnergyVortex/Daemon | Players field more/utility pets cheaply | Cheaper swarm/utility summons vs one primary pet | Adapt |
| Duel restriction removal | Removed ConPVP "sudden death" `CheckCast` in Cure/Heal/Str/Cunning/Agility/GreaterHeal/CleanseByFire | Strips PvP-only casting friction | Don't port PvP gates that don't fit PvE shard | Skip (context-specific) |
| Timing normalization | `Core.ML ? 10 : 12 → 12` across many spells | Consistent cast/recovery regardless of expansion flag | Deterministic spell timing constants | Adapt |
| Buff vs curse duration split | `GetDuration` → `GetBonusDuration` / `GetCurseDuration` | Separate tuning for buffs vs debuffs | Independent buff/debuff duration levers | Adopt |
| Stable capacity | AnimalTrainer max `2/3/4/5 → 10/11/12/13`, wider claim range, single-pet claim | Pet-heavy QoL without micromanagement | Larger stable + one-at-a-time claim | Adapt |
| Housing cost | Customization `10000→100`, per-component `500→50` | Near-free player housing customization | Cheap personal/base customization sink | Adapt |
| Recall cost | Recall via runebook charge (no mana) | Travel without mana tax | Charge/consumable-based travel | Adopt |
| Skill training | TeachEntry always teaches, skips gold | Free early skill access | Subsidized starter training | Adapt |
| Barding difficulty | Uses current `Hits/Stam/Mana` vs max | Easier to bard damaged targets | Situational skill-difficulty tuning | Consider |
| Vendor activity | `IsActiveBuyer/Seller` require `SBInfos.Count > 0` | Stops empty vendors erroring/interacting | Vendors only trade with real stock lists | Adopt |
| Item policy | TreasureMap `LootType.Blessed` removed | Maps become droppable/lootable | Explicit protected/risky/volatile item tiers | Adapt |
| Spell gating | ArcanistSpell requires epic quest completion | Locks a school behind a quest | Affinity/quest-gated spell families | Adopt |
| Command access | `Where` Counselor→Player; `Cast`/`Client` Counselor→GameMaster | Players self-locate; tighten power cmds | Player-facing utility commands, tight power cmds | Adapt |
| Detection threshold | Hidden-check `AccessLevel.Player → GameMaster` in traps/effects/switches | Only true GMs bypass, not counselors | Precise staff-tier boundaries | Adapt |
| Loot resilience | LootPack `IsInTokuno` null-safe (no mobile) | Custom loot flows won't crash | Defensive null-safety in custom loot | Adopt |
| Starter economy | CharacterCreation newbie gold + bank checks | Front-loaded startup capital | Bounded starter coin/bank seed | Adapt (bound it) |

### C. Server-support / identity adaptations

| Change | What it accomplishes | EQ concept | Verdict |
| --- | --- | --- | --- |
| `Console.WriteLine → ConsoleLog/AccountLog` everywhere | Centralized, categorized logging | Structured server logging standard | Adopt |
| `ServerName = "Featherstone"`, email/crash config | Server identity + crash/ops routing | Shard identity + ops alerting | Adapt |
| Activity/chat logs + `ServerInfo` readout | Player-visible world/service state | Player service notices + status board | Adapt |

### Carry-forward shortlist (highest concept value for EQ)

1. Personal recall clicky + NPC service hub (travel + services in one place).
2. Renewable supply depot to kill restock grind.
3. Cheaper/utility summons layered on one primary pet.
4. Independent buff vs debuff duration tuning.
5. Explicit item-policy tiers (protected/risky/volatile).
6. Quest/affinity-gated custom spell families.
7. Structured logging + player-facing service notices.

### Explicitly skip / re-scope for EQ

- PvP/duel-context removals (Featherstone-specific, not relevant to a PvE shard).
- Raw currency mega-grants (adopt the *intent*, not the 50k/1M magnitudes).
- Imported distro bulk content (baseline, not design signal).

## Methodology (brief)

The catalog above is grounded in a diff of `Development/Scripts` against `UO2.3` and `Base`
baselines, covering both edited common files and added/removed files (dev-only content).
Custom work lives in `Scripts` (RunUO `Source` is core engine and not script-populated), so
script-layer coverage is complete for concept extraction. Raw scan artifacts live in `.tmp/`
(`runuo_micro_context_report.md`, `runuo_scripts_setdiff.md`, `runuo_devonly_focus.md`) if a
detailed trace is ever needed; they are disposable and not the source of truth \u2014 this catalog is.

One durable principle from the passes: **impact is not proportional to diff size**. Several
one-line edits (durations, follower slots, access thresholds, item policy) are among the
highest-value concepts, so low-churn files stay in scope for any future review.

## Starter spells / starter loot philosophy for EQ

RunUO's `CharacterCreation.cs` is explicit: you front-loaded gold, travel, deeds, mounts,
and even full spellbook-style support. The closest EQ analogue is very viable.

### Feasible implementation lanes

- **Starter spell satchel / class kit (preferred early path)**
  Sold or granted by an NPC, keyed by class and level band. Contains the normal
  vendor-purchasable scrolls/tomes for that class up to a target level
  (e.g. 1-20, 1-40, 1-50). Player still **scribes** the items normally, so this
  stays close to stock behavior.

- **Bag-generating spell set token**
  A clicky/token or quest reward that summons a bag of the right spell items.
  EQ already has item-summon effects and item-summon-into-bag effects in `spdat`.

- **Direct auto-scribe (more invasive)**
  Write directly into the spellbook/profile instead of generating items. Possible,
  but more invasive because it touches scribing semantics, spellbook state, and any
  `allow_spellscribe` / spell global / spell bucket rules.

### Starter-spell recommendation

Use **items first, automation second**:

- **starter loot** = a new-character boon package
- **starter spells** = class-specific spell satchels or purchasable spell-set bundles
- **later convenience** = optional direct-scribe helper only if the item flow feels too clunky

That mirrors the Featherstone pattern cleanly: preserve the recognizable ritual, remove the
needless vendor scavenger hunt.

## Concrete recommendations

### 1) Pets: fake “multiple pets” before building true multiple pets

### What the code says now

- The active command flow in `zone/client_packet.cpp` is centered on **one** `GetPet()`.
- State is stored as one `PetID`, one `m_petinfo`, and one `m_suspendedminion`.
- That means true multiple permanent pets is not a light patch; it is a cross-cutting rewrite.

### What actually works sooner

- Keep **one primary controllable pet**.
- Add **swarm pets, totems, wards, turrets, spirits, shades** as timed helpers.
- Add pet-stance improvements and small-group utility buffs to the primary pet.

### Why this threads the needle

- Players feel like they have a richer summon/squad identity.
- The client still only has to command one true pet.
- Server logic remains understandable and reversible.

### 2) Bags: improve capacity, not the UI contract

`common/item_data.h` explicitly documents:

- `BagSlots` = **2, 4, 6, 8, or 10**
- `BagSize` and `BagWR` already exist as stock fields

### Safe path

- Add more **10-slot**, **Giant-size**, **80-100% WR** bags.
- Gate better bags by quests, factions, attunement milestones, or self-found achievements.
- Add role-specific utility bags (reagent satchel, pet-tool satchel, forager pack) via normal item data.
- Add **house supply chests / depot clickies** inspired by Featherstone: not more bag UI,
  but renewable access to baseline materials so players spend less time restocking.

### Avoid early

- Anything implying **more than 10 visible bag slots**.
- Any custom container UI requirement.

### 3) Loot: prefer richer tables and curated pseudo-affixes over procedural packets

The server already gives you excellent hooks:

- `zone/loot.cpp` — loottables and lootdrops
- `zone/global_loot_manager.*` — broad overlays
- `zone/gm_commands/lootsim.cpp` — built-in simulation to validate drop economics
- `zone/inventory.cpp` / `OP_GroundSpawn` — dropped objects on the ground

### High-value early ideas

- Refresh early/midgame trash mobs with **global utility drops**.
- Add **supply caches** and **treasure chests** to grind loops.
- Add **treasure-runner NPCs** that flee, kite, or call help.
- Create **pre-authored item families** (same model, different tuned stats / proc / clicky) instead of true random affixes.
- Add **quest / house-linked refill caches** as a controlled, opt-in anti-grind system
  instead of forcing gather loops for basic upkeep.

### Why pre-authored beats fully random early

- The client already knows how to display a stock item by ID.
- You can still make loot feel spicy without inventing new packet semantics.
- Balance remains scriptable and testable.

### 4) NPC intelligence: start with “script brains,” not cloud brains

Best current seams:

- `zone/aggro.cpp`
- `zone/attack.cpp`
- `zone/hate_list.cpp`
- quest events (`EVENT_SAY`, `EVENT_ITEM`, `EVENT_TIMER`, `EVENT_COMBAT`, `EVENT_AGGRO`)

### Good first-generation intelligence

- Role packages: ambusher, runner, summoner, protector, priest, pack leader.
- Context reactions: flee at HP thresholds, call nearby allies, prioritize healers, prefer weak targets, reset to guard spots.
- Zone flavor state: dialogue or availability changes based on time, flags, local kills, or faction.
- Service-NPC state: vendor finder, attunement broker, supply quartermaster, travel clerk,
  and bounty board NPCs that present the world as a friendly operating hub.

### External AI later, maybe

- If used at all, keep it for **flavor text or quest prose generation**, not runtime authority.
- Combat resolution, loot, quest flags, and unlocks stay deterministic on the server.

### 5) Zeal UI: configuration is plausible, not just display

The local Zeal repo shows:

- writable settings via `zeal.ini`, `UI_<name>_pq.ini`, `<name>_spellsets.ini`, etc.
- a full options window implementation in `ui_options.cpp`
- UI managers and custom XML support under `uifiles/zeal`

### Implication

- An Equalizer/Attunement panel can plausibly be **interactive**.
- The client can store local presets and present sliders/buttons.
- The **server still validates everything** when the player applies a build.

### Recommended posture

- Start with NPC / item / command-driven flows.
- Add Zeal UI later as a convenience layer on top of the same server APIs/rules.
- Mirror the Featherstone pattern: **world object / NPC first, UI second**.

### 6) Patcher / launcher: optional delivery layer, not a prerequisite

A custom patcher is viable later, but it should remain a **distribution convenience** for:

- `zeal.asi`
- a Thorne UI skin / XML updates
- optional docs / presets

It should **not** be required to prove the server design.

## Suggested rollout order

1. **Stock server + client proof** — no gameplay changes yet.
2. **NPC-driven attunement flows** — declaration, role swap, respec.
3. **Featherstone-style convenience layer** — travel clicky, starter kits, supply caches,
   player-help hub services.
4. **Small-group sustain pass** — regen, duration, consumable packs, basic pet polish.
5. **Loot refresh pass** — low/mid tables, supply caches, treasure runners.
6. **Rule-based NPC intelligence pass** — smarter encounters and service NPCs.
7. **Zeal convenience layer** — readout first, configuration second.
8. **Long-tail experiments** — multiple permanent pets, patcher, pseudo-affixes, external AI flavor.

## Repo placement recommendation

- **Hub repo (`thorne-eq`)**: orchestration, rebuild scripts, DB/bootstrap SQL, design docs, cross-repo plans.
- **Server fork (`server/`)**: C++ engine changes, quest-engine changes, rule additions, source-level hooks.
- **Quests fork (`quests/`)**: Bazaar/Nexus NPC flows, bounty boards, treasure-runner scripts, attunement trials.
- **UI/Zeal forks**: XML skinning, Zeal options window changes, client-side convenience features.

That split keeps the hub as the rebuild brain and each fork as the code-of-record for its own runtime layer.
