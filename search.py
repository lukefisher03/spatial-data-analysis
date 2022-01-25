from time import time
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandas.io import excel
import numpy

root_tk = tk.Tk()
root_tk.withdraw()

repeat = True
print("What file would you like to search?")
file_to_search = filedialog.askopenfilename()

excel_df = pd.read_excel(file_to_search)
def find_avearages():
    time_range = []
    start = input("In the range of times to search, what would you like the start time to be(minutes:seconds) - ")
    stop = input("In the range of times to search, what would you like the end time to be(minutes:seconds) - ")

    start_values = start.split(":")
    time_range.append((int((start_values[0])) * 60) + int(start_values[1]))
    stop_values = stop.split(":")
    time_range.append((int((stop_values[0])) * 60)+ int(stop_values[1]))
    
    left_diameters, right_diameters, edas = [],[],[]
    for i in range(time_range[0], time_range[1]+1):
        line = excel_df.loc[i]
        print("Searching for values at time: " + str(line["Timestamp (Seconds)"]) + " seconds")
        if type(line["Left Pupil Diameter"]) == float:
            left_diameters.append(line["Left Pupil Diameter"])
        if type(line["Right Pupil Diameter"]) == float:
            right_diameters.append(line["Right Pupil Diameter"])
        if type(line["EDA"]) in [float, numpy.float64]:
            edas.append(line["EDA"])
    print("Searched " + str((time_range[1] - time_range[0])) + " rows")
    try:
        print("The average left pupil diameter is: " + str(sum(left_diameters)/len(left_diameters)))
    except:
        print("There were no real numbers in this time range to calculate the average left pupil diameter")
    try:
        print("The average right pupil diameter is: " + str(sum(right_diameters)/len(right_diameters)))
    except:
        print("There were no real numbers in this time range to calculate the average right pupil diameter")
    try:
        print("The average EDA is: " + str(sum(edas)/len(edas)))
    except:
        print("There were no real numbers in this time range to calculate the average EDA")

while repeat:
    find_avearages()

    run_again = input("Would you like to re-run this program? (y/n)")
    if run_again not in ["Yes", "yes", "y", "1", "ye", "Y", "Ye"]:
        repeat = False