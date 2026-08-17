import struct
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PATCH_DIR = os.path.join(SCRIPT_DIR, "patch_data", "DBFilesClient")
ORIG_DIR = os.path.join(SCRIPT_DIR, "original_dbcs")
os.makedirs(PATCH_DIR, exist_ok=True)

def get_dbc_path(name):
    patched = os.path.join(PATCH_DIR, name)
    orig = os.path.join(ORIG_DIR, name)
    return patched if os.path.exists(patched) else orig

PORTAL_MAPPINGS = {
    # Item Use Spell: Clone 8690 (Hearthstone) -> 90200 (Portalstone Item Use Spell)
    8690: 90200,

    # Portals (Original ID -> New Cloned ID)
    10059: 90201, # Portal: Stormwind
    11416: 90202, # Portal: Ironforge
    11419: 90203, # Portal: Darnassus
    11417: 90205, # Portal: Orgrimmar
    11418: 90206, # Portal: Undercity
    11420: 90207, # Portal: Thunder Bluff
}

def patch_spell_dbc():
    dbc_path = get_dbc_path("Spell.dbc")
    with open(dbc_path, "rb") as f:
        header = f.read(20)
        magic, record_count, field_count, record_size, string_block_size = struct.unpack('<4sIIII', header)
        fmt = '<' + 'I' * field_count
        records = []
        for _ in range(record_count):
            records.append(bytearray(f.read(record_size)))
        string_block = bytearray(f.read(string_block_size))

    # Remove existing custom target IDs if re-running
    target_ids = set(range(90200, 90230))
    records = [r for r in records if struct.unpack('<I', r[:4])[0] not in target_ids]

    # Custom description string offset for 90200
    custom_desc = b"Summons a Shimmering Portal to your bound home location.\x00"
    desc_offset = len(string_block)
    string_block += custom_desc

    for orig_id, new_id in PORTAL_MAPPINGS.items():
        orig_rec = None
        for r in records:
            if struct.unpack('<I', r[:4])[0] == orig_id:
                orig_rec = r
                break

        if not orig_rec:
            print(f"WARNING: Spell {orig_id} not found in Spell.dbc!")
            continue

        fields = list(struct.unpack(fmt, orig_rec))
        fields[0] = new_id  # Set new spell ID

        # Clear recovery time / cooldown
        fields[28] = 0  # RecoveryTime
        fields[29] = 0  # CategoryRecoveryTime

        # Clear reagents (indices 52-59 Reagent_1..8, 60-67 ReagentCount_1..8)
        for i in range(52, 68):
            fields[i] = 0

        # Special handling for item use spell 90200
        if new_id == 90200:
            for i in range(170, 186):
                fields[i] = desc_offset

        records.append(bytearray(struct.pack(fmt, *fields)))

    out_path = os.path.join(PATCH_DIR, "Spell.dbc")
    with open(out_path, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(records), field_count, record_size, len(string_block)))
        for r in records:
            f.write(r)
        f.write(string_block)
    print(f"Successfully patched Spell.dbc with {len(PORTAL_MAPPINGS)} custom portal spells!")

if __name__ == "__main__":
    patch_spell_dbc()
