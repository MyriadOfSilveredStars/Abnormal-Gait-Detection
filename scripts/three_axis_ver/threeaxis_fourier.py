import numpy as np

from extract_3axis_data import get_everything

def fourier(chunk):

    fftout = np.fft.fft(chunk) #fourier transform the data chunks

    magout = np.abs(fftout) #magnitude spectrum. amount of each freq in signal. real numbers
    magout = magout / np.max(magout) #normalises the data

    return magout #save that in the data part of the dictionary


def fourier_caller(data):
    #calls the fourier transformer for each axis

    for chunk in data:
        chunk = fourier(chunk)

    return data


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

    fourier_data = []

    for sec in data_full:
        sec["data"] = chunk_it(sec["data"])


    for sec in data_full:
        gait_type = sec["type"]
        
        chunklet_dict = {
            "id" : sec["id"],
            "data" : fourier_caller(sec["data"]),
            "type" : gait_type
        }
        
        fourier_data.append(chunklet_dict)


    #print(fourier_data[0])
    return fourier_data


"""
all_data = get_everything()
stuff = main_fourier(all_data)
print("Successfully fouried shit")
print(stuff[0])
"""