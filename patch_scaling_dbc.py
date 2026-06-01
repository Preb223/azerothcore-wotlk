import struct
import os

INPUT_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\original_dbcs\ScalingStatDistribution.dbc'
OUTPUT_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\ScalingStatDistribution.dbc'
PATCHED_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\ScalingStatDistribution_patched.dbc'

def patch_dbc():
    if not os.path.exists(INPUT_DBC_PATH):
        print(f"ERROR: {INPUT_DBC_PATH} not found!")
        return False
        
    with open(INPUT_DBC_PATH, 'rb') as f:
        data = f.read()
        
    magic, rc, fc, rs, ss = struct.unpack_from('<4sIIII', data, 0)
    print(f"Input DBC: Magic={magic.decode('utf-8', errors='ignore')}, Records={rc}, Fields={fc}, RecordSize={rs}, StringSize={ss}")
    
    # Read all existing records, filtering out 995-999 to avoid duplication
    records = []
    for i in range(rc):
        off = 20 + i * rs
        entry = struct.unpack_from('<I', data, off)[0]
        if entry < 995:
            records.append(data[off:off + rs])
            
    print(f"Loaded {len(records)} original records (filtered out custom ones)")
    
    # Define our custom records
    # 995: Strength (4), Agility (3), Stamina (7)
    # 996: Strength (4), Stamina (7), Defense (12)
    # 997: Strength (4), Stamina (7), Crit (32), Hit (31)
    # 998: Strength (4), Stamina (7), Crit (32)
    # 999: Strength (4), Stamina (7), Defense (12), Spell Power (45)
    custom_definitions = [
        (995, [4, 3, 7, -1, -1, -1, -1, -1, -1, -1], [5259, 5259, 7888, 0, 0, 0, 0, 0, 0, 0], 80),
        (996, [4, 7, 12, -1, -1, -1, -1, -1, -1, -1], [5259, 7888, 5259, 0, 0, 0, 0, 0, 0, 0], 80),
        (997, [4, 7, 32, 31, -1, -1, -1, -1, -1, -1], [5259, 7888, 5259, 5259, 0, 0, 0, 0, 0, 0], 80),
        (998, [4, 7, 32, -1, -1, -1, -1, -1, -1, -1], [5259, 7888, 5259, 0, 0, 0, 0, 0, 0, 0], 80),
        (999, [4, 7, 12, 45, -1, -1, -1, -1, -1, -1], [5259, 7888, 5259, 5200, 0, 0, 0, 0, 0, 0], 80)
    ]
    
    for new_entry_id, stat_mods, modifiers, max_level in custom_definitions:
        new_record = struct.pack('<I 10i 10I I', new_entry_id, *stat_mods, *modifiers, max_level)
        records.append(new_record)
        print(f"Appended custom record {new_entry_id}")
        
    # Rebuild headers
    new_rc = len(records)
    new_header = struct.pack('<4sIIII', magic, new_rc, fc, rs, ss)
    
    # Combine everything
    records_data = b''.join(records)
    string_block = data[20 + rc * rs:]
    new_data = new_header + records_data + string_block
    
    # Overwrite the output path
    with open(OUTPUT_DBC_PATH, 'wb') as f:
        f.write(new_data)
    print(f"Saved patched DBC: {OUTPUT_DBC_PATH}")
        
    # Write a copy to the patched output path
    with open(PATCHED_DBC_PATH, 'wb') as f:
        f.write(new_data)
    print(f"Saved patched DBC copy to: {PATCHED_DBC_PATH}")
    
    return True

if __name__ == '__main__':
    patch_dbc()
