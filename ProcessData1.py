import requests
import csv
import json

headers = {
    'Content-Type': 'application/json',
    'access-token': '' #Update when running
}

json_data = {
    'orderBy': 'jointime',
    'limit': 1,
    'offset': 1
}

def next_order_no(n):
    order_file_path = 'meand_orders.csv'
    with open(order_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_no = 0
        for row in csv_reader:
            line_no += 1
            if line_no == n:
                order_no_value = row[0]

    return (n+1, int(order_no_value))

def find_orderer_name(order_number):
    order_file_path = 'meand_orders.csv'
    with open(order_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == str(order_number):
                row_data = eval(row[2]) #ChatGPT: https://chat.openai.com/share/d44d8aa8-a735-48bc-9658-82be06f944f9
                return row_data['name']

def find_item_category(ordered_items):
    item_file_path = 'meand_items.csv'
    prod_categories = []
    with open(item_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] in ordered_items:
                prod_categories.append(row[1])
    return prod_categories

def add_to_CSV(i):
    order_no = next_order_no(i)[1]
    orderer = find_orderer_name(order_no)

    order_response = requests.get(f'https://api.imweb.me/v2/shop/orders/{order_no}/prod-orders', headers=headers, json=json_data) 
    order_response_data = order_response.json()

    ordered_items = []
    for item in order_response_data['data']:
        ordered_items.append(str(item['items'][0]['prod_no']))

    prod_order_no = []
    for item in order_response_data['data']:
        prod_order_no.append(item['order_no'])
    
    prod_categories = find_item_category(ordered_items)
    
    
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    order_info = {'order_no': order_no,
                        'name': orderer,
                        'prod_no': ordered_items,
                        'prod_category': prod_categories,
                        'prod_order_no': prod_order_no}
    writer.writerow(order_info)

csv_file_path = 'process_data_1.csv'
field_names = ['order_no', 'name', 'prod_no', 'prod_category', 'prod_order_no']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:  # Ensure UTF-8 encoding
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    for i in range (2, 1254):
        add_to_CSV(i)