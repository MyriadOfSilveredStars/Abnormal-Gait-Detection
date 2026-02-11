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

def get_Y_and_X_fourier(fouriered_dataset):
    X_stuff = []
    Y_stuff = []

    for chunklet in fouriered_dataset:
        X_stuff.append(chunklet["data"])
        Y_stuff.append(chunklet["type"])

    return X_stuff, Y_stuff

def get_Y_and_X_percent(percentaged_dataset):
    X_stuff = []
    Y_stuff = []

    for ind_data in percentaged_dataset:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    #print("Data length:", len(X_stuff))
    #print("Type length:", len(Y_stuff))

    return X_stuff, Y_stuff

def get_X_Y_Raw(virgin_data):
    #this just gets x and y without changing the data
    #either fourier or percentages
    X_stuff = []
    Y_stuff = []

    #print(len(virgin_data))

    for ind_data in virgin_data:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    return X_stuff, Y_stuff

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


## THE... MACHINE... DUN DUN DUUUUN ##

def deepthought(X, Y):
    #this takes the dataset and splits it
    #so each iteration takes one sample out and tests it against the rest
    #and then each iteration takes out a different sample

    iterations = len(X) - 1
    all_accuracies = []
    

    for sample in range(0, iterations):
        X_test, Y_test, X_train, Y_train = get_train_and_test(X, Y, sample)

        #print(len(X_train))
        #print(len(Y_train))

        X_train = np.array(X_train)#.reshape(-1, 1)
        X_test = np.array(X_test)#.reshape(-1, 1)

        svm = SVC(kernel='linear')
        svm.fit(X_train, Y_train)

        y_pred_svm = svm.predict(X_test)
        accuracy = metrics.accuracy_score(Y_test, y_pred_svm) * 100

        print("SVM Accuracy: " + str(accuracy) + "%")
        print("\n")
        print(metrics.classification_report(Y_test, y_pred_svm, zero_division=1))
        print("\n\n")

    #return all_accuracies

def main():
    data = main_extract()
    dataset = main_extract()
    #fouriered = main_fourier(data)
    percentaged = main_percent(dataset) 

    X, Y = get_Y_and_X_percent(percentaged)
    #X, Y = get_Y_and_X_fourier(fouriered)
    #X, Y = get_X_Y_Raw(data)

    accuracies = deepthought(X, Y)
    mean_accuracy = statistics.mean(accuracies)
    print("The Ultimate Accuracy Report:")
    print(mean_accuracy + "%")

main()


