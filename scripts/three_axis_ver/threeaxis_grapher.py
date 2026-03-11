# This file contains the code needed to create graphs of various .csv files
# It is very changeable depending on the graphs you want to make

import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

from extract_3axis_data import get_everything

def draw_graphs(data, indices):

    data1 = indices[0]
    data2 = indices[1]
    data3 = indices[2]
    data4 = indices[3]

    fig, axs = plt.subplots(2,2) #two by two graph for all four gaits

    axs[0, 0].plot(list(range(0,len(data[data1]["dataX"]))), data[data1]["dataX"], label="X-Axis")
    axs[0, 0].plot(list(range(0,len(data[data1]["dataY"]))), data[data1]["dataY"], label="Y-Axis")
    axs[0, 0].plot(list(range(0,len(data[data1]["dataZ"]))), data[data1]["dataZ"], label="Z-Axis")
    axs[0, 0].set_title(data[data1]["id"])



    axs[0, 1].plot(list(range(0,len(data[data2]["dataX"]))), data[data2]["dataX"], label="X-Axis")
    axs[0, 1].plot(list(range(0,len(data[data2]["dataY"]))), data[data2]["dataY"], label="Y-Axis")
    axs[0, 1].plot(list(range(0,len(data[data2]["dataZ"]))), data[data2]["dataZ"], label="Z-Axis")
    axs[0, 1].set_title(data[data2]["id"])



    axs[1, 0].plot(list(range(0,len(data[data3]["dataX"]))), data[data3]["dataX"], label="X-Axis")
    axs[1, 0].plot(list(range(0,len(data[data3]["dataY"]))), data[data3]["dataY"], label="Y-Axis")
    axs[1, 0].plot(list(range(0,len(data[data3]["dataZ"]))), data[data3]["dataZ"], label="Z-Axis")
    axs[1, 0].set_title(data[data3]["id"])



    axs[1, 1].plot(list(range(0,len(data[data4]["dataX"]))), data[data4]["dataX"], label="X-Axis")
    axs[1, 1].plot(list(range(0,len(data[data4]["dataY"]))), data[data4]["dataY"], label="Y-Axis")
    axs[1, 1].plot(list(range(0,len(data[data4]["dataZ"]))), data[data4]["dataZ"], label="Z-Axis")
    axs[1, 1].set_title(data[data4]["id"])

    for ax in axs.flat:
        ax.set(xlabel='Time (seconds)', ylabel='Acceleration (m/s^2)', ylim = (0, 50))

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    plt.title = "Acceleration in Three Axes Over Time"

    plt.show()

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


def main():
    print("It's Graph Time")

    graph_data = get_everything()


    try:
        #fetch the indices of the specific volunteer and leg
        selection_indices = select_data(graph_data)
        #print(selection_indices)

        #then create the graphs
        draw_graphs(graph_data, selection_indices)

    except:
        print("The selection didn't return four indices so it broke :(")

main()