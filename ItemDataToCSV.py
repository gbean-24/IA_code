import requests
import csv

headers = {
    'Content-Type': 'application/json',
    'access-token': 'a394f0ee89dba75d60cfb956db2c0d3f'
}

json_data = {
    'orderBy': 'jointime',
    'limit': 100,
    'offset': 1
}

response = requests.get('https://api.imweb.me/v2/shop/products', headers=headers, json=json_data) 


def add_to_CSV(input_data):
    csv_file_path = 'meand_products.csv'

    items = []
    if 'data' in input_data and 'list' in input_data['data']:
        items = input_data['data']['list']
        field_names = ['no', 'categories', 'name', 'simple_content', 'price', 'weight', 'is_exist_options', 'is_mix']

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        for item in items:
            simplified_item = {'no': item.get('no',''),
                                'categories': item.get('categories', ''),
                                'name': item.get('name', ''),
                                'simple_content': item.get('simple_content', ''),
                                'price': item.get('price', ''),
                                'weight': item.get('weight', ''),
                                'is_exist_options': item.get('is_exist_options', ''),
                                'is_mix': item.get('is_mix', ''),
                                }
            writer.writerow(simplified_item)
        


response_data = response.json()
# print(response_data['data']['list'][0])

csv_file_path = 'meand_products.csv'

items = []
if 'data' in response_data and 'list' in response_data['data']:
    items = response_data['data']['list']

field_names = ['no', 'categories', 'name', 'simple_content', 'price', 'weight', 'is_exist_options', 'is_mix']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:  # Ensure UTF-8 encoding
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    add_to_CSV(response_data)

    for i in range(4):
        json_data['offset'] +=1
        response = requests.get('https://api.imweb.me/v2/shop/products', headers=headers, json=json_data) 
        response_data = response.json()
        add_to_CSV(response_data)