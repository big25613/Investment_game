import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Person:

    def __init__(self, username, password):
        self.username = username
        self.password = password


#portfolio_db = [Portfolio(...), Portfolio(...)]
persons_db = [Person("marjolein", "marjolein"),Person("GyungJu","GyungJu")]

portfolio= pd.DataFrame()
portfolio_per_stock=pd.DataFrame()
portfolio_aantal_stock=pd.DataFrame()

class Portfolio:
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

    def GetPrices():
        balance=Portfolio.cash_balance()

        print("The balance on your account is:",balance)
        while True:
            ticker=input("Give a ticker: ")
            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey=G2NO055HSLUUAZWI")

                    # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
            # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            if response.status_code != 200:
                raise ValueError("Could not retrieve data, code:", response.status_code)
            raw_data = response.json()
            if 'Time Series (Daily)' not in raw_data:
                print("ticker not found, please try again")
                continue

            data = raw_data['Time Series (Daily)']
            df = pd.DataFrame(data).T.apply(pd.to_numeric)
            df.sort_index(ascending=True,inplace=True)
            while True:
                try:
                    numberofstocks = int(input("How many stocks do you want to buy?"))
                    break
                except:
                    print("This is not a number, please fill in a number ")
                    continue

            if numberofstocks <= 0:
                while numberofstocks <= 0:
                    try:
                        numberofstocks = int(input("Please fill in a positive number "))
                    except:
                        print("This is not a number, please fill in a number")
                        continue
            price_per_stock = df.iloc[:, 3]
            portfolio_per_stock[ticker] = price_per_stock
            portfolio_aantal_stock[ticker]= [numberofstocks]
            price = numberofstocks * price_per_stock
            portfolio[ticker] = price

            purchase_price=df.iloc[0,3]
            if balance<numberofstocks*purchase_price:
                print("you don't have enough balance to buy this stock")
                answer = input("Want to continue [y/n]? ")
                if answer == 'y':
                    continue
                else:
                    break
            else:
                balance -= numberofstocks * purchase_price
                print("your remaining balance is:", balance)
            answer = input("Want to continue [y/n]? ")
            if answer == 'y':
                continue
            else:
                break
        portfolio['total'] = portfolio.sum(axis=1)
        Portfolio.plot()


    def plot():
        fig = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.03,
            specs=[[{"type": "table"}],
                   [{"type": "scatter"}]]
        )

        for i in range(0, len(portfolio.columns)):
            fig.add_trace(
                go.Scatter(x=portfolio.index, y=portfolio.iloc[:, i],
                           mode='lines', name=portfolio.columns[i]),
                row=2, col=1
            )

        for i in range(0, len(portfolio_per_stock.columns)):
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=["Stocks in portfolio", "Number of Stock in portfolio", "Price per stock", "Total Value"],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
                    cells=dict(values=[portfolio_per_stock.columns, list(portfolio_aantal_stock.iloc[0, :]),
                                       list(portfolio_per_stock.iloc[0, :]), list(portfolio.iloc[0, :])],
                               line_color='darkslategray',
                               fill_color='lightcyan',
                               align='left')),
                row=1, col=1
            )

        fig.show()




def check_username():
    person = None
    username = input("What is your username?")
    for p in persons_db:
        if p.username == username:
            person = username
    return person



def check_password(username):
    while True:
        password = input("What is your password?")
        for p in persons_db:
            if p.username == username and p.password == password:
                stock_price = Portfolio.GetPrices()
                data = pd.merge(portfolio, portfolio_per_stock, left_index=True, right_index=True)
                sortdata = data.sort_index(ascending=True)
            elif p.username != username:
                continue
            else:
                print("Password not correct, try again")
                continue




if __name__ == "__main__":
    persoon = check_username()
    if persoon is not None:
        check_password(persoon)
    else:
        check_username()


