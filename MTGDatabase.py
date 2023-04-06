import sqlite3
from datetime import datetime

class MTGDatabase(): 
    def __init__(self):
        self.todays_date = int(str(datetime.date(datetime.now())).replace("-",""))

        self.con = sqlite3.connect('MTGDatabase.db')
        with self.con:
            if int(str(datetime.time(datetime.now())).replace(":","").replace(".","")) < 160800000000:
                self.con.execute(f"""CREATE TABLE IF NOT EXISTS ALLCARDS (tcg_id INT, card_name TEXT, card_set TEXT, "{self.todays_date}" FLOAT);""")
            else:
                self.con.execute(f"""CREATE TABLE IF NOT EXISTS ALLCARDS (tcg_id INT, card_name TEXT, card_set TEXT, "{self.todays_date + 1}" FLOAT);""")
            
    def make_db(self, json):  
        print("Buckle Up:  ~ 10s until Database Generator go BRRRRRRRRR")
        sql = f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, "{self.todays_date}") values (?, ?, ?, ?)"""
        with self.con:
            for i in json:
                data = (i[3], i[0], i[1], i[2])
                print(data)
                self.con.executemany(sql, (data,))
                self.con.commit() 

    def make_column(self):
        with self.con:
            self.con.execute(f"""ALTER TABLE ALLCARDS ADD "{self.todays_date + 1}" FLOAT;""")

    def update_price(self, json):
        with self.con:
            for i in json:
                self.con.execute(f"""UPDATE ALLCARDS SET "{self.todays_date + 1}" = "{i[2]}" WHERE tcg_id = "{i[-1]}";""")

    def add_card_to_db(self, json):
        with self.con:
            for i in json:
                new_row = (i[3], i[0], i[1], i[2])
                print(new_row)
                self.con.execute(f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, "{self.todays_date + 1}") SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM ALLCARDS WHERE tcg_id = ?)""", new_row + (new_row[0],))
  
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
        
    def get_card_by_tcgID(self, tcg_search):  # Gathers card of a specific TCG ID # from the DB.
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
                print("No match found for that TCG ID #")
            return self.card_list_by_tcg # Returns either an empty list, or a dictionary of the card with that specific TCG ID#.           