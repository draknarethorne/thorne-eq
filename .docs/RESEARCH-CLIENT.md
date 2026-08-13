# Research — Client Architecture & Adaptation Strategy

> Strategic analysis of EQ client options (TAKP vs RoF2), where to source them, how to customize each,
> and the roadmap for Thorne-EQ's UI/client strategy. Companion: `ROADMAP.md`, `DECISIONS.md`.

## The client choice decision (executive summary)

| Axis | TAKP/Mac | RoF2 |
|------|----------|------|
| **Where to get** | Already own / TAKP community | Internet Archive (~8.3GB) |
| **Customization model** | Zeal ASI + XML UI files | Native RoF2 XML UI + Zeal equivalent |
| **Long-term UI (Phase 4-5)** | ❌ Clunky (NPC workarounds) | ✅ Native windows, panels, gauges |
| **Current TAKP UI work** | Thorne-UI (already written) | Would need RoF2 skin port |
| **Server opcode complexity** | Simple, TAKP-only | More complex, RoF2-only |
| **Innovation/differentiation** | Limited UI ceiling | Full modern client feature space |
| **Recommendation** | Use for Phase 1 spike test | Switch to for Phase 2+ shipping |

**Decision point:** After Phase 1 spike validation, commit to RoF2 for all Phase 2+ development.

---

## Part A: Understanding the EQ Client Landscape

### The three client tiers (as relevant to Thorne-EQ)

1. **Classic (Titanium, SoF, SoD, UF)**
   - Era: 2003–2010
   - Opcode set: Small, fixed, limited feature space
   - UI: Basic XML, limited extensibility
   - Used by: Classic/era-locked servers (Project 1999, etc.)
   - **Relevance to us:** Historical reference, not a target

2. **TAKP / Mac Al'Kabor**
   - Era: Planes of Power (2002–2003)
   - Opcode set: Tight, optimized for PoP features only
   - UI: Classic XML, enhanced by Zeal ASI framework
   - Customization: Zeal (ASI) + XML UI mods + limited Zeal extensions
   - Used by: TAKP, Project Quarm, Ascendant (some)
   - **Relevance to us:** Phase 0-1 testing, long-term optional support

3. **RoF2 (Rain of Fear 2, last modern client)**
   - Era: 2013 (December 2013 patch, final patch before EQ Live diverged)
   - Opcode set: Large, modern, supports expansions up to RoF2
   - UI: Advanced XML, native window system, extensible without DLL injection
   - Customization: Direct XML + asset swaps + client-native features (housing, pets, mercenaries, augments)
   - Compression: Modern (SOE compression, XOR encryption)
   - Used by: THJ, PerkyCrew, Ascendant, most modern EQEmu servers
   - **Relevance to us:** Phase 2+ primary target, richest feature space

### Protocol handshake is non-negotiable

When a client connects to an EQEmu server:

1. Client sends protocol identifier (e.g., `TAKP_PROTOCOL_VERSION`, `ROF2_PROTOCOL_VERSION`)
2. Server checks its opcode definitions for that protocol
3. **Match required** — if server doesn't have the client's protocol, connection rejected
4. **No crossover** — TAKP client cannot talk to RoF2 server, and vice versa

**Why this matters for Thorne-EQ:**
- Your choice of **server base** (EQMacEmu vs SecretsOTheP/Server) **locks in** which client(s) you can use
- EQMacEmu = TAKP protocol only
- SecretsOTheP/Server = RoF2 protocol (can optionally add TAKP support, but not default)
- You can build a **dual-protocol server**, but that's Phase 6+ complexity

---

## Part B: Obtaining Each Client

### TAKP / Mac Al'Kabor Client

**Sources:**
1. **Already have it** — you're actively playing TAKP, so you have a running copy
2. **TAKP community** — official download instructions at https://www.takproject.net/ or https://wiki.takp.info/
3. **Launcher tools** — QuarmPlus or other community patchers handle updates

**Setup for development:**
- You likely have this at `C:\TEQ` or similar
- For local testing: copy to a dev version like `C:\Thorne-EQ-Client-TAKP\`
- Zeal and Thorne-UI are already integrated (you know the workflow)

**Storage footprint:** ~500MB–1GB installed

---

### RoF2 (Rain of Fear 2) Client

**Primary source:**
- **Internet Archive:** https://archive.org/download/everquest_rof2 (~8.3 GB zip)
  - This is a community-archived copy of the last live RoF2 client
  - Legal status: Gray area (archived legacy client, not actively distributed by Daybreak)

**Secondary sources (community patchers):**
- **Firiona Vie Project:** https://fvproject.com/index.php/Client (includes patcher)
- **EQ Might:** https://www.eqmight.com/setup (includes patcher)
- **EQEmu forums:** https://www.eqemulator.org/forums/ (links and guides)

**Setup steps:**

1. **Download & Extract**
   ```
   1. Download everquest_rof2.zip (~8.3 GB) from Internet Archive
   2. Extract to C:\Thorne-EQ-Client-RoF2\
   3. (Do NOT use Program Files; use a user-owned directory)
   ```

2. **Patch the client**
   ```
   1. Download server-specific patcher (e.g., from Firiona Vie or EQEmu Discord)
   2. Run patcher in the C:\Thorne-EQ-Client-RoF2\ directory
   3. Patcher replaces obsolete files, applies protocol patches for EQEmu compatibility
   ```

3. **Verify launch**
   ```
   1. Right-click eqgame.exe → Properties → Shortcut
   2. Target: C:\Thorne-EQ-Client-RoF2\eqgame.exe patchme
   3. (The "patchme" flag tells the client to use EQEmu mode, not live)
   4. Launch and verify it reaches login screen
   ```

4. **Do NOT update via live launcher**
   - Never run the official Daybreak patcher on this client
   - It will break EQEmu compatibility
   - Keep Daybreak services/launcher disabled

**Storage footprint:** ~8–12 GB after extraction and patching

**Network requirements:** One-time download (8.3 GB), then local-only for testing

---

## Part C: Customization & Extension Models

### TAKP / Mac Client (Current model)

**Customization layers:**

| Layer | Tool | Scope | Example |
|-------|------|-------|---------|
| **Client executable** | None (sealed) | Protocol, opcodes (server-side only) | N/A |
| **DLL injection** | Zeal ASI (`zeal.asi`) | Runtime enhancements, extended commands, patches | `/zeal version`, camera controls, extra keybinds |
| **UI/XML** | XML files in `uifiles/` | Layout, colors, fonts, window positions, new gauges | Thorne-UI, custom spell windows, hotbars |
| **Assets** | Image files (TGA, PNG) | Textures, icons, UI graphics | Custom artwork for windows, gauges |

**Zeal framework specifics:**
- **Repository:** https://github.com/CoastalRedwood/Zeal (open source, actively maintained)
- **Installation:** Extract `zeal.asi` to EQ root directory; Zeal's UI folder to `uifiles/`
- **Extension points:**
  - Custom UI XML using Zeal's extended control set
  - `/zeal options` window for configuration
  - Zeal-aware macros and keybinds
  - Limited custom gauge/readout support
- **Limitations:**
  - Cannot add true new windows easily (XML-based only)
  - No native gauges beyond Zeal's built-in set
  - Cannot modify opcode-level features (must be server-side)

**Your current Thorne-UI:**
- XML-based, Zeal-compatible
- Runs on TAKP/Mac client
- Would need **porting to RoF2 UI model** (not a 1:1 translation, roughly 30-40% rework)

---

### RoF2 Client (Future model)

**Customization layers:**

| Layer | Tool | Scope | Example |
|-------|------|-------|---------|
| **Client executable** | None (sealed) | Protocol, opcodes (server-side only) | N/A |
| **DLL injection** | Zeal-equivalent or direct | Similar to Mac, but more extensible | Hypothetical custom loader |
| **UI/XML** | Native RoF2 XML system | Advanced windows, native gauges, complex layouts | Custom Attunement panel, Renown/Momentum gauges |
| **Assets** | Image files (DDS, TGA) | Textures, UI graphics, item icons | Custom artwork for modern windows |
| **Server-side features** | Packets, rule-driven UI state | Advanced: housing, augments, pets, mercenaries, real-time stat updates | Renown meter updates, multi-pet commands |

**RoF2 native capabilities (vs TAKP):**
- **Advanced window system:** Native support for dockable, resizable windows with more complex controls
- **Persistent UI state:** Windows can reflect server-side data (housing, pet status, mercenary commands)
- **Native gauges:** Built-in gauge/meter support (not Zeal-bolted-on)
- **Item evolution:** Items can visually change based on augmentation or upgrades (not just static icons)
- **Housing / real estate:** Full player housing UI and management
- **Mercenaries:** NPC hire/command UI (built-in)
- **Advanced chat:** Multi-channel, color coding, tell windows (native)

**Customization approach for Thorne-EQ:**
- Start with a **base RoF2 UI** (e.g., from community: NillipussUI, FrankenUI, or stock RoF2)
- **Port Thorne-UI elements** to RoF2 XML (roughly 2-3 weeks work for full feature parity)
- **Add new elements** for Phase 4-5:
  - Renown gauge (custom UI panel, connected to server-side data via packets)
  - Momentum meter (ephemeral, updates in real-time)
  - Attunement point-buy panel (custom window with sliders, apply/save buttons)
  - Declaration tome selector (integrated into an NPC interface or custom clicky window)

**UI development workflow:**
1. Edit XML files in `uifiles/thorne-ui-rof2/`
2. Launch client, type `/loadskin thorne-ui-rof2 1` (the `1` prevents reset on error)
3. Test hot-reload of UI changes
4. Iterate until happy

---

## Part D: THJ Client (What you have)

**What you have:** A custom RoF2 client + patcher setup from when you played THJ

**Where it came from:**
- THJ team built a custom **patcher/launcher** (open source, on GitHub)
  - https://github.com/botanicvelious/thj-launcher
  - https://github.com/christopherhspellman/thj-patcher
- But the **client itself** is just a patched RoF2 (not custom-built from source)
- Patcher handles server-specific opcode patches, UI files, and client tweaks

**Why it's valuable for your spike test:**
- It's **RoF2-compatible** (same protocol as modern EQEmu servers)
- It already has **server patches applied** (no need to re-patcher for testing THJ architecture)
- You can use it as-is for studying RoF2 customization patterns
- It gives you a working RoF2 environment **without** re-downloading 8.3 GB

**How to use it for Thorne-EQ:**
1. **Spike test (Phase 1):** Run multiclass validation on your THJ client
2. **Architecture study:** Examine how THJ's patcher structures UI files, opcodes
3. **Long-term:** Don't keep THJ client as shipping base (due to legal/optics concerns)
   - Instead, switch to a fresh, unmodified RoF2 from Internet Archive + your own patcher/setup
   - This gives you full control and zero baggage

---

## Part E: Opcode & Protocol Differences (Why this matters)

### TAKP Protocol

**Opcode definition set:** Tight, ~150–200 active opcodes
**Struct sizes:** Small, optimized for PoP features
**Example packets:**
- `OP_PlayerProfile` — character data
- `OP_CharacterCreate` — character creation
- `OP_Spawn` — NPC/player spawn
- `OP_CastSpell` — cast action
- `OP_ManaChange` — mana update
- `OP_ItemPlayerPacket` — inventory item

**Multiclass implications on TAKP:**
- Class bitmask stored in `data_buckets` (server-side, not sent in PP)
- Spell eligibility checked server-side (`CanUseSpell()`)
- Client sees only the primary class (no multiclass UI element)
- AA abilities are primary-class-only (no AA multiclass check needed)

### RoF2 Protocol

**Opcode definition set:** Large, ~400+ opcodes
**Struct sizes:** Larger, supports modern features (housing, mercenaries, augments)
**Example new opcodes (not in TAKP):**
- `OP_MercenaryList` — hire/command mercenaries
- `OP_HousingData` — player housing state
- `OP_AugmentItem` — item augmentation
- `OP_RealEstateLookup` — housing UI
- `OP_PetitionRefresh` — petitions system

**Multiclass implications on RoF2:**
- Class bitmask can optionally be sent in extended fields (if you add it)
- Spell eligibility still checked server-side (`CanUseSpell()`)
- **UI can show secondary classes** (custom window, not limited to single class display)
- AA abilities can respect bitmask (more flexibility in THJ's model)
- Augments and item eligibility based on bitmask (more feature space)

---

## Part F: Architecture Decision: Which server base + which client?

### The fork + client matrix

| Option | Server base | Client | Pros | Cons | Recommendation |
|--------|-----|-----|-----|-----|-----|
| **A: TAKP-only** | EQMacEmu | TAKP/Mac | Small scope, know the code | Phase 4-5 UI pain, limited audience | No (avoid) |
| **B: RoF2-only** | SecretsOTheP/Server | RoF2 | Rich feature space, native UI, modern | 8GB download, porting Thorne-UI (~2 weeks) | **YES (recommended)** |
| **C: Dual-protocol** | SecretsOTheP/Server | Both TAKP + RoF2 | Maximum compatibility | Double opcode work, Phase 6+ complexity | No (too early) |
| **D: Switch after Phase 1** | EQMacEmu (Phase 1) → SecretsOTheP/Server (Phase 2+) | TAKP (Phase 1) → RoF2 (Phase 2+) | Validate on TAKP, ship on RoF2 | Porting effort, but staged | **YES (pragmatic)** |

**Recommended path: Option D (staged switch)**
- **Phase 0-1:** Use EQMacEmu + TAKP client (you're already there)
- **Phase 1 spike:** Multiclass validation on TAKP (proves the concept)
- **Phase 2 boundary:** Switch to SecretsOTheP/Server + RoF2 client
- **Phase 2+:** Build Declaration, Equalizer, swap-lock on RoF2
- **Phase 4:** Identity layer (Renown/Momentum/Death) uses native RoF2 UI
- **Phase 5+:** Equalizer point-buy, optional TAKP support if demand warrants

---

## Part G: Practical Setup Roadmap

### Immediate (Phase 0-1): TAKP validation

**Actions:**
1. ✅ You have: TAKP client at `C:\TEQ`, Zeal, Thorne-UI
2. Complete Phase 0: Server brings up, client connects
3. Run Phase 1 spike: Necro + Mage multiclass test on TAKP
4. Document: What works, what doesn't (especially scribe-time enforcement)

**Outcome:** Multiclass architecture proven on TAKP, no client mods needed (or minimal)

### Medium-term (Phase 2 prep): RoF2 environment

**Actions (do this in parallel with Phase 1, or immediately after):**
1. Download RoF2 client from Internet Archive (~8.3 GB, ~2-4 hours depending on connection)
2. Extract to `C:\Thorne-EQ-Client-RoF2\`
3. Download + run a patcher (use Firiona Vie or EQMight, or build your own from botanicvelious/thj-patcher source)
4. Verify launch: `eqgame.exe patchme` reaches login screen
5. Fork SecretsOTheP/Server to a **parallel dev environment** (don't switch main server yet)
6. Test that RoF2 client can connect to a RoF2-protocol EQEmu server
7. Build a simple test character, verify basic gameplay works

**Outcome:** RoF2 environment ready, zero production risk (Phase 1 still on TAKP)

### Long-term (Phase 2 start): Full pivot

**Actions:**
1. Commit client choice to DECISIONS.md: "Switching from EQMacEmu/TAKP to SecretsOTheP/Server/RoF2 for Phase 2+"
2. Port multiclass logic from EQMacEmu → SecretsOTheP/Server (cherry-pick code, adapt to RoF2 opcode layer)
3. Port Thorne-UI to RoF2 XML (reuse design, adapt control set; ~2-3 weeks)
4. Build Declaration NPC + matrix on RoF2 server
5. Build UI panels for Declaration, Attunement, Renown/Momentum (RoF2-native)

**Outcome:** Shipping server on RoF2, full feature set ready for Phase 3+

---

## Part H: UI/Client Development Workflow Comparison

### TAKP workflow (what you know)

```
1. Edit Thorne-UI XML in uifiles/thorne-ui/
2. Launch TAKP client (Zeal loads automatically)
3. Type /loadskin thorne-ui 1 (reload with safety flag)
4. Test changes in real-time
5. Repeat
6. Commit XML files to git
```

### RoF2 workflow (what you'll learn)

```
1. Edit RoF2 UI XML in uifiles/thorne-ui-rof2/
2. Launch RoF2 client (no special loader, native XML support)
3. Type /loadskin thorne-ui-rof2 1 (reload with safety flag)
4. Test changes in real-time
5. Repeat
6. Commit XML files to git
```

**Similarity:** Virtually identical (XML-driven, hot-reload, same iteration cycle)

**Difference:** RoF2 has more advanced UI controls available natively (custom gauges, dockable windows, complex layouts)

---

## Part I: Custom Client Modifications (future consideration)

### If you need to modify the client itself (Phase 6+)

**Current constraints:**
- RoF2 client executable is not open source (closed IP)
- **Cannot legally redistribute modified client source**
- But you CAN inject via DLL (like Zeal does)

**Options if a feature requires client modification:**

1. **ASI Loader + DLL injection** (like Zeal)
   - Write a C++ DLL that hooks into the client at runtime
   - Use ASI Loader or similar to inject
   - Preserves stock client binary, adds features via runtime patching
   - Legal gray area, but established pattern in EQ community

2. **Advocate for feature via server-side mechanics**
   - Most features (Renown/Momentum/Attunement) can be entirely server-driven
   - Client just displays server-sent data (UI panels, gauges)
   - **Preferred approach** — no client modification, 100% legal

3. **Wait for upstream EQEmu support**
   - If feature becomes popular, EQEmu may add native support
   - Then your server code is portable to other forks/instances

**Recommendation:** Avoid client-level mods. Design Thorne-EQ entirely server-authoritative. Features like Renown/Momentum/Attunement are all server-side math; the UI is just a presentation layer (custom XML windows, packet-driven updates).

---

## Part J: Questions for Phase 2 decision

**Before you commit to the RoF2 pivot, answer these:**

1. **Can you live without your current Thorne-UI on day one of Phase 2?**
   - Yes, ship with default RoF2 UI initially, port Thorne-UI over ~2 weeks
   - Or: Spend 1 week porting Thorne-UI before switching

2. **Do you want to support TAKP players long-term?**
   - No: Ship RoF2-only (cleaner, faster development)
   - Yes: Plan for Phase 6+ dual-protocol support (much more work)

3. **Is 8GB download + setup acceptable for your dev environment?**
   - Yes: Go ahead with RoF2 setup in parallel
   - No: Skip RoF2 local testing until Phase 2 is approved

4. **Do you want to build your own patcher, or use an existing one?**
   - Build: Study botanicvelious/thj-patcher as a reference
   - Use: Adapt Firiona Vie or EQ Might patchers for your needs

---

## References & Resources

### TAKP/Mac Client
- **Official:** https://www.takproject.net/
- **Zeal framework:** https://github.com/CoastalRedwood/Zeal
- **Zeal guides:** https://quarm.guide/2024/11/24/zeal-readme/
- **UI modding:** https://www.eqinterface.com/ (search "Zeal" for compatible skins)

### RoF2 Client
- **Internet Archive source:** https://archive.org/download/everquest_rof2
- **Community patchers:** https://fvproject.com/index.php/Client, https://www.eqmight.com/setup
- **THJ patcher source:** https://github.com/botanicvelious/thj-launcher, https://github.com/christopherhspellman/thj-patcher
- **EQEmu forums:** https://www.eqemulator.org/forums/ (search "RoF2 setup" or "client")

### Opcode & Protocol
- **EQEmu opcodes:** https://github.com/EQEmu/Server/tree/master/opcodes
- **Packet wiki:** https://wiki.eqemulator.org/p=opcode:opcode_reference2

### Server Bases
- **SecretsOTheP/Server:** https://github.com/SecretsOTheP/Server (RoF2-capable)
- **EQMacEmu:** https://github.com/SecretsOTheP/EQMacEmu (TAKP-only)
- **Official EQEmu:** https://github.com/EQEmu/Server (most conservative, largest community)

---

## Next decision: Commit to RoF2 pivot timeline

After Phase 1 spike completes, you'll have two data points:
1. **Does multiclass scribe work on stock TAKP client?** (answers DECISIONS.md D6)
2. **Is the RoF2 environment ready for Phase 2?** (answers fork + client choice)

Document your Phase 2 decision as **A12** in DECISIONS.md:
```
A12 | Long-term client strategy | Pivot to SecretsOTheP/Server + RoF2 after Phase 1 spike. Phase 2 development on RoF2 + native UI. Optional TAKP support added Phase 6+ if demand. | Richest feature space, native windows for identity layer (Phase 4), avoids UI pain. | Phase 1-2 boundary |
```
