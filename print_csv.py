import csv
import glob
import os
fp = "C:\\Users\\camer\\Desktop\\test_1\\*"

# get the latest file in the folder
list_of_files = glob.glob(fp)
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


def print_out_csv():

    try:
        with open(latest_file, "r") as f:
            csv_r = csv.reader(f)
            for row in csv_r:
                print(row)
    except FileNotFoundError:
        print("No such file exits")


print_out_csv()