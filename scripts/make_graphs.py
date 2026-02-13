# This file contains the code needed to create graphs of various .csv files
# It is very changeable depending on the graphs you want to make

import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

#from clean_files import main_clean
from extract_data_new import main_extract
from percenttime import main_percent

def print_all_traindata(train_data, all_ids):
    #train data is the formatted data for the machine

    print(len(train_data))
    print(len(all_ids))

    id_counter = 0
    os.chdir("..")
    pdf = PdfPages('fourieredGraphs.pdf')

    for ind in train_data:
        #print(ind)
        x_axis = list(range(0, len(ind)))

        plt.figure(figsize=(8,6))

        plt.plot(x_axis, ind)
        plt.ylim(0, 1)
        plt.title("Plot for " + all_ids[id_counter])
        plt.xlabel("I can't remember what this axis was supposed to be")
        plt.ylabel("Frequency")

        id_counter += 1

        pdf.savefig()
        plt.close()
        #plt.show()
    pdf.close()



def select_data(data):
    #this lets me choose which volunteer and leg I want to look at
    #because guessing their index was annoying and this is faster
    vol_num = input("Please enter the volunteer number >>> ")
    leg = input("Please enter which leg: L or R >>> ")

    indices = []

    for ind in data: #basically finds all the indices where IDs contain the number and leg
        #should be four, will throw an exception if not
        if ind["id"].find(vol_num) != -1 and ind["id"].find(leg) != -1:
            indices.append(data.index(ind))

    return indices


def draw_percent_graphs(data):

    indices = select_data(data)

    data1 = indices[0]
    data2 = indices[1]
    data3 = indices[2]
    data4 = indices[3]

    fig, axs = plt.subplots(2,2)

    axs[0, 0].plot(list(range(0,len(data[data1]["data"]))), data[data1]["data"])
    axs[0, 0].set_title(data[data1]["id"])
    axs[0, 1].plot(list(range(0,len(data[data2]["data"]))), data[data2]["data"], 'tab:orange')
    axs[0, 1].set_title(data[data2]["id"])
    axs[1, 0].plot(list(range(0,len(data[data3]["data"]))), data[data3]["data"], 'tab:green')
    axs[1, 0].set_title(data[data3]["id"])
    axs[1, 1].plot(list(range(0,len(data[data4]["data"]))), data[data4]["data"], 'tab:red')
    axs[1, 1].set_title(data[data4]["id"])

    for ax in axs.flat:
        ax.set(xlabel='Arbitrary Unit', ylabel='Percentage of Difference from Mean Acceleration', ylim = (-100, 800))

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    plt.show()
    

def draw_graph(data):
    #draw a graph for each set of data

    data1 = 21
    data2 = 2
    data3 = 20
    data4 = 1

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(data[data1]["data"]['time'], data[data1]["data"]['aT'])
    axs[0, 0].set_title(data[data1]["id"])
    axs[0, 1].plot(data[data2]["data"]['time'], data[data2]["data"]['aT'], 'tab:orange')
    axs[0, 1].set_title(data[data2]["id"])
    axs[1, 0].plot(data[data3]["data"]['time'], data[data3]["data"]['aT'], 'tab:green')
    axs[1, 0].set_title(data[data3]["id"])
    axs[1, 1].plot(data[data4]["data"]['time'], data[data4]["data"]['aT'], 'tab:red')
    axs[1, 1].set_title(data[data4]["id"])

    for ax in axs.flat:
        ax.set(xlabel='Time (seconds)', ylabel='Total Acceleration (m/s^2)', ylim = (0, 90))

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    plt.show()


def main():
    print("It's Graph Time")

    #main_clean() #only need to call this if new files have been added

    graph_data = main_extract()
    percent_data = main_percent(graph_data)

    try:
        #draw_graph(graph_data)
        draw_percent_graphs(percent_data)
    except:
        print("The selection didn't return four indices so it broke :(")

main()