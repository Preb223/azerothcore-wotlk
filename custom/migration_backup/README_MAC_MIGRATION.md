# 🚀 Complete AzerothCore Server Migration & Backup Guide

This guide details how to export the **entire server** (all accounts, characters, playerbots, custom items, spells, vendors, and world edits) from your existing host and cleanly restore it to a new host (such as macOS or Linux) with **zero data corruption**.

---

## 📦 Part 1: Export Complete Server on Source Host (Windows / Source PC)

> [!IMPORTANT]
> Always dump and compress inside the MySQL container, then use `docker cp` to extract the file. This prevents Windows/PowerShell from converting or corrupting line endings and binary data streams.

Open **PowerShell** or **Command Prompt** on your source computer in your `azerothcore-wotlk` directory:

```powershell
# 1. Dump all 4 databases directly inside the MySQL container (into /tmp)
docker exec ac-database bash -c "mysqldump -uroot -ppassword --databases acore_auth acore_characters acore_playerbots acore_world > /tmp/full_backup.sql"

# 2. Compress the dump directly inside Linux
docker exec ac-database bash -c "gzip -f /tmp/full_backup.sql"

# 3. Copy the compressed archive out to your host folder
docker cp ac-database:/tmp/full_backup.sql.gz ./full_backup.sql.gz
```

This creates **`full_backup.sql.gz`** in your current folder.

---

## 🚚 Part 2: Transfer Backup to the Destination Machine (Mac)

Copy `full_backup.sql.gz` to your target machine and place it in the root of the repository:
```text
~/Documents/GitHub/azerothcore-wotlk/full_backup.sql.gz
```
*(You can use a USB flash drive, local network file sharing, AirDrop, Google Drive, etc.)*

---

## 📥 Part 3: Restore Everything on Destination Host (Mac)

Open **Terminal** on your Mac in the repository root:

```bash
cd ~/Documents/GitHub/azerothcore-wotlk
```

### Step A: Ensure Database Container is Running
```bash
docker compose up -d ac-database
```
*Wait ~10 seconds for the database to become healthy.*

### Step B: Import the Full Backup
```bash
# Decompress and import all 4 databases in a single command
gunzip -c full_backup.sql.gz | docker exec -i ac-database mysql -uroot -ppassword
```

### Step C: Update the Realmlist IP (if server IP changed)
If the Mac has IP `192.168.1.214`:
```bash
docker exec -i ac-database mysql -uroot -ppassword acore_auth -e "UPDATE realmlist SET address = '192.168.1.214', localAddress = '192.168.1.214' WHERE id = 1;"
```

### Step D: Restart All Services
```bash
docker compose restart ac-worldserver ac-authserver
```

---

## 🎮 Part 4: WoW Client Setup (All Connecting PCs)

1. **Realmlist**:
   Edit `Data/enUS/realmlist.wtf` (or `Data/enGB/realmlist.wtf`):
   ```text
   set realmlist 192.168.1.214
   ```
   *(Or `set realmlist 127.0.0.1` if playing locally on the same Mac hosting the server).*

2. **Custom Patch**:
   - Copy `custom/patch-4.MPQ` into your WoW Client `Data/patch-4.MPQ`.
   - Delete your WoW Client `Cache/` folder.

---

## 🛠️ Verification & Useful Commands

```bash
# Check character count after restore
docker exec -i ac-database mysql -uroot -ppassword -e "SELECT COUNT(*) AS total_characters FROM acore_characters.characters;"

# Check accounts after restore
docker exec -i ac-database mysql -uroot -ppassword -e "SELECT id, username FROM acore_auth.account;"

# View worldserver live logs
docker compose logs -f ac-worldserver

# View authserver live logs
docker compose logs -f ac-authserver
```
