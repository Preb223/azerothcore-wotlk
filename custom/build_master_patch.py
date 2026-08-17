import struct
import os
import subprocess
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ORIG_DIR = os.path.join(SCRIPT_DIR, "original_dbcs")
PATCH_DIR = os.path.join(SCRIPT_DIR, "patch_data", "DBFilesClient")
os.makedirs(PATCH_DIR, exist_ok=True)

def rebuild_all():
    print("=" * 60)
    print("1. Running Heirloom Sets Builder")
    print("=" * 60)
    
    # Import and run build_heirlooms
    import build_heirlooms
    build_heirlooms.build_heirlooms(dbc_only=True, sql_only=False)
    
    print("\n" + "=" * 60)
    print("2. Injecting Standalone Items & Spells into DBCs")
    print("=" * 60)
    
    # --- A. Patch Item.dbc (Always starting from clean original_dbcs) ---
    item_dbc_path = os.path.join(ORIG_DIR, "Item.dbc")
    with open(item_dbc_path, "rb") as f:
        magic, count, fields, rec_size, str_size = struct.unpack('<4sIIII', f.read(20))
        records = [f.read(rec_size) for _ in range(count)]
        string_block = f.read(str_size)
    
    # Query database for all custom items >= 90000
    res = subprocess.run(
        'docker exec -i ac-database mysql -u root -ppassword acore_world -s -e "SELECT entry, class, subclass, SoundOverrideSubclass, Material, displayid, InventoryType, sheath FROM item_template WHERE entry >= 90000 ORDER BY entry;"',
        shell=True, capture_output=True, text=True
    )
    
    existing_ids = {struct.unpack('<I', r[:4])[0] for r in records}
    added_items = 0
    for line in res.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        entry, cls, subcls, snd, mat, disp, inv, sheath = [int(p) for p in parts]
        if snd == -1:
            snd = 0xFFFFFFFF
        
        rec_bytes = struct.pack('<8I', entry, cls, subcls, snd, mat, disp, inv, sheath)
        if entry in existing_ids:
            # Replace existing
            for idx, r in enumerate(records):
                if struct.unpack('<I', r[:4])[0] == entry:
                    records[idx] = rec_bytes
                    break
        else:
            records.append(rec_bytes)
            existing_ids.add(entry)
            added_items += 1
            
    out_item_path = os.path.join(PATCH_DIR, "Item.dbc")
    with open(out_item_path, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(records), fields, rec_size, len(string_block)))
        for r in records:
            f.write(r)
        f.write(string_block)
    print(f"Item.dbc successfully updated: {len(records)} total records (added/updated {added_items} custom items).")

    # --- B. Patch Spell.dbc (Always starting from clean original_dbcs) ---
    spell_dbc_path = os.path.join(ORIG_DIR, "Spell.dbc")
    with open(spell_dbc_path, "rb") as f:
        magic, count, fields, rec_size, str_size = struct.unpack('<4sIIII', f.read(20))
        records = [f.read(rec_size) for _ in range(count)]
        string_block = bytearray(f.read(str_size))
        
    spell_map = {struct.unpack('<I', r[:4])[0]: r for r in records}
    
    # 8690 (Hearthstone) -> 90200 (Portalstone Use Spell)
    hearth_rec = spell_map.get(8690)
    if hearth_rec:
        fmt = '<' + 'I' * fields
        unpacked = list(struct.unpack(fmt, hearth_rec))
        unpacked[0] = 90200  # New ID
        unpacked[28] = 0     # RecoveryTime
        unpacked[29] = 0     # CategoryRecoveryTime
        
        custom_desc = b"Summons a Shimmering Portal to your bound home location.\x00"
        desc_offset = len(string_block)
        string_block += custom_desc
        for i in range(170, 186):
            unpacked[i] = desc_offset
            
        new_rec = struct.pack(fmt, *unpacked)
        # Remove old 90200 if exists
        records = [r for r in records if struct.unpack('<I', r[:4])[0] != 90200]
        records.append(new_rec)
        print("Spell 90200 (Portalstone Item Use) successfully cloned into Spell.dbc.")
    else:
        print("WARNING: Hearthstone spell 8690 not found in Spell.dbc!")

    with open(spell_dbc_path, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(records), fields, rec_size, len(string_block)))
        for r in records:
            f.write(r)
        f.write(string_block)
    print(f"Spell.dbc successfully written: {len(records)} records.")

    # --- C. Verify Integrity of All DBCs ---
    print("\n" + "=" * 60)
    print("3. Validating Binary Integrity of All DBCs")
    print("=" * 60)
    for fname in sorted(os.listdir(PATCH_DIR)):
        if fname.endswith(".dbc"):
            fpath = os.path.join(PATCH_DIR, fname)
            with open(fpath, "rb") as f:
                header = f.read(20)
                m, cnt, flds, rsz, ssz = struct.unpack('<4sIIII', header)
                for i in range(cnt):
                    r = f.read(rsz)
                    if len(r) != rsz:
                        raise ValueError(f"Corrupted DBC {fname} at record {i}!")
                sb = f.read(ssz)
                if len(sb) != ssz:
                    raise ValueError(f"Corrupted String Table in {fname}!")
            print(f"  [OK] {fname:30s} Count={cnt:<6d} RecSize={rsz:<4d} StrSize={ssz}")

    # --- D. Copy into Live Docker Volume ---
    print("\n" + "=" * 60)
    print("4. Copying DBCs into Docker Volume")
    print("=" * 60)
    cmd = (
        'docker run --rm '
        '-v azerothcore-wotlk_ac-client-data:/data '
        f'-v {PATCH_DIR}:/custom '
        'alpine sh -c "mkdir -p /data/dbc && cp -v /custom/*.dbc /data/dbc/"'
    )
    subprocess.run(cmd, shell=True, check=True)

    # --- E. Package patch-4.MPQ ---
    print("\n" + "=" * 60)
    print("5. Packaging patch-4.MPQ")
    print("=" * 60)
    import package_client_patch
    package_client_patch.main() if hasattr(package_client_patch, 'main') else subprocess.run('python3 custom/package_client_patch.py', shell=True, check=True)
    print("\n[SUCCESS] Master DBC build & packaging completed perfectly!")

if __name__ == "__main__":
    rebuild_all()
