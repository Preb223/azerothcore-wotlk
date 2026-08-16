# AzerothCore macOS Migration Guide

This package contains compressed database backups and step-by-step instructions for running your AzerothCore WotLK server on macOS (Apple Silicon M1/M2/M3 or Intel Mac).

---

## 1. Prerequisites on macOS

1. **Install Docker Desktop for Mac**:
   Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) (select Apple Silicon or Intel based on your Mac). Start Docker Desktop and ensure it is running.

2. **Install Git & Homebrew** (optional, recommended):
   Open Terminal on macOS and install Homebrew if not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

---

## 2. Copy Repository & Migration Backup to Mac

Copy your entire `azerothcore-wotlk` directory (or clone from Git and pull) to your MacBook, e.g. `~/azerothcore-wotlk`.

---

## 3. Database Restore & Server Startup (on MacBook Terminal)

Open **Terminal** on your MacBook and navigate to the project directory:

```bash
cd ~/azerothcore-wotlk
```

### Step A: Start MySQL Database Container
```bash
docker compose up -d ac-database
```
*Wait ~15-20 seconds for MySQL to initialize and become healthy.*

### Step B: Import Compressed Database Backups
Import all 4 compressed `.sql.gz` database dumps:

```bash
gunzip -c custom/migration_backup/acore_auth.sql.gz | docker exec -i ac-database mysql -uroot -ppassword acore_auth
gunzip -c custom/migration_backup/acore_characters.sql.gz | docker exec -i ac-database mysql -uroot -ppassword acore_characters
gunzip -c custom/migration_backup/acore_playerbots.sql.gz | docker exec -i ac-database mysql -uroot -ppassword acore_playerbots
gunzip -c custom/migration_backup/acore_world.sql.gz | docker exec -i ac-database mysql -uroot -ppassword acore_world
```

### Step C: Build & Launch Worldserver and Authserver
```bash
docker compose up -d --build
```

---

## 4. WoW Client MPQ Data

* Copy `custom/patch-4.MPQ` to your WoW 3.3.5a Client `Data/patch-4.MPQ`.
* Clear your WoW Client `Cache/` folder.

---

## Useful Docker Commands on Mac

- View live worldserver logs: `docker compose logs -f ac-worldserver`
- Restart worldserver: `docker compose restart ac-worldserver`
- Stop all containers: `docker compose down`
