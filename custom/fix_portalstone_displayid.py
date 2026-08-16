import struct
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PATCH_DIR = os.path.join(SCRIPT_DIR, "patch_data", "DBFilesClient")
ORIG_DIR = os.path.join(SCRIPT_DIR, "original_dbcs")

def fix_item_dbc():
    dbc_path = os.path.join(PATCH_DIR, "Item.dbc")
    if not os.path.exists(dbc_path):
        dbc_path = os.path.join(ORIG_DIR, "Item.dbc")

    with open(dbc_path, "rb") as f:
        header = f.read(20)
        magic, record_count, field_count, record_size, string_block_size = struct.unpack('<4sIIII', header)
        fmt = '<' + 'I' * field_count
        records = []
        for _ in range(record_count):
            records.append(bytearray(f.read(record_size)))
        string_block = bytearray(f.read(string_block_size))

    # Remove existing 90124 record
    records = [r for r in records if struct.unpack('<I', r[:4])[0] != 90124]

    # Add correct 90124 record with displayid = 6418 (Hearthstone)
    # (id=90124, class=15, subclass=0, sound_override=0xFFFFFFFF, material=7, displayid=6418, inv_type=0, sheath=0)
    new_fields = [90124, 15, 0, 4294967295, 7, 6418, 0, 0]
    records.append(bytearray(struct.pack(fmt, *new_fields)))

    out_path = os.path.join(PATCH_DIR, "Item.dbc")
    with open(out_path, "wb") as f:
        f.write(struct.pack('<4sIIII', magic, len(records), field_count, record_size, len(string_block)))
        for r in records:
            f.write(r)
        f.write(string_block)

    print(f"Successfully updated Item.dbc record 90124 with displayid = 6418!")

if __name__ == "__main__":
    fix_item_dbc()
