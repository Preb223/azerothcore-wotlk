# End-to-End Instructions: Creating Custom & Heirloom Items in AzerothCore 3.3.5a

Follow this exact step-by-step workflow whenever creating custom items, heirlooms, weapons, bags, or quivers to ensure zero errors, proper tooltips, client synchronization, and database persistence.

---

## Step 1: ID Allocation & Registry
1. Open `custom/project_reference.md` and check the **Custom ID Registry** for the next available item ID (`90000+`).
2. Assign sequential IDs for all new items and immediately update the registry in `project_reference.md` to prevent ID collisions across chat sessions.

---

## Step 2: Client DBC Registration (`DBFilesClient/Item.dbc`)
Every custom item in WoW 3.3.5a MUST be registered in `Item.dbc` so the game client displays icons, names, and item types.

1. Open `custom/patch_data/DBFilesClient/Item.dbc` using a Python struct script.
2. Insert 8-field record: `(ID, Class, SubClass, SoundOverrideSubclass, Material, DisplayID, InventoryType, SheatheType)`:
   * **`ID`**: Custom Item ID (e.g. `90111`)
   * **`Class`**: `1` (Container), `2` (Weapon), `4` (Armor), `11` (Quiver), `15` (Misc)
   * **`SubClass`**: Subclass ID corresponding to item type
   * **`SoundOverrideSubclass`**: `4294967295` (`-1`)
   * **`Material`**: `2` (Leather), `1` (Metal), `3` (Wood), `7` (Cloth), etc.
   * **`DisplayID`**: Valid 3.3.5a display model ID
   * **`InventoryType`**: `18` (Bag / Quiver), `1` (Head), `13` (One-Hand), `17` (Two-Hand), `11` (Finger), `2` (Neck), etc.
   * **`SheatheType`**: `0` (None), `1` (Back), `2` (Hip), etc.
3. Save `Item.dbc`.

---

## Step 3: Server Database Registration (`item_template`)
Insert the item record into `acore_world.item_template` and permanent SQL file `custom/sql/01_items.sql`.

### Crucial Field Requirements:
* **Non-Weapon Items (Armor, Bags, Quivers, Jewelry)**:
  * Set `dmg_min1 = 0` and `dmg_max1 = 0`! *(Failing to do this causes "1 - 0 Damage" to show on non-weapon tooltips).*
  * Set `delay = 0`.
* **Heirlooms**:
  * `Quality = 7` (Gold heirloom border)
  * `Flags = 134221824` (Bind to Account)
  * `bonding = 7` (Bind to Account)
  * `RequiredLevel = 1`, `ItemLevel = 1`
* **Quivers & Ammo Pouches**:
  * `class = 11` (Quiver)
  * `subclass`: `2` (Arrows), `3` (Bullets)
  * `BagFamily`: `1` (Arrows), `2` (Bullets), `3` (Universal Arrows + Bullets)
  * **Ranged Speed Aura**: Include spell `29414` (Quiver +15% Speed) or `14829` (Ammo Pouch +15% Speed) with `spelltrigger_1 = 1` (Equip).
* **Equip Spells**:
  * Up to 5 equip spells can be defined (`spellid_1` through `spellid_5` with `spelltrigger_X = 1`).

---

## Step 4: Vendor Integration (`npc_vendor`)
Map the new item to vendor NPCs:
* **Vendor ID `9000000`** (Weapons, Quivers, Main Heirloom Vendor)
* **Vendor ID `9000051`** (Trinkets, Rings, Necklaces, Bags & Misc)

1. Run SQL: `REPLACE INTO npc_vendor (entry, item) VALUES (9000000, <ID>), (9000051, <ID>);`
2. Update `modules/mod-assistant/data/sql/world/mod_assistant.sql`.

---

## Step 5: MPQ Patch Packaging (`patch-4.MPQ`)
1. Run `python custom/package_client_patch.py`.
2. Verify output: `Successfully created C:\ChromieCraft_3.3.5a\Data\patch-4.MPQ`.
3. **WoW Client Sync**:
   * If the WoW Client (`Wow.exe`) is open during packaging, **close and restart the client** so it reads the newly patched `Item.dbc` from `patch-4.MPQ`.

---

## Step 6: Server Cache Flush & Worldserver Reload
SQL queries directly update MySQL disk storage, BUT the running `ac-worldserver` container caches item templates in RAM.

To flush the memory cache:
1. Run `.reload item_template` and `.reload npc_vendor` in-game, OR
2. Restart the worldserver container: `docker restart ac-worldserver`.

---

## Step 7: Documentation & Backup
1. **`custom/project_reference.md`**:
   * Add new item IDs to Custom ID Registry table.
   * Bump "Next available" ID marker.
   * Add entry to Changelog at bottom of file.
2. **`doc/useful_gm_commands.md`**:
   * Add item under Section 5 with `.additem <ID>` command, WoW class colors (if applicable), and description.
3. **Backup**:
   * Run backup script `python scratch/create_full_backup.py` (or dump database into `custom/backups/<timestamp>/`).
