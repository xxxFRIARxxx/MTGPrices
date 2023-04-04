from urllib.request import urlopen
import json

class MtgJson():
    def __init__(self):
        self.bulk_json_url = None
        self.outcome = 0
        self.old_balance = 0

    def get_latest_json_url(self): 
        bulk_data_update_url = "https://api.scryfall.com/bulk-data/"
        with urlopen(bulk_data_update_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            for dictionary in data["data"]:
                if dictionary["name"] == "Default Cards":
                    self.bulk_json_url = dictionary["download_uri"]
                    print(self.bulk_json_url)

    def open_json(self):
        with urlopen(f"{self.bulk_json_url}") as default_cards_response:
            default_cards_data = json.loads(default_cards_response.read().decode('utf-8'))
            for card_object in default_cards_data:
                if card_object["name"] != "":
                    # print(card_object["name"], card_object["set_name"], card_object["prices"]["usd"])
                    yield card_object["name"], card_object["set_name"], card_object["prices"]["usd"]
                # print(card["name"], card["prices"]["usd"])

# TODO: check url against most recent json
# TODO: write card name, card set, and card price to db
# TODO: instead of "fork":     if card_object["name"] != "":