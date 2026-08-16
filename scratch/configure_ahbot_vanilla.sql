-- Update minitems and maxitems to 5000 per AH
UPDATE mod_auctionhousebot SET 
  minitems = 5000, 
  maxitems = 5000, 
  maxstackwhite = 20, 
  maxstackgrey = 20, 
  maxstackgreen = 5, 
  maxstackblue = 5, 
  maxstackpurple = 5;

-- Truncate existing disabled items
TRUNCATE mod_auctionhousebot_disabled_items;

-- Disable all TBC and WotLK items (Expansion > 0 OR RequiredLevel > 60)
INSERT INTO mod_auctionhousebot_disabled_items (item)
SELECT entry FROM item_template WHERE Expansion > 0 OR RequiredLevel > 60;
