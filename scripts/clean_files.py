# File to hold all the code that cleans the csv files before they're used
import os
import pandas as pd

def convert_csv_txt(filename):
    txt_filename = filename.replace(".csv", ".txt")
    
    #turn the csv file into a text file
    with open(filename, 'r') as f_in, open(txt_filename, 'w') as f_out:
        content = f_in.read()
        f_out.write(content)

        f_in.close()
        f_out.close()
        
    delete_preamble(txt_filename)

def delete_preamble(filename):
    #code from https://www.geeksforgeeks.org/python/python-program-to-delete-specific-line-from-file/
    print("Deleting Preamble...")


    with open(filename, 'r') as fr:
        # reading line by line
        lines = fr.readlines()

        #remove the (m/s^2) from the headers
        lines[3] = lines[3].replace(" (m/s^2)", "")
    
        # opening in writing mode
        with open(filename, 'w') as fw:
            for line in lines:
            
                # we want to remove the first 3, which is the preamble
                if line.count("#") == 0:
                    fw.write(line)
    print("Deleted!")

    convert_txt_csv(filename) #time to convert to a .csv again

def convert_txt_csv(filename):
    csv_filename = filename.replace(".txt", ".csv")

    #have pandas read the file as a csv, and then export it as such
    txtfile = pd.read_csv(filename)
    txtfile.to_csv(csv_filename, index = None)

    #finally, remove the temporary text file
    os.remove(filename) 

def main_clean():
    try:
        os.chdir(".venv")
        os.chdir("csv_files")
    except:
        print("Already in that location!")

    print("Foreign Contaminant!")

    #get all files in folder
    all_files = os.listdir()

    for filename in all_files:
        print("\n")
        print(filename)
        convert_csv_txt(filename)
    
main_clean()