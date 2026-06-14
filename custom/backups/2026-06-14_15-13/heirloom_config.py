# Configuration for new Heirloom sets
#
# SSD Templates (ScalingStatDistribution):
#   993: Leather hybrid - Agi/Sta/Int/Spirit (Rogue, Druid, Hunter)
#   994: Cloth caster - Int/Sta/Spirit/Spi/Hit (Warlock, Mage, Priest)
#   999: Plate hybrid - Str/Sta/Int/Def/SP (Paladin, Warrior)
#
# SSV (ScalingStatValue) is auto-calculated per slot by build_heirlooms.py

SETS = [
    {
        "name": "Stormrage",
        "class": "Druid",
        "original_itemset": 214,   # Stormrage Raiment
        "new_itemset": 1000,
        "scaling_template": 993,
        "vendor_id": 9000061,
        "original_items": {
            16900: 90060,  # Stormrage Cover (Head)
            16901: 90061,  # Stormrage Pauldrons (Shoulder)
            16897: 90062,  # Stormrage Chestguard (Chest)
            16904: 90063,  # Stormrage Belt (Waist)
            16903: 90064,  # Stormrage Legguards (Legs)
            16899: 90065,  # Stormrage Boots (Feet)
            16898: 90066,  # Stormrage Bracers (Wrist)
            16902: 90067,  # Stormrage Handguards (Hands)
        },
        "spell_clones": {
            21894: 99060,  # 3-piece bonus
            21872: 99061,  # 5-piece bonus
            21871: 99062,  # 8-piece bonus
        }
    },
    {
        "name": "Ten Storms",
        "class": "Shaman",
        "original_itemset": 216,   # The Ten Storms (CORRECTED from 215)
        "new_itemset": 1001,
        "scaling_template": 993,
        "vendor_id": 9000062,
        "original_items": {
            16947: 90070,  # Helmet of Ten Storms (Head)
            16945: 90071,  # Epaulets of Ten Storms (Shoulder)
            16950: 90072,  # Breastplate of Ten Storms (Chest)
            16944: 90073,  # Belt of Ten Storms (Waist)
            16946: 90074,  # Legplates of Ten Storms (Legs)
            16949: 90075,  # Greaves of Ten Storms (Feet)
            16943: 90076,  # Bracers of Ten Storms (Wrist)
            16948: 90077,  # Gauntlets of Ten Storms (Hands)
        },
        "spell_clones": {
            21899: 99070,  # 3-piece bonus (was 99063 with wrong spells)
            23570: 99071,  # 5-piece bonus
            23551: 99072,  # 8-piece bonus
        }
    },
    {
        "name": "Dragonstalker",
        "class": "Hunter",
        "original_itemset": 215,   # Dragonstalker Armor
        "new_itemset": 1002,
        "scaling_template": 993,   # Leather/mail hybrid Agi
        "vendor_id": 9000063,
        "original_items": {
            16939: 90080,  # Dragonstalker's Helm (Head)
            16937: 90081,  # Dragonstalker's Spaulders (Shoulder)
            16942: 90082,  # Dragonstalker's Breastplate (Chest)
            16936: 90083,  # Dragonstalker's Belt (Waist)
            16938: 90084,  # Dragonstalker's Legguards (Legs)
            16941: 90085,  # Dragonstalker's Greaves (Feet)
            16935: 90086,  # Dragonstalker's Bracers (Wrist)
            16940: 90087,  # Dragonstalker's Gauntlets (Hands)
        },
        "spell_clones": {
            21928: 99080,  # 5-piece bonus
            23578: 99081,  # 8-piece bonus
            23559: 99082,  # 3-piece bonus
        }
    },
    {
        "name": "Wrath",
        "class": "Warrior",
        "original_itemset": 218,   # Battlegear of Wrath
        "new_itemset": 1003,
        "scaling_template": 999,   # Plate Str/Sta
        "vendor_id": 9000064,
        "original_items": {
            16963: 90090,  # Helm of Wrath (Head)
            16961: 90091,  # Pauldrons of Wrath (Shoulder)
            16966: 90092,  # Breastplate of Wrath (Chest)
            16960: 90093,  # Waistband of Wrath (Waist)
            16962: 90094,  # Legplates of Wrath (Legs)
            16965: 90095,  # Sabatons of Wrath (Feet)
            16959: 90096,  # Bracelets of Wrath (Wrist)
            16964: 90097,  # Gauntlets of Wrath (Hands)
        },
        "spell_clones": {
            23563: 99090,  # 3-piece bonus
            21890: 99091,  # 5-piece bonus
            23548: 99092,  # 8-piece bonus
        }
    },
    {
        "name": "Corruptor",
        "class": "Warlock",
        "original_itemset": 646,   # Corruptor Raiment (T5)
        "new_itemset": 1004,
        "scaling_template": 994,   # Cloth caster (same as Nemesis)
        "vendor_id": 9000065,
        "original_items": {
            30212: 90098,  # Hood of the Corruptor (Head)
            30215: 90099,  # Mantle of the Corruptor (Shoulder)
            30214: 90100,  # Robe of the Corruptor (Chest)
            30213: 90101,  # Leggings of the Corruptor (Legs)
            30211: 90102,  # Gloves of the Corruptor (Hands)
        },
        "spell_clones": {
            37381: 99098,  # 2-piece bonus: Pet healed for 15% of damage dealt
            61992: 99099,  # 4-piece bonus: Corruption/Immolate +5% damage
        }
    },
]
