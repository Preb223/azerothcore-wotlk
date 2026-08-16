UPDATE ai_playerbot_texts SET 
  text = REPLACE(REPLACE(REPLACE(text, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc1 = REPLACE(REPLACE(REPLACE(text_loc1, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc2 = REPLACE(REPLACE(REPLACE(text_loc2, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc3 = REPLACE(REPLACE(REPLACE(text_loc3, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc4 = REPLACE(REPLACE(REPLACE(text_loc4, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc5 = REPLACE(REPLACE(REPLACE(text_loc5, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc6 = REPLACE(REPLACE(REPLACE(text_loc6, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc7 = REPLACE(REPLACE(REPLACE(text_loc7, 'â€™', '\''), '’', '\''), '‘', '\''),
  text_loc8 = REPLACE(REPLACE(REPLACE(text_loc8, 'â€™', '\''), '’', '\''), '‘', '\'');

UPDATE playerbots_speech SET 
  text = REPLACE(REPLACE(REPLACE(text, 'â€™', '\''), '’', '\''), '‘', '\'');
