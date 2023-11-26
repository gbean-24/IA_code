import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#Create the model
def model_RFC():
    dataframe = pd.read_csv('MLdatafinal.csv')
    x = ['category11', 'category13', 'category14', 'category15']
    y = ['item1', 'item2', 'item3']

    train_df, test_df = train_test_split(dataframe, test_size = 0.2, random_state = 42)

    #Make train data
    X_train = train_df[x]
    y_train = train_df[y]
    
    #Model chosen from best accuracy
    model = RandomForestClassifier(max_depth=20, n_estimators=54, max_features='sqrt', random_state=41)
    model.fit(X_train, y_train)
    return model

#Use the user's name to find user data
def find_user_data(name):
    csv_path = 'MLdatafinal.csv'
    user_data = []
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[1] == name:
                user_data.append(row[2])
                user_data.append(row[3])
                user_data.append(row[4])
                user_data.append(row[5])
    return user_data

#Model to export
def train_model_RFC(name):
    x = ['category11', 'category13', 'category14', 'category15']
    model = model_RFC()

    #Format user data to input to ML model
    user_data = find_user_data(name)
    new_data = pd.DataFrame([{
        'category11': user_data[0],
        'category13': user_data[1],
        'category14': user_data[2],
        'category15': user_data[3],
        }])
    new_data = new_data[x]
    print(new_data)

    #Sorting predictions from highest to lowest accuracy
    user_prob_predictions = model.predict_proba(new_data)
    user_sorted_index_predictions = [np.argsort(-probs, axis=1) for probs in user_prob_predictions]
    user_sorted_class_predictions = [model.classes_[i][indices.flatten()] for i, indices in enumerate(user_sorted_index_predictions)]

    #Code help: https://chat.openai.com/share/3660289f-655c-47bb-998c-4b25b3be2c5a
    return user_sorted_class_predictions

#Input is user data instead of user's name - for users without shopping history
def train_model_manual(category_list):
    x = ['category11', 'category13', 'category14', 'category15']
    model = model_RFC()

    new_data = pd.DataFrame([{
        'category11': category_list[0],
        'category13': category_list[1],
        'category14': category_list[2],
        'category15': category_list[3],
        }])

    new_data = new_data[x]

    user_prob_predictions = model.predict_proba(new_data)
    user_sorted_index_predictions = [np.argsort(-probs, axis=1) for probs in user_prob_predictions]
    user_sorted_class_predictions = [model.classes_[i][indices.flatten()] for i, indices in enumerate(user_sorted_index_predictions)]

    return user_sorted_class_predictions

# inputlist = ['0','0','5','0']
# RFCtrain = train_model_RFC('user3')
# manualtrain = train_model_manual(inputlist)
# print(f"{RFCtrain[0][0]} + {RFCtrain[1][0]} + {RFCtrain[0][0]}")
# print(f"{manualtrain[0][0]} + {manualtrain[1][0]} + {manualtrain[0][0]}")