import sqlite3
import MTGJson

class MTGDatabase(): 
    def __init__(self):
        self.match_count = 0
        self.con = sqlite3.connect('MTGDatabase.db')
        with self.con:
            self.con.execute("""CREATE TABLE IF NOT EXISTS ALLCARDS (
                card_name TEXT,
                card_set TEXT,
                mkt_price FLOAT
            );
        """)
            
    def record_changes(self, card_name, card_set, mkt_price):  

        # NOTE: *******DO NOT FORGET TO ALSO CHANGE get_most_recent() WITH UPDATED KEYS YOU ADD/REMOVE FROM THE LIST ON THE LINE BELOW THIS ONE:*******

        sql = 'INSERT INTO ALLCARDS (card_name, card_set, mkt_price) values (?, ?, ?)'
        data = [(card_name, card_set, mkt_price)]
        try:
            with self.con:
                self.con.executemany(sql, data)
                self.con.commit()       
        except Exception:
            print("Oh shit")               
        else:
            print(f"Record has been recorded!")    