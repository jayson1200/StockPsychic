import requests
import pandas as pd
from requests.models import HTTPError


#Get the data in CSV format

# I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF
def getStockInfo(ticker, apiKey):
    try:
        response = requests.get("""https://api.tdameritrade.com/v1/instruments?apikey="""+ apiKey +"""&symbol=""" + ticker +"""&projection=fundamental""")
    except HTTPError:
        print("We don't have your info")
    except Exception:
            print("Something Happened")
        
    print(pd.read_json(response.json(), 'split'))
"""
Get the data you want
Put it into the dataframe
make sure the price is always one period ahead
and delete the info for the first and last periods
"""