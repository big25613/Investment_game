import requests
import pandas as pd
import matplotlib.pyplot as plt

def cash_balance():
    while True:
        try:
            cash_balance=float(input("What amount of money would you like to invest? "))
            if cash_balance <= 0:
                while cash_balance <= 0:
                    try:
                        cash_balance = float(input("Please fill in a positive number "))
                    except:
                        print("Amount not found, please fill in a number")
                        continue
            break
        except:
            print("Amount not found, please fill in a number")
            continue
    return cash_balance

portfolio={}
def GetPrices():
    balance=cash_balance()
    print("The balance on your account is:",balance)
    while True:
        try:
            ticker=input("Give a ticker: ")
            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey=G2NO055HSLUUAZWI")

            # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
            # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            if response.status_code != 200:
                raise ValueError("Could not retrieve data, code:", response.status_code)
            raw_data = response.json()

            data = raw_data['Time Series (Daily)']
            df = pd.DataFrame(data).T.apply(pd.to_numeric)
            df.sort_index(ascending=True,inplace=True)

            purchase_price=df.iloc[0,3]
            if balance<purchase_price:
                print("you don't have enough balance to buy this stock")
                answer = input("Want to continue [y/n]? ")
                if answer == 'y':
                    continue
                else:
                    break
            else:
                balance -= purchase_price
                print("your remaining balance is:", balance)

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

# print(list(portfolio.values()))
# data = pd.DataFrame(portfolio.values()).T
# sortdata = data.sort_index(ascending=True)
# sortdata.plot()
#
#
# totalvalue = sum(portfolio.values())
# print(totalvalue)
# totalvalue.plot()
# plt.title('Portfolio')
# list_legend = list(portfolio.keys())
# list_legend.append("Total value")
# plt.legend(list_legend)
# plt.show()


# balance=cash_balance()
# print("Your cash balance is $", float(balance))