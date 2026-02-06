# Code to turn the data into chunks that can be fourier transformed
# REMOVE THE TIME
# Okay and do the percentage thingie which will be explained in more detail lower down
import numpy as np
import statistics

from extract_data_new import main_extract

def the_fourierr(chunklet):
    #print("Fouriering...")
    #print(chunklet)
    fftout = np.fft.fft(chunklet) #fourier transform the data chunks

    # output is 500 complex numbers. real + imaginary

    magout = np.abs(fftout) #magnitude spectrum. amount of each freq in signal. real numbers

    magout = magout / np.max(magout) #normalises the data (?)
    #print(magout.shape)
    return magout #save that in the data part of the dictionary

#code from https://bobbyhadz.com/blog/pandas-split-dataframe-into-chunks#split-a-pandas-dataframe-into-chunks-every-n-rows
def split_every_n_rows(dataframe, chunk_size):
    chunks = []
    num_chunks = len(dataframe) // chunk_size

    for index in range(num_chunks):
        chunks.append(dataframe[index * chunk_size:(index+1) * chunk_size])

    return chunks


def the_chunkerr(data_sec):
    #print("Slicing data into chunks...")
    data_length = 500
    chunklet = split_every_n_rows(data_sec, data_length)

    return chunklet

def get_typing(chunk_id):
    g_type = "none"

    #print(chunk_id)

    if chunk_id.endswith("N") == True:
        g_type = "normal"
    elif chunk_id.endswith("T") == True:
        g_type = "toe-walk"
    elif chunk_id.endswith("F") == True:
        g_type = "flatfoot"
    elif chunk_id.endswith("S") == True:
        g_type = "skew foot"
    else:
        print("There has been a problem for this one, chief")

    return g_type

def main_fourier(data_full):
    print("Beginning the transforming...")
    # data here is an array of dictionaries, with an id and the dataframe for each
    # one element of an array is one volunteer's single gait type. 
    #print(data_full[5]["id"])
    #print(data_full[5]["data"])

    for sec in data_full:
        sec["data"] = the_chunkerr(sec["data"]["aT"]) #change the data into the chunks

    #print(data_full[5]["data"])

    all_chunklets = []
    
    for chunk in data_full:
        gait_type = get_typing(chunk["id"])
        for chunklet in chunk["data"]:
            chunklet_dict = {
                "id" : chunk["id"],
                "data" : the_fourierr(chunklet),
                "type" : gait_type
            }
            all_chunklets.append(chunklet_dict)

    #print(all_chunklets)
    return all_chunklets


#data = main_extract()
#main_fourier(data)