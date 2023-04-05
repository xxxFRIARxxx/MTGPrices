from bs4 import BeautifulSoup
import socket
import threading
import time
import os
import requests
import pandas as pd





URL_STOCKS = "https://www.mtgstocks.com/interests"
URL_GOLDFISH = "https://www.mtggoldfish.com/index/RESERVED_LIST#paper"
URL_TCGPLAYER = "https://www.tcgplayer.com/product/"
URL_KINGDOM = ""
SCRY_API = "https://api.scryfall.com"

# sesh = requests.session()
# sesh_resp = sesh.get(SCRY_API)
# print(sesh_resp)


# if response.status_code == 200:
#     resp = response.json()
#     print(resp)
# else:
#     print("Bad status code", response.status_code, response)

# response=requests.get('https://api.scryfall.com/cards/search?q=cmc:12')

# print(response)
# print(results)
# print('results["data"] contains '+str(len(results['data']))+' elements')
# print('name='+results['data'][4]['name'])
# print('set_name='+results['data'][4]['set_name'])
# print('set='+results['data'][4]['set'])
# print('usd='+results['data'][4]['prices']["usd"])
# print('eur='+str(results['data'][4]['eur']))



class MTGScraper(): 
    def __init__(self):

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def get_TCG_price(self):
            # self.response = requests.get("https://www.tcgplayer.com/product/90945/magic-magic-2015-m15-elvish-mystic?xid=pif6372c5d-1464-4330-97d8-b28935094d55&page=1&Language=English")
            self.response = self.session.get("https://www.tcgplayer.com/product/90945/magic-magic-2015-m15-elvish-mystic?xid=pif6372c5d-1464-4330-97d8-b28935094d55&page=1&Language=English")
            # bal_req = self.refresh_session()
            soup_parser = BeautifulSoup(self.response.content, "html.parser")
            # balance = soup_parser.find("table")#.string.replace(',', '')
            mydivs = soup_parser.find_all("table")#, {"class": "product-listing__pricing"})
            # print(mydivs)

            # price = driver.find_elements_by_xpath("//section[@class='product-listings']/div/div[@class='product-listing__pricing']/span[@class='product-listing__price']")
    
    def get_SCRY_price(self):
        self.response = requests.get(f"{SCRY_API}/cards/search?q=is%3Areserved+prefer:oldest")
        # self.response = requests.get(f"{SCRY_API}/cards/search?as=grid&order=name&q=is%3Areserved")
        self.results=self.response.json()

    def get_info(self):
        self.get_SCRY_price()     
        # for row in self.results["data"]:
        #     yield row

        for i in range(0,len(self.results['data'])):

            multiverse_ID = self.results['data'][i]['multiverse_ids']
            card_name=self.results['data'][i]['name']
            set_name=self.results['data'][i]['set_name']
            set_tckr=self.results['data'][i]['set']
            usd=self.results['data'][i]["prices"]['usd']

            yield (multiverse_ID ,card_name, set_name, set_tckr, usd)


    def make_df(self, db_list):
        self.db_list = list(db_list)
        self.data_frame = pd.DataFrame(self.db_list, columns =["Multiverse #", "Card Name", "Set", "Set Name", "Price"])
        df2 = self.data_frame.to_string(index=False, justify="center")
        print(df2)

#preview the dataframe
# print(repo)


# df = pd.DataFrame({'text': ['foo foo', 'bar bar'],
#                  'number': [1, 2]})

# df.style.set_properties(**{'text-align': 'center'})

# print(df)
scraper = MTGScraper()

scraper.get_info()

scraper.make_df(scraper.get_info())

# scraper.get_SCRY_price()