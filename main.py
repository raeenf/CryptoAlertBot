from multiprocessing.connection import wait
from tokenize import String
import requests
import urllib.request
import keys
import pandas as pd
from time import sleep


#gets data of all 3 cryptos and returns it as a dataframe
def get_crypto(currency = 'USD', cryp = 'BTC,ETH,XRP'):

    url = 'https://api.nomics.com/v1/currencies/ticker'
    payload = {'key' : keys.NOMICS_API_KEY, 'convert': currency, 'ids': cryp, 'interval': '1d'}
    response = requests.get(url, params = payload)
    data = response.json()
    
    crypto_currency, crypto_price, crypto_time = [],[],[]

    for asset in data:
        crypto_currency.append(asset['currency'])
        crypto_price.append(str(format(float(asset['price']), ".3f")))
        crypto_time.append(asset['price_timestamp'])

    
    raw_data = {'assets': crypto_currency, 'rates' : crypto_price, 'time': crypto_time}

    df = pd.DataFrame(raw_data)
    
    return df


def alert(df, crypto, price_alert):
    curr_value = df[df['assets'] == crypto]['rates'].item()

    if float(curr_value) >= price_alert:
        resp = requests.post('https://textbelt.com/text', {
        'phone': '0123456789',
        'message': f"{crypto} has reached {price_alert}!!!",
        'key': keys.TEXTBELT_KEY,
        })
        print(resp.json())
        return True
    else:
        print(df[df['assets'] == crypto])
        return False

while not alert(get_crypto(), 'BTC', 29700):
    sleep(30)
