#Sometimes, during the recording of the EDA values, the wristband would disconnect. This created multiple files
#That had to be dealt with. This prgram intakes multiple EDA files, compares their timestamps to sort them, and then finally stitches them together.
#Any reading that is missed during the transition from one EDA file to another is populated with simply "No EDA"

import csv
import tkinter as tk
from tkinter import filedialog

root_tk = tk.Tk()
root_tk.withdraw()

#Some of the wristband files are seperated into multiple folders. This stictches them
#al together.

frequency = 4 #however many times per second the device reads an EDA value. In our case every quarter second.
raw_files = []
files_to_sort = {} #our hashmap to correlate timestamps with their respective file paths
timestamp_map = []
values = [] #output values that will populate the final EDA file.

num_files = int(input("How many files do you need to stitch together?"))
for x in range(num_files):
    print("Please select file {}".format(x + 1))
    raw_files.append(filedialog.askopenfilename())#Create our list of files

for file in raw_files:
    with open(file, newline="") as f:
        csv_reader = csv.reader(f)
        ts = float(next(csv_reader)[0])
        files_to_sort[ts] = file
        timestamp_map.append(ts)

timestamp_map.sort()#sort the timestamps into a map so that we know what order the files are supposed to go in.

for i in range(len(timestamp_map)):
    with open(files_to_sort[timestamp_map[i]], newline="") as file:
        csv_reader = csv.reader(file)
        ts_skip = next(csv_reader)
        frequency_skip = next(csv_reader)

        for row in enumerate(csv_reader):
            print("Appending row: " + str(row))
            values.append(float(row[1][0]))

    if i != len(timestamp_map)-1: #evidently, the last file won't have any timestamps to compare to.
        print(i)
        diff = timestamp_map[i+1] - timestamp_map[i]
        for j in range(int(diff)*frequency):
            values.append("No EDA")
print(values)
print("Stitched "+ str(len(values)) + " values")

print("Where would you like to write the file to?")
with open(filedialog.askdirectory() + "/"+ input("Name of the participant for which these EDA values are for (No spaces):") + "_EDA.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow([timestamp_map[0]])#write the headers
    writer.writerow([frequency])

    # write the data
    for val in values:
        writer.writerow([val])