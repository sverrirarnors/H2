import csv
import random
import time

x_value = 0 #tími
gogn_1 = 1000
gogn_2 = 1000

fieldnames = ["x_value", "gogn_1", "gogn_2"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "gogn_1": gogn_1,
            "gogn_2": gogn_2
        }

        csv_writer.writerow(info)
        print(x_value, gogn_1, gogn_2)

        x_value += 1
        gogn_1 += random.randint(-6, 8)
        #gogn_1 = 5
        gogn_2 += random.randint(-5, 6)
        #gogn_2 = 3

    time.sleep(0.1)