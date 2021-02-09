import xlsxwriter
from random import random
t_rise = list()
for i in range(25):
    t_rise.append(random())
workbook = xlsxwriter.Workbook('Characterisation Results.xlsx')
worksheet = workbook.add_worksheet(name = "Tfall")
bold = workbook.add_format({'bold': 1})
input_nodes = ['A','B']
input_slew = [1.2,2.3,3.4,4.5,5.6]
output_capacitance = [0.06,0.18,0.42,0.99,0.19]

column = 'B'
row = 1
## Write Row Header
for i in range(len(input_slew)):
    index = column + str(row)
    worksheet.write(index, str(input_slew[i]) + " ns",bold)
    column = chr(ord(column)+1)

column = 'A'
row = 2 
## Write Column Header
for j in range(len(output_capacitance)):
    index = column + str(row)
    worksheet.write(index, str(output_capacitance[j]) + " pF",bold)
    row = row+1


column = 'B'
row = 2
m=0
for i in range(len(input_slew)):
    for j in range(len(output_capacitance)):
        index = chr(ord(column)+i) + str(row+j)
        worksheet.write(index, str(t_rise[m]) + " ns")
        m=m+1

# delete
worksheet = workbook.add_worksheet(name = "asdvaskdjv")
bold = workbook.add_format({'bold': 1})
input_nodes = ['A','B']
input_slew = [1.2,2.3,3.4,4.5,5.6]
output_capacitance = [0.06,0.18,0.42,0.99,0.19]

column = 'B'
row = 1
## Write Row Header
for i in range(len(input_slew)):
    index = column + str(row)
    worksheet.write(index, str(input_slew[i]) + " ns",bold)
    column = chr(ord(column)+1)

column = 'A'
row = 2 
## Write Column Header
for j in range(len(output_capacitance)):
    index = column + str(row)
    worksheet.write(index, str(output_capacitance[j]) + " pF",bold)
    row = row+1


column = 'B'
row = 2
m=0
for i in range(len(input_slew)):
    for j in range(len(output_capacitance)):
        index = chr(ord(column)+i) + str(row+j)
        worksheet.write(index, str(t_rise[m]) + " ns")
        m=m+1

workbook.close()
        
    
