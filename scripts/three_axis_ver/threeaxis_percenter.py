import numpy as np
import statistics
import itertools

from extract_3axis_data import get_everything

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

    del peaks_n_troughs[200:num_values-1]

    #print(len(peaks_n_troughs))
    return peaks_n_troughs

def the_percenterr(ind_data, mean):
    #print("Finding data as a percentage...")
    percentages = []

    ind_data = np.array(ind_data)
    ind_data = ind_data.squeeze()


    for data_point in ind_data:
        #find what this value is as a percentage of the mean
        #value/mean
        
        diff = data_point - mean

        percentage = (diff / mean) * 100
        percentages.append(percentage)

    return percentages

def main_percent(data_full):
    #takes the data with three axis

    percent_data_x = []
    percent_data_y = []
    percent_data_z = []

    #first, find the percentages of each axis

    #print(data_full[1]["id"])
    #print(data_full[1]["dataX"])

    for sec in data_full:
        secType = sec["type"]
        secID = sec["id"]

        sec["dataX"] = the_percenterr(sec["dataX"], sec["mean"][0])
        sec["dataY"]= the_percenterr(sec["dataY"], sec["mean"][1])
        sec["dataZ"] = the_percenterr(sec["dataZ"], sec["mean"][2])

        x_dict = {
                "id" : secID,
                "data" : find_troughs_peaks(sec["dataX"]),
                "type" : secType
            }
        
        y_dict = {
                "id" : secID,
                "data" : find_troughs_peaks(sec["dataY"]),
                "type" : secType
            }
        
        z_dict = {
                "id" : secID,
                "data" : find_troughs_peaks(sec["dataZ"]),
                "type" : secType
            }

        percent_data_x.append(x_dict)
        percent_data_y.append(y_dict)
        percent_data_z.append(z_dict)

    return [percent_data_x, percent_data_y, percent_data_z]

#all_data = get_everything()
#main_percent(all_data)