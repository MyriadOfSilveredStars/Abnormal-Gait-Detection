#This is the Machine. Hopefully. Model time

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

from extract_data_new import main_extract
#from find_avg import main_avg
from fouriertime import main_fourier
from percenttime import main_percent
    

## MY DATASET ##
# All code here is liberated from https://www.geeksforgeeks.org/machine-learning/comprehensive-guide-to-classification-models-in-scikit-learn/#2-knearest-neighbors-knn
# Because there ain't no way I'm coding this from scratch

dataset = main_extract()
data = main_extract()

fouriered = main_fourier(dataset)

percentaged = main_percent(data)

def get_all_names(dataset):
    all_ids = []
    for data in dataset:
        all_ids.append(data["id"])

    return all_ids

def get_Y_and_X_fourier(percentaged_dataset):
    X_stuff = []
    Y_stuff = []

    print(len(percentaged_dataset))

    for chunklet in percentaged_dataset:
        X_stuff.append(chunklet["data"])
        Y_stuff.append(chunklet["type"])

    #print(Y_stuff)

    return X_stuff, Y_stuff

def get_Y_and_X_percent(percentaged_dataset):
    X_stuff = []
    Y_stuff = []

    print(len(percentaged_dataset))

    for ind_data in percentaged_dataset:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    print("Data length:", len(X_stuff))
    print("Type length:", len(Y_stuff))

    return X_stuff, Y_stuff

def get_X_Y_Raw(virgin_data):
    #this just gets x and y without changing the data
    #either fourier or percentages
    X_stuff = []
    Y_stuff = []

    print(len(virgin_data))

    for ind_data in virgin_data:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    #print(X_stuff)
    return X_stuff, Y_stuff

all_ids = get_all_names(fouriered) #get all the ids for graphing


#X_mine, Y_mine = get_Y_and_X_percent(percentaged)
X_mine, Y_mine = get_Y_and_X_fourier(fouriered)
#X_mine, Y_mine = get_X_Y_Raw(data)

#X_mine = np.array(X_mine)#.reshape(-1, 1)
#print(X_mine.shape)

from make_graphs import print_all_traindata

print_all_traindata(X_mine, all_ids)


gait_types = ["normal", "toe-walk", "flatfoot", "skew foot"]
gait_features = ["Total Acceleration m/s2"]


encoder = LabelEncoder()
encoded_feature = encoder.fit_transform(Y_mine)
#print(Y_mine)
#print(encoded_feature)

X_train, X_test, y_train, y_test = train_test_split(X_mine, Y_mine, test_size=0.4, random_state=1)

## RANDOM FOREST ##
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

accuracy = metrics.accuracy_score(y_test, y_pred)
classification_rep = metrics.classification_report(y_test, y_pred)

print(f"Random Forest Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_rep)



## LOGISTIC REGRESSION ##

log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)

y_pred = log_reg.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred) * 100

print("Logistic Regression model accuracy: " + str(accuracy) + "%")
print("\n")
print(metrics.classification_report(y_test, y_pred, zero_division=1))
print("\n\n")

"""
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=gait_types)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.show()
"""

## K NEAREST NEIGHBOUR ##

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred_knn) * 100

print("K-Nearest Neighbour Accuracy: " + str(accuracy) + "%")
print("\n")
print(metrics.classification_report(y_test, y_pred_knn, zero_division=1))
print("\n\n")

## SVC ##

svm = SVC(kernel='linear')
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred_svm) * 100

print("SVM Accuracy: " + str(accuracy) + "%")
print("\n")
print(metrics.classification_report(y_test, y_pred_svm, zero_division=1))
print("\n\n")

cm = confusion_matrix(y_test, y_pred_svm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=gait_types)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix for SVM')
plt.show()

## Decision Tree ##

tree = DecisionTreeClassifier(max_depth=5)
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred_tree) * 100

print("Decision Tree Accuracy: " + str(accuracy) + "%")
print("\n")
print(metrics.classification_report(y_test, y_pred_tree, zero_division=1))







