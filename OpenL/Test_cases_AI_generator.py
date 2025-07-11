import requests, json, base64, re
import pandas as pd
from pprint import pprint


api_key = 'api_key'
URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
file = pd.read_csv('rules_table.csv',sep='\t')
csv_string = file.to_csv(index=False)
csv_bytes = csv_string.encode('utf-8')
csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')

#example_payload = {"contents": [{"parts": [{"text": "Considering this json: {'context': {'currentDateTime': '2025-07-07T13:46:37','currentUser': {}},'shipment': {'numberOfPieces': 10.00000,'originCountry': 'CA'}} make another one where in the addition of those two fields you also add originCode with the value 126 and another json with the value 130. Also in your json response, change the single quoting in the original one for double"}]}]}
example_payload = {"contents":
                       [{"parts":
                             [{"inline_data":
                                   {"mime_type": "text/csv", "data": csv_base64}},
                              {"text": "This is a rule table for openl that means the column "
                                       "headers are the names of the parameters taken into consideration "
                                       "and the last column is the expected result. "
                                       "Now taking into consideration this json: "
                                       "{'context': {'currentDateTime': '2025-07-07T13:46:37','currentUser': {}},"
                                       "'shipment': {'numberOfPieces': 10.00000,'originCountry': 'CA'}} "
                                       "make another 10 more jsons with different combinations to test the expected results."
                                       "It is not mandatory to include the initial 'numberOfPieces or originCountry unless they are"
                                       "of course necesary to test the rule."
                                       "In your response simply return the json don't give any further explanations or descriptions"}]}]}
def submit_prompt (api_key, payload):
    headers = {'Content-Type': 'application/json','X-goog-api-key': api_key }
    response = requests.post(URL,json=payload,headers=headers)
    print(response)
    response = (response.text)
    response = json.loads(response)
    response = (response['candidates'][0]['content']['parts'][0]['text'])
    json_blocks = re.findall(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    return json_blocks

json_blocks = submit_prompt(api_key,example_payload)
for i, block in enumerate(json_blocks):
    try:
        json_object = json.loads(block)
        json_object = json.dumps(json_object)
        print(f"\n--- JSON Object {i+1} ---")
        print(json_object)
    except json.JSONDecodeError as e:
        print(f"\n--- Error parsing JSON object {i+1} ---")
        print(f"Error: {e}")
        print(f"Problematic block:\n{block}")


