import requests
import csv

headers = {
    'Content-Type': 'application/json',
    'access-token': '' #Update when running code
}

json_data = {
    'orderBy': 'jointime',
    'limit': 100,
    'offset': 1
}

response = requests.get('https://api.imweb.me/v2/member/members', headers=headers, json=json_data) 

# Defines fieldnames, processes input data
def add_to_CSV(input_data):
    members = input_data['data']['list']
    field_names = ['member_code', 'name', 'gender', 'birth', 'email']

    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    for member in members:
        simplified_member = {'member_code': member['member_code'],
                                'name': member['name'],
                                'gender': member['gender'],
                                'birth': member['birth'],
                                'email': member['email']}
        writer.writerow(simplified_member)
        


response_data = response.json()

csv_file_path = 'meand_users.csv'

field_names = ['member_code', 'name', 'gender', 'birth', 'email']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    add_to_CSV(response_data)

    # Each offset has 100 data rows as specified in json_data['limit']. There are approximately 500 users.
    for i in range(6):
        json_data['offset'] +=1
        response = requests.get('https://api.imweb.me/v2/member/members', headers=headers, json=json_data) 
        response_data = response.json()
        add_to_CSV(response_data)