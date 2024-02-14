import MTGJson
import MTGDatabase

the_json = MTGJson.MtgJson()
database = MTGDatabase.MTGDatabase()

the_json.get_latest_json_url()
the_json.url_and_db_manager()

# database.get_card_by_tcgID("12684")
# database.get_card_by_name("Sol Ring")
# database.get_cards_in_set("mh2")

# TODO:

# Looking for low stock, high movement
# Prices and tracker
# -MTGstocks
#    -price increase (within +/- 5%) (Differentiate resere list cards.  Noted with an asterisk.  Might not be able to do @ goldfish)
#    -price decrease
#    -if possible highlight reserve list cards  
#    -all of cards $2 dollars and more
 
# (all sets from alpha to current no sealed products)
# -MTG goldfish
#    -price increase 
#    -price decrease 
#    -if possible highlight reserve list cards 
#    -all of cards $2 dollars and more
# (all sets from alpha to current no sealed products) 

#------------------------------------------------

# Inventory and card movement (near mint only)
# -TCGplayer
#    -Current stock of cards listed from above sites
#    -Card sales of 10 or more in 1 day
#    -have cards lowest price @ Near mint 
   
# -Card kingdom
#    -Current stock of cards listed from above sites
#    -have cards lowest price @ Near mint 

# FUTURE:
# - if possible, rarity of cards
# -if a card has less stock online, it'll stick out
# -make weekly card movements 40 sales or more in 7 day period, also 
  