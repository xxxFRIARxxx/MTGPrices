import ijson
import urllib.request
import json
import pandas as pd

webUrl=urllib.request.urlopen('https://www.python.org/')



# f = urllib.request.urlopen('https://www.python.org/')
# objects = ijson.items(f, 'earth.europe.item')
# cities = (o for o in objects if o['type'] == 'city')
# for city in cities:
#     print(city)


with open('AllPrices.json') as fp:
    prices = json.load(fp)

    data = []
    for uuid in prices['data']:
        df = pd.json_normalize(prices['data'][uuid]) \
               .filter(like='paper.cardmarket.retail.normal')
        if df.empty:
            continue
        df.columns = df.columns.str.rsplit('.', 1).str[-1]
        df.index = [uuid]
        data.append(df)
    df = pd.concat(data)