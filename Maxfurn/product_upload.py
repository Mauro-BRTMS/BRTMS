from uuid7 import UUIDv7
import requests, json, time
import pandas as pd

token=""

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "x-api-key" : ""
}

df = pd.read_csv("BlueRock_articlegroups.csv", sep=";", dtype=str)
for _, row in df.iterrows():
    uuid = UUIDv7()
    url = 'https://api.test.bluerockplatform.com/maxfurn/lm/operations/api/configuration/products/' + str(uuid)
    payload = '{"code": "' + str(row["Code"]) + '", "name": "' + str(row["Name"]) + '", "category": "' + str(row["Catagory "]) + '", "requirements": [ ]}'
    print(payload)
    print(url)
    response = requests.put(url, headers=headers, data=payload)
    print(response)
