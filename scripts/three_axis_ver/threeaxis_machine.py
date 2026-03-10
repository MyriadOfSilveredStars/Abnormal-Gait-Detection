
## IMPORTING LIBRARIES ##

import matplotlib.pyplot as plt
import numpy as np
import statistics

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

## IMPORTING OWN MODULES ##

from extract_3axis_data import get_everything
#from extract_data_new import cut_raw_chunks
#from find_avg import main_avg
from threeaxis_fourier import main_fourier
#from percenttime import main_percent

## MY DATASET ##

fouriered = main_fourier(get_everything()) #the data that is fouriered
#percentaged = main_percent(main_extract()) #the data that is percentaged
#raw = cut_raw_chunks(main_extract()) # the unchanged data, cut down to 500 bit chunks

fouriered_length = len(fouriered) - 1
#percentaged_length = len(percentaged) - 1
#raw_length = len(raw) - 1

all_accuracies = []


## SOME FUNCTIONS ##

def get_all_names(dataset):
    all_ids = []
    for data in dataset:
        all_ids.append(data["id"])

    return all_ids    

def get_train_test(dataset, volNo): #YOU ARE THE PROBLEM
    #splits the dataset into test and train data
    #where one volunteer will become a test and the others, training
    training = []
    testing = []

    for i in range(0, len(dataset)):
        if dataset[i]["id"].find(str(volNo)) != -1:
            testing.append(dataset[i])
        else:
            training.append(dataset[i])

    return training, testing

def get_X_and_Y(dataset):
    #this separates the x and y values (data and type)
    X_stuff = []
    Y_stuff = []

    #print("Length of Dataset:", len(dataset))

    for ind_data in dataset:
        X_stuff.append(ind_data["data"])
        Y_stuff.append(ind_data["type"])

    #print(np.array(X_stuff[0]))
    #print("Data length:", len(X_stuff))
    #print("Type length:", len(Y_stuff))

    for chunk in X_stuff:
        chunk = np.array(chunk).reshape(-1,1)

    return X_stuff, Y_stuff


## MACHINE ALGORITHMS CODE ##
#by having 

def LogisticRegression(X_train, Y_train, X_test, Y_test):
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train, Y_train)

    Y_pred = log_reg.predict(X_test)
    accuracy = metrics.accuracy_score(Y_test, Y_pred) * 100
    return accuracy

def KNN(X_train, Y_train, X_test, Y_test):
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, Y_train)

    Y_pred_knn = knn.predict(X_test)
    accuracy = metrics.accuracy_score(Y_test, Y_pred_knn) * 100

    return accuracy

def SVM(X_train, Y_train, X_test, Y_test):
    svm = SVC(kernel='linear')
    svm.fit(X_train, Y_train)

    Y_pred_svm = svm.predict(X_test)
    accuracy = metrics.accuracy_score(Y_test, Y_pred_svm) * 100

    return accuracy


## CONTINUE TO MACHINE ##

def deepthought(dataset, all_accuracies):
    print("\n\n")

    data_x = dataset[0]
    data_y = dataset[1]
    data_z = dataset[2]


    for i in range(1, 10):
        #separate out one person
        train_x, test_x = get_train_test(data_x, i)
        train_y, test_y = get_train_test(data_y, i)
        train_z, test_z = get_train_test(data_z, i)

        #then split the data into X (data) and Y (catagory)
        X_train_x, Y_train_x = get_X_and_Y(train_x)
        X_test_x, Y_test_x = get_X_and_Y(test_x)

        X_train_y, Y_train_y = get_X_and_Y(train_y)
        X_test_y, Y_test_y = get_X_and_Y(test_y)

        X_train_z, Y_train_z = get_X_and_Y(train_z)
        X_test_z, Y_test_z = get_X_and_Y(test_z)

        #reshape to numpy arrays and squeeze to make 2d rather than 3d
        X_train_x = np.array(X_train_x)
        X_test_x = np.array(X_test_x)
        X_train_x = X_train_x.squeeze()
        X_test_x = X_test_x.squeeze()

        X_train_y = np.array(X_train_y)
        X_test_y = np.array(X_test_y)
        X_train_y = X_train_y.squeeze()
        X_test_y = X_test_y.squeeze()

        X_train_z = np.array(X_train_z)
        X_test_z = np.array(X_test_z)
        X_train_z = X_train_z.squeeze()
        X_test_z = X_test_z.squeeze()
        

        try:
            
            accuracy_x = SVM(X_train_x, Y_train_x, X_test_x, Y_test_x)
            accuracy_y = SVM(X_train_y, Y_train_y, X_test_y, Y_test_y)
            accuracy_z = SVM(X_train_z, Y_train_z, X_test_z, Y_test_z)

            print("X-axis accuracy: " + str(accuracy_x) + "%")
            print("Y-axis accuracy: " + str(accuracy_y) + "%")
            print("Z-axis accuracy: " + str(accuracy_z) + "%")

            #log_reg_x = LogisticRegression(max_iter=1000)
            #log_reg_x.fit(X_train_x, Y_train_x)
            #Y_pred_x = log_reg_x.predict(X_test_x)
            #accuracy_x = metrics.accuracy_score(Y_test_x, Y_pred_x) * 100

            accuracy = (accuracy_x + accuracy_y + accuracy_z) / 3

            print("Round " + str(i) + " Accuracy: " + str(accuracy) + "%")
            print("\n")

            all_accuracies.append(accuracy)

        except:
            print("Volunteer 6 never actually recorded data\n\n")
    
            

    print("It's the final accuracy do do do doooo do do do do doooooo")
    print(str(statistics.mean(all_accuracies)) + "%")

deepthought(fouriered, all_accuracies)
#to change which dataset is used, swap out the first parameter
#either fouriered, percentaged, or raw