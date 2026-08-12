# Research — Multi-Class EQ Projects

> Living notes on how other EverQuest emu projects implement multi-classing, to learn from
> and borrow. Captured per the "script/save everything" principle. Deep code analysis is
> staged as a follow-up (clone THJ as a reference and grep it).

## Sources (confirmed)

| Project | What it is | Source / link | Client |
| --- | --- | --- | --- |
| **The Heroes' Journey (THJ)** | Multiclass progression server; the project this repo's vision cites | **Open source: `firestormalpha/TheHeroesJourneyServer`** (branch `staging`, ~138 MB) | RoF2 |
| **PerkyCrew** | Solo/duo-friendly; "multiclass-style AA choices", Rebirth, custom end-game | perkycrewserver.com (server; source not confirmed) | RoF2 |
| **Ascendant** | EQEmu progression server (mentioned alongside) | (to confirm) | RoF2 |
| **EQ Classless 3.0** | Classless on the **Mac client** — already on disk | `B:\SecretsOTheP\classless-dll` (MQ2-style client DLL) | Mac/TAKP |

## Early takeaways (from public info)

- **THJ multiclass = a fixed 3-class combo** chosen by the player (e.g. `clr/rog/sk`,
  `clr/mnk/xx`), not free-form classless. This matches our **"curated, not classless"** pillar
  — a strong validation of the declaration-first direction.
- THJ leans heavily on **AA** for cross-class power and QoL ("op hammer pet", etc.), and is
  **solo/duo tuned** — same north star as ours (small groups do big content).
- **PerkyCrew** frames multiclass as **AA choices + Rebirth** (a prestige/respec loop) rather
  than raw class stacking — a lighter-weight model worth comparing to our Equalizer (Phase 5).
- **Client difference matters:** THJ/PerkyCrew/Ascendant are **RoF2**; we are **Mac/TAKP**.
  Their UI-driven mechanics (custom windows, pet bags) may not port — but their **server-side**
  class/spell/AA handling is the transferable part. Cross-check against EQ Classless 3.0
  (`B:\SecretsOTheP\classless-dll`), which is our on-client precedent.
- **IP/legal note:** several emu servers (incl. THJ) hit Daybreak legal action in 2025; Quarm
  returned under an agreement. Keep Thorne-EQ private/personal and IP-careful.

## Deep-dive plan (next research pass)

1. Clone `firestormalpha/TheHeroesJourneyServer` as a read-only reference (near the `B:\` repos).
2. Grep for how a character's multiple classes are **stored** (extra column? data bucket? AA?)
   and how **spell/skill eligibility** is resolved for the combo (the choke point we care about).
3. Compare THJ's approach to our `CanUseSpell` overlay plan in `MULTI-CLASS-DESIGN.md`.
4. Extract any **missing pieces** we lack (e.g. tables, rules, AA definitions) and fold into
   `db/bootstrap/` if useful.
5. Record concrete findings here with file/function citations.

## Open questions to answer from THJ source

- Does THJ change the `class` field, add a second-class field, or overlay via AA/scripts?
- How does it gate which spells a combo can scribe/cast (server-side vs client)?
- How are the 3-class combos defined/curated (a table? hardcoded matrix?)?
- What does "Rebirth"/respec look like mechanically (PerkyCrew)?
