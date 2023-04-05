from urllib.request import urlopen
import json

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

    def manage_url_text_file(self):
        with open("json_url.txt", "a+") as text_file:
            text_file.seek(0)
            lines = text_file.readlines()
            if lines == []:
                text_file.write(f"{self.bulk_json_url}\n")
                print("No previous pricing URL found.  The latest URL has been recorded.")
            elif lines != []:
                last_line = lines[-1].rstrip()
                if last_line == self.bulk_json_url:
                    print("Same pricing as last time.  Check again between 4 and 4:15pm CST.")
                elif last_line != self.bulk_json_url:
                    text_file.write(f"{self.bulk_json_url}\n")
                    print("New pricing found!  The latest URL has been recorded.")
                    
    def open_json(self):
        with urlopen(f"{self.bulk_json_url}") as default_cards_response:
            default_cards_data = json.loads(default_cards_response.read().decode('utf-8'))
            for card_object in default_cards_data:
                if (card_object.get("tcgplayer_id") is not None) and (card_object["prices"]["usd"] is not None):
                    yield card_object["name"], card_object["set_name"], card_object["prices"]["usd"], card_object.get('tcgplayer_id')