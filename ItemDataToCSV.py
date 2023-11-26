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

response = requests.get('https://api.imweb.me/v2/shop/products', headers=headers, json=json_data) 
# Original curl code: curl -X GET -H "Content-Type: application/json" -H "access-token: {ACCESS_TOKEN}" -d '{"version":"latest"}' https://api.imweb.me/v2/shop/products

# Defines fieldnames, processes input data
def add_to_CSV(input_data):
    items = input_data['data']['list']
    field_names = ['no', 'category', 'name', 'prod_status', 'price', 'weight', 'is_exist_options', 'is_mix', 'simple_content_plain', 'image_url', 'product_url']
    
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    # Define category values
    for item in items:
        category_text = item['categories'][0]
        if category_text == 's20220425ea020885bd822' or category_text == 's202204251b13d985b8512':
            category = '13'
        elif category_text == "s2021032769daa46c5be83" or category_text == 's20221012cd81f911a176f':
            category = '11'
        elif '처음' in item['name']:
            category = '14'
        elif '앤드' in item['name']:
            category = '15'
        else:
            category = category_text
        
        # Define product image url
        image_key = item['images'][0]
        image_url = item['image_url'][str(image_key)]

        # Define product urls to client website
        name = item['name']
        no = item['no']
        if '텐셀' in name:
            product_url = f'https://meand.co.kr/35/?idx={no}'
        elif no == '91' or no == '92':
            product_url = f'https://meand.co.kr/40/?idx={no}'
        elif '수피마' in name:
            product_url = f'https://meand.co.kr/36/?idx={no}'
        elif no == '69' or no == '70':
            product_url = f'https://meand.co.kr/33/?idx={no}'
        elif category == '11':
            product_url = f'https://meand.co.kr/shop_acc/?idx={no}'
        elif category == '13':
            product_url = f'https://meand.co.kr/34/?idx={no}'

        # Define values to be written in csv file 
        simplified_item = {'no': no,
                            'category': category,
                            'name': name,
                            'prod_status': item['prod_status'],
                            'price': item['price'],
                            'weight': item['weight'],
                            'is_exist_options': item['is_exist_options'],
                            'is_mix': item['is_mix'],
                            'simple_content_plain': item['simple_content_plain'].replace('\n', ' '),
                            'image_url': image_url,
                            'product_url': product_url
                            }
        writer.writerow(simplified_item)

# Format response_data to json        
response_data = response.json()

csv_file_path = 'meand_items_test.csv'

field_names = ['no', 'category', 'name', 'prod_status', 'price', 'weight', 'is_exist_options', 'is_mix', 'simple_content_plain', 'image_url', 'product_url']

# Write header
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file: #Needs uft-8 encoding for korean characters
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    add_to_CSV(response_data)

    response = requests.get('https://api.imweb.me/v2/shop/products', headers=headers, json=json_data) 
    response_data = response.json()
    add_to_CSV(response_data)
print('task_complete')