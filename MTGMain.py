import MTGJson
import MTGDatabase

the_json = MTGJson.MtgJson()
database = MTGDatabase.MTGDatabase()

the_json.get_latest_json_url()
the_json.url_and_db_manager()

# database.make_column() 
# database.update_price(the_json.generator_from_json())
# database.get_card_by_tcgID("2110")
# database.add_card_to_db(the_json.generator_from_json())


# TODO: https://www.tcgplayer.com/product/INSERT_TCG_PLAYER_ID_HERE?page=1














# Reserved List

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
# -make weekly card movements 40 or more in 7 day period 
  