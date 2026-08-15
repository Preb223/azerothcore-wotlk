import struct
import zlib
import os

CLIENT_MPQ_PATH = r'C:\ChromieCraft_3.3.5a\Data\patch-4.MPQ'
FALLBACK_MPQ_PATH = r'custom\patch-4.MPQ'

def generate_crypt_table():
    seed = 0x00100001
    crypt_table = {}
    for i in range(256):
        index = i
        for j in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            temp1 = (seed & 0xFFFF) << 16
            seed = (seed * 125 + 3) % 0x2AAAAB
            temp2 = seed & 0xFFFF
            crypt_table[index] = temp1 | temp2
            index += 256
    return crypt_table

CRYPT_TABLE = generate_crypt_table()

def mpq_hash_string(string, hash_type):
    seed1 = 0x7FED7FED
    seed2 = 0xEEEEEEEE
    for ch in string.upper():
        ch = ord(ch)
        seed1 = CRYPT_TABLE[(hash_type << 8) + ch] ^ ((seed1 + seed2) & 0xFFFFFFFF)
        seed2 = (ch + seed1 + seed2 + (seed2 << 5) + 3) & 0xFFFFFFFF
    return seed1 & 0xFFFFFFFF

def encrypt_block(data, key):
    assert len(data) % 4 == 0
    seed = 0xEEEEEEEE
    out = bytearray()
    
    for i in range(0, len(data), 4):
        val = struct.unpack_from('<I', data, i)[0]
        
        seed_add = CRYPT_TABLE[0x400 + (key & 0xFF)]
        seed = (seed + seed_add) & 0xFFFFFFFF
        
        ch = (val ^ (key + seed)) & 0xFFFFFFFF
        
        not_key = (~key) & 0xFFFFFFFF
        key = (((not_key << 21) + 0x11111111) & 0xFFFFFFFF) | (key >> 11)
        key = key & 0xFFFFFFFF
        
        seed = (val + seed + (seed << 5) + 3) & 0xFFFFFFFF
        
        out += struct.pack('<I', ch)
        
    return bytes(out)

def create_mpq(files, output_path):
    hash_table_size = 16
    while hash_table_size < len(files) * 2:
        hash_table_size *= 2

    file_entries = []
    raw_data = bytearray()

    for archive_path, file_data in files.items():
        block_data = file_data
        flags = 0x80000000  # EXISTS (uncompressed)
        compressed_size = len(block_data)

        file_entries.append({
            'path': archive_path,
            'offset': len(raw_data),
            'compressed_size': compressed_size,
            'file_size': len(file_data),
            'flags': flags
        })
        raw_data += block_data

    # Generate hash table
    hash_table = [{'hash_a': 0xFFFFFFFF, 'hash_b': 0xFFFFFFFF, 'locale': 0, 'platform': 0, 'block_index': 0xFFFFFFFF, 'reserved': 0} for _ in range(hash_table_size)]
    
    for block_index, entry in enumerate(file_entries):
        path = entry['path']
        hash_offset = mpq_hash_string(path, 0) & (hash_table_size - 1)
        hash_a = mpq_hash_string(path, 1)
        hash_b = mpq_hash_string(path, 2)

        while hash_table[hash_offset]['block_index'] != 0xFFFFFFFF:
            hash_offset = (hash_offset + 1) & (hash_table_size - 1)

        hash_table[hash_offset] = {
            'hash_a': hash_a,
            'hash_b': hash_b,
            'locale': 0,
            'platform': 0,
            'block_index': block_index,
            'reserved': 0
        }

    header_size = 32
    archive_size = header_size + len(raw_data) + len(hash_table)*16 + len(file_entries)*16
    hash_table_offset = header_size + len(raw_data)
    block_table_offset = hash_table_offset + len(hash_table)*16
    data_offset = header_size

    block_table = []
    for entry in file_entries:
        block_table.append({
            'offset': entry['offset'] + data_offset,
            'compressed_size': entry['compressed_size'],
            'file_size': entry['file_size'],
            'flags': entry['flags']
        })

    # Encrypt hash and block tables
    hash_data = bytearray()
    for h in hash_table:
        hash_data += struct.pack('<II', h['hash_a'], h['hash_b'])
        hash_data += struct.pack('<HBB', h['locale'], h['platform'], h['reserved'])
        hash_data += struct.pack('<I', h['block_index'])
    
    hash_key = mpq_hash_string('(hash table)', 3)
    enc_hash_data = encrypt_block(hash_data, hash_key)

    block_data = bytearray()
    for b in block_table:
        block_data += struct.pack('<IIII', b['offset'], b['compressed_size'], b['file_size'], b['flags'])
    
    block_key = mpq_hash_string('(block table)', 3)
    enc_block_data = encrypt_block(block_data, block_key)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, 'wb') as f:
            f.write(b'MPQ\x1A')
            f.write(struct.pack('<I', header_size))
            f.write(struct.pack('<I', archive_size))
            f.write(struct.pack('<H', 0)) # version
            f.write(struct.pack('<H', 3)) # sector size shift
            f.write(struct.pack('<I', hash_table_offset))
            f.write(struct.pack('<I', block_table_offset))
            f.write(struct.pack('<I', hash_table_size))
            f.write(struct.pack('<I', len(file_entries)))

            f.write(raw_data)
            f.write(enc_hash_data)
            f.write(enc_block_data)
        print(f"Successfully created {output_path} ({os.path.getsize(output_path)} bytes)")
    except PermissionError:
        print(f"WARNING: Permission denied writing to {output_path} (WoW Client is running).")
        if output_path != FALLBACK_MPQ_PATH:
            print(f"Saving copy to {FALLBACK_MPQ_PATH}...")
            create_mpq(files, FALLBACK_MPQ_PATH)

if __name__ == '__main__':
    files = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    patch_dir = os.path.join(script_dir, 'patch_data')
    if os.path.exists(patch_dir):
        for root, _, filenames in os.walk(patch_dir):
            for name in filenames:
                file_path = os.path.join(root, name)
                archive_path = os.path.relpath(file_path, patch_dir).replace('/', '\\')
                with open(file_path, 'rb') as f:
                    files[archive_path] = f.read()
        
        if files:
            create_mpq(files, CLIENT_MPQ_PATH)
        else:
            print("No files found in patch_data/")
    else:
        print("ERROR: patch_data directory not found!")