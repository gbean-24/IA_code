import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{"key": "", "secret":""}' #key and secret key deleted for security purposes

response = requests.post('https://api.imweb.me/v2/auth', headers=headers, data=data)

print(response.json())
#Access tokens need to be updated everytime when accessing client database

# Sources
# curl to python converter: https://curlconverter.com/
# Imweb official document: https://developers.imweb.me/getstarted/token
# Original code: curl -d '{"key": "{API_KEY}", "secret":"{SECRET}"}' https://api.imweb.me/v2/auth
