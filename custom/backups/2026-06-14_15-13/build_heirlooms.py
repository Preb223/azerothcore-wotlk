"""
build_heirlooms.py — Unified Heirloom Set Builder

Reads heirloom_config.py and performs the complete pipeline:
1. Patches Item.dbc, ItemSet.dbc, Spell.dbc with cloned entries
2. Patches ScalingStatDistribution.dbc with new SSD entries if needed
3. Generates correct item_template SQL (using dynamic schema discovery)
4. Generates npc_vendor SQL
5. Applies SQL to the database
6. Packages patch-4.MPQ
7. Prints C++ snippets for mod_assistant

Usage:
    python build_heirlooms.py              # Full pipeline
    python build_heirlooms.py --dbc-only   # Only patch DBCs, skip DB/MPQ
    python build_heirlooms.py --sql-only   # Only generate SQL, skip DBC/MPQ
"""

import struct
import os
import subprocess
import sys
import shutil

# Resolve paths relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- ScalingStatValue bitmask lookup ---
# These are derived from existing working heirloom items.
# Key = SSD ID, Value = {big_slot_ssv, small_slot_ssv}
SSV_LOOKUP = {
    993: {"big": 2097160, "small": 65},      # Leather hybrid (Bloodfang/Stormrage)
    994: {"big": 1048584, "small": 33},       # Cloth caster (Nemesis/Netherwind)
    999: {"big": 8388616, "small": 257},      # Plate (Judgement)
}

BIG_SLOTS = {1, 5, 7, 20}  # Head, Chest, Legs, Robe


class DBC:
    """Simple DBC reader/writer for WoW 3.3.5a DBC files."""
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            header = f.read(20)
            self.magic, self.record_count, self.field_count, self.record_size, self.string_block_size = struct.unpack('<4sIIII', header)
            self.records = []
            for _ in range(self.record_count):
                self.records.append(f.read(self.record_size))
            self.string_block = f.read(self.string_block_size)
        self.fmt = '<' + 'I' * self.field_count

    def unpack(self, record):
        return list(struct.unpack(self.fmt, record))

    def pack(self, fields):
        return struct.pack(self.fmt, *fields)

    def get_ids(self):
        return {struct.unpack('<I', r[:4])[0] for r in self.records}

    def find(self, record_id):
        for r in self.records:
            if struct.unpack('<I', r[:4])[0] == record_id:
                return r
        return None

    def remove_ids(self, ids_to_remove):
        self.records = [r for r in self.records if struct.unpack('<I', r[:4])[0] not in ids_to_remove]

    def write(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(struct.pack('<4sIIII', self.magic, len(self.records), self.field_count, self.record_size, len(self.string_block)))
            for r in self.records:
                f.write(r)
            f.write(self.string_block)


def get_dbc_path(name, patch_dir, orig_dir):
    """Use patched version if it exists, otherwise use original."""
    patched = os.path.join(patch_dir, name)
    orig = os.path.join(orig_dir, name)
    return patched if os.path.exists(patched) else orig


def get_db_columns():
    """Query the actual database schema to get item_template columns."""
    result = subprocess.run(
        'docker exec -i ac-database mysql -u root -ppassword acore_world -s -e "DESCRIBE item_template;"',
        shell=True, capture_output=True, text=True
    )
    cols = []
    for line in result.stdout.strip().split("\n"):
        if line:
            cols.append(line.split("\t")[0])
    return cols


def get_ssv_for_slot(ssd_id, inventory_type):
    """Get the correct ScalingStatValue bitmask for a given SSD and slot type."""
    lookup = SSV_LOOKUP.get(ssd_id)
    if not lookup:
        print(f"  WARNING: No SSV lookup for SSD {ssd_id}, using 1032 as fallback")
        return 1032
    if inventory_type in BIG_SLOTS:
        return lookup["big"]
    else:
        return lookup["small"]


def build_heirlooms(dbc_only=False, sql_only=False):
    sys.path.insert(0, SCRIPT_DIR)
    from heirloom_config import SETS

    patch_dir = os.path.join(SCRIPT_DIR, "patch_data", "DBFilesClient")
    orig_dir = os.path.join(SCRIPT_DIR, "original_dbcs")
    os.makedirs(patch_dir, exist_ok=True)

    # --- Step 1: Patch DBCs ---
    if not sql_only:
        print("=" * 60)
        print("STEP 1: Patching DBCs")
        print("=" * 60)

        item_dbc = DBC(get_dbc_path("Item.dbc", patch_dir, orig_dir))
        itemset_dbc = DBC(get_dbc_path("ItemSet.dbc", patch_dir, orig_dir))
        spell_dbc = DBC(get_dbc_path("Spell.dbc", patch_dir, orig_dir))

        # Also handle SSD
        ssd_dbc = DBC(get_dbc_path("ScalingStatDistribution.dbc", patch_dir, orig_dir))

        # Collect all target IDs to remove before re-adding (idempotent)
        target_items = set()
        target_itemsets = set()
        target_spells = set()
        target_ssds = set()

        for s in SETS:
            target_itemsets.add(s["new_itemset"])
            target_ssds.add(s["new_itemset"])  # SSD IDs match itemset IDs
            for new_id in s["original_items"].values():
                target_items.add(new_id)
            for new_id in s.get("spell_clones", {}).values():
                target_spells.add(new_id)

        item_dbc.remove_ids(target_items)
        itemset_dbc.remove_ids(target_itemsets)
        spell_dbc.remove_ids(target_spells)
        ssd_dbc.remove_ids(target_ssds)

        for s in SETS:
            print(f"\n  Processing {s['name']} ({s['class']})...")

            # 1a. Clone Item.dbc entries
            new_item_ids = []
            for orig_id, new_id in s["original_items"].items():
                new_item_ids.append(new_id)
                orig_row = item_dbc.find(orig_id)
                if orig_row:
                    fields = item_dbc.unpack(orig_row)
                    fields[0] = new_id
                    item_dbc.records.append(item_dbc.pack(fields))
                else:
                    print(f"    WARNING: Item {orig_id} not found in Item.dbc")

            # 1b. Clone Spell.dbc entries
            spell_mapping = s.get("spell_clones", {})
            for orig_id, new_id in spell_mapping.items():
                orig_row = spell_dbc.find(orig_id)
                if orig_row:
                    fields = spell_dbc.unpack(orig_row)
                    fields[0] = new_id
                    # Replace any internal spell references
                    for i in range(1, len(fields)):
                        if fields[i] in spell_mapping:
                            fields[i] = spell_mapping[fields[i]]
                    spell_dbc.records.append(spell_dbc.pack(fields))
                else:
                    print(f"    WARNING: Spell {orig_id} not found in Spell.dbc")

            # 1c. Clone ItemSet.dbc entry
            orig_setid = s["original_itemset"]
            new_setid = s["new_itemset"]
            orig_row = itemset_dbc.find(orig_setid)
            if orig_row:
                fields = itemset_dbc.unpack(orig_row)
                fields[0] = new_setid
                # Clear item slots (fields 18-34) and fill with new IDs
                for i in range(18, 35):
                    fields[i] = 0
                for i, nid in enumerate(new_item_ids[:17]):
                    fields[18 + i] = nid
                # Update spell references (fields 35-42)
                for i in range(35, 43):
                    if fields[i] in spell_mapping:
                        fields[i] = spell_mapping[fields[i]]
                itemset_dbc.records.append(itemset_dbc.pack(fields))
            else:
                print(f"    WARNING: ItemSet {orig_setid} not found in ItemSet.dbc")

            # 1d. Clone SSD entry if needed
            ssd_template = s["scaling_template"]
            new_ssd_id = s["new_itemset"]  # We use itemset ID as SSD ID
            if new_ssd_id not in ssd_dbc.get_ids():
                template_row = ssd_dbc.find(ssd_template)
                if template_row:
                    fields = ssd_dbc.unpack(template_row)
                    fields[0] = new_ssd_id
                    ssd_dbc.records.append(ssd_dbc.pack(fields))
                    print(f"    Added SSD {new_ssd_id} (cloned from {ssd_template})")

        # Write patched DBCs
        item_dbc.write(os.path.join(patch_dir, "Item.dbc"))
        itemset_dbc.write(os.path.join(patch_dir, "ItemSet.dbc"))
        spell_dbc.write(os.path.join(patch_dir, "Spell.dbc"))
        ssd_dbc.write(os.path.join(patch_dir, "ScalingStatDistribution.dbc"))
        print("\n  DBCs saved to patch_data/DBFilesClient/")

    # --- Step 2: Generate SQL ---
    print("\n" + "=" * 60)
    print("STEP 2: Generating SQL")
    print("=" * 60)

    # Get actual DB columns dynamically
    print("  Querying database schema...")
    cols = get_db_columns()
    if not cols:
        print("  ERROR: Could not query database schema!")
        return
    print(f"  Found {len(cols)} columns in item_template")

    item_sql = ""
    vendor_sql = ""

    for s in SETS:
        new_item_ids = list(s["original_items"].values())
        orig_item_ids = list(s["original_items"].keys())
        new_setid = s["new_itemset"]
        ssd_id = s.get("scaling_template", s["new_itemset"])

        # Generate item_template INSERT...SELECT for each item
        for i, new_id in enumerate(new_item_ids):
            orig_id = orig_item_ids[i]
            item_sql += f"DELETE FROM item_template WHERE entry = {new_id};\n"

            # We need to know the InventoryType to set the right SSV.
            # Query it from the original item.
            inv_result = subprocess.run(
                f'docker exec -i ac-database mysql -u root -ppassword acore_world -s -N -e "SELECT InventoryType FROM item_template WHERE entry = {orig_id};"',
                shell=True, capture_output=True, text=True
            )
            inv_type = int(inv_result.stdout.strip()) if inv_result.stdout.strip() else 0
            ssv = get_ssv_for_slot(ssd_id, inv_type)

            insert_cols = []
            select_cols = []
            for c in cols:
                insert_cols.append(c)
                if c == "entry":
                    select_cols.append(str(new_id))
                elif c == "ScalingStatDistribution":
                    select_cols.append(str(ssd_id))
                elif c == "ScalingStatValue":
                    select_cols.append(str(ssv))
                elif c == "itemset":
                    select_cols.append(str(new_setid))
                elif c == "Quality":
                    select_cols.append("7")  # Heirloom quality (gold border)
                elif c == "bonding":
                    select_cols.append("7")  # Bind to Account
                elif c == "Flags":
                    select_cols.append("134221824")  # ITEM_FLAG_BIND_TO_ACCOUNT | ITEM_FLAG_NO_DURABILITY
                elif c == "RequiredLevel":
                    select_cols.append("1")  # Heirlooms usable from level 1
                else:
                    select_cols.append(c)

            item_sql += f"INSERT INTO item_template ({', '.join(insert_cols)}) SELECT {', '.join(select_cols)} FROM item_template WHERE entry = {orig_id};\n"

        # Generate npc_vendor SQL
        vendor_id = s["vendor_id"]
        vendor_sql += f"DELETE FROM npc_vendor WHERE entry = {vendor_id};\n"
        for i, nid in enumerate(new_item_ids):
            vendor_sql += f"INSERT INTO npc_vendor (entry, slot, item, maxcount, incrtime, ExtendedCost) VALUES ({vendor_id}, {i}, {nid}, 0, 0, 0);\n"

    with open(os.path.join(SCRIPT_DIR, "heirloom_items.sql"), "w") as f:
        f.write(item_sql)
    with open(os.path.join(SCRIPT_DIR, "heirloom_vendor.sql"), "w") as f:
        f.write(vendor_sql)
    print("  Wrote heirloom_items.sql and heirloom_vendor.sql")

    # --- Step 3: Apply SQL ---
    if not dbc_only:
        print("\n" + "=" * 60)
        print("STEP 3: Applying SQL to database")
        print("=" * 60)

        for sql_file in ["heirloom_items.sql", "heirloom_vendor.sql"]:
            sql_path = os.path.join(SCRIPT_DIR, sql_file)
            print(f"  Applying {sql_file}...")
            result = subprocess.run(
                f'powershell -Command "Get-Content \"{sql_path}\" | docker exec -i ac-database mysql -u root -ppassword acore_world"',
                shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"    ERROR: {result.stderr.strip()}")
            else:
                print(f"    OK")

    # --- Step 3.5: Sync Item.dbc displayids from database ---
    if not dbc_only and not sql_only:
        print("\n" + "=" * 60)
        print("STEP 3.5: Syncing Item.dbc displayids from database")
        print("=" * 60)

        # Collect all custom item IDs
        all_custom_ids = set()
        for s in SETS:
            all_custom_ids.update(s["original_items"].values())

        if all_custom_ids:
            ids_str = ",".join(str(i) for i in sorted(all_custom_ids))
            result = subprocess.run(
                f'docker exec -i ac-database mysql -u root -ppassword acore_world -s -N -e '
                f'"SELECT entry, displayid, InventoryType FROM item_template WHERE entry IN ({ids_str})"',
                shell=True, capture_output=True, text=True
            )

            db_data = {}
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    db_data[int(parts[0])] = {"displayid": int(parts[1]), "invtype": int(parts[2])}

            # Read Item.dbc and patch
            item_dbc_path = os.path.join(patch_dir, "Item.dbc")
            with open(item_dbc_path, 'rb') as f:
                header = f.read(20)
                h_magic, h_count, h_fields, h_recsize, h_strsize = struct.unpack('<4sIIII', header)
                dbc_records = []
                for _ in range(h_count):
                    dbc_records.append(bytearray(f.read(h_recsize)))
                dbc_strings = f.read(h_strsize)

            dbc_fmt = '<' + 'I' * h_fields
            fixes = 0
            for idx, rec in enumerate(dbc_records):
                fields = list(struct.unpack(dbc_fmt, rec))
                rid = fields[0]
                if rid in db_data:
                    changed = False
                    if fields[5] != db_data[rid]["displayid"]:
                        fields[5] = db_data[rid]["displayid"]
                        changed = True
                    if fields[6] != db_data[rid]["invtype"]:
                        fields[6] = db_data[rid]["invtype"]
                        changed = True
                    if changed:
                        dbc_records[idx] = bytearray(struct.pack(dbc_fmt, *fields))
                        fixes += 1

            with open(item_dbc_path, 'wb') as f:
                f.write(struct.pack('<4sIIII', h_magic, len(dbc_records), h_fields, h_recsize, len(dbc_strings)))
                for rec in dbc_records:
                    f.write(rec)
                f.write(dbc_strings)
            print(f"  Synced {fixes} Item.dbc records with database displayids")

    # --- Step 4: Package MPQ ---
    if not dbc_only and not sql_only:
        print("\n" + "=" * 60)
        print("STEP 4: Packaging patch-4.MPQ")
        print("=" * 60)
        pkg_script = os.path.join(SCRIPT_DIR, "package_client_patch.py")
        result = subprocess.run([sys.executable, pkg_script], capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip()}")

    # --- Step 5: Print C++ snippets ---
    print("\n" + "=" * 60)
    print("STEP 5: C++ Snippets for mod_assistant")
    print("=" * 60)
    for s in SETS:
        name_upper = s['name'].upper().replace(' ', '_')
        vendor_id = s['vendor_id']
        print(f"""
// mod_assistant.h — add to enum:
    ASSISTANT_VENDOR_HEIRLOOM_{name_upper} = {vendor_id},

// mod_assistant.h — add #define:
#define GOSSIP_HEIRLOOMS_{name_upper} "|cffa335ee|r{s['name']} ({s['class']} T2)"

// mod_assistant_npc.cpp — add to T2 submenu:
        AddGossipItemFor(player, GOSSIP_ICON_VENDOR, GOSSIP_HEIRLOOMS_{name_upper}, GOSSIP_SENDER_MAIN, ASSISTANT_GOSSIP_HEIRLOOM + NN);

// mod_assistant_npc.cpp — add to switch:
        case ASSISTANT_GOSSIP_HEIRLOOM + NN:
            id = ASSISTANT_VENDOR_HEIRLOOM_{name_upper};
            break;
""")

    print("=" * 60)
    print("DONE! Remember to:")
    print("  1. Add C++ snippets above to mod_assistant (if new sets)")
    print("  2. docker compose build ac-worldserver (if C++ changed)")
    print("  3. docker compose restart ac-worldserver")
    print("  4. Clear client WoW cache before launching")
    print("=" * 60)


if __name__ == "__main__":
    dbc_only = "--dbc-only" in sys.argv
    sql_only = "--sql-only" in sys.argv
    build_heirlooms(dbc_only=dbc_only, sql_only=sql_only)
