# Data opvragen (GET)
# Data toevoegen (POST)
# Data wijzigen (PUT)
# Data verwijderen (DEL)

# Response:
# 200: Succesvol
# 401: Geen toegang
# 404: Niet gevonden

#Resultaat in XML

import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL_HOUSE_PRICES = 'https://opendata.cbs.nl/ODataFeed/odata/83625NED/TypedDataSet'
API_URL_THERMOSTAT = 'http://192.168.178.144:8080/bridge/zones/zn1/status'


headers = {
    'accept': 'application/json'
}

params = {
    '$filter': "startswith(RegioS, 'NL01')",
}


response = requests.get(url=API_URL_HOUSE_PRICES, headers=headers, params=params)
json_data = response.json()['value']
df = pd.DataFrame(json_data)

response1 = requests.get(API_URL_THERMOSTAT, headers=headers)
json_data1 = response1.json()['id']
df1 = pd.DataFrame(json_data1)

print(response1)
print(response1.json) #response in XML is niet goed werkbaar daarom JSON-format
print(response1.json().keys())
print(df1)

# print(response)
# print(response.ok)
# print(response.text) #response in XML is niet goed werkbaar daarom JSON-format
# print(response.json)
# print(response.json().keys())
# print(df)

# Add column year.
df['year'] = df['Perioden'].str[:4].astype(int)

# Create plot.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df['year'], df['GemiddeldeVerkoopprijs_1'])
ax.set_xlabel('Year')
ax.set_ylabel('Price (€)')
ax.set_title('Gemiddelde huis prijs in Nederland per jaar')
plt.show()