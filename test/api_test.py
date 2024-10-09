import requests

url = "http://192.168.1.92:5000/api/mecanism"

# JSON con la operación que se quiere realizar
json_data = {
    "operation": "test_lock"
}

response = requests.post(url, json=json_data)

if response.status_code == 200:
    result = response.text
    print( result)
else:
    print(f"Error: {response.status_code}")