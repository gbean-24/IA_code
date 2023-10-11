import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{"key": "9f53630e104b054678d692c48f1f4fa66e56dca24b", "secret":"1a2fbebc264a4e001616e1"}'

response = requests.post('https://api.imweb.me/v2/auth', headers=headers, data=data)

print(response.json())

#Access tokens need to be updated everytime

# Sources
# curl to python converter: https://curlconverter.com/
# Imweb official document: https://developers.imweb.me/getstarted/token