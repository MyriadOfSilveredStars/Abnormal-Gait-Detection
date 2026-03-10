import numpy as np
import pandas as pd

from extract_3axis_data import get_everything

def fourier(chunk):

    fftout = np.fft.fft(chunk) #fourier transform the data chunks

    magout = np.abs(fftout) #magnitude spectrum. amount of each freq in signal. real numbers
    magout = magout / np.max(magout) #normalises the data

    return magout #save that in the data part of the dictionary


def fourier_caller(data_chunk, column):
    #calls the fourier transformer for each axis

    chunk = fourier(data_chunk)

    chunk = pd.DataFrame(chunk, columns=[column])

    return chunk
        


def split_every_n_rows(data, chunk_size):
    chunks = []

    num_chunks = (len(data) // chunk_size)
    #each file is going to be different lengths and so have a different number of chunks

    for i in range(num_chunks):
        chunks.append(data[i * chunk_size:(i+1) * chunk_size])

    return chunks


def chunk_it(data_section):
    data_length = 500
    data_section = split_every_n_rows(data_section, data_length)

    return data_section

def main_fourier(data_full):
    print("It's Fourier Time...")

    fourier_data_x = []
    fourier_data_y = []
    fourier_data_z = []

    for sec in data_full:
        sec["dataX"] = chunk_it(sec["dataX"])
        sec["dataY"] = chunk_it(sec["dataY"])
        sec["dataZ"] = chunk_it(sec["dataZ"])

    #print(len(data_full[0]["dataX"]))

    for sec in data_full:
        gait_type = sec["type"]
        for chunk in sec["dataX"]:
            chunklet_dict = {
                "id" : sec["id"],
                "data" : fourier_caller(chunk, "ax"),
                "type" : gait_type
            }
            
            fourier_data_x.append(chunklet_dict)

    for sec in data_full:
        gait_type = sec["type"]
        for chunk in sec["dataY"]:
            chunklet_dict = {
                "id" : sec["id"],
                "data" : fourier_caller(chunk, "ay"),
                "type" : gait_type
            }
            
            fourier_data_y.append(chunklet_dict)

    for sec in data_full:
        gait_type = sec["type"]
        for chunk in sec["dataZ"]:
            chunklet_dict = {
                "id" : sec["id"],
                "data" : fourier_caller(chunk, "az"),
                "type" : gait_type
            }
            
            fourier_data_z.append(chunklet_dict)

    #print(len(fourier_data_x))

    return [fourier_data_x, fourier_data_y, fourier_data_z]


"""
all_data = get_everything()
#print(len(all_data))
stuff = main_fourier(all_data)
print("Successfully fouried shit")
print(np.shape(stuff))
"""
