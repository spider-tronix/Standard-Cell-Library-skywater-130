import subprocess
import os
import csv
import xlsxwriter
def Netlist_Build(output_nodes,input_nodes,Pulse_Node,input_slew,output_capacitance,Time_Period,Vdd,source_circuit):
    
    print ("\n for input " + Pulse_Node +  " vs " + " output node Y\n" )
    temp_circuit = source_circuit[:]
    temp_circuit.append("CL " + output_nodes[0] + " " + "0 " + output_capacitance + "F")
    
    ## Pulsating Node :  Syntax 	 PULSE(V1 V2 TD TR TF PW PER) Ex : V2 A 0 PULSE(0 1.8 0 0 0 5 10)
    ## V2 A 0 PULSE(0 1.8 0 0.06n 0.06n 10.0n 20n)
    temp_circuit.append("V2 " + Pulse_Node + " 0" + " PULSE(0 " + str(Vdd) + " 0 " +  input_slew + " "  + input_slew + " " + str(Time_Period/2) + "n " + str(Time_Period) + "n)")
    
    ## other input nodes
    k=3
    for i in range(len(input_nodes)):
        if((input_nodes[i]!=Pulse_Node)):
            temp_circuit.append("V" + str(k) + " " + input_nodes[i] + " 0 1.8")
            
    ## Add .tran command
    temp_circuit.append(".tran 0.001n 50n")

    ## Add control commands
    temp_circuit.append(".control")
    temp_circuit.append("run")
    temp_circuit.append("wrdata "+Pulse_Node+"_"+input_slew + "_" + output_capacitance +  ".data" + " v(Y) " + "v(" +  Pulse_Node + ")")
    temp_circuit.append(".endc")
    ## Add .end command 
    temp_circuit.append(".end")
    
    ## Concatenate all Values
    result = ''
    for l in range(len(temp_circuit)):
        result = result + "\n" + temp_circuit[l]
##    print(result)

    ## Return Result
    return result

def NgSpice_Run(input_nodes,input_slew,output_capacitance):
    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                try:
                    filename = str(i)+str(j)+str(k)+".cir"
                    command = "ngspice -b ../Characterization/" + filename 
                    subprocess.check_call(command,shell=True)
                    #a = subprocess.check_output(['ngspice', '-b', filename], shell=True). subprocess.check_call()
                except:
                    print(filename + " spice file executed")
                    
    print("NGSpice Simulation Runs Successfully completed")

def Characterization_run(input_nodes,input_slew,output_capacitance,pulse_node,slew_lower_threshold,slew_upper_threshold,Vdd):
    filename = pulse_node+"_"+input_slew + "_" + output_capacitance +  ".data"
    #filename = "A_0.6n_0.1.data"
    file = open(filename,"r")
    vectors = file.read()
    vectors = vectors.split("\n")
    Vout = list()
    Vin = list()
    t = list()
    values = list()
    for i in range(len(vectors)):
        values_temp = vectors[i].split(" ")
        values = list()
        for j in range(len(values_temp)):
            if (len(values_temp[j])!=0):
                values.append(values_temp[j])
        try:
            t.append(float(values[0]))
        except:
            print("T Read complete")
        try:
            Vout.append(float(values[1]))
        except:
            print("Vout Read Complete")     
        try:
            Vin.append(float(values[3]))
        except:
            print("Vin Read Complete")
        values.clear()
        
    
    V_out_upper_threshold = (slew_uppper_threshold/100)*Vdd
    V_out_lower_threshold = (slew_lower_threshold/100)*Vdd
    V_out_mid_threshold = 0.5*Vdd

    V_out_upper_line = list()
    V_out_upper_line_slope = list()
    V_out_lower_line = list()
    V_out_lower_line_slope = list()
    V_out_mid_line = list()
    V_out_mid_line_slope = list()

    for i in range(len(Vout)):
        if(abs(Vout[i] - V_out_upper_threshold)<0.1):
            V_out_upper_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_upper_line_slope.append(-1)
            else:
                V_out_upper_line_slope.append(1)
            #print(str(V_out_upper_threshold) + " " + str(Vout[i]))
        if(abs(Vout[i] - V_out_lower_threshold)<0.1):
            V_out_lower_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_lower_line_slope.append(-1)
            else:
                V_out_lower_line_slope.append(1)
        if(abs(Vout[i] - V_out_mid_threshold)<0.1):
            V_out_mid_line.append(i)
            if(Vout[i]-Vout[i-1]<0):
                V_out_mid_line_slope.append(-1)
            else:
                V_out_mid_line_slope.append(1)

##                
##            print(str(V_out_upper_threshold) + " " + str(Vout[i]))
##            print(str(V_out_lower_threshold) + " " + str(Vout[i]))
            
##    print(V_out_upper_line)
##    print(V_out_upper_line_slope)
##    print(V_out_lower_line)
##    print(V_out_lower_line_slope)

    i = 1
    while(i<len(V_out_upper_line)):
        if(V_out_upper_line_slope[i-1]==V_out_upper_line_slope[i]):
            if(Vout[V_out_upper_line[i]]-V_out_upper_threshold > Vout[V_out_upper_line[i-1]]-V_out_upper_threshold):
                V_out_upper_line.pop(i)
                V_out_upper_line_slope.pop(i)
            else:
                V_out_upper_line.pop(i-1)
                V_out_upper_line_slope.pop(i-1)
        else:
            i=i+1
            
    i = 1
    while(i<len(V_out_lower_line)):
        if(V_out_lower_line_slope[i-1]==V_out_lower_line_slope[i]):
            if(Vout[V_out_lower_line[i]]-V_out_lower_threshold > Vout[V_out_lower_line[i-1]]-V_out_lower_threshold):
                V_out_lower_line.pop(i)
                V_out_lower_line_slope.pop(i)
            else:
                V_out_lower_line.pop(i-1)
                V_out_lower_line_slope.pop(i-1)
        else:
            i=i+1

    i = 1
    while(i<len(V_out_mid_line)):
        if(V_out_mid_line_slope[i-1]==V_out_mid_line_slope[i]):
            if(Vout[V_out_mid_line[i]]-V_out_mid_threshold > Vout[V_out_mid_line[i-1]]-V_out_mid_threshold):
                V_out_mid_line.pop(i)
                V_out_mid_line_slope.pop(i)
            else:
                V_out_mid_line.pop(i-1)
                V_out_mid_line_slope.pop(i-1)
        else:
            i=i+1


##
##    print("filtered Values")
##    print("V_out_upper")
##    print(V_out_upper_line)
##    print(V_out_upper_line_slope)
##    print("V_out_mid")
##    print(V_out_mid_line)
##    print(V_out_mid_line_slope)
##    print("V_out_lower")
##    print(V_out_lower_line)
##    print(V_out_lower_line_slope)

    V_in_mid_line = list()
    V_in_mid_line_slope = list()
    V_in_mid_threshold = 0.5*Vdd

    for i in range(len(Vin)):
        if(abs(Vin[i] - V_in_mid_threshold)<0.1):
            V_in_mid_line.append(i)
            if(Vin[i]-Vin[i-1]<0):
                V_in_mid_line_slope.append(-1)
            else:
                V_in_mid_line_slope.append(1)


    i = 1
    while(i<len(V_in_mid_line)):
        if(V_in_mid_line_slope[i-1]==V_in_mid_line_slope[i]):
            if(Vin[V_in_mid_line[i]]-V_in_mid_threshold > Vin[V_in_mid_line[i-1]]-V_in_mid_threshold):
                V_in_mid_line.pop(i)
                V_in_mid_line_slope.pop(i)
            else:
                V_in_mid_line.pop(i-1)
                V_in_mid_line_slope.pop(i-1)
        else:
            i=i+1
        
##    print("V_in_Mid")
##    print(V_in_mid_line)
##    print(V_in_mid_line_slope)
    t_rise = list()
    t_fall = list()
    t_temp_1 = 0
    t_temp_2 = 0



    ## Find Output Rise and Fall Delay
    for i in range(len(V_out_upper_line_slope)):
        
        ## Fall
        if (V_out_upper_line_slope[i] == -1):
    ##        if Vout[V_out_upper_line[i]] >  V_out_upper_threshold :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]+1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]+1]-Vout[V_out_upper_line[i]])
    ##        else :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]-1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]-1]-Vout[V_out_upper_line[i]])
    ##
    ##        if Vout[V_out_lower_line[i]] >  V_out_lower_threshold :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]+1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]+1]-Vout[V_out_lower_line[i]])
    ##        else :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]-1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]-1]-Vout[V_out_lower_line[i]])
    ##        t_fall.append(t_temp_2-t_temp_1)
            t_fall.append(t[V_out_lower_line[i]]-t[V_out_upper_line[i]]) 
            
        ## Rise
        else:
    ##        if Vout[V_out_upper_line[i]] >  V_out_upper_threshold :
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]-1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]-1]-Vout[V_out_upper_line[i]])
    ##        else:
    ##            t_temp_1 = t[i] + (V_out_upper_threshold - Vout[V_out_upper_line[i]])*(t[V_out_upper_line[i]+1]-t[V_out_upper_line[i]])/(Vout[V_out_upper_line[i]+1]-Vout[V_out_upper_line[i]])
    ##
    ##        if Vout[V_out_lower_line[i]] >  V_out_lower_threshold :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]-1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]-1]-Vout[V_out_lower_line[i]])
    ##        else :
    ##            t_temp_2 = t[i] + (V_out_lower_threshold - Vout[V_out_lower_line[i]])*(t[V_out_lower_line[i]+1]-t[V_out_lower_line[i]])/(Vout[V_out_lower_line[i]+1]-Vout[V_out_lower_line[i]])
    ##        t_rise.append(t_temp_1-t_temp_2)
            t_rise.append(t[V_out_upper_line[i]]-t[V_out_lower_line[i]] ) 
            

##    print("T fall Output")
##    print(t_fall)
##    print("T rise Output")
##    print(t_rise)
    try:
        output_rise_time  = sum(t_rise)/len(t_rise)
    except:
        print(filename)
    output_fall_time  = sum(t_fall)/len(t_fall)

##    print("Output Rise Time in ns : ")
##    print(output_rise_time*10**9)
##    print("Output Fall Time in ns : ")
##    print(output_fall_time*10**9)

    t_cell_rise = list()
    t_cell_fall = list()
    t_temp_1 = 0
    t_temp_2 = 0

    ## Find Cell Rise and Cell Fall Delay
    for i in range(len(V_in_mid_line_slope)):
        ## Fall
        if (V_out_mid_line_slope[i] == -1):
            t_cell_fall.append(t[V_out_mid_line[i]]-t[V_in_mid_line[i]])
        else:
            t_cell_rise.append(t[V_out_mid_line[i]]-t[V_in_mid_line[i]])

##    print("Cell Fall delay")
##    print(t_cell_fall)
##    print("Cell Rise delay")
##    print(t_cell_rise)

    cell_rise_time = sum(t_cell_rise)/len(t_cell_rise)
    cell_fall_time = sum(t_cell_fall)/len(t_cell_fall)

##    print("Cell rise delay")
##    print(cell_rise_time)
##    print("Cell fall delay")
##    print(cell_fall_time)

    return [cell_rise_time*(10**9),cell_fall_time*(10**9),output_rise_time*(10**9),output_fall_time*(10**9)]

def Delete_Files(input_nodes,input_slew,output_capacitance):
    for i in range(len(input_nodes)):
        for j in range(len(input_slew)):
            for k in range(len(output_capacitance)):
                filename = str(i)+str(j)+str(k)+".cir"
                os.remove("../Characterization/"+filename)
                print("Deleted file " + filename)
                os.remove(input_nodes[i]+"_"+input_slew[j] + "_" + output_capacitance[k] +  ".data")
                print("Deleted file " + input_nodes[i]+"_"+input_slew[j] + "_" + output_capacitance[k] +  ".data")

        
def Excel_writer(name,workbook,input_nodes,output_capacitance,input_slew,t):
    bold = workbook.add_format({'bold': 1})
    for k in range(len(input_nodes)):
        worksheet = workbook.add_worksheet(name +" IN " + input_nodes[k])
        worksheet.set_column('A:A', 35) 
        start = 'B'
        end = chr(ord(start)+len(input_slew))
        worksheet.set_column(start+":"+end, 30)
        
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

        table_size = len(input_slew)*len(output_capacitance)
        for i in range(len(input_slew)):
            for j in range(len(output_capacitance)):
                index = chr(ord(column)+i) + str(row+j)
                worksheet.write(index, str(t[m+k*table_size]) + " ns")
                m=m+1

##---- Main Function----##
                
##def main():

##----List The spice files in the directory and get the choice----##
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

##---- Read the csv file for input datas----##
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
        m = str(float(temp[i][:-1])*100/60)+'n'
        print(m)
        input_slew.append(m)
    i=i+1

output_capacitance = list()
i=1
temp = str(data[5][0]).split(",")
while(i<len(temp)):
    if len(temp[i]) > 0 :
        output_capacitance.append(temp[i])
    i=i+1

slew_lower_threshold = float(data[6][0].split(",")[1])
slew_upper_threshold = float(data[7][0].split(",")[1])

##-----Processing Netlist-----##
    
f = open("../Characterization/Netlists/"+ choice_file, "r")
circuit = f.read()
circuit = circuit.split("\n")
circuit.remove(".end")
circuit.append("\nV1 Vdd 0 " + str(Vdd))
source_circuit = circuit
temp_circuit = list()
cir = ''
print("Source Circuit Read")
print("Building Netlists")

##----- Create Netlists for all different combinations-----##
for i in range(len(input_nodes)):
    for j in range(len(input_slew)):
        for k in range(len(output_capacitance)):
            cir = Netlist_Build(output_nodes,input_nodes,input_nodes[i],input_slew[j],output_capacitance[k],T,Vdd,source_circuit)
            file = open("../Characterization/"+str(i)+str(j)+str(k)+".cir", "w")
            print("Netlist Build For " + str(i)+str(j)+str(k)+".cir" + " Complete ")
            file.write(cir)
            file.close()

print("Netlists Built Successfully for all different combinations")

print("Running Simulations")

NgSpice_Run(input_nodes,input_slew,output_capacitance)
            
Timing = [["cell_rise_time (ns)","cell_fall_time (ns)","output_rise_time (ns)","output_fall_time (ns)"]]

print(" Characterization Algorithm beginning ... ")
print(" Analyzing Data files ")
m=1
file = open("../Characterization/" + input_read_file+ "Characterisation Results" + ".txt", "w")
string = ''
rise_transition = list()
cell_rise = list()
fall_transition = list()
cell_fall = list()
input_slew_original = list()
for i in range(len(input_slew)):
    input_slew_original.append(str(float(input_slew[i][:-1])*60/100))
##    return [cell_rise_time*(10**9),cell_fall_time*(10**9),output_rise_time*(10**9),output_fall_time*(10**9)]
for i in range(len(input_nodes)):
    for j in range(len(input_slew)):
        for k in range(len(output_capacitance)):
            Timing.append(Characterization_run(input_nodes,input_slew[j],output_capacitance[k],input_nodes[i],slew_lower_threshold,slew_upper_threshold,Vdd))
            cell_rise.append(Timing[m][0])
            cell_fall.append(Timing[m][1])
            rise_transition.append(Timing[m][2])
            fall_transition.append(Timing[m][3])
            print(" Case : " + str(m) + "Input Node : " + input_nodes[i] + " Input Slew : " + input_slew_original[j] + " Output Capacitance : " + output_capacitance[k] + "Complete")
            print(Timing[0])
            print(Timing[m])
            print("\n")
            file.write(str(m) + ". Input Node : " + input_nodes[i] + " Input Slew : " + input_slew_original[j] + " Output Capacitance : " + output_capacitance[k])
            file.write("\n")
            file.write(str(Timing[0]))
            file.write("\n")
            file.write(str(Timing[m]))
            file.write("\n")
            file.write("\n")
            m = m+1
x = 0
file.close()
workbook = xlsxwriter.Workbook("../Characterization/"+input_read_file + 'Characterisation Results.xlsx')

##    name,workbook,input_nodes,output_capacitance,input_slew
Excel_writer(" rise_transition ",workbook,input_nodes,output_capacitance,input_slew_original,rise_transition)
Excel_writer(" cell_rise  ",workbook,input_nodes,output_capacitance,input_slew_original,cell_rise)
Excel_writer(" fall_transition  ",workbook,input_nodes,output_capacitance,input_slew_original,fall_transition)
Excel_writer(" cell_fall  ",workbook,input_nodes,output_capacitance,input_slew_original,cell_fall)
workbook.close()
Delete_Files(input_nodes,input_slew,output_capacitance,)

##if __name__ == "__main__":
##    main()
##    
