#this finds the average acceleration in each gait type
# I hope

from extract_data import main_extract


def split_gaits(dataset):
    normal = []
    toe = []
    flat = []
    skew = []    


    for sec in dataset:
        if "N" in sec["id"]:
            normal.append(sec)
        elif "T" in sec["id"]:
            toe.append(sec)
        elif "F" in sec["id"]:
            flat.append(sec)
        elif "S" in sec["id"]:
            skew.append(sec)

    return [normal, toe, flat, skew]

def total_average_finder(set):
    total = 0
    div = len(set)

    for data in set:
        temp_total = data["data"]["aT"].sum()
        temp_avg = temp_total / len(data["data"].index)
        total += temp_avg

    average = total / div
    #print("The average acceleration is: " + str(average))

    return average

def all_averages_finder(full_set):
    averages = []

    for data in full_set[0]:
        temp_total = data["data"]["aT"].sum()
        temp_avg = temp_total / len(data["data"].index)
        averages.append(temp_avg)

    for data in full_set[1]:
        temp_total = data["data"]["aT"].sum()
        temp_avg = temp_total / len(data["data"].index)
        averages.append(temp_avg)

    for data in full_set[2]:
        temp_total = data["data"]["aT"].sum()
        temp_avg = temp_total / len(data["data"].index)
        averages.append(temp_avg)

    for data in full_set[3]:
        temp_total = data["data"]["aT"].sum()
        temp_avg = temp_total / len(data["data"].index)
        averages.append(temp_avg)

    return averages


def main_avg():
    dataset = main_extract()
    split_data = split_gaits(dataset)

    target_averages = []

    training_avgs = all_averages_finder(split_data)

    for set in split_data:
        value = total_average_finder(set)
        for i in range (0, 9):
            target_averages.append(value)

    return training_avgs, target_averages

main_avg()
