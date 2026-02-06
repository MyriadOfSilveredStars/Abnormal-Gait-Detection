# This file contains the code needed to extract data from files
# It then returns the data to whichever other file called the method

import pandas as pd
import matplotlib.pyplot as plt
import os
import re

#change the directory so pandas can find the csv files
def change_dir():

    try:
        os.chdir(".venv")
        os.chdir("csv_files")
    except:
        print("Already in that location!")


#run a quick function to get all filenames in the directory
def get_all_files():

    all_files = os.listdir()

    return all_files

#use pandas to extract the csv data
def read_csv(filename):
    #only extract the time and average acceleration for now, easy to modify later
    file_extract_csv = pd.read_csv(filename, usecols=["time", "aT"])
    name = filename.split(".")

    file_extract = {
        "id" : name[0],
        "data" : file_extract_csv
    }

    return file_extract

def get_everything():
    change_dir()
    raw_csvs = get_all_files()

    extracted_csvs = []
    snipped_extracts = []

    for csv in raw_csvs:
        temp = read_csv(csv)
        extracted_csvs.append(temp)

    for extract in extracted_csvs:
        snipped_extract = remove_inactivity(extract)
        snipped_extracts.append(snipped_extract)

    all_extracts = split_csvs(snipped_extracts)

    return all_extracts

def extract_exact_name(data_id):
    vol_no = ''.join(re.findall(r'\d', data_id)) #get the vol number
    sensor = ''.join(re.findall(r'[LRP]', data_id)) #get the sensor type
    location = ''.join(re.findall(r'[WCZ]', data_id))#get location type

    return "vol" + vol_no + sensor + location

#code from https://bobbyhadz.com/blog/pandas-split-dataframe-into-chunks#split-a-pandas-dataframe-into-chunks-every-n-rows
def split_every_n_rows(dataframe, chunk_size):
    chunks = []
    num_chunks = 4

    for index in range(num_chunks):
        chunks.append(dataframe[index * chunk_size:(index+1) * chunk_size])

    return chunks


def split_csvs(extracted_data):
    split_data = [] #will be a VERY long list of dictionaries

    for data in extracted_data:
        name = extract_exact_name(data["id"]) #this gets the first bit of the name
        #then we can add the gait type after splitting the csv
        data_length = len(data["data"].index) // 4

        sections = split_every_n_rows(data["data"], data_length)
        normal_sec = {
            "id" : name + "N",
            "data" : sections[0]
        }

        toe_sec = {
            "id" : name + "T",
            "data" : sections[1]
        }
        flat_sec = {
            "id" : name + "F",
            "data" : sections[2]
        }
        skew_sec = {
            "id" : name + "S",
            "data" : sections[3]
        }

        split_data.append(normal_sec)
        split_data.append(toe_sec)
        split_data.append(flat_sec)
        split_data.append(skew_sec)
        
    return split_data

def remove_inactivity(data):
    df = data["data"]
    i = 0
    num_blanks = 0

    #print(df)

    while float(df['aT'].iloc[i]) <= 4.0:
        timestamp = df['time'].iloc[i]

        j = df[(df.time == timestamp)].index

        data["data"].drop(j, inplace = True)

        i += 1
        num_blanks += 1

    #print(df)
    #print("There were " + str(num_blanks) + " blank spaces")
    #print("\n\n")

    data["data"] = df
    return data

def snip_snip(data_seg):
    #removes periods of inactivity from the data
    #run this before and after splitting into four segments
    df = data_seg["data"]
    i = 0

    #print("Did have " + str(len(df['aT'])) + " rows")

    while float(df['aT'].iloc[i]) <= 7:
        timestamp = df['time'].iloc[i]

        j = df[(df.time == timestamp)].index

        data_seg["data"].drop(j, inplace = True)

        i += 1

    i = len(df['aT']) - 1

    while float(df['aT'].iloc[i]) <= 7:
        timestamp = df['time'].iloc[i]

        j = df[(df.time == timestamp)].index

        data_seg["data"].drop(j, inplace = True)

        i -= 1

    #print("Now has " + str(len(df['aT'])) + " rows")

    data_seg["data"] = df
    return data_seg


def main_extract():
    datastuff = get_everything()
    snipped_data = []

    for data_seg in datastuff:
        try:
            #print("\nData ID: " + data_seg["id"])
            snipped_data.append(snip_snip(data_seg))
        except TypeError as e:
            print("There's a string for some reason : " + str(e))
            continue

    return snipped_data

