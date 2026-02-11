#The new machine overtakes the old
#As it will always be

## IMPORTING ##

import matplotlib.pyplot as plt
import numpy as np
import statistics
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


## SOME METHODS AND THINGS ##

def get_training_testing(dataset, sample_no):
    training_set = []

    for i in range(0, len(dataset)-1):
        if i == sample_no:
            testing_set = dataset[i]
        else:
            training_set.append(dataset[i])

    return training_set, testing_set

def get_train_and_test(x, y, sampleNo):
    training_x = []
    training_y = []

    for i in range(0, len(x)-1):
        if i == sampleNo:
            testing_x = x[sampleNo]
            testing_y = y[sampleNo]
        else:
            training_x.append(x[sampleNo])
            training_y.append(y[sampleNo])

    return testing_x, testing_y, training_x, training_y


def split_x_and_y_training(dataset):
    X_stuff = []
    Y_stuff = []

    for ind_data in dataset:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    print(len(Y_stuff))
    print(len(X_stuff))

    return X_stuff, Y_stuff

def split_x_and_y_testing(data):
    return data["data"], data["type"]

def split_x_and_y(dataset):
    X_stuff = []
    Y_stuff = []

    for ind_data in dataset:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    return X_stuff, Y_stuff


## THE... MACHINE... DUN DUN DUUUUN ##

def deepthought(dataset):
    #this takes the dataset and splits it
    #so each iteration takes one sample out and tests it against the rest
    #and then each iteration takes out a different sample

    iterations = len(dataset) - 1
    all_accuracies = []

    X_stuff, Y_stuff = split_x_and_y(dataset)
    

    for sample in range(0, iterations):
        X_test, Y_test, X_train, Y_train = get_train_and_test(X_stuff, Y_stuff, sample)

        print(len(X_train))
        print(len(Y_train))

        X_train = np.array(X_train)#.reshape(-1, 1)
        X_test = np.array(X_test)#.reshape(-1, 1)

        #print(len(X_train))
        #print(len(Y_train))

        rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier.fit(X_train, Y_train)

        Y_pred = rf_classifier.predict(X_test)

        accuracy = metrics.accuracy_score(Y_test, Y_pred)
        all_accuracies.append(accuracy)
        classification_rep = metrics.classification_report(Y_test, Y_pred)

        print(f"Random Forest Accuracy: {accuracy:.2f}")
        print("\nClassification Report:\n", classification_rep)

    #return all_accuracies

def main():
    data = main_extract()
    dataset = main_extract()
    #fouriered = main_fourier(data)
    percentaged = main_percent(dataset) 

    #print(percentaged)

    accuracies = deepthought(percentaged)
    mean_accuracy = statistics.mean(accuracies)
    print("The Ultimate Accuracy Report:")

main()


