import requests
import pandas as pd




response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo")

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# The service sends JSON data, we parse that into a Python datastructure
raw_data = response.json()
print(type(raw_data))

data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)
print(df.head())
price = df.iloc[0,3]
print(price)