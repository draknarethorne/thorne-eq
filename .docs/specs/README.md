# Thorne-EQ Specs

> **Specs decide; the backlog inspires.** `BACKLOG.md` collects wants; `ROADMAP.md` sequences
> phases; **these specs are the buildable contracts** — enough analysis and a concrete design +
> coding approach to validate a thesis *before* pure coding/hacking/fixing.
>
> Each spec is small, testable, and behind a feature flag. If a spec can't state its **acceptance
> test** and **rollback**, it isn't ready to build.

## Spec template

Every spec uses the same shape:

1. **Purpose** — the one thesis this validates, in a sentence.
2. **MVP expression** — the smallest shippable form (what we build first).
3. **Design & approach** — how it works; the rules/data model.
4. **Data & code seams** — exact tables, rules, and source hooks touched.
5. **Acceptance test** — the observable pass/fail that proves the thesis.
6. **Rollback** — how to turn it off with zero residue.
7. **Open questions** — decisions still owed (cross-ref `DECISIONS.md`).
8. **Status** — `Draft` / `Ready` / `In progress` / `Validated`.

## Delivery order (validate the thesis first, then enable the fun)

| # | Spec | Proves | Phase | Status |
| ---: | --- | --- | --- | --- |
| 01 | [Multi-Class Spike](SPEC-01-multiclass-spike.md) | Server-granted cross-class spells scribe/mem/cast on the Mac/Quarm client | 1 | Draft |
| 02 | [New Player Fast-Start](SPEC-02-new-player-fast-start.md) | A new character is combat-functional in minutes, no external twink | 1/2 | Draft |
| 03 | Rested / Offline XP+AA foundation | Day-1 offline bonus accrues for all characters, abuse-bounded | 3 | Planned |
| 04 | Renown / Momentum foundation schema | Two-meter contribution/streak model with active-participation gate | 2/4 | Planned |
| 05 | Death, Risk & Recovery | Death matters without item loss or deep-CR misery | 3/4 | Planned |
| 06+ | Reward crates, dupe-fusion, item ranks, Codex, seasonal | Retention/collector hooks (Sovereign DNA) | 4/5 | Planned |

## Principle

Prove the **crux** (multi-class) and the **first-hour feel** (fast-start) before anything
else. Rested XP and the meta layer lay schema early but activate after the crux is validated.
Keep every step reversible; never an irreversible global change in one commit.
