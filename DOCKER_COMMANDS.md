# 🎮 AzerothCore WoW Server — Docker Commands & Operations

Quick reference guide for starting, stopping, managing, and connecting to your local AzerothCore World of Warcraft (3.3.5a) server on macOS.

---

## 🚀 1. Starting the Server

Before running the server, make sure **Docker Desktop** is running.

```bash
# Open terminal to azerothcore-wotlk directory
cd ~/Documents/GitHub/azerothcore-wotlk

# Launch Docker Desktop if not already open
open -a Docker

# Start all server containers in the background (from the repo root)
docker compose up -d
```

---

## 🛑 2. Stopping & Shutting Down

```bash
# Gracefully stop and shut down all containers (recommended)
docker compose down

# Temporarily pause/stop containers without removing them
docker compose stop
```

---

## 🔄 3. Restarting the Server

```bash
# Restart the worldserver (e.g. after updating SQL tables or configs)
docker compose restart ac-worldserver

# Restart all services (authserver, worldserver, database)
docker compose restart
```

---

## 📊 4. Status & Live Logs

```bash
# Check status and health of all containers
docker compose ps

# Follow live world server logs (Press Ctrl+C to exit)
docker compose logs -f ac-worldserver

# Follow live auth / login server logs
docker compose logs -f ac-authserver

# Follow database logs
docker compose logs -f ac-database
```

---

## 💻 5. Worldserver Console & GM Commands

### Interactive Console
```bash
# Attach directly to the worldserver console
docker attach ac-worldserver
```
> [!IMPORTANT]
> To detach from the console without stopping the server, press **`Ctrl + P` followed by `Ctrl + Q`**.

### One-Line Commands (Without Attaching)
```bash
# Create a new account
docker exec -i ac-worldserver worldserver -c "account create <username> <password>"

# Set account security level (3 = GM / Admin)
docker exec -i ac-worldserver worldserver -c "account set gmlevel <username> 3 -1"

# Reload item templates after making SQL changes
docker exec -i ac-worldserver worldserver -c "reload item_template"

# Send server broadcast announcement
docker exec -i ac-worldserver worldserver -c "announce Server restart in 5 minutes"
```

---

## 🔌 6. Client Connection Info

1. **Realmlist configuration**:
   Edit your WoW 3.3.5a Client `Data/enUS/realmlist.wtf` (or `Data/enGB/realmlist.wtf`):
   - **Playing on this Mac**: `set realmlist 127.0.0.1`
   - **Playing from another device on local Wi-Fi**: `set realmlist 192.168.1.214`

2. **Custom Patch**:
   - Copy `custom/patch-4.MPQ` into your WoW Client `Data/patch-4.MPQ`.
   - Delete your WoW Client `Cache/` folder whenever custom items or spells are updated.

---

## 🗄️ 7. Database Quick Commands

```bash
# Open interactive MySQL shell
docker exec -it ac-database mysql -uroot -ppassword acore_world

# Run a quick SQL query from terminal
echo "SELECT entry, name FROM item_template WHERE entry >= 90000;" | docker exec -i ac-database mysql -uroot -ppassword acore_world -t
```
