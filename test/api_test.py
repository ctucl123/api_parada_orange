import requests



url = "http://192.168.1.92:5000/api/database?operation=last_transactions"

payload = {}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)
