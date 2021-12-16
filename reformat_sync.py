######SYNCING THE DATASET#######
#1. Note the sample rates of each device. The wristband samples 4 cycles per second and the eyetracker cycles 50 times per second.
#2. The eyetracker was generally started AFTER the wristband, subtract the start time (given in iso 8601 which needs to be converted to Unix time) for the eyetracker from the start time(Unix) of the wristband. This gives us the difference between the two in seconds.
#3. We know the sample rate of the eyetracker is 50 cycles per second or 0.02 seconds per new reading. If we take our value containing the start times of each device and divide it by 0.02, that gives us the number of items that need to be removed from the beginning of the eyetracker data to properly “sync” the time stamps of the two devices.
#4. Now we run into another issue. The eyetracker sample rate of 50 cycles per second cannot be divided by the wristband’s sample rate evenly. We get 12.5 eyetracker readings per every 4 wristband cycles, which is not presentable as data because you can’t have half of an eyetracker reading. Becuase of this we need to trim down our eyetracker data further. 
#5. To resolve this issue we must remove every 49th and 50th entry so that we’re left with a new sample rate of the eyetracker: 48 cycles per second. Now this new rate is divisible by our wristband sample rate of 4. 
#6. Finally, we need to correlate the data and combine it all into one spreadsheet. This is done by reading the EDA values in order and for each EDA value appending 12 (48/4) eyetracker values. 
#7. And this is all written out to an xlsx file for data analysis afterwards.
################################

import pandas as pd
import json
import csv
import tkinter as tk
from tkinter import filedialog
import dateutil.parser as dp

root_tk = tk.Tk()
root_tk.withdraw()

print("Please select the participant directory:")
root = filedialog.askdirectory()
print("Please select your eye tracker folder")
gazedata_folder = filedialog.askdirectory()
print("Please select your EDA file")
eda_filepath = filedialog.askopenfilename()
print("Please type the label for the output files")
output_name = input("Identifier for data: ")
print("Please select the path to the target folder")
output_folder = filedialog.askdirectory()

gazedata_path = gazedata_folder + "/" + "gazedata"
recording_file = gazedata_folder + "/recording.g3"

gaze_objects = []
eda_lines = []

with open(recording_file) as f:
    data = json.load(f)
with open(root + "/WristBand/EDA.csv", newline="") as f:
    csv_reader = csv.reader(f)
    wristband_start_time = float(next(csv_reader)[0])

eyetracker_start_time_parsed = dp.parse(data["created"])
eyetracker_start_time = float(eyetracker_start_time_parsed.timestamp())#convert the eyetracker timestamp from iso 8601 to Unix. 
start_time_diff = abs(eyetracker_start_time - wristband_start_time) #this gives us the offset between the two start times of the equipment (wristband/eyetracker).

tracker = 0
if eyetracker_start_time < wristband_start_time:
    #The eyetracker started first, so we need to use our time diff variable to cut off the unsynced portion of the data on the eyetracker data.
    #also we need to cut out every 25th and 50th element of the dataset.
    with open(gazedata_path) as eyetracker_file: #open the original line by line to append our JSON objects
        for i, jsonObj in enumerate(eyetracker_file):
            if i >= start_time_diff/0.02 and tracker < 25 :#make sure that the data for the eyetracker and wristband start at the same time.
                gaze_obj = json.loads(jsonObj)
                gaze_objects.append(gaze_obj)
            else:
                print("Reset the tracker!")
                tracker = 0
            print(str(i) + " elements sorted")
            tracker+= 1
    with open(eda_filepath, newline="") as eda_file:
        csv_reader = csv.reader(eda_file)
        header = next(csv_reader)
        sample_rate = next(csv_reader)

        for eda in f:
            eda_lines.append(float(eda))
else:

    with open(gazedata_path) as f: #open the original line by line to append our JSON objects
        for i, jsonObj in enumerate(f):
            if tracker < 24 :
                gaze_obj = json.loads(jsonObj)
                gaze_objects.append(gaze_obj)
            else:
                print("Reset the tracker!")
                tracker = 0
            print(str(i) + " elements sorted")
            tracker += 1
    with open(eda_filepath) as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        sample_rate = next(csv_reader)

        for i,eda in enumerate(csv_reader):
            print(i)
            if i >= (start_time_diff/0.25) - 3:
               eda_lines.append(eda)

gaze_out = output_folder + "/gazedata_reformatted_" +output_name +".json"
eda_out = output_folder + "/eda_reformatted" + output_name + ".csv"

with open(gaze_out, "w") as outfile: #write out our reformatted JSON.
    json.dump(gaze_objects, outfile, indent=4)

with open(eda_out, 'w') as file:
    mywriter = csv.writer(file)
    mywriter.writerows(eda_lines)

##########################################
#Sync the data now
##########################################

print("Please selected the formatted EDA file: ")
eda_csv_path = filedialog.askopenfilename()
print("Please selected the formatted gazedata file: ")
formatted_gaze_data_path = filedialog.askopenfilename()
print("Please selected the target folder to write to: ")
output_folder = filedialog.askdirectory()

output_data = {
    "Left Pupil Diameter": [],
    "Right Pupil Diameter": [],
    "EDA": [],
    "Timestamp (Seconds)": [],
    "Timestamp (Minutes)": [],
    "Timestamp List (the timestamps of the diameter values that make up the average values)": []
}
with open(formatted_gaze_data_path) as file:
    gazedata = json.load(file)

gazedata_length = len(gazedata)

tracker = 0
with open(eda_csv_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    sample_rate = next(csv_reader)

    for i,row in enumerate(csv_reader): #since the EDA readings happen more frequently, base each new data entry on individual EDA readings.
        output_data["EDA"].append(float(row[0]))
        left_pupil_values,right_pupil_values = [],[]
        timestamps = []
        try:
            while gazedata[tracker]["timestamp"] < (i * 0.25) + 0.25: 
                try:
                    left_pupil_values.append(gazedata[tracker]["data"]["eyeleft"]["pupildiameter"])
                except:
                    print("No Data")

                try:
                    right_pupil_values.append(gazedata[tracker]["data"]["eyeright"]["pupildiameter"])
                except:
                    print("No Data")
                try:
                    timestamps.append(gazedata[tracker]["timestamp"])
                except:
                    timestamps.append("No Data")
                tracker += 1

        except:
            print("No more timestamps")

        try:
            output_data["Left Pupil Diameter"].append(sum(left_pupil_values)/len(left_pupil_values))
        except:
            output_data["Left Pupil Diameter"].append("Not enough values to calculate average")

        try:
            output_data["Right Pupil Diameter"].append(sum(right_pupil_values)/len(right_pupil_values))
        except:
            output_data["Right Pupil Diameter"].append("Not enough values to calculate average")
        
        try:
            output_data["Timestamp List (the timestamps of the diameter values that make up the average values)"].append(timestamps)
        except:
            output_data["Timestamp List (the timestamps of the diameter values that make up the average values)"].append("No Data")
        output_data["Timestamp (Seconds)"].append(i*0.25)
        output_data["Timestamp (Minutes)"].append(round(i*0.25/60,2))

output_df = pd.DataFrame(output_data)
output_csv = output_df.to_excel(output_folder + "/synced-data-1.xlsx", sheet_name="Wristband and Eyetracker Data",index=False)
