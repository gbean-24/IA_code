import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np

#Complete
def train_model_current(X_train, y_train, estimator):
    base_classifier = RandomForestClassifier(n_estimators=estimator, random_state=37)
    model = MultiOutputClassifier(base_classifier, n_jobs=-1)
    model.fit(X_train, y_train)
    return model

def train_model_RFC(X_train, y_train, depth, estimators,r_state):
    model = RandomForestClassifier(max_depth=depth, n_estimators=estimators, max_features='sqrt', random_state=r_state)
    model.fit(X_train, y_train)
    return model

#Complete
def train_model_DC(X_train, y_train, depth):
    model = tree.DecisionTreeClassifier(max_depth=depth)
    model.fit(X_train, y_train)
    return model

#Complete
def train_model_KNN(X_train, y_train, neighbor):
    model = KNeighborsClassifier(neighbor)
    model.fit(X_train, y_train)
    return model

df = pd.read_csv('MLdatafinal.csv')
target_columns = ['item1', 'item2', 'item3']
x = ['category11', 'category13', 'category14', 'category15']
y = ['item1', 'item2', 'item3']

train_df, test_df = train_test_split(df, test_size = 0.2, random_state = 42)

X_train = train_df[x]
y_train = train_df[y]

X_test = test_df[x]
y_test = test_df[y]

# #for KNN
# for neighbor in range (1,30):
#     model = train_model_KNN(X_train, y_train, neighbor)
#     y_pred = model.predict(X_test)
    
#     accuracy_list = []
#     for i, col in enumerate(y):
#         acc = accuracy_score(y_test[col], y_pred[:, i])
#         accuracy_list.append((col, round(acc, 3)))
#     print(f"Score for NN = {neighbor}: {accuracy_list}")
#     #Best performance: NN = 18/19, NN = 10/11/12/13, NN = 13 => NN=13

# #for DecisionTree
# for depth in range (1,30):
#     model = train_model_DC(X_train, y_train, depth)
#     y_pred = model.predict(X_test)
    
#     accuracy_list = []
#     for i, col in enumerate(y):
#         acc = accuracy_score(y_test[col], y_pred[:, i])
#         accuracy_list.append((col, round(acc, 3)))
#     print(f"Score for depth = {depth}: {accuracy_list}")
#     #Best performance: Depth = 5

# #for current model
# for estimator in range (60,90):
#     model = train_model_current(X_train, y_train, estimator)
#     y_pred = model.predict(X_test)
    
#     accuracy_list = []
#     for i, col in enumerate(y):
#         acc = accuracy_score(y_test[col], y_pred[:, i])
#         accuracy_list.append((col, round(acc, 4)))
#     print(f"Score for N_es = {estimator}: {accuracy_list}")
#     #Best performance: estimator = 32, 62

# for RFC, changing depth and estimator
# depth = 20
# random_state = 42
# for estimator in range(1,60):
#     model = train_model_RFC(X_train, y_train, depth, estimator, random_state)
#     y_pred = model.predict(X_test)

#     accuracy_list = []
#     for i, col in enumerate(y):
#         acc = accuracy_score(y_test[col], y_pred[:, i])
#         accuracy_list.append((col, round(acc, 4)))
#     print(f"Score for estimator = {estimator}: {accuracy_list}")

# model = train_model_KNN(X_train, y_train, 13)
# y_pred = model.predict(X_test)
# accuracy_list = []
# for i, col in enumerate(y):
#     acc = accuracy_score(y_test[col], y_pred[:, i])
#     accuracy_list.append((col, round(acc, 3)))
# print(f"KNN Accuracy: {accuracy_list}")

# model = train_model_DC(X_train, y_train, 5)
# y_pred = model.predict(X_test)
# accuracy_list = []
# for i, col in enumerate(y):
#     acc = accuracy_score(y_test[col], y_pred[:, i])
#     accuracy_list.append((col, round(acc, 3)))
# print(f"DC Accuracy: {accuracy_list}")

# model = train_model_current(X_train, y_train, 32)
# y_pred = model.predict(X_test)
# accuracy_list = []
# for i, col in enumerate(y):
#     acc = accuracy_score(y_test[col], y_pred[:, i])
#     accuracy_list.append((col, round(acc, 4)))
# print(f"Current Accuracy: {accuracy_list}")

# model = train_model_RFC(X_train, y_train, 20, 54, 4)
# y_pred = model.predict(X_test)
# accuracy_list = []
# for i, col in enumerate(y):
#     acc = accuracy_score(y_test[col], y_pred[:, i])
#     accuracy_list.append((col, round(acc, 4)))
# print(f"RFC Accuracy: {accuracy_list}")

# model = train_model_RFC(X_train, y_train, 20, 54, 4)
# y_pred = model.predict(X_test)

# prob_predictions = model.predict_proba(X_test)
# sorted_index_predictions = [np.argsort(-probs, axis=1) for probs in prob_predictions]
# sorted_class_predictions = [model.classes_[i][sorted_indices] for i, sorted_indices in enumerate(sorted_index_predictions)]

# print(len(sorted_class_predictions[0]))

# https://chat.openai.com/share/e8fe1205-6b3c-4829-bb47-fec6a5f65e51