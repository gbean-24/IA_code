import requests
import csv

headers = {
    'Content-Type': 'application/json',
    'access-token': '0fb29547968f04d2d0b59f4389fcfcf8'
}

json_data = {
    'orderBy': 'jointime',
    'limit': 100,
    'offset': 1
}

response = requests.get('https://api.imweb.me/v2/member/members', headers=headers, json=json_data) 


def add_to_CSV(input_data):
    members = []
    if 'data' in input_data and 'list' in input_data['data']:
        members = input_data['data']['list']
        field_names = ['member_code', 'name', 'gender', 'birth']

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        for member in members:
            simplified_member = {'member_code': member.get('member_code',''),
                                    'name': member.get('name', ''),
                                    'gender': member.get('gender', ''),
                                    'birth': member.get('birth', '')}
            writer.writerow(simplified_member)
        


response_data = response.json()
# print(response_data['data']['list'][0])

csv_file_path = 'meand_users.csv'

members = []
if 'data' in response_data and 'list' in response_data['data']:
    members = response_data['data']['list']

field_names = ['member_code', 'gender', 'birth']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:  # Ensure UTF-8 encoding
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    add_to_CSV(response_data)

    for i in range(4):
        json_data['offset'] +=1
        response = requests.get('https://api.imweb.me/v2/member/members', headers=headers, json=json_data) 
        response_data = response.json()
        add_to_CSV(response_data)