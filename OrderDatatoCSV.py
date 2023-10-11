import requests
import csv

headers = {
    'Content-Type': 'application/json',
    'access-token': '0fb29547968f04d2d0b59f4389fcfcf8'
}

json_data = {
    'status': 'COMPLETE',
    'limit': 100,
    'offset': 1
}

response = requests.get('https://api.imweb.me/v2/shop/orders', headers=headers, json=json_data) 

response_data = response.json()

def add_to_CSV(input_data):
    orders = []
    if 'data' in input_data and 'list' in input_data['data']:
        orders = input_data['data']['list']
        field_names = ['order_no', 'order_time', 'orderer', 'delivery']

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        for order in orders:
            simplified_member = {'order_no': order.get('order_no',''),
                                 'order_time': order.get('order_time', ''),
                                    'orderer': order.get('orderer', ''),
                                    'delivery': order.get('delivery', '')}
            writer.writerow(simplified_member)
        


response_data = response.json()
# print(response_data['data']['list'][0])

csv_file_path = 'meand_orders.csv'

members = []
if 'data' in response_data and 'list' in response_data['data']:
    members = response_data['data']['list']

field_names = ['order_no', 'order_time', 'orderer', 'delivery']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:  # Ensure UTF-8 encoding
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    add_to_CSV(response_data)

    for i in range(15):
        json_data['offset'] +=1
        response = requests.get('https://api.imweb.me/v2/shop/orders', headers=headers, json=json_data) 
        response_data = response.json()
        add_to_CSV(response_data)