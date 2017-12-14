'''
Jeff Zhao (jiecheng.zhao@gmail.com)
12/06/3017

Python: Python3

Amend the Conversion Index of the data from UGA with reporting rate higher
than 100 Hz

Due to the defintion and bit limitation of the F-NET data protocol, there are
only two ASCII characters avaialbe for Conversion Index (ConvNum). Therefore,
all those whose ConvNum equal or over 100 lost their hundredths digit.

Requirement:

Data file:
Require the data in .csv file with the format of F-NET protocol, i.e. the columns
are Index, UnitID, Sample_Date&Time, ConvNum, FirstFreq, FinalFreq, VoltageAng,
VoltageMag, DateCreated, and TimeIndex, in sequence

Need to be sorted according to Index, ascending

Header or no Header in the first Column is fine

Reporting Rate:
Need to input this value
'''

import csv, sys, os

print("ConvNum convertion...")

if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    fileName = input("Please type the name of the csv file: ")

if len(sys.argv) < 3:
    strDataRate = input("What is the data rate (Hz)? ")
else:
    strDataRate = sys.argv[2]

try:
    datarate = int(strDataRate)
except:
    print("Data rate should be an integer value.")
    exit(1)

if datarate >= 200:
    print("Too large data rate. Wait for upgraded version to handle.")
    exit(1)

Index = []
UnitID = []
Sample_Date = []
ConvNum = []
FirstFreq = []
FinalFreq = []
VoltageAng = []
VoltageMag = []
DateCreated = []
TimeIndex = []

with open(fileName,'rt') as csv_in:
    csvreader = csv.reader(csv_in)
    for row in csvreader:
        Index_temp, UnitID_temp, Sample_Date_temp, ConvNum_temp, FirstFreq_temp,\
        FinalFreq_temp, VoltageAng_temp, VoltageMag_temp, DateCreated_temp,\
        TimeIndex_temp = row
        Index.append(Index_temp)
        UnitID.append(UnitID_temp)
        Sample_Date.append(Sample_Date_temp)
        ConvNum.append(ConvNum_temp)
        FirstFreq.append(FirstFreq_temp)
        FinalFreq.append(FinalFreq_temp)
        VoltageAng.append(VoltageAng_temp)
        VoltageMag.append(VoltageMag_temp)
        DateCreated.append(DateCreated_temp)
        TimeIndex.append(TimeIndex_temp)

# determine if first row is field name (header)
tableHeader = False
for i, Conv in enumerate(ConvNum):
    if (not Conv.isnumeric()):
        tableHeader = True
        continue
    elif i == 0:
        continue
    elif i == 1 and tableHeader == True:
        continue
    elif int(ConvNum[i]) < int(ConvNum[i-1]) and Sample_Date[i] == Sample_Date[i-1]:
        ConvNum[i] = str(int(ConvNum[i]) + 100)
    elif Sample_Date[i] != Sample_Date[i-1]:
        ConvNum[i] = str((int(ConvNum[i-1]) + int(Index[i]) - int(Index[i-1]))%datarate)
    else:
        continue

route, ext = os.path.splitext(fileName)
routeList = route.split('\\')
routeList[-1] = 'conv_' + routeList[-1]
newFileName = os.path.join('\\'.join(routeList) + ext)

with open(newFileName, 'wt', newline = '') as csv_out:
    csvwriter = csv.writer(csv_out)
    rows = zip(Index, UnitID, Sample_Date, ConvNum, FirstFreq, FinalFreq, \
    VoltageAng, VoltageMag, DateCreated, TimeIndex)
    # print(list(rows))
    csvwriter.writerows(rows)

print('Conversion finished!')
