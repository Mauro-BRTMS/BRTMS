import requests, json, time
import pandas as pd

url = "https://lsc-api.q1.ca.bluerockplatform.com/addresses"
with open("token.txt", "r") as file:
    token = file.read().strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
response = requests.get(url, headers=headers)
print(response)
response = response.text
response_dict = response[1:-1]
with open("response.txt", "w") as file:
   file.write(response)
time.sleep(5)
#print(response)

with open("response.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()

data = json.loads(raw)
df = pd.DataFrame(data)
df = df[["code","id"]]
df = df.sort_values(by="id")
df2 = pd.read_csv("BR_format_checking.csv", sep=";")
df['code'] = df['code'].astype(str)
df2['code'] = df2['destinationCode'].astype(str)
df3 = pd.merge(df,df2, on = "code", how = "left")
df3 = df3[["code","id","deliveryDay","deliveryWindow","handoverLocation"]]
day_dict = {"MONDAY":1, "TUESDAY":2,"WEDNESDAY":4,"THURSDAY":8,"FRIDAY":16,"SATURDAY":32,"SUNDAY":64}
df3["days"] = df3["deliveryDay"].map(day_dict)
df3[["openingHours", "closingHours"]] = df3["deliveryWindow"].str.split(" - ", expand=True)
df3["openingHours"] = pd.to_datetime(df3["openingHours"], format="%I:%M%p").dt.strftime("%H:%M")
df3["closingHours"] = pd.to_datetime(df3["closingHours"], format="%I:%M%p").dt.strftime("%H:%M")
df3["closed"] = "false"
df3 = df3.rename(columns={"id": "address"})
df3 = df3[df3['handoverLocation'] == "DIRECT"]
df3 = df3[["code","closed","closingHours","days","openingHours","address"]]
for _, row in df3.iterrows():
    n = 0
    url = 'https://lsc-api.q1.ca.bluerockplatform.com/addresses/' + str(row['address']) + '/time_windows'
    response = requests.get(url, headers=headers)
    response = response.text
    response = json.loads(response)
    if response:
        n = n + 1
        timewindow_id = response[0]["id"]
        payload = '[{"closed": ' + str(row["closed"]) + ', "closingHours": "' + str(row["closingHours"]) + '", "days": ' + str(int(row["days"])) + ', "id": '+ str(int(timewindow_id)) +', "openingHours": "' + str(row["openingHours"]) + '", "address":' + str(row["address"]) + '}]'
        response = requests.put(url, headers=headers, data=payload)
        print(n)
        print(payload)
        print(response)
    else:
        n = n + 1
        payload = '[{"closed": '+str(row["closed"])+', "closingHours": "'+str(row["closingHours"])+'", "days": '+str(int(row["days"]))+', "openingHours": "'+str(row["openingHours"])+'", "address":'+str(row["address"])+'}]'
        response = requests.post(url, headers=headers , data=payload)
        print(n)
        print(payload)
        print(response)

df3.to_csv("all_addresses_direct.csv", index=False, sep=";")
