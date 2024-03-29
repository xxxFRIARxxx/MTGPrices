import sqlite3
import csv
import os
from datetime import datetime
from alive_progress import alive_bar

class MTGDatabase(): 
    def __init__(self):
        os.system('cls')
        self.count = None
        self.todays_date = int(str(datetime.date(datetime.now())).replace("-",""))

        self.con = sqlite3.connect('MTGDatabase.db')
        with self.con:
            self.con.execute(f"""CREATE TABLE IF NOT EXISTS ALLCARDS (tcg_id INT, card_name TEXT, card_set TEXT, is_reserved BOOL, "{self.todays_date}" FLOAT);""")
            ###THE CODE BELOW IS FOR A 2-A-DAY PRICE LOGGING###
            # if int(str(datetime.time(datetime.now())).replace(":","").replace(".","")) < 160800000000:
            #     self.con.execute(f"""CREATE TABLE IF NOT EXISTS ALLCARDS (tcg_id INT, card_name TEXT, card_set TEXT, is_reserved BOOL, "{self.todays_date}" FLOAT);""")
            # else:
            #     self.con.execute(f"""CREATE TABLE IF NOT EXISTS ALLCARDS (tcg_id INT, card_name TEXT, card_set TEXT, is_reserved BOOL, "{self.todays_date + 1}" FLOAT);""")

    def json_length(self,json):
        with alive_bar (title="Reticulating Splines...",spinner="waves",enrich_print=False, length=15, bar=None,unknown="wait",stats=False, elapsed=False, monitor=False, elapsed_end="Done!"):
            self.count = len(list(json))
            
    def make_db(self,json):  
        sql = f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date}") values (?, ?, ?, ?, ?)"""
        ###THE CODE BELOW IS FOR A 2-A-DAY PRICE LOGGING###
        # if int(str(datetime.time(datetime.now())).replace(":","").replace(".","")) < 160800000000:
        #     sql = f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date}") values (?, ?, ?, ?, ?)"""
        # else:
        #     sql = f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date + 1}") values (?, ?, ?, ?, ?)"""
        with self.con:
            with alive_bar(self.count, title="Building Database...",spinner="waves",enrich_print=False,stats=False,bar=False, monitor_end=False, elapsed_end="Done!") as bar:
                for i in (json):
                    data = (i[0], i[1], i[2], i[3], i[4])
                    bar()
                    self.con.executemany(sql, (data,))
                     
    def make_column(self):
        with self.con:
            self.con.execute(f"""ALTER TABLE ALLCARDS ADD "{self.todays_date}" FLOAT;""")
            ###THE CODE BELOW IS FOR A 2-A-DAY PRICE LOGGING###
            # if int(str(datetime.time(datetime.now())).replace(":","").replace(".","")) < 160800000000:
            #     self.con.execute(f"""ALTER TABLE ALLCARDS ADD "{self.todays_date}" FLOAT;""")
            # else:
            #     self.con.execute(f"""ALTER TABLE ALLCARDS ADD "{self.todays_date + 1}" FLOAT;""")

    def update_price(self, json): # TODO:  Maybe "insert" instead of "update" for speed?
        with self.con:
            with alive_bar(title="Updating pricing...", spinner="waves", bar=False, enrich_print=False, monitor_end=False, stats_end=False, elapsed_end="Done!") as bar:
                for i in json:
                    data = ((i[-1], i[0]),)
                    bar()
                    self.con.executemany(f"""UPDATE ALLCARDS SET "{self.todays_date}" = ? WHERE tcg_id = ? """, data)
                    ###THE CODE BELOW IS FOR A 2-A-DAY PRICE LOGGING###
                    #self.con.executemany(f"""UPDATE ALLCARDS SET "{self.todays_date + 1}" = ? WHERE tcg_id = ? """, data)

    def add_card_to_db(self, json): # TODO:  Look at this again
        with self.con:
            with alive_bar(title="Adding cards to DB...", spinner="waves", bar=False, enrich_print=False) as bar:
                for i in json:
                    new_row = (i[0], i[1], i[2], i[3], i[4])
                    # data = ((item,) for item in new_row)
                    data = (new_row + (new_row[0],),)
                    bar()
                    self.con.executemany(f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date}") SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM ALLCARDS WHERE tcg_id = ?)""", data)
                    ###THE CODE BELOW IS FOR A 2-A-DAY PRICE LOGGING - TOP LINE ONLY, NOT BOTH###
                    #self.con.executemany(f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date + 1}") SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM ALLCARDS WHERE tcg_id = ?)""", data)
                    # self.con.execute(f"""INSERT INTO ALLCARDS (tcg_id, card_name, card_set, is_reserved, "{self.todays_date + 1}") SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM ALLCARDS WHERE tcg_id = ?)""", new_row + (new_row[0],))
  
    def get_card_by_name(self, player_search):  # Gathers all cards of a selected name from the DB. 
        with self.con:
            data = self.con.execute(f"""SELECT * FROM ALLCARDS WHERE card_name = ("{player_search}");""")
            self.card_list_by_name = data.fetchall()
            if self.card_list_by_name != []:  # If a card exists by that name in the DB:                          
                keys = ["tcg_id", "card_name", "card_set", "is_reserved","mkt_price"]
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
                keys = ["tcg_id", "card_name", "card_set", "is_reserved","mkt_price"]
                dict_list = []
                for i in range(len(self.card_list_by_tcg)):
                    dict_list.append(dict(zip(keys, self.card_list_by_tcg[i])))
                for cards in dict_list:
                    print(cards)
            elif self.card_list_by_tcg == []:
                print("No match found for that TCG ID #")
            return self.card_list_by_tcg # Returns either an empty list, or a dictionary of the card with that specific TCG ID#.           
    
    def get_cards_in_set(self, set_search):  # Gathers the entire set (from abbreviation) from the DB.
        with self.con:
            data = self.con.execute(f"""SELECT * FROM ALLCARDS WHERE card_set = ("{set_search}");""")
            self.card_list_by_set= data.fetchall()
            if self.card_list_by_set != []:  # If a card exists by that set abbreviation in the DB:                            
                keys = ["tcg_id", "card_name", "card_set", "is_reserved","mkt_price"]
                dict_list = []
                for i in range(len(self.card_list_by_set)):
                    dict_list.append(dict(zip(keys, self.card_list_by_set[i])))
                for cards in dict_list:
                    print(cards)
            elif self.card_list_by_set == []:
                print("No match found for that set #")
            return self.card_list_by_set # Returns either an empty list, or a dictionary of the cards in a specific set. 
    
    def convert_db_to_csv(self, db_filename, csv_filename):
        # Connect to the SQLite database
        self.con = sqlite3.connect(db_filename)
        with self.con:
            data = self.con.execute(f"SELECT * FROM ALLCARDS")
            rows = data.fetchall()
            column_names = [desc[0] for desc in data.description]
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(column_names)
            csv_writer.writerows(rows)
        print(f"CSV file saved as {csv_filename}")
    