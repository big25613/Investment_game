import requests
import pandas as pd
import matplotlib.pyplot as plt

portfolio={}
def GetPrices():
    while True:
        try:
            ticker=input("Give a ticker: ")
            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey=demo")

            # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
            # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            if response.status_code != 200:
                raise ValueError("Could not retrieve data, code:", response.status_code)
            raw_data = response.json()

            data = raw_data['Time Series (Daily)']
            df = pd.DataFrame(data).T.apply(pd.to_numeric)
            price = df.iloc[:, 3]
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
print(list(portfolio.values()))
data = pd.DataFrame(portfolio.values()).T
sortdata = data.sort_index(ascending=True)
sortdata.plot()


totalvalue = sum(portfolio.values())
print(totalvalue)
totalvalue.plot()
plt.title('Portfolio')
list_legend = list(portfolio.keys())
list_legend.append("Total value")
plt.legend(list_legend)
plt.show()

test