import struct
import os

INPUT_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\original_dbcs\Spell.dbc'
OUTPUT_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\Spell.dbc'
PATCHED_DBC_PATH = r'c:\Users\Blake\GitHub Repositories\azerothcore-wotlk\patch_data\DBFilesClient\Spell.dbc'

def patch_spell():
    if not os.path.exists(INPUT_DBC_PATH):
        print(f"ERROR: {INPUT_DBC_PATH} not found!")
        return False
        
    with open(INPUT_DBC_PATH, 'rb') as f:
        data = bytearray(f.read())
        
    magic, rc, fc, rs, ss = struct.unpack_from('<4sIIII', data, 0)
    print(f"Original DBC: Magic={magic.decode('utf-8', errors='ignore')}, Records={rc}, Fields={fc}, RecordSize={rs}, StringSize={ss}")
    
    # 1. Define new strings to append to the string block
    str_99015 = b"When struck in combat has a 3% chance of stealing life from the target enemy.\x00"
    str_99016 = b"When struck in combat has a 1% chance of dealing Fire damage to all targets around you.\x00"
    str_99992 = (
        b"Blasts your enemy with lightning, dealing Nature damage and then jumping to additional nearby enemies. "
        b"Each jump reduces that victim's Nature resistance. Affects up to 5 targets. "
        b"Your primary target is also consumed by a cyclone, slowing its attack speed by 20% for 12 sec.\x00"
    )
    
    offset_99015 = ss
    offset_99016 = ss + len(str_99015)
    offset_99992 = ss + len(str_99015) + len(str_99016)
    
    # Append the new strings to the end of the DBC data (end of the string block)
    string_block_offset = 20 + rc * rs
    string_block = data[string_block_offset:]
    
    # Let's read all original records
    records = []
    original_records = {}
    for i in range(rc):
        off = 20 + i * rs
        entry = struct.unpack_from('<I', data, off)[0]
        # Filter out our custom spells to make it idempotent
        if entry not in (99015, 99016, 99017, 99018, 99992):
            records.append(data[off:off + rs])
            original_records[entry] = data[off:off + rs]
            
    print(f"Loaded {len(records)} original records.")
    
    # Check if we have all needed template spells
    needed = [18815, 18816, 18817, 18818, 21992]
    for n in needed:
        if n not in original_records:
            print(f"ERROR: Template spell {n} not found in original records!")
            return False
            
    original_string_block = data[20 + rc * rs : 20 + rc * rs + ss]
    
    # Create the new string block
    new_string_block = original_string_block + str_99015 + str_99016 + str_99992
    new_ss = len(new_string_block)
    
    # Now duplicate and modify the records
    # 99017 (duplicate of 18817)
    rec_99017 = bytearray(original_records[18817])
    struct.pack_into('<I', rec_99017, 0, 99017) # Change ID to 99017
    
    # 99018 (duplicate of 18818)
    rec_99018 = bytearray(original_records[18818])
    struct.pack_into('<I', rec_99018, 0, 99018) # Change ID to 99018
    
    # 99015 (duplicate of 18815, triggers 99017, generic description)
    rec_99015 = bytearray(original_records[18815])
    struct.pack_into('<I', rec_99015, 0, 99015) # Change ID to 99015
    struct.pack_into('<I', rec_99015, 116 * 4, 99017) # Change trigger spell ID to 99017
    for lang in range(16):
        struct.pack_into('<I', rec_99015, (170 + lang) * 4, offset_99015) # Set description offset
        
    # 99016 (duplicate of 18816, triggers 99018, generic description)
    rec_99016 = bytearray(original_records[18816])
    struct.pack_into('<I', rec_99016, 0, 99016) # Change ID to 99016
    struct.pack_into('<I', rec_99016, 116 * 4, 99018) # Change trigger spell ID to 99018
    for lang in range(16):
        struct.pack_into('<I', rec_99016, (170 + lang) * 4, offset_99016) # Set description offset
        
    # 99992 (duplicate of 21992, generic description)
    rec_99992 = bytearray(original_records[21992])
    struct.pack_into('<I', rec_99992, 0, 99992) # Change ID to 99992
    for lang in range(16):
        struct.pack_into('<I', rec_99992, (170 + lang) * 4, offset_99992) # Set description offset
        
    # Append the custom records to the records list
    records.append(rec_99017)
    records.append(rec_99018)
    records.append(rec_99015)
    records.append(rec_99016)
    records.append(rec_99992)
    
    # Rebuild header
    new_rc = len(records)
    new_header = struct.pack('<4sIIII', magic, new_rc, fc, rs, new_ss)
    print(f"New DBC: Records={new_rc}, Fields={fc}, RecordSize={rs}, StringSize={new_ss}")
    
    # Combine everything
    new_data = new_header + b''.join(records) + new_string_block
    
    # Save patched Spell.dbc in both root and patch_data
    with open(OUTPUT_DBC_PATH, 'wb') as f:
        f.write(new_data)
    print(f"Saved patched Spell.dbc to root: {OUTPUT_DBC_PATH}")
    
    os.makedirs(os.path.dirname(PATCHED_DBC_PATH), exist_ok=True)
    with open(PATCHED_DBC_PATH, 'wb') as f:
        f.write(new_data)
    print(f"Saved patched Spell.dbc copy to client patch directory: {PATCHED_DBC_PATH}")
    
    return True

if __name__ == '__main__':
    patch_spell()
