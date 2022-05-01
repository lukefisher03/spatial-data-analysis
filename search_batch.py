from time import time
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandas.io import excel
import numpy
import csv

root_tk = tk.Tk()
root_tk.withdraw()

repeat = True
print("What file would you like to search?")
file_to_search = filedialog.askopenfilename()
print("Where would you like to output the log?")
log_path = filedialog.askdirectory()


excel_df = pd.read_excel(file_to_search)

outfile = open(log_path + "/parsed_data.txt","w+")
outfile.write("Left Pupil   Right Pupil     EDA     Start      Stop")

left_avg, right_avg, eda_avg = [], [], []

def find_avearages(start, stop):
    time_range = []

    start_values = start.split(":")
    time_range.append((int((start_values[0])) * 60) + int(start_values[1]))
    stop_values = stop.split(":")
    time_range.append((int((stop_values[0])) * 60)+ int(stop_values[1]))
    
    left_diameters, right_diameters, edas = [],[],[]
    for i in range((time_range[0]*4), (time_range[1]*4)+1):
        line = excel_df.loc[i]
        #print("Searching for values at time: " + str(line["Timestamp (Seconds)"]) + " seconds")
        if type(line["Left Pupil Diameter"]) == float:
            left_diameters.append(line["Left Pupil Diameter"])
        if type(line["Right Pupil Diameter"]) == float:
            right_diameters.append(line["Right Pupil Diameter"])
        if type(line["EDA"]) in [float, numpy.float64]:
            edas.append(line["EDA"])
    #print("Searched " + str(((time_range[1]*4) - (time_range[0])*4)+1) + " rows")
    #print("Time range: {0} - {1}".format(start, stop))
    #print("Time range in seconds: {}".format(time_range))
    try:
        #print("The average left pupil diameter is: {:.3f}".format(sum(left_diameters)/len(left_diameters)))
        left = sum(left_diameters)/len(left_diameters)
    except:
        #print("There were no real numbers in this time range to calculate the average left pupil diameter")
        left = "NA"
    try:
        #print("The average right pupil diameter is: {:.3f}".format(sum(right_diameters)/len(right_diameters)))
        right = sum(right_diameters)/len(right_diameters)
    except:
        #print("There were no real numbers in this time range to calculate the average right pupil diameter")
        right = "NA"
    try:
        #print("The average EDA is: {:.3f}".format(sum(edas)/len(edas)))
        eda = sum(edas)/len(edas)
    except:
        #print("There were no real numbers in this time range to calculate the average EDA")
        eda = "NA"
    outfile.write(f"\n\n{left:.3}        {right:.3}              {eda:.3}      {start}       {stop}")
    left_avg.append(left)
    right_avg.append(right)
    eda_avg.append(eda)
times = [
#insert array of times to search here
]
#Since I'm hardcoding the function to run with inputted times into an array, this code is not needed, but ought to be kept for later use.
# while repeat:
#     find_avearages()
#     run_again = input("Would you like to re-run this program? (y/n)")
#     if run_again not in ["Yes", "yes", "y", "1", "ye", "Y", "Ye"]:
#         repeat = False


for i in range(len(times)-1):
    find_avearages(times[i], times[i+1])

index = 0
for left, right, eda in zip(left_avg, right_avg, eda_avg):
    index += 1
    
    try:
        print(f"{index}\t{left:.3f}\t{right:.3f}\t{eda:.3f}\n")
    except:
        print(f"{index}\t{left}\t{right}\t{eda}\n")



outfile.write("\n")
outfile.close()