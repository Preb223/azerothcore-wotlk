#include "mod_assistant.h"

// ---------------------------------------------------------------------------
// Damage scaling for heirloom legendary weapons
// ---------------------------------------------------------------------------
class mod_assistant_player_heirloom_weapon_scaling : public PlayerScript
{
public:
    mod_assistant_player_heirloom_weapon_scaling() : PlayerScript("mod_assistant_player_heirloom_weapon_scaling") { }

    void OnPlayerApplyWeaponDamage(Player* player, uint8 /*slot*/, ItemTemplate const* proto, float& minDamage, float& maxDamage, uint8 damageIndex) override
    {
        // Scale damage for our custom heirloom legendary weapons
        if (damageIndex != 0)
            return;

        // Heirloom Frostmourne (90000), Ashbringer (90001), Corrupted Ashbringer (90002)
        // Also original Ashbringer IDs for backwards compatibility
        if (proto->ItemId != 90000 && proto->ItemId != 90001 && proto->ItemId != 90002 &&
            proto->ItemId != 22958 && proto->ItemId != 20504)
            return;

        uint32 level = player->GetLevel();
        if (level > 80)
            level = 80;

        if (ScalingStatValuesEntry const* ssv = sScalingStatValuesStore.LookupEntry(level))
        {
            float baseDPS = ssv->getDPSMod(16392);
            if (baseDPS > 0.0f)
            {
                float targetDPS = baseDPS * (90.0f / 91.0f);
                float average = targetDPS * proto->Delay / 1000.0f;

                minDamage = 0.7f * average;
                maxDamage = 1.3f * average;
            }
        }
    }
};

// ---------------------------------------------------------------------------
// Scaling proc handler for heirloom legendary weapons
// Uses UnitScript::OnDamage to intercept melee hits and fire scaled procs
// Handles: Ashbringer heal-on-hit and Frostmourne/Corrupted Ashbringer life steal
// ---------------------------------------------------------------------------
class mod_assistant_heirloom_legendary_procs : public UnitScript
{
public:
    mod_assistant_heirloom_legendary_procs() : UnitScript("mod_assistant_heirloom_legendary_procs") { }

    void OnDamage(Unit* attacker, Unit* victim, uint32& /*damage*/) override
    {
        if (!attacker || !victim || !attacker->IsPlayer() || !victim->IsAlive())
            return;

        Player* player = attacker->ToPlayer();
        if (!player)
            return;

        // Check if player has one of our heirloom legendary weapons equipped
        Item* mainHand = player->GetItemByPos(INVENTORY_SLOT_BAG_0, EQUIPMENT_SLOT_MAINHAND);
        if (!mainHand)
            return;

        uint32 itemId = mainHand->GetEntry();
        uint32 level = player->GetLevel();
        if (level > 80) level = 80;

        // --- Ashbringer (90001): Heal on hit ---
        if (itemId == 90001)
        {
            // ~5% proc chance per hit
            if (urand(0, 100) < 5)
            {
                // Scale heal: level * 5 (e.g., level 10 = 50 HP, level 40 = 200 HP, level 80 = 400 HP)
                int32 healAmount = level * 5;
                player->CastCustomSpell(player, 25423, &healAmount, nullptr, nullptr, true, mainHand);
            }
        }
        // --- Frostmourne (90000) or Corrupted Ashbringer (90002): Life steal ---
        else if (itemId == 90000 || itemId == 90002)
        {
            // ~8% proc chance per hit
            if (urand(0, 100) < 8)
            {
                // Scale drain: level * 4 (e.g., level 10 = 40 dmg+heal, level 40 = 160, level 80 = 320)
                int32 drainAmount = level * 4;
                player->CastCustomSpell(victim, 17484, &drainAmount, nullptr, nullptr, true, mainHand);
            }
        }
    }
};

// ---------------------------------------------------------------------------
// Module registration
// ---------------------------------------------------------------------------
Assistant::Assistant() : CreatureScript("npc_assistant"), WorldScript("AssistantWorldScript") {}

void Addmod_assistantScripts()
{
    new Assistant();
    new mod_assistant_player_heirloom_weapon_scaling();
    new mod_assistant_heirloom_legendary_procs();
}
