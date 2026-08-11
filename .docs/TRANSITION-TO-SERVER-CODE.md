# Transition Guide — Thorne-EQ Server Bootstrap

## Purpose

This document is the handoff bridge for opening a fresh workspace + chat and deciding how to establish the canonical server-code foundation for `thorne-eq`.

## Current State

- Local project root: `C:\Thorne-EQ`
- Remote repo: `https://github.com/draknarethorne/thorne-eq`
- Repo status: initialized with planning docs (`README.md`, `.docs/*`, `VERSION`)
- Strategic baseline preference: Quarm-compatible lineage with server-authoritative progression systems

## Decision We Need in Next Chat

Choose **one** source-control model for server code intake:

1. **Fork-first model (recommended for long-term maintainability)**
   - Fork upstream codebase to your GitHub.
   - Add upstream remotes and sync strategy.
   - Keep your custom mechanics isolated in feature branches.

2. **Direct vendor import model (faster start, harder long-term sync)**
   - Import snapshot into this repo directly.
   - Maintain manual merges from upstream as needed.

## Upstream Candidate Priority

1. `SecretsOTheP/EQMacEmu` (Quarm-adjacent practical baseline)
2. `EQMacEmu/Server` (Al'Kabor-focused upstream lineage)
3. `EQEmu/EQEmu` (broad ecosystem fallback/reference)

## Recommended Starting Path

- Preferred: **Fork `SecretsOTheP/EQMacEmu`** and track `EQMacEmu/Server` as upstream reference.
- Why: Quarm-relevant behavior today + realistic path for continuing sync discipline.

## First Technical Objectives After Code Intake

1. Build + run baseline server unchanged.
2. Document branch/remotes strategy.
3. Introduce feature flags for hybrid capability system.
4. Add first data model scaffolding for:
   - affinity tracks,
   - spell-family restrictions,
   - archetype profile grants/limits.

## Client Constraint Guardrails

- Keep core logic server-side; avoid requiring broad client rewrites.
- Treat Zeal/extensions as optional UX enhancement, not core authority.
- Preserve classic EQ class readability while enabling curated cross-domain progression.

## Suggested New Chat Kickoff Prompt

Use this prompt in a new chat opened from `thorne-eq.code-workspace`:

> We are in `C:\Thorne-EQ`. Use `TRANSITION-TO-SERVER-CODE.md` and `README.md` as authority. Help me choose and execute the best source intake path for Quarm-compatible server code (fork vs direct import), then set up remotes/branch strategy for long-term upstream sync and feature-flagged hybrid class progression work.

## Definition of Done for Transition Phase

- Workspace opens cleanly in VS Code.
- Source intake model chosen and documented.
- Upstream/fork remotes configured and verified.
- Baseline server compiles/runs without custom gameplay changes.
- Next milestone issues created for v0.1 implementation.
