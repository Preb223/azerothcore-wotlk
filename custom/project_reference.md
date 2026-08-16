# AzerothCore WoTLK Project Reference

> [!CAUTION]
> ## MANDATORY — READ AND FOLLOW THESE INSTRUCTIONS
>
> **This is a living reference document.** It exists to prevent redundant research and ensure continuity across sessions.
>
> ### On Session Start
> 1. **ALWAYS read this file first** before doing any work. It is listed in the artifact summaries — look for `project_reference.md`.
> 2. Use the ID registries, file locations, patterns, and user preferences below instead of re-discovering them.
> 3. If the project state seems inconsistent with this document, **verify against the live database/code** before trusting this file — it could be stale.
>
> ### On Session End (or after significant work)
> 1. **ALWAYS update this file** to reflect changes made during the session.
> 2. Specifically, update:
>    - **Custom ID Registry** — any new item IDs, set IDs, spell IDs, vendor IDs created. Bump the "Next available" markers.
>    - **File Locations** — any new files created or moved.
>    - **User Preferences** — any new design decisions the user made.
>    - **Gotchas & Lessons Learned** — any new pitfalls discovered.
>    - **Gossip Architecture** — if new menus or vendors were added.
>    - **Legendary Weapon Spells** — if weapon effects changed.
>    - **Changelog** (at the bottom) — a one-line entry with the date and what changed.
> 3. Do NOT wait to be asked — update proactively as part of wrapping up.
>
> ### When Creating New Custom Content
> 1. Check the "Next available" ID in the relevant registry **before** picking an ID.
> 2. After creating it, **immediately update** the registry and bump the "Next available" marker.
> 3. This prevents ID collisions across sessions.
>
> ### When User States a Preference or Decision
> 1. Record it in the **User Preferences** section immediately.
> 2. Future sessions must honor these unless the user explicitly changes their mind.

---


## Project Overview

- **Repo**: `C:\Users\Blake\GitHub Repositories\azerothcore-wotlk`
- **Game Version**: WoW 3.3.5a (Wrath of the Lich King)
- **Server**: AzerothCore, running via Docker Compose
- **Client Path**: `C:\ChromieCraft_3.3.5a\`
- **Custom Work**: Heirloom item sets, legendary weapons, necklaces, rings, vendor system
- **LAN IP**: `192.168.1.58` (Wi-Fi 2 adapter) — update if DHCP assigns a new IP
- **Player Guide**: `C:\ChromieCraft_3.3.5a\README - How to Connect.txt`

---

## Docker Architecture

| Container | Purpose |
|-----------|---------|
| `ac-database` | MySQL database (root/password) |
| `ac-worldserver` | Game server binary |
| `ac-authserver` | Login/auth server |
| `ac-db-import` | Auto-applies pending SQL on startup |
| `ac-client-data-init` | Client data initialization |

### Common Commands

```powershell
# Build after C++ changes
docker compose build ac-worldserver

# Deploy (restarts worldserver)
docker compose up -d ac-worldserver

# Database query (one-liner)
echo "SELECT ..." | docker exec -i ac-database mysql -u root -ppassword acore_world -t

# Database dump
docker exec ac-database mysqldump -u root -ppassword acore_world <table> --where="<condition>" --no-create-info --complete-insert > output.sql
```

### Build Cycle
1. Edit C++ files in `modules/mod-assistant/src/`
2. `docker compose build ac-worldserver` (~55-60 seconds)
3. `docker compose up -d ac-worldserver` (~15-20 seconds)
4. Player must relog (`.server shutdown 1` in-game to force)

---

## Database Schema

- **Database name**: `acore_world`
- **Credentials**: `root` / `password`

### Key Tables

| Table | Purpose |
|-------|---------|
| `item_template` | All item definitions (138 columns) |
| `npc_vendor` | Vendor → item mappings |
| `spell_dbc` | Server-side spell overrides (NOT all spells — most are in DBC files) |
| `itemset_dbc` | Server-side item set overrides |

### item_template Critical Columns

| Column | Heirloom Value | Notes |
|--------|---------------|-------|
| `Quality` | `7` | Heirloom quality (gold border) |
| `bonding` | `7` | Bind to Account |
| `Flags` | `134221824` | `ITEM_FLAG_BIND_TO_ACCOUNT \| ITEM_FLAG_NO_DURABILITY` |
| `RequiredLevel` | `1` | Must be 1 for heirlooms |
| `ScalingStatDistribution` | SSD ID | Links to ScalingStatDistribution.dbc |
| `ScalingStatValue` | SSV bitmask | Determines which stats scale (slot-dependent) |
| `itemset` | Set ID | Links to ItemSet.dbc |
| `spellid_1..5` | Spell IDs | Item procs/equip effects |
| `spelltrigger_1..5` | 0=Use, 1=Equip, 2=Chance on Hit | |

---

## Custom ID Registry

### Item IDs (90000–90108)

| Range | Content |
|-------|---------|
| 90000 | Frostmourne (2H Sword) |
| 90001 | Ashbringer (2H Sword) |
| 90002 | Corrupted Ashbringer (2H Sword) |
| 90003 | Thunderfury (1H Sword) |
| 90004 | Skullflame Shield (Shield) |
| 90005 | Atiesh, Greatstaff of the Guardian (Staff) |
| 90010–90017 | Nemesis Raiment (Warlock T2, set 998) |
| 90020–90027 | Judgement Armor (Paladin T2, set 999) |
| 90030–90037 | Bloodfang Armor (Rogue T2, set 997) |
| 90040–90047 | Netherwind Regalia (Mage T2, set 996) |
| 90050–90057 | Vestments of Transcendence (Priest T2, set 995) |
| 90060–90067 | Stormrage Raiment (Druid T2, set 1000) |
| 90070–90077 | The Ten Storms (Shaman T2, set 1001) |
| 90080–90087 | Dragonstalker Armor (Hunter T2, set 1002) |
| 90090–90097 | Battlegear of Wrath (Warrior T2, set 1003) |
| 90098–90102 | Corruptor Raiment (Warlock T5, set 1004) — 5 pieces only |
| 90103 | Pendant of Arcane Mastery (Caster Neck, 10% XP) |
| 90104 | Pendant of the Iron Wall (Tank Neck, 10% XP) |
| 90105 | Pendant of Swift Strikes (Melee Neck, 10% XP) |
| 90106 | Signet of Arcane Authority (Caster Ring, 5% XP) |
| 90107 | Signet of the Bastion (Tank Ring, 5% XP) |
| 90108 | Signet of Lethal Precision (Melee Ring, 5% XP) |
| 90109 | Bag of Infinite Holdings (36-Slot Heirloom Bag) |
| 90110 | Barman Shanker (1H Dagger Heirloom) |
| **Next available**: 90111+ | |

### Custom Set IDs

| Set ID | Set Name | Class | Source |
|--------|----------|-------|--------|
| 995 | Transcendence | Priest | T2 clone |
| 996 | Netherwind | Mage | T2 clone |
| 997 | Bloodfang | Rogue | T2 clone |
| 998 | Nemesis | Warlock | T2 clone |
| 999 | Judgement | Paladin | T2 clone |
| 1000 | Stormrage | Druid | T2 clone (pipeline) |
| 1001 | Ten Storms | Shaman | T2 clone (pipeline) |
| 1002 | Dragonstalker | Hunter | T2 clone (pipeline) |
| 1003 | Wrath | Warrior | T2 clone (pipeline) |
| 1004 | Corruptor | Warlock | T5 clone (pipeline) |
| **Next available**: 1005+ | | | |

### Custom Spell IDs (cloned set bonuses)

| Range | Set |
|-------|-----|
| 99060–99062 | Stormrage bonuses |
| 99070–99072 | Ten Storms bonuses |
| 99080–99082 | Dragonstalker bonuses |
| 99090–99092 | Wrath bonuses |
| 99098–99099 | Corruptor bonuses |
| **Next available**: 99100+ | |

### Vendor IDs

| Vendor ID | Content | Menu Location |
|-----------|---------|---------------|
| 9000000 | Weapons | Heirlooms → I want weapons |
| 9000001 | Dreadmist (Cloth) | Heirlooms → Dreadmist |
| 9000046 | Shadowcraft (Leather) | Heirlooms → Shadowcraft |
| 9000047 | Wildheart (Druid) | Heirlooms → Wildheart |
| 9000048 | Elements (Mail) | Heirlooms → Elements |
| 9000049 | Lightforge (Paladin) | Heirlooms → Lightforge |
| 9000050 | Might & Valor (Warrior) | Heirlooms → Might & Valor |
| 9000051 | Trinkets, Necklaces, Rings, Misc | Heirlooms → Trinkets & Misc |
| 9000053 | Legendary & Epic Weapons | Heirlooms → Legendary |
| 9000055 | Nemesis (Warlock T2) | Tier Sets → Nemesis |
| 9000056 | Judgement (Paladin T2) | Tier Sets → Judgement |
| 9000057 | Bloodfang (Rogue T2) | Tier Sets → Bloodfang |
| 9000059 | Netherwind (Mage T2) | Tier Sets → Netherwind |
| 9000060 | Transcendence (Priest T2) | Tier Sets → Transcendence |
| 9000061 | Stormrage (Druid T2) | Tier Sets → Stormrage |
| 9000062 | Ten Storms (Shaman T2) | Tier Sets → Ten Storms |
| 9000063 | Dragonstalker (Hunter T2) | Tier Sets → Dragonstalker |
| 9000064 | Wrath (Warrior T2) | Tier Sets → Wrath |
| 9000065 | Corruptor (Warlock T5) | Tier Sets → Corruptor |
| **Next available**: 9000066+ | | |

---

## ScalingStatDistribution (SSD) Templates

| SSD ID | Stat Profile | Used By |
|--------|-------------|---------|
| 993 | Leather hybrid (Agi/Sta/Int/Spirit) | Bloodfang, Stormrage, Ten Storms, Dragonstalker |
| 994 | Cloth caster (Int/Sta/Spirit/Hit) | Nemesis, Netherwind, Transcendence, Corruptor |
| 999 | Plate hybrid (Str/Sta/Int/Def/SP) | Judgement, Wrath |
| 251 | Trinket (Swift Hand of Justice) | Trinkets |
| 271 | Trinket (Discerning Eye) | Trinkets |
| 371 | Ring/Neck (Dread Pirate Ring) | Necklaces, Rings |

### ScalingStatValue (SSV) Bitmasks by Slot

| SSD | Big Slots (Head/Chest/Legs/Robe) | Small Slots (Shoulders/Belt/Boots/Bracers/Gloves) |
|-----|----------------------------------|---------------------------------------------------|
| 993 | 2097160 | 65 |
| 994 | 1048584 | 33 |
| 999 | 8388616 | 257 |

Big slots: `InventoryType` ∈ {1, 5, 7, 20}

---

## Legendary Weapon Spells

### Ashbringer (90001)
| Slot | Spell | Name | Trigger |
|------|-------|------|---------|
| 1 | 18112 | Firebolt (700 Fire dmg) | 2 (Chance on Hit) |
| 2 | 25423 | Holy Bolt (heal, scaled by C++) | 2 (Chance on Hit) |

### Corrupted Ashbringer (90002)
| Slot | Spell | Name | Trigger |
|------|-------|------|---------|
| 1 | 28282 | Ashbringer equip aura | 1 (Equip) |
| 2 | 28414 | Call of the Ashbringer (AoE proc) | 2 (Chance on Hit) |
| 3 | 7598 | +2% Crit | 1 (Equip) |
| 4 | 15464 | +2% Hit | 1 (Equip) |
| 5 | 17484 | Shadow Touch (life steal, scaled by C++) | 2 (Chance on Hit) |

### Frostmourne (90000)
| Slot | Spell | Name | Trigger |
|------|-------|------|---------|
| 1 | 28282 | Ashbringer equip aura | 1 (Equip) |
| 2 | 7598 | +2% Crit | 1 (Equip) |
| 3 | 15464 | +2% Hit | 1 (Equip) |
| 4 | 17484 | Life steal (scaled by C++) | 2 (Chance on Hit) |

### Atiesh (90005)
| Slot | Spell | Name | Trigger |
|------|-------|------|---------|
| 1 | 28148 | Portal: Karazhan | 0 (Use) |

### C++ Scaling (mod_assistant.cpp)
- **Heal proc** (Ashbringer): `level × 5` HP, 5% proc chance
- **Life steal** (Frostmourne/Corrupted Ashbringer): `level × 4` HP drain+heal, 8% proc chance
- **Weapon DPS**: All three scale via `ScalingStatValuesEntry::getDPSMod(16392)`

---

## XP Bonus Spells

| Spell ID | XP Bonus | Used By |
|----------|----------|---------|
| 57353 | ~10% XP | Shoulders, Chests, Necklaces |
| 71354 | ~5% XP | Dread Pirate Ring, Custom Rings |

---

## File Locations

### Custom Scripts (kept)
```
custom/
├── build_heirlooms.py         # Main pipeline (DBC + SQL + MPQ)
├── heirloom_config.py         # Set definitions for pipeline
├── package_client_patch.py    # Builds patch-4.MPQ from patch_data/
├── create_account.py          # Account creation helper (SOAP + DB fallback)
├── project_reference.md       # THIS FILE (living reference)
├── original_dbcs/             # Pristine 3.3.5a DBC files
│   ├── CharBaseInfo.dbc
│   ├── Item.dbc
│   ├── ItemSet.dbc
│   ├── ScalingStatDistribution.dbc
│   └── Spell.dbc
├── patch_data/DBFilesClient/  # Patched DBCs (input for MPQ + Docker mounts)
│   ├── CharBaseInfo.dbc
│   ├── Item.dbc
│   ├── ItemSet.dbc
│   ├── ScalingStatDistribution.dbc
│   └── Spell.dbc
└── backups/                   # Timestamped backups
```

### Docker Compose Override
- **File**: `docker-compose.override.yml` (repo root)
- DBC volume mounts point to `./custom/patch_data/DBFilesClient/*.dbc`
- Contains environment variables for playerbots, AH bot, individual progression

### Mod Assistant (C++ source)
```
modules/mod-assistant/src/
├── mod_assistant.cpp          # Script registration + weapon scaling + proc scaling + Undead Paladin restriction
├── mod_assistant.h            # Enums, vendor IDs, gossip strings, class declaration
├── mod_assistant_npc.cpp      # Gossip menu handler (OnGossipSelect state machine)
├── mod_assistant_config.cpp   # Config loading from .conf
└── mod_assistant_functions.cpp # Utility functions
```

### Additional Modules
- `modules/mod-learn-spells/` — Auto-learns class spells on level up (no trainer visits needed)
  - Config: `LearnSpells.Enable = 1`, `LearnSpells.MaxLevel = 80`

### Client Patch
- **Output**: `C:\ChromieCraft_3.3.5a\Data\patch-4.MPQ`
- Contains patched DBC files that the client needs to display custom items

---

## Mod Assistant Gossip Architecture

The NPC gossip menu is a state machine driven by `action` integers:

```
Main Menu (action=1)
├── Heirlooms (ASSISTANT_GOSSIP_HEIRLOOM = 100)
│   ├── Weapons (+1) → vendor 9000000
│   ├── Dreadmist (+2) → vendor 9000001
│   ├── Shadowcraft (+3) → vendor 9000046
│   ├── Wildheart (+4) → vendor 9000047
│   ├── Elements (+5) → vendor 9000048
│   ├── Lightforge (+6) → vendor 9000049
│   ├── Might & Valor (+7) → vendor 9000050
│   ├── Trinkets & Misc (+8) → vendor 9000051
│   ├── Tier Sets (+20) → submenu
│   │   ├── Nemesis (+21) → vendor 9000055
│   │   ├── Judgement (+22) → vendor 9000056
│   │   ├── Bloodfang (+23) → vendor 9000057
│   │   ├── Netherwind (+24) → vendor 9000059
│   │   ├── Transcendence (+25) → vendor 9000060
│   │   ├── Stormrage (+26) → vendor 9000061
│   │   ├── Ten Storms (+27) → vendor 9000062
│   │   ├── Dragonstalker (+28) → vendor 9000063
│   │   ├── Wrath (+29) → vendor 9000064
│   │   └── Corruptor (+40) → vendor 9000065
│   └── Legendary (+30) → vendor 9000053
├── Glyphs (200)
├── Gems (400)
├── Elixirs (500)
├── Food (600)
├── Enchants (700)
├── Containers (800)
├── Flight Paths (900)
├── Utilities (1000)
├── Professions (1100)
└── Instances (1200)
```

### Adding a New Vendor Menu Item
1. Add `ASSISTANT_VENDOR_HEIRLOOM_XXX = 90000NN` to enum in `mod_assistant.h`
2. Add `#define GOSSIP_HEIRLOOMS_XXX "..."` in `mod_assistant.h`
3. Add `AddGossipItemFor(...)` line in `mod_assistant_npc.cpp` under the appropriate submenu
4. Add `case` in the vendor switch block in `mod_assistant_npc.cpp`
5. Add items to `npc_vendor` table with the vendor ID
6. Build + deploy

---

## DBC File Formats (3.3.5a)

All DBCs use the same binary format:
```
Header: 'WDBC' (4 bytes) + record_count (4) + field_count (4) + record_size (4) + string_block_size (4)
Records: record_count × record_size bytes
String Block: string_block_size bytes (null-terminated strings)
```

### Item.dbc (8 fields, 32 bytes/record)
`ID, Class, SubClass, SoundOverrideSubclass, Material, DisplayID, InventoryType, SheatheType`

### ItemSet.dbc (53 fields, 212 bytes/record)
`ID, Name_Lang[16+mask], Items[17], SetSpellID[8], SetThreshold[8], RequiredSkill, RequiredSkillRank`

### Spell.dbc (234 fields, 936 bytes/record)
- Field 136 = `Name_Lang_enUS` (string offset)
- Field 170 = `Description_Lang_enUS` (string offset)
- Fields 65-67 = Effect type (3 effects)
- Fields 78-80 = EffectBasePoints
- Fields 99-101 = EffectAura
- Fields 108-110 = EffectTriggerSpell

### ScalingStatDistribution.dbc
Contains stat distribution profiles linking SSD IDs to stat types and bonuses per level.

---

## Heirloom Pipeline (build_heirlooms.py)

### Usage
```powershell
python custom\build_heirlooms.py              # Full pipeline
python custom\build_heirlooms.py --dbc-only   # Only patch DBCs
python custom\build_heirlooms.py --sql-only   # Only generate + apply SQL
```

### Pipeline Steps
1. **Patch DBCs**: Clone Item/ItemSet/Spell/SSD entries for new sets
2. **Generate SQL**: CREATE item_template rows via INSERT...SELECT from originals, override heirloom columns
3. **Apply SQL**: Push to database via docker exec
4. **Sync DBC displayids**: Pull displayid from DB → patch Item.dbc
5. **Package MPQ**: Build patch-4.MPQ for client
6. **Print C++ snippets**: Output code to paste into mod_assistant

### Adding a New Set via Pipeline
1. Add entry to `custom/heirloom_config.py` with:
   - `name`, `class`, `original_itemset`, `new_itemset`, `scaling_template`, `vendor_id`
   - `original_items`: dict mapping original_id → new_id
   - `spell_clones`: dict mapping original_spell → new_spell
2. Run `python custom/build_heirlooms.py`
3. Add C++ snippets from output to mod_assistant header + NPC source
4. Build + deploy

---

## Common Patterns

### Query Template for Checking Items
```sql
SELECT entry, name, Quality, bonding, Flags, RequiredLevel, itemset, 
       ScalingStatDistribution, ScalingStatValue,
       spellid_1, spelltrigger_1, spellid_2, spelltrigger_2
FROM item_template WHERE entry BETWEEN <start> AND <end> ORDER BY entry;
```

### Validation Query
```sql
SELECT entry, name,
    CASE WHEN Quality = 7 THEN 'OK' ELSE 'FAIL' END AS quality,
    CASE WHEN bonding = 7 THEN 'OK' ELSE 'FAIL' END AS bonding,
    CASE WHEN Flags = 134221824 THEN 'OK' ELSE 'FAIL' END AS flags,
    CASE WHEN RequiredLevel <= 1 THEN 'OK' ELSE 'FAIL' END AS level
FROM item_template WHERE entry BETWEEN 90000 AND 90108 ORDER BY entry;
```

### Backup Command
```powershell
$ts = Get-Date -Format "yyyy-MM-dd_HH-mm"
$dir = "custom\backups\$ts"
New-Item -ItemType Directory -Force -Path $dir
# ... copy scripts, dump DB
docker exec ac-database mysqldump -u root -ppassword acore_world item_template --where="entry BETWEEN 90000 AND 90108" --no-create-info --complete-insert > "$dir\custom_items.sql"
```

---


---

## End-to-End Workflow: Creating Custom & Heirloom Items

Follow this exact 7-step process when creating any heirloom, custom item, bag, or quiver:

1. **ID Allocation & Registry**:
   - Check `project_reference.md` for next available ID (`90000+`).
   - Register ID in `project_reference.md` table and bump marker immediately.
2. **Client Registration (`DBFilesClient/Item.dbc`)**:
   - Add 8-field record: `(ID, Class, SubClass, SoundOverrideSubclass, Material, DisplayID, InventoryType, SheatheType)`.
3. **Server Database Registration (`item_template` & `custom/sql/01_items.sql`)**:
   - **Non-Weapons (Armor, Bags, Quivers, Jewelry)**: Set `dmg_min1 = 0`, `dmg_max1 = 0`, and `delay = 0`!
   - **Heirlooms**: `Quality = 7`, `Flags = 134221824`, `bonding = 7`, `RequiredLevel = 1`, `ItemLevel = 1`.
   - **Quivers/Pouches**: `class = 11`, `subclass`: 2 (Arrows), 3 (Bullets), `BagFamily`: 1 (Arrows), 2 (Bullets), 3 (Universal).
   - **Ranged Speed**: Include equip spell `29414` (Quiver 15% speed) or `14829` (Ammo Pouch 15% speed) with `spelltrigger_1 = 1`.
4. **Vendor Registration (`npc_vendor`)**:
   - Add to vendor `9000000` (Weapons & Quivers) and `9000051` (Trinkets, Necklaces, Rings, Bags & Misc).
   - Update `modules/mod-assistant/data/sql/world/mod_assistant.sql`.
5. **MPQ Client Patching**:
   - Run `python custom/package_client_patch.py`.
   - If `Wow.exe` was running, restart the WoW Client to reload `Item.dbc` from `patch-4.MPQ`.
6. **Server Memory Cache Flush**:
   - Run `.reload item_template` and `.reload npc_vendor` in-game, or run `docker restart ac-worldserver`.
7. **Documentation & Backup**:
   - Update `doc/useful_gm_commands.md` and `custom/project_reference.md`.
   - Run backup script `python scratch/create_full_backup.py`.

## User Preferences (Recorded)

- Thunderfury heirloom size: **Leave as-is**
- Vendor grouping: **Set-based** (not slot-based) for default heirlooms
- Tier 2 sets: **Keep in their own submenu** (separate from default heirloom sets)
- Legendary weapons: **Single vendor window** (no submenu)
- All gossip icons: **Coin purse** (`GOSSIP_ICON_VENDOR`), not crossed swords
- Heal/life steal procs: **C++ scaling** (Option 2), not flat amounts
- Necklaces: **10% XP**, Rings: **5% XP**
- Necklaces/Rings vendor: **Trinkets & Miscellaneous** (9000051)
- Corruptor T5 set: **Nemesis base stats** + **real T5 set bonuses**
- Custom scripts: **Live in `custom/` subdirectory**
- Dual spec: **Available from level 1** (MinDualSpecLevel = 1)
- Mail delivery: **Instant** (MailDeliveryDelay = 0)
- Auto-account creation: **Via `custom/create_account.py`** (SOAP + DB fallback)
- Undead Paladin: **Restricted to account ID 1 (MALIKYTH)** via `AccountScript::CanAccountCreateCharacter` in mod_assistant.cpp
- Auto-learn spells: **Enabled** via `mod-learn-spells` module
- Quest item sparkles: **Already enabled** (`Visibility.ObjectSparkles = 1`)
- Individual Progression Balance: **VanillaPowerAdjustment = 0.6** (60% damage scaling), **VanillaHealingAdjustment = 1.0** (100% full healing output)
- Playerbots: **1,000–1,500 bots**, synced level with players (±3 levels of current logged in players), max level 60, blue gear cap, 50% imperfect gear, bots invite players, chat enabled, BGs enabled

---

## Gotchas & Lessons Learned

1. **spell_dbc table ≠ Spell.dbc file**: Most spells are only in the DBC binary file, not the MySQL table. To look up spell names, parse the DBC directly (field 136 = name).

2. **Item.dbc is required for client**: Even if an item exists in `item_template`, the client won't display it without a matching `Item.dbc` entry. Always add to both.

3. **ScalingStatValue is slot-dependent**: Head/Chest/Legs/Robe get "big" SSV values, other slots get "small" values. Using the wrong one causes items to have no stats.

4. **`PlayerScript` does NOT have `OnDamage`**: Use `UnitScript::OnDamage` for intercepting damage events. `PlayerScript` has `OnPlayerApplyWeaponDamage` for weapon damage scaling only.

5. **Cache clearing**: Client must clear WoW cache after DBC changes. Delete `C:\ChromieCraft_3.3.5a\Cache\` contents.

6. **Virtual vendor IDs**: AzerothCore supports `SendListInventory(creature_guid, vendor_id)` where `vendor_id` can be any `npc_vendor.entry` — it doesn't need to match the creature's entry. This is how the mod_assistant provides multiple vendor windows from one NPC.

7. **Generated SQL files are throwaway**: `heirloom_items.sql` and `heirloom_vendor.sql` are regenerated each pipeline run. Don't version them.

8. **PowerShell multiline Python**: Use script files instead of `python -c "..."` for anything with quotes or multiline — PowerShell escaping is painful.

9. **Docker DBC volume mounts**: `docker-compose.override.yml` bind-mounts DBC files into the worldserver container. If you move/delete those files, the container will fail to start with a cryptic mount error. The mounts must point to `./custom/patch_data/DBFilesClient/`. Always use `docker compose up -d` (not `restart`) after changing volume paths — `restart` reuses the old container config.

10. **Realmlist for LAN**: The `address` and `localAddress` in `acore_auth.realmlist` must be the host's LAN IP (not 127.0.0.1) for other machines to connect. Update with: `UPDATE realmlist SET address='<LAN_IP>', localAddress='<LAN_IP>' WHERE id=1;`

---

## Changelog

> Update this section every time you modify this document. Newest entries first.

| Date | Summary |
|------|---------|
| 2026-08-16 | Completed full server migration to macOS (Apple M4 Max, 16GB Docker RAM). Restored all characters, accounts, playerbots, and world DB. Scaled playerbots to 1,000–1,500 concurrent bots with level sync (±3 levels of active players, max level 60). |
| 2026-08-15 | Fixed Barman Shanker (90110). Added 3 custom 36-slot Heirloom Quivers & Ammo Pouches (90111-90113): Quiver of the Infinite Hunt (universal 36-slot), Quiver of the Windrunner (arrows 36-slot), and Ammo Pouch of the Dragonflight (bullets 36-slot) with built-in 15% speed, +2% crit, and +5% XP. Integrated with Gabriella Special Item Vendor, patched Item.dbc, rebuilt patch-4.MPQ, updated useful_gm_commands.md with class colors and formatting, and created timestamped database backup. |
| 2026-06-14 | Installed mod-learn-spells (auto-learn class spells on level up). Added Undead Paladin (race=5/class=2) restricted to account 1: playercreateinfo DB row + CharBaseInfo.dbc patch + AccountScript in mod_assistant.cpp. Updated playerbots: 150-200 bots, invite players, chat broadcasts, blue gear cap, 50% imperfect gear, BG queuing, smart scale max 60. Rebuilt patch-4.MPQ with CharBaseInfo.dbc. |
| 2026-06-14 | Added LAN config (realmlist, firewall, player guide), QoL settings (dual spec lvl 1, instant mail), create_account.py, docker-compose.override.yml docs, gotchas #9-10. Fixed DBC volume mount paths after repo cleanup. |
| 2026-06-14 | Initial creation. Documented all 89 items (90000–90108), 10 set IDs (995–1004), vendor architecture, DBC formats, pipeline workflow, C++ scaling scripts, legendary weapon spells, XP bonus jewelry, user preferences, and 8 gotchas. Added mandatory self-referencing instructions. |
