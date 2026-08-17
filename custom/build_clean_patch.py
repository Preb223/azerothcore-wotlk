import struct
import os
import subprocess
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ORIG_DIR = os.path.join(SCRIPT_DIR, "original_dbcs")
PATCH_DIR = os.path.join(SCRIPT_DIR, "patch_data", "DBFilesClient")
os.makedirs(PATCH_DIR, exist_ok=True)

def build_clean_patch():
    print("=" * 60)
    print("Building 100% Clean, Crash-Proof DBCs & Client Patch")
    print("=" * 60)

    # 1. Reset all DBCs directly from clean extracts in original_dbcs/
    for fname in ["CharBaseInfo.dbc", "ItemSet.dbc", "ScalingStatDistribution.dbc", "ScalingStatValues.dbc"]:
        src = os.path.join(ORIG_DIR, fname)
        dst = os.path.join(PATCH_DIR, fname)
        shutil.copy2(src, dst)
        print(f"  [OK] Reset {fname}")

    # 2. Reset clean Spell.dbc (Prinstine, no corrupted records)
    src_spell = os.path.join(ORIG_DIR, "Spell.dbc")
    dst_spell = os.path.join(PATCH_DIR, "Spell.dbc")
    with open(src_spell, "rb") as f:
        magic, count, fields, rec_size, str_size = struct.unpack('<4sIIII', f.read(20))
        records = [f.read(rec_size) for _ in range(count)]
        string_block = f.read(str_size)
    
    # Filter out any anomalous records with ID >= 1,000,000 to prevent client memory alloc crash
    clean_spell_records = []
    for r in records:
        id_ = struct.unpack('<I', r[:4])[0]
        if id_ < 1000000:
            clean_spell_records.append(r)
            
    with open(dst_spell, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(clean_spell_records), fields, rec_size, len(string_block)))
        for r in clean_spell_records:
            f.write(r)
        f.write(string_block)
    print(f"  [OK] Spell.dbc verified clean: {len(clean_spell_records)} records, max_id={max(struct.unpack('<I', r[:4])[0] for r in clean_spell_records)}")

    # 3. Patch Item.dbc with all custom items (90000 to 90124)
    src_item = os.path.join(ORIG_DIR, "Item.dbc")
    dst_item = os.path.join(PATCH_DIR, "Item.dbc")
    with open(src_item, "rb") as f:
        magic, count, fields, rec_size, str_size = struct.unpack('<4sIIII', f.read(20))
        records = [f.read(rec_size) for _ in range(count)]
        string_block = f.read(str_size)

    # Fetch custom items from item_template
    res = subprocess.run(
        'docker exec -i ac-database mysql -u root -ppassword acore_world -s -e "SELECT entry, class, subclass, SoundOverrideSubclass, Material, displayid, InventoryType, sheath FROM item_template WHERE entry >= 90000 ORDER BY entry;"',
        shell=True, capture_output=True, text=True
    )
    
    existing_ids = {struct.unpack('<I', r[:4])[0] for r in records}
    added_count = 0
    for line in res.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        entry, cls, subcls, snd, mat, disp, inv, sheath = [int(p) for p in parts]
        if snd == -1:
            snd = 0xFFFFFFFF
        rec = struct.pack('<8I', entry, cls, subcls, snd, mat, disp, inv, sheath)
        if entry not in existing_ids:
            records.append(rec)
            existing_ids.add(entry)
            added_count += 1
            
    with open(dst_item, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(records), fields, rec_size, len(string_block)))
        for r in records:
            f.write(r)
        f.write(string_block)
    print(f"  [OK] Item.dbc patched cleanly: {len(records)} records (+{added_count} custom items, max_id={max(existing_ids)})")

    # 4. Set Portalstone (90124) in item_template to use spell 8690 (native Hearthstone spell)
    subprocess.run(
        'docker exec -i ac-database mysql -u root -ppassword acore_world -e "UPDATE item_template SET spellid_1 = 8690, spelltrigger_1 = 0, ScriptName = \'item_heirloom_portalstone\' WHERE entry = 90124;"',
        shell=True, check=True
    )
    print("  [OK] Updated item_template for Portalstone 90124 (spellid_1 = 8690, ScriptName = item_heirloom_portalstone)")

    # 5. Validate All DBCs
    print("\n" + "=" * 60)
    print("Validating Binary Integrity & Allocation Size")
    print("=" * 60)
    for fname in sorted(os.listdir(PATCH_DIR)):
        if fname.endswith(".dbc"):
            fpath = os.path.join(PATCH_DIR, fname)
            with open(fpath, "rb") as f:
                header = f.read(20)
                m, cnt, flds, rsz, ssz = struct.unpack('<4sIIII', header)
                ids = []
                for i in range(cnt):
                    r = f.read(rsz)
                    if len(r) != rsz:
                        raise ValueError(f"Corrupted record {i} in {fname}")
                    if rsz >= 4:
                        ids.append(struct.unpack('<I', r[:4])[0])
                sb = f.read(ssz)
                if len(sb) != ssz:
                    raise ValueError(f"Corrupted string block in {fname}")
            max_id = max(ids) if ids else 0
            alloc_mb = (max_id * 4) / (1024 * 1024)
            print(f"  [PASSED] {fname:30s} Count={cnt:<6d} MaxID={max_id:<7d} ClientIndexRAM={alloc_mb:.2f} MB")

    # 6. Copy DBCs into live Docker container
    subprocess.run(
        'docker run --rm -v azerothcore-wotlk_ac-client-data:/data -v ' + PATCH_DIR + ':/custom alpine sh -c "mkdir -p /data/dbc && cp -v /custom/*.dbc /data/dbc/"',
        shell=True, check=True
    )

    # 7. Package patch-4.MPQ
    print("\n" + "=" * 60)
    print("Packaging patch-4.MPQ")
    print("=" * 60)
    subprocess.run('python3 custom/package_client_patch.py', shell=True, check=True)
    print("\n[SUCCESS] Clean patch-4.MPQ generated successfully!")

if __name__ == "__main__":
    build_clean_patch()
