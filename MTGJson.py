import json

from MTGDatabase import MTGDatabase
from urllib.request import urlopen

database = MTGDatabase()

class MtgJson():
    def __init__(self):
        self.bulk_json_url = None

    def get_latest_json_url(self):
        bulk_data_update_url = "https://api.scryfall.com/bulk-data/"
        with urlopen(bulk_data_update_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            for dictionary in data["data"]:
                if dictionary["name"] == "Default Cards":
                    self.bulk_json_url = dictionary["download_uri"]
                    return self.bulk_json_url

    def url_and_db_manager(self):
        with open("json_url.txt", "a+") as text_file:
            text_file.seek(0)
            lines = text_file.readlines()
            if lines == []:
                text_file.write(f"{self.bulk_json_url}\n")
                print("No previous pricing URL found.  The latest URL has been recorded.")
                database.json_length(self.generator_from_json())
                database.make_db(self.generator_from_json())
            elif lines != []:
                last_line = lines[-1].rstrip()
                ### THE CODE COMMENTED OUT BELOW IS IF WE NEED TO MOVE TO 2-A-DAY PRICING
                # q = last_line.split("-")[-1].rsplit(".")[0].rsplit(str(database.todays_date))[-1]
                # j = self.bulk_json_url.split("-")[-1].rsplit(".")[0].rsplit(str(database.todays_date))[-1]
                if (last_line == self.bulk_json_url) or (str(database.todays_date) in last_line): #or (q == j): commented out code is for 2-a-day pricing
                    print("Same pricing as last time.  Check again tomorrow after 4:08am/pm CST.")
                elif last_line != self.bulk_json_url:
                    ### THE CODE COMMENTED OUT BELOW IS IF WE NEED TO MOVE TO 2-A-DAY PRICING
                    # if (str(database.todays_date) in last_line) and (q != j):
                    #     print("New same-day pricing found!")
                    text_file.write(f"{self.bulk_json_url}\n")
                    print("New pricing found!  The latest URL has been recorded.")
                    database.make_column()
                    database.update_price(self.generator_from_json())
                    database.add_card_to_db(self.generator_from_json())
                    database.convert_db_to_csv('MTGDatabase.db', 'ALLCARDS.csv')
                    
    def generator_from_json(self):
        with urlopen(f"{self.bulk_json_url}") as default_cards_response:
            default_cards_data = json.loads(default_cards_response.read().decode('utf-8'))
            for card_object in default_cards_data:
                if (card_object.get("tcgplayer_id") is not None) and (card_object["prices"]["usd"] is not None):
                    yield card_object.get('tcgplayer_id'), card_object["name"], card_object["set"], card_object["reserved"], card_object["prices"]["usd"]