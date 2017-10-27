import requests
import json


# website =  'http://edgaronline.api.mashery.com/v2/companies.json?primarysymbols='FB'&appkey={API_Key}'
# payload = {'appkey' = 'Secret_key'}
# r = requests.get('http://edgaronline.api.mashery.com/v2/companies.json', params=payload)


# http://financials.morningstar.com/income-statement/is.html?t=X&ops=clear
payload = {'t':'X', 'ops': 'clear'}
r = requests.get('http://financials.morningstar.com/income-statement/is.html', params=payload)
data = r.json
print(data)

json_data = json.dumps(data)
print(json_data)