import requests
import pandas as pd

portfolio={}
def GetPrices():
    while True:
        try:
            ticker=input("Give a ticker: ")
            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+ticker+ "&interval=5min&outputsize=full&apikey=demo")

            # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
            # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            if response.status_code != 200:
                raise ValueError("Could not retrieve data, code:", response.status_code)
            raw_data = response.json()

            time_series = raw_data['Time Series (5min)']
            data = raw_data['Time Series (5min)']
            df = pd.DataFrame(data).T.apply(pd.to_numeric)
            #print(df)
            price=df.iloc[0, 3]
            portfolio[ticker]=price
            answer = input("Want to continue [y/n]? ")
            if answer == 'y':
                continue
            else:
                break
        except:
            print("ticker not found, please try again")




stock_price=GetPrices()
print(portfolio)
