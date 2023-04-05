import sqlite3
import MTGJson

class MTGDatabase(): 
    def __init__(self):
        # self.card_list = []
        self.con = sqlite3.connect('MTGDatabase.db')
        with self.con:
            self.con.execute("""CREATE TABLE IF NOT EXISTS ALLCARDS (
                card_name TEXT,
                card_set TEXT,
                mkt_price FLOAT,
                tcg_id INT
            );
        """)
            
    def make_db(self, json):  
        sql = 'INSERT INTO ALLCARDS (card_name, card_set, mkt_price, tcg_id) values (?, ?, ?, ?)'
        with self.con:
            for i in json:
                data = (i[0], i[1], i[2], i[3])
                print(data)
                self.con.executemany(sql, (data,))
                self.con.commit() 

    def make_column(self):
        pass
  
    def get_card_by_name(self, player_search):  # Gathers all cards of a selected name from the DB. 
        with self.con:
            data = self.con.execute(f"""SELECT * FROM ALLCARDS WHERE card_name = ("{player_search}");""")
            self.card_list_by_name = data.fetchall()
            if self.card_list_by_name != []:  # If a card exists by that name in the DB:                          
                keys = ["card_name", "card_set", "mkt_price", "tcg_id"]
                dict_list = []
                for i in range(len(self.card_list_by_name)):
                    dict_list.append(dict(zip(keys, self.card_list_by_name[i])))
                for cards in dict_list:
                    print(cards)
            elif self.card_list_by_name == []:
                print("No exact match found for that name.  (Capitalization matters for now)")
            return self.card_list_by_name # Returns either an empty list, or a list of dictionaries, with each dictionary containing 1 version of the card with the specified name.   
        
    def get_card_by_tcgID(self, tcg_search):
        with self.con:
            data = self.con.execute(f"""SELECT * FROM ALLCARDS WHERE tcg_id = ("{tcg_search}");""")
            self.card_list_by_tcg= data.fetchall()
            if self.card_list_by_tcg != []:  # If a card exists by that TCG ID# in the DB:                            
                keys = ["card_name", "card_set", "mkt_price", "tcg_id"]
                dict_list = []
                for i in range(len(self.card_list_by_tcg)):
                    dict_list.append(dict(zip(keys, self.card_list_by_tcg[i])))
                for cards in dict_list:
                    print(cards)
            elif self.card_list_by_tcg == []:
                print("No exact match found for that name.  (Capitalization matters for now)")
            return self.card_list_by_tcg # Returns either an empty list, or a dictionary of the card with that specific TCG ID#.   
        