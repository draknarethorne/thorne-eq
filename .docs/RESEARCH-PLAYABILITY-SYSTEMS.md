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
