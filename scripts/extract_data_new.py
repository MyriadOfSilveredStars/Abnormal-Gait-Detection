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

#change the directory so pandas can find the csv files
def change_dir():

    try:
        os.chdir(".venv")
        os.chdir("all_data")
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

def main_extract():

    return get_everything()

#main_extract()