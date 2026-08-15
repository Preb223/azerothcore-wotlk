# 🛠️ Useful AzerothCore GM Commands & Server Content Reference

This document serves as a comprehensive reference guide for essential AzerothCore (WotLK 3.3.5a) GM commands, server administration tools, and custom server content.

> 💡 **Note**: Commands can be executed in the **Worldserver Console** (without a leading `.`) or **in-game in chat** (with a leading `.`).

---

## ⚙️ 1. Server Administration & Account Management

### 🖥️ 1.1 Server Controls
| Command | Description |
| :--- | :--- |
| ℹ️ `.server info` | Displays server version and online player count. |
| 🔄 `.server restart <delay>` | Restarts the server after `<delay>` seconds (e.g., `.server restart 60`). |
| 🛑 `.server shutdown <delay>` | Shuts down the server after `<delay>` seconds. |
| ⚙️ `.reload config` | Reloads `worldserver.conf` without restarting the server. |
| 📜 `.reload command` | Reloads GM command permissions and table updates. |

### 👤 1.2 Account Management
| Command | Description |
| :--- | :--- |
| ➕ `account create <user> <pass>` | Creates a new account with the specified credentials. |
| 🎮 `account set addon <user> 2` | Sets expansion level to WotLK (0 = Classic, 1 = TBC, 2 = WotLK). |
| 👑 `account set gmlevel <user> <lvl> -1` | Sets GM rank (0 = Player, 1 = Mod, 2 = GM, 3 = Admin) across all realms (`-1`). |
| 🔑 `account set password <user> <pass> <pass>` | Resets an account password. |
| ❌ `account delete <user>` | Deletes an account and all of its characters. |

### 🔨 1.3 Moderation & Player Control
| Command | Description |
| :--- | :--- |
| 👢 `.kick <playername> [reason]` | Kicks a player from the server. |
| 🔇 `.mute <playername> <mins> [reason]` | Mutes chat for all characters on the player's account. |
| 🔊 `.unmute <playername>` | Removes chat mute from a player. |
| ⛔ `.ban account <account> <dur> <reason>` | Bans an account (`4d20h` or `-1d` for permanent ban). |
| ✅ `.unban account <account>` | Unbans an account. |

---

## 🛠️ 2. GM Utilities, Movement & Cheats

### 👻 2.1 GM State & Visibility
| Command | Description |
| :--- | :--- |
| 🛡️ `.gm on` / `.gm off` | Enables or disables GM mode badge/state. |
| 👁️ `.gm visible on` / `off` | Makes your GM character visible or invisible to normal players. |
| 🕊️ `.gm fly on` / `off` | Enables 3D flight mode for your GM character. |

### 💖 2.2 Healing & Resource Restoration
| Command | Description |
| :--- | :--- |
| ✨ `.revive` | Instantly heals to 100% HP/Mana (and revives if dead) for target or self. |
| ❤️ `.modify hp <amount>` | Sets current Health Points for selected target or self (e.g., `.modify hp 100000`). |
| 💧 `.modify mana <amount>` | Sets current Mana Points for target or self. |
| 😡 `.modify rage <amount>` | Sets current Rage for target or self. |
| ⚡ `.modify energy <amount>` | Sets current Energy for target or self. |
| 💀 `.modify runicpower <amount>` | Sets current Runic Power for target or self. |

### 🛡️ 2.3 Invulnerability & Cooldowns
| Command | Description |
| :--- | :--- |
| 🦸 `.cheat god on` / `off` | Toggles invulnerability (God mode). |
| ⏳ `.cheat cooldown on` / `off` | Disables spell cooldowns for your character. |
| ⏱️ `.cheat casttime on` / `off` | Removes cast times for all spells. |
| 🔄 `.cooldown` | Resets active spell cooldowns immediately. |

### 🚀 2.4 Teleportation & Player Movement
| Command | Description |
| :--- | :--- |
| 🔮 `.teleport name <player> <loc>` | Teleports a specified player to a named location (e.g., `.teleport name Player2 dalaran`). |
| 🏠 `.teleport name <player> $home` | Teleports a specified player to their set Hearthstone location. |
| 🖐️ `.summon <playername>` | Teleports a player directly to your current GM position. |
| 🌌 `.appear <playername>` | Teleports your GM character directly to the specified player's location. |
| 👥 `.teleport group <location>` | Teleports your target player and their entire party to a specified location. |
| 🌀 `.teleport <location>` | Teleports yourself to a specified location (e.g., `.teleport orgrimmar`). |
| 🔍 `.lookup teleport <searchterm>` | Searches for predefined teleport location names matching the search term. |
| 🆘 `.unstuck <playername> [inn/gy/start]` | Teleports a stuck player to an inn, graveyard, or starting zone. |

---

## 📦 3. Spawning NPCs, Vendors & Game Objects

### 👩‍💼 3.1 Special Item Vendor NPC (Gabriella, The Assistant)
To spawn your server's special item vendor NPC (who sells all custom heirlooms, weapons, glyphs, gems, enchants, bags, and utilities):

```text
.npc add 9000000
```
* 👩 **NPC Name**: Gabriella, The Assistant
* 🔢 **NPC Entry ID**: `9000000`
* 🛍️ **Features**: Interactive gossip menu for custom heirlooms, tier sets, legendaries, glyphs, gems, elixirs, food, enchants, containers, flight paths, professions, and instance resets.

### 🏺 3.2 Standard World Spawns
| Command | Description |
| :--- | :--- |
| 🔎 `.lookup creature <name>` | Searches the database for NPC template IDs. |
| 🧞 `.npc add <creatureid>` | Spawns an NPC at your current location. |
| 🗑️ `.npc delete` | Deletes the targeted NPC permanently from the database. |
| 🚪 `.lookup gobject <name>` | Searches for Game Object IDs (doors, chests, portals, etc.). |
| 📦 `.gobject add <objectid>` | Spawns a game object at your current location. |
| ❌ `.gobject delete <guid>` | Deletes the targeted game object. |

---

## 📈 4. Gameplay Progression & Item Commands

| Command | Description |
| :--- | :--- |
| 🎁 `.additem <itemid> [count]` | Adds the specified item to your inventory or selected player. |
| 📦 `.additem set #itemsetid` | Adds 1 of each item in the specified item set ID to inventory. |
| 🔍 `.lookup item <name>` | Searches the database for item IDs by name. |
| 📜 `.lookup itemset <name>` | Searches for item set IDs by name (e.g., `.lookup itemset Lightsworn`). |
| ⬆️ `.character level <player> <lvl>` | Sets a player's character level (e.g., `.character level Player2 80`). |
| 📖 `.learn <spellid>` | Teaches a spell to your target or self. |
| 🎓 `.learn all my class` | Learns all class spells and talents for your character's class. |
| 🎯 `.maxskill` | Maxes out weapon and profession skills for the targeted player. |
| 🛠️ `.gear repair` | Repairs all equipped gear for the selected player. |
| 💰 `.modify money <amount>` | Adds/removes copper/gold (e.g., `.modify money 1000000` for 100 gold). |

---

## 👑 5. Master Heirloom Catalog (Default WotLK & Custom Server Heirlooms)

> 💡 **Note**: Standard heirlooms are individual items (use `.additem <itemid>`), while Custom Heirloom Tier Sets can be spawned as full sets using `.additem set <SetID>`.

### 📜 5.1 Standard WotLK Leveling Heirlooms

#### 🛡️ Chests (+10% XP)
* 🧥 **Leather (Agility)**: `.additem 48685` *(Stained Shadowcraft Tunic)*
* 🛡️ **Plate (Physical)**: `.additem 48683` *(Polished Breastplate of Valor)*
* ⛓️ **Mail (Physical)**: `.additem 48687` *(Champion's Deathdealer Breastplate)*
* 🥋 **Cloth (Spell)**: `.additem 48689` *(Tattered Dreadmist Robe)*
* ⚡ **Mail (Spell)**: `.additem 48691` *(Mystical Vest of Elements)*

#### ⚔️ Shoulders (+10% XP)
* 🧥 **Leather (Agility)**: `.additem 42952` *(Stained Shadowcraft Spaulders)*
* 🛡️ **Plate (Physical)**: `.additem 42949` *(Polished Spaulders of Valor)*
* ⛓️ **Mail (Physical)**: `.additem 42950` *(Champion's Herod's Shoulder)*
* 🥋 **Cloth (Spell)**: `.additem 42951` *(Tattered Dreadmist Mantle)*
* ✨ **Plate (Holy)**: `.additem 44100` *(Pristine Lightforge Spaulders)*
* 🛡️ **Plate (Tank)**: `.additem 44099` *(Strengthened Stockade Pauldrons)*

#### 🗡️ Weapons & Accessories
* 🪓 **2H Axe**: `.additem 42943` *(Bloodied Arcanite Reaper)*
* ⚔️ **1H Sword**: `.additem 42944` *(Venerable Dal'Rend's Sacred Charge)*
* 🏹 **Ranged Bow**: `.additem 42946` *(Charmed Ancient Bone Bow)*
* 🪄 **Spell Staff**: `.additem 42947` *(Dignified Headmaster's Charge)*
* ⚡ **Trinket (Haste)**: `.additem 42991` *(Swift Hand of Justice)*
* 💍 **Ring (+5% XP)**: `.additem 50255` *(DreadPirate Ring)*

---

### 💎 5.2 Custom Server XP Accessories & Bags

#### 🧥 Cloaks (+5% XP)
* 🔮 **Caster**: `.additem 20145` *(Ancient Bloodmoon Cloak)*
* 🏃 **Agility**: `.additem 20218` *(Inherited Cape of the Black Baron)*
* 🏋️ **Strength**: `.additem 20219` *(Ripped Sandstorm Cloak)*
* 🛡️ **Tank**: `.additem 20241` *(Worn Stoneskin Gargoyle Cape)*

#### 📿 Necklaces (+10% XP)
* 🔮 **Caster**: `.additem 90103` *(Pendant of Arcane Mastery)*
* 🛡️ **Tank**: `.additem 90104` *(Pendant of the Iron Wall)*
* ⚔️ **Melee**: `.additem 90105` *(Pendant of Swift Strikes)*

#### 💍 Rings (+5% XP)
* 🔮 **Caster**: `.additem 90106` *(Signet of Arcane Authority)*
* 🛡️ **Tank**: `.additem 90107` *(Signet of the Bastion)*
* ⚔️ **Melee**: `.additem 90108` *(Signet of Lethal Precision)*

#### 🎒 Custom Heirloom Bags & Quivers
* 🎒 **Bag of Infinite Holdings** (36-Slot Heirloom Bag): `.additem 90109`
  * 📜 *Description*: "A gift from the Titans themselves." (Bind to Account, 36 slots).
* 🏹 **Quiver of the Infinite Hunt** (36-Slot Universal Quiver & Ammo Pouch): `.additem 90111`
  * 📜 *Description*: "A universal munition vault for arrows and bullets alike." (Holds Arrows + Bullets, +15% Ranged Speed, +2% Crit, +5% Movement Speed, +5% XP).
* 🏹 **Quiver of the Windrunner** (36-Slot Arrow Quiver): `.additem 90112`
  * 📜 *Description*: "Stitched from sun-gilded leather and blessed by Sylvanas." (Holds Arrows, +15% Ranged Speed, +5% XP).
* 💣 **Ammo Pouch of the Dragonflight** (36-Slot Bullet Pouch): `.additem 90113`
  * 📜 *Description*: "Forged from red dragonscales to keep shot fiery and true." (Holds Bullets, +15% Ranged Speed, +5% XP).

---

### 🛡️ 5.3 Custom Classic Heirloom Armor Sets (T0 / T0.5 8-Piece Scaling)
Use **`.additem <ID>`** to spawn individual custom heirloom armor pieces:

| Set Name / Class | 🪖 Head | 🛡️ Shoulders | 🥋 Chest | 🥋 Waist | 🦵 Legs | 🦶 Feet | 🧤 Wrists | 🥊 Hands |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🛡️ **Tarnished Valor** (Plate) | `20138` | `42949` | `48685` | `20142` | `20139` | `20039` | `20135` | `20137` |
| ✝️ **Polished Lightforge** (<span style="color:#F48CBA; font-weight:bold;">Paladin</span>) | `20246` | `44100` | `48685` | `20213` | `20247` | `20141` | `20239` | `20242` |
| ⚔️ **Burnished Might** (<span style="color:#C69E6D; font-weight:bold;">Warrior</span>) | `20286` | `42949` | `48685` | `20252` | `20287` | `20251` | `20281` | `20284` |
| 🗡️ **Stained Shadowcraft** (<span style="color:#FFF468; font-weight:bold;">Rogue</span>) | `20270` | `42952` | `48689` | `20267` | `20272` | `20268` | `20269` | `20271` |
| 🐾 **Preened Wildheart** (<span style="color:#FF7C0A; font-weight:bold;">Druid</span>) | `20301` | `42984` | `48687` | `20216` | `20306` | `20255` | `20300` | `20304` |
| ⚡ **Mystical Elements** (<span style="color:#0070DD; font-weight:bold;">Shaman</span>) | `20773` | `42951` | `48683` | `20778` | `20779` | `20780` | `20776` | `20777` |
| 🔮 **Tattered Dreadmist** (Cloth) | `24563` | `42985` | `48691` | `24561` | `25800` | `24565` | `24572` | `24566` |

---

### ✨ 5.4 Custom Scaling Heirloom Tier Sets (T2 & T5 Sets)
Spawn full custom scaling heirloom tier sets at once using **`.additem set <SetID>`**:

| Class | Heirloom Set Name | Set ID | Item ID Range | `.additem set` Command |
| :--- | :--- | :---: | :---: | :--- |
| <span style="color:#F0F0F0; font-weight:bold;">Priest</span> | Transcendence Raiment | `995` | `90050–90057` | `.additem set 995` |
| <span style="color:#3FC7EB; font-weight:bold;">Mage</span> | Netherwind Regalia | `996` | `90040–90047` | `.additem set 996` |
| <span style="color:#FFF468; font-weight:bold;">Rogue</span> | Bloodfang Armor | `997` | `90030–90037` | `.additem set 997` |
| <span style="color:#8788EE; font-weight:bold;">Warlock</span> | Nemesis Raiment | `998` | `90010–90017` | `.additem set 998` |
| <span style="color:#F48CBA; font-weight:bold;">Paladin</span> | Judgement Armor | `999` | `90020–90027` | `.additem set 999` |
| <span style="color:#FF7C0A; font-weight:bold;">Druid</span> | Stormrage Raiment | `1000` | `90060–90067` | `.additem set 1000` |
| <span style="color:#0070DD; font-weight:bold;">Shaman</span> | The Ten Storms | `1001` | `90070–90077` | `.additem set 1001` |
| <span style="color:#AAD372; font-weight:bold;">Hunter</span> | Dragonstalker Armor | `1002` | `90080–90087` | `.additem set 1002` |
| <span style="color:#C69E6D; font-weight:bold;">Warrior</span> | Battlegear of Wrath | `1003` | `90090–90097` | `.additem set 1003` |
| <span style="color:#8788EE; font-weight:bold;">Warlock</span> | Corruptor Raiment (T5) | `1004` | `90098–90102` | `.additem set 1004` |

---

### 🗡️ 5.5 Custom Scaling Heirloom Weapons & Legendaries

| Item Name | Item ID | Item Type | Command | Special Effects / Procs |
| :--- | :---: | :--- | :--- | :--- |
| ❄️ **Frostmourne** | `90000` | 2H Sword | `.additem 90000` | Lifesteal & Chilled procs |
| ☀️ **Ashbringer** | `90001` | 2H Sword | `.additem 90001` | Holy Bolt heal proc |
| 💀 **Corrupted Ashbringer** | `90002` | 2H Sword | `.additem 90002` | Shadow Lifesteal proc |
| ⚡ **Thunderfury, Blessed Blade of the Windseeker** | `90003` | 1H Sword | `.additem 90003` | Custom scaling |
| 🔥 **Skullflame Shield** | `90004` | Shield | `.additem 90004` | Custom scaling |
| 🦅 **Atiesh, Greatstaff of the Guardian** | `90005` | Staff | `.additem 90005` | Karazhan Portal |
| 🗡️ **Barman Shanker** | `90110` | 1H Dagger | `.additem 90110` | Custom scaling heirloom |

---

## 🏰 6. Non-Heirloom Standard Armor Tier Sets

### 💀 6.1 Classic Dungeon Sets (Tier 0 & Tier 0.5)

| Class | Tier 0 Set Name | Set ID | Tier 0.5 Set Name | Set ID |
| :--- | :--- | :---: | :--- | :---: |
| <span style="color:#FFF468; font-weight:bold;">Rogue</span> | Shadowcraft Armor | `184` | Darkmantle Armor | `512` |
| <span style="color:#C69E6D; font-weight:bold;">Warrior</span> | Battlegear of Valor | `192` | Battlegear of Heroism | `520` |
| <span style="color:#F48CBA; font-weight:bold;">Paladin</span> | Lightforge Armor | `191` | Soulforge Armor | `518` |
| <span style="color:#AAD372; font-weight:bold;">Hunter</span> | Beaststalker Armor | `186` | Beastmaster Armor | `511` |
| <span style="color:#FF7C0A; font-weight:bold;">Druid</span> | Wildheart Raiment | `185` | Feralheart Raiment | `513` |
| <span style="color:#3FC7EB; font-weight:bold;">Mage</span> | Magister's Regalia | `187` | Sorcerer's Regalia | `514` |
| <span style="color:#F0F0F0; font-weight:bold;">Priest</span> | Devout Vestments | `188` | Vestments of the Virtuous | `515` |
| <span style="color:#8788EE; font-weight:bold;">Warlock</span> | Dreadmist Raiment | `189` | Deathmist Raiment | `516` |
| <span style="color:#0070DD; font-weight:bold;">Shaman</span> | The Elements | `190` | The Five Thunders | `517` |

### 🐉 6.2 Classic Raid Sets (Tier 1, Tier 2, Tier 2.5, Tier 3)
Spawn standard raid sets using **`.additem set <SetID>`**:

| Class | Tier 1 (MC) | ID | Tier 2 (BWL) | ID | Tier 2.5 (AQ40) | ID | Tier 3 (Naxx 40) | ID |
| :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| <span style="color:#FF7C0A; font-weight:bold;">Druid</span> | Cenarion Raiment | `205` | Stormrage Raiment | `214` | Genesis Raiment | `492` | Dreamwalker Raiment | `525` |
| <span style="color:#AAD372; font-weight:bold;">Hunter</span> | Giantstalker Armor | `206` | Dragonstalker Armor | `215` | Striker's Garb | `493` | Cryptstalker Armor | `530` |
| <span style="color:#3FC7EB; font-weight:bold;">Mage</span> | Arcanist Regalia | `201` | Netherwind Regalia | `210` | Enigma Vestments | `494` | Frostfire Regalia | `526` |
| <span style="color:#F48CBA; font-weight:bold;">Paladin</span> | Lawbringer Armor | `208` | Judgement Armor | `217` | Avenger's Attire | `495` | Redemption Armor | `528` |
| <span style="color:#F0F0F0; font-weight:bold;">Priest</span> | Vestments of Prophecy | `202` | Vestments of Transcendence | `211` | Garb of the Oracle | `496` | Vestments of Faith | `527` |
| <span style="color:#FFF468; font-weight:bold;">Rogue</span> | Nightslayer Armor | `204` | Bloodfang Armor | `213` | Deathdealer's Embrace | `497` | Bonescythe Armor | `524` |
| <span style="color:#0070DD; font-weight:bold;">Shaman</span> | Earthfury Vestments | `207` | The Ten Storms | `216` | Stormcaller's Garb | `498` | The Earthshatterer | `529` |
| <span style="color:#8788EE; font-weight:bold;">Warlock</span> | Felheart Raiment | `203` | Nemesis Raiment | `212` | Doomcaller's Attire | `499` | Plagueheart Raiment | `523` |
| <span style="color:#C69E6D; font-weight:bold;">Warrior</span> | Battlegear of Might | `209` | Battlegear of Wrath | `218` | Conqueror's Battlegear | `500` | Dreadnaught's Battlegear | `521` |


### 🎯 5.3 Custom Heirloom Ranged Weapons, Relics & Cosmetic Gear

#### 🎯 Throwing, Guns & Crossbows
* 🎯 **Shadowblade Throwing Star** (Heirloom Throwing Weapon): `.additem 90114`
  * 📜 *Description*: "An infinite shadowblade forged for stealthy precision." (Infinite ammo, Agi/Sta/AP/Crit, +5% XP).
* 🔫 **Dwarven Dragon-Rifle** (Heirloom Gun): `.additem 90115`
  * 📜 *Description*: "Engineered in Ironforge to unleash dragonfire." (Agi/Sta/AP/Crit, +10% XP).
* 🏹 **Arbalest of the Windrunner** (Heirloom Crossbow): `.additem 90116`
  * 📜 *Description*: "Crafted for elven rangers with deadly accuracy." (Agi/Sta/AP/ArPen, +10% XP).
* 🪄 **Baton of Nether Energies** (Heirloom Wand): `.additem 90117`
  * 📜 *Description*: "Channels raw arcane energy without draining mana." (Int/Sta/SP/Crit, +5% XP).

#### ✝️ Class Relics
* 📜 **Libram of Divine Purpose** (Paladin Relic): `.additem 90118`
* 🗿 **Totem of Elemental Fury** (Shaman Relic): `.additem 90119`
* 🐾 **Idol of the Wild Spirit** (Druid Relic): `.additem 90120`
* 💀 **Sigil of the Frozen Throne** (Death Knight Relic): `.additem 90121`

#### 🎽 XP Cosmetics & Shirts
* 🏷️ **Tabard of the Veteran Adventurer** (Heirloom Tabard): `.additem 90122` (+10% XP).
* 👕 **Shirt of the Hero** (Heirloom Shirt): `.additem 90123` (+5% Movement Speed & +5% XP).