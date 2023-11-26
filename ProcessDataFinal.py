import pandas as pd
import csv

dataframe = pd.read_csv('meand_users.csv')
dataframe = dataframe.drop(['gender', 'birth'], axis=1)

def find_category_frequency(name):
    category11 = 0
    category13 = 0
    category14 = 0
    category15 = 0

    csv_path = 'processed_data_2.csv'
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[1] == name:
                if row[3] == '11':
                    category11 += 1
                elif row[3] == '13':
                    category13 += 1
                elif row[3] == '14':
                    category14 += 1
                elif row[3] == '15':
                    category15 += 1
    return [category11, category13, category14, category15]

def find_first_three(name):
    items_list = []
    csv_path = 'processed_data_2.csv'
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[1] == name:
                items_list.append(row[2])
        if len(items_list) == 0:
            for i in range(3):
                items_list.append('0')
        elif len(items_list) == 1:
            for i in range(2):
                items_list.append(items_list[0])
        elif len(items_list) == 2:
            items_list.append(items_list[1])
        else:
            items_list = items_list[:3]
    return items_list


dataframe['categories'] = dataframe['name'].apply(find_category_frequency)
dataframe['category11'] = dataframe['categories'].apply(lambda x: x[0])
dataframe['category13'] = dataframe['categories'].apply(lambda x: x[1])
dataframe['category14'] = dataframe['categories'].apply(lambda x: x[2])
dataframe['category15'] = dataframe['categories'].apply(lambda x: x[3])
dataframe = dataframe.drop(['categories'], axis=1)

dataframe['allitems'] = dataframe['name'].apply(find_first_three)
dataframe['item1'] = dataframe['allitems'].apply(lambda x: x[0])
dataframe['item2'] = dataframe['allitems'].apply(lambda x: x[1])
dataframe['item3'] = dataframe['allitems'].apply(lambda x: x[2])
dataframe = dataframe.drop(['allitems'], axis=1)
dataframe = dataframe.drop(['email'], axis=1)

dataframe.to_csv('MLdatafinal.csv', index=False)