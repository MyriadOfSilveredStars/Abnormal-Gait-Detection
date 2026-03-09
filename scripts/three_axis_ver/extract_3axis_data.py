import pandas as pd
import matplotlib as plt
import os
import re
import statistics
import numpy as np

def change_dir():
    try:
        os.chdir("data")
    except:
        print("Already in that location!")

def get_all_files():
    all_files = os.listdir()
    return all_files

def find_mean(data):
    means = [statistics.mean(data["ax"]), statistics.mean(data["ay"]), statistics.mean(data["az"])]
             
    return means

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

def reformat_data(file_extract):
    temp_x = []
    temp_y = []
    temp_z = []
    for i in range(0, len(file_extract["ax"])):
        temp_x.append(file_extract["ax"][i])
        temp_y.append(file_extract["ay"][i])
        temp_z.append(file_extract["az"][i])

    temp_x = pd.DataFrame(temp_x, columns=["ax"])
    temp_y = pd.DataFrame(temp_y, columns=["ay"])
    temp_z = pd.DataFrame(temp_z, columns=["az"])

    return [temp_x, temp_y, temp_z]



def read_csv(filename):
    file_extract_csv = pd.read_csv(filename, usecols=["time", "ax", "ay", "az"])

    name = filename.split(".")

    mean = find_mean(file_extract_csv)

    split_axis = reformat_data(file_extract_csv)

    file_extract = {
        "id" : name[0],
        "dataX" : split_axis[0],
        "dataY" : split_axis[1],
        "dataZ" : split_axis[2],
        "mean" : mean,
        "type" : get_typing(name[0])
    }

    return file_extract

def get_everything():
    change_dir()
    raw_csvs = get_all_files()
    
    extracted_csvs = []

    for csv in raw_csvs:
        temp = read_csv(csv)
        extracted_csvs.append(temp)

    #print(extracted_csvs[0])

    return extracted_csvs

#get_everything()