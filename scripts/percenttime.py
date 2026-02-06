#The premise of this is to assume that, whilst people might walk at different speeds and
#therefore have higher or lower acceleration cycles, they still walk in a cyclical fashion
#So we find the average acceleration for each person and change each data point to a 
#percentage of that mean. This normalises the data across each person and hopefully is more 
# accurate. 
# Let's begin

import numpy as np
import statistics
import itertools

from extract_data_new import main_extract


def find_troughs_peaks(ind_data):
    #this finds only the top and bottom 10% of the gait cycle, aka the troughs and peaks
    #perhaps the repeating patterns will be more illustrative of each gait?

    num_values = len(ind_data)
    extreme_percent = int(num_values * 0.1)

    peaks_n_troughs = []

    for i in range(0, extreme_percent):
        biggest = max(ind_data)
        smallest = min(ind_data)

        ind_data.remove(biggest)
        ind_data.remove(smallest)

        peaks_n_troughs.append(biggest)
        peaks_n_troughs.append(smallest)

    #del peaks_n_troughs[200:num_values-1]

    #print(len(peaks_n_troughs))
    return peaks_n_troughs

def tiny_chunks(ind_data):
    #takes the list of peaks and troughs and divvies it into small chunks
    #of about 20, say, for Peak Data Levels
    chunk_size = 200
    splice_list = []

    split_list = list(itertools.batched(ind_data["data"], chunk_size))

    for splice in split_list:
        if len(splice) == chunk_size:
            splice_dict = {
                "id" : ind_data["id"],
                "data" : splice,
                "type" : ind_data["type"]
            }
            splice_list.append(splice_dict)

    return splice_list

def the_percenterr(ind_data):
    #print("Finding data as a percentage...")
    mean = ind_data["mean"]
    percentages = []

    for data_point in ind_data["data"]["aT"]:
        #find what this value is as a percentage of the mean
        #value/mean

        diff = data_point - mean

        percentage = (diff / mean) * 100
        percentages.append(percentage)


    return percentages


def main_percent(data_full):

    all_chunks = [] #a huge list of all the tiny, 20-bit chunk dictionaries

    for ind_data in data_full:
        ind_data["data"] = the_percenterr(ind_data)

        ind_data["data"] = find_troughs_peaks(ind_data["data"])

        ind_data["data"] = tiny_chunks(ind_data)

        all_chunks = all_chunks + ind_data["data"]

    print("\n The values have been changed to percentages of the mean:")
    #print(data_full[1])
    #print(all_chunks[1]["data"])
    #print("Number of chunks:", len(all_chunks[1]["data"]))

    return all_chunks


#data = main_extract()
#main_percent(data) 


