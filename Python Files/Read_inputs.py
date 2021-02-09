import csv
import os
Netlists_Total = os.listdir("../Characterization/Netlists")
i = 1 
while(i<len(Netlists_Total)):
    if(Netlists_Total[i].endswith(".cir")) == False:
        Netlists_Total.pop(i)
    else:
        i=i+1
    
for i in range(len(Netlists_Total)):
    print( str(i) + " : " + Netlists_Total[i])
    

print("\n")
choice = input("Enter the index of the circuit to be characterised \n")
choice_file = Netlists_Total[int(choice)]
input_read_file = choice_file.split(".")[0]
data = list()
with open("../Characterization/Netlists/"+input_read_file + '.csv', newline='') as csvfile:
    input_data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in input_data:
        data.append(row)
        
input_nodes = list()
i=1
temp = str(data[0][0]).split(",")
while(i<len(temp)):
    if temp[i].isalnum() == True :
        input_nodes.append(temp[i])
    i=i+1

output_nodes = list()
i=1
temp = str(data[1][0]).split(",")
while(i<len(temp)):
    if temp[i].isalnum() == True :
        output_nodes.append(temp[i])
    i=i+1

Vdd = float(data[2][0].split(",")[1])
T = float(data[3][0].split(",")[1])

input_slew = list()
i=1
temp = str(data[4][0]).split(",")
while(i<len(temp)):
    if len(temp) > 0 :
        input_slew.append(temp[i])
    i=i+1

output_capacitance = list()
i=1
temp = str(data[5][0]).split(",")
while(i<len(temp)):
    if len(temp[i]) > 0 :
        output_capacitance.append(temp[i])
    i=i+1
