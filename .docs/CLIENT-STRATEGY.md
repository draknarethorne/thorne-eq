# Client Strategy — What We Will and Won't Do

> **Status: DRAFT / provisional.** This captures the client-modification philosophy so
> we can keep digging, planning, and re-planning. Nothing here is locked until we've
> (1) seen the **stock, unmodified** server run and (2) completed a client login test.
> Companion docs: `MULTI-CLASS-DESIGN.md`, `RESEARCH-MULTICLASS.md`, `BACKLOG.md`.

---

## 1) The core question

THJ (The Heroes' Journey) shipped a **custom client** so players could **declare a class
blend at character creation**. That gave them a clean up-front experience, but it also
means every player must run their bespoke executable and they own a client fork forever.

We want the *idea* (declared, curated hybrid classes) **without inheriting a custom
char-create client**. So the guiding question for every client-touching feature is:

> Can the **server** drive this through interactions the **stock/approved client already
> understands** — instead of changing the client executable?

Default answer: **yes, push it server-side.** The client stays a compatible viewer.

---

## 2) Guiding principle (unchanged from repo charter)

- **Server-authoritative always.** Declarations, unlocks, caps, and prohibitions are
  enforced and stored server-side. The client is never the source of truth.
- **Client-compatible always.** We target the stock Mac/Quarm client plus a small set of
  **approved** add-ons. No full client rewrite, ever.
- **Unique, not a THJ clone.** We borrow the *concept*; we differentiate on *delivery*
  (NPC-driven, hub-based, curated) and on *systems* (affinity + equalizer layering).

---

## 3) Tiers of client change — the will/won't list

| Tier | Example | Verdict |
| --- | --- | --- |
| **T0 — Stock client** | Mac/Quarm client, 15 base classes, standard opcodes | **Must always work** with zero mods. The floor. |
| **T1 — Approved DLLs** | Zeal (`zeal.asi`, CoastalRedwood fork), `eqw.dll` | **Allowed** — QoL/UX only, no server authority. |
| **T2 — UI XML** | `uifiles/` edits, Zeal custom windows/gauges | **Allowed** — our Thorne-UI work lives here. |
| **T3 — Custom EXE behavior** | new char-create screen, new class enum, protocol/opcode changes | **Won't do.** This is the THJ path we're avoiding. |

The dividing line: **T0-T2 are viewers/skins; T3 changes the game the client thinks it's
playing.** We stay at or below T2.

---

## 4) How the interactions fit without a custom client

Because we won't touch char-create (T3), the hybrid experience moves to **post-creation,
NPC-driven** flows the stock client already renders:

- **Character creation:** unchanged. Player picks one of the 15 stock classes as their
  **primary anchor** (fixes melee floors / core fantasy).
- **Declaration (adding secondaries):** visit an **Attunement NPC** at a hub
  (Bazaar / Nexus). Uses stock **dialogue + item turn-in / token** mechanics (Perl/Lua
  quest scripts). Server writes the declared-class bitmask to storage.
- **Role swap (between fights):** an NPC or a **consumable item** toggles which declared
  lines are active — out of combat, in a safe location.
- **Re-attunement / respec:** same hub NPC, gated by cost/cooldown.
- **Readout (optional, later):** a **Zeal panel** (T2) shows declared classes / affinity —
  display only, no authority.

This keeps every interaction inside opcodes the stock client understands: say-dialogue,
loot/turn-in, buffs, item clicks.

---

## 5) What makes ours unique (vs THJ)

1. **No custom client** — approved DLLs + UI only; anyone on the compatible client can play.
2. **NPC/hub-driven, curated declaration** — the blend is discovered through the world
   (Bazaar/Nexus), not chosen on a bespoke creation screen.
3. **Affinity + Equalizer layering** — hybrid power comes from earned affinity tracks and a
   point-buy cap equalizer, not just a class checkbox (see `MULTI-CLASS-DESIGN.md`).
4. **Small-group self-sufficiency as the north star** — every feature is judged by whether
   it helps a **2-3 player group** stand in for a raid, cleanly and without exploits.

---

## 6) Open questions to validate (before committing)

- **Client capability audit (T0/T1):** does the Mac/Quarm client + Zeal support the
  dialogue/turn-in UX we want for declaration and role-swap? Any opcode gaps?
- **`/cast` from spellbook:** can we drive buff macros by spellbook slot (no spellbar
  swap)? Client-side feasibility drives this QoL item (`BACKLOG.md`).
- **Multiple pets:** how many controlled pets can the client display/target sanely? Pet
  bar / targeting limits inform the "2-3 pets per controller" idea.
- **Server-side storage uniqueness:** store declared classes / affinity / allocation in
  the schema-change-free `data_buckets` (portable, THJ-style) **or** a dedicated custom
  table (e.g. `thorne_character_build` — more queryable/efficient, but a schema addition)?
  Decide with an eye to rebuild-from-scratch portability + query cost.

---

## 7) Decision gate

Revisit and firm up Section 3 (will/won't) and Section 6 **after** the stock server runs
end-to-end and we've logged in once with the compatible client. Until then: experiment
freely server-side, keep the client at T2 or below, and record findings back here.
