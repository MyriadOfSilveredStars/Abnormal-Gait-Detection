# This extracts the data from the individual .csv files
# Rather than splitting the long csv files into four gait types
# Because... well that didn't work very well 
# But this does... at the cost of my sanity from manually splitting the files

import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import statistics
import numpy
from matplotlib.backends.backend_pdf import PdfPages

def print_all_traindata(train_data, all_ids):
    #train data is the formatted data for the machine
    #this is solely for the raw data

    print(len(train_data))
    print(len(all_ids))

    id_counter = 0
    os.chdir("..")
    pdf = PdfPages('rawDataGraphs.pdf')

    for ind in train_data:

        plt.figure(figsize=(8,6))

        plt.plot(ind["time"], ind["aT"])
        plt.ylim(0, 100)
        plt.title("Plot for " + all_ids[id_counter])
        plt.xlabel("Time (seconds)")
        plt.ylabel("Acceleration (m/s2)")

        id_counter += 1

        pdf.savefig()
        plt.close()
        #plt.show()
    pdf.close()


#change the directory so pandas can find the csv files
def change_dir():

    try:
        os.chdir("data")
    except:
        print("Already in that location!")

#run a quick function to get all filenames in the directory
def get_all_files():

    all_files = os.listdir()

    return all_files

def find_mean(data): #use the statistics library to find the mean of the acceleration data for 
                     #each person's gait types
    return statistics.mean(data["aT"])

def remove_outliers(data): #run this once we have the mean to remove any outliers
    no_outliers = []
    
    std = numpy.std(data["data"]["aT"]) #get the standard deviation
    #print(str(std) + "\n\n\n")

    #now find the upper and lower limits that define outliers
    outlier_threshold_upper = float(data["mean"] + (2 * std))
    outlier_threshold_lower = float(data["mean"] - (2 * std))

    #remove them from the dataset
    for datapoint in data["data"]["aT"]:
        if datapoint <= outlier_threshold_upper:
            no_outliers.append(datapoint)
        elif datapoint >= outlier_threshold_lower:
            no_outliers.append(datapoint)
        else:
            print("Outlier detected! Exterminate!")

    return no_outliers


def get_typing(data_id):
    g_type = "none"

    #print(data_id)

    if data_id.endswith("N") == True:
        g_type = "normal"
    elif data_id.endswith("T") == True:
        g_type = "toe-walk"
    elif data_id.endswith("F") == True:
        g_type = "flatfoot"
    elif data_id.endswith("S") == True:
        g_type = "skew foot"
    else:
        print("There has been a problem for this one, chief")

    return g_type


#use pandas to extract the csv data
def read_csv(filename):
    #only extract the time and average acceleration for now, easy to modify later
    file_extract_csv = pd.read_csv(filename, usecols=["time", "aT"])
    name = filename.split(".")

    mean = find_mean(file_extract_csv)

    file_extract = {
        "id" : name[0],
        "data" : file_extract_csv,
        "mean" : mean, #this will be important later, hopefully
        "type" : get_typing(name[0])
    }

    file_extract["data"]["aT"] = remove_outliers(file_extract)

    #print(file_extract["id"])

    return file_extract

def get_everything():
    change_dir()
    raw_csvs = get_all_files()

    extracted_csvs = []

    for csv in raw_csvs:
        temp = read_csv(csv)
        extracted_csvs.append(temp)

    return extracted_csvs

def get_all_names(dataset):
    all_ids = []
    for data in dataset:
        all_ids.append(data["id"])

    return all_ids

def just_data(dataset):
    all_data = []

    for dict in dataset:
        all_data.append(dict["data"])

    return all_data

def main_extract():

    return get_everything()

#this just made a pdf with all the graphs printed into one
#for ease and everything
"""
data = main_extract()
names = get_all_names(data)
just_data = just_data(data)

print_all_traindata(just_data, names)
"""


