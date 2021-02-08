import subprocess

def Netlist_Build(output_nodes,input_nodes,Pulse_Node,input_slew,output_capacitance,Time_Period,source_circuit):
    
    print ("\n for input " + Pulse_Node +  " vs " + " output node Y\n" )
    temp_circuit = source_circuit[:]
    temp_circuit.append("CL " + output_nodes[0] + " " + "0 " + output_capacitance + "pF")
    
    ## Pulsating Node :  Syntax 	 PULSE(V1 V2 TD TR TF PW PER) Ex : V2 A 0 PULSE(0 1.8 0 0 0 5 10)
    ## V2 A 0 PULSE(0 1.8 0 0.06n 0.06n 10.0n 20n)
    temp_circuit.append("V2 " + Pulse_Node + " 0" + " PULSE(0 1.8 0 " +  input_slew + " "  + input_slew + " " + str(Time_Period/2) + "n " + str(Time_Period) + "n)")
    
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
                    command = "ngspice -b /home/akil/Standard-Cell-Library-skywater-130/Characterization/" + filename 
                    subprocess.check_call(command,shell=True)
                    #a = subprocess.check_output(['ngspice', '-b', filename], shell=True). subprocess.check_call()
                except:
                    print(filename + " spice file executed")
                    
    print("NGSpice Simulation Runs Successfully completed")

def Characterization_run(input_nodes,input_slew,output_capacitance,pulse_node):
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
        
    Vdd = 1.8
    V_out_upper_threshold = 0.8*Vdd
    V_out_lower_threshold = 0.2*Vdd
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
            print(str(V_out_upper_threshold) + " " + str(Vout[i]))
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

    return [cell_rise_time,cell_fall_time,output_rise_time,output_fall_time]


##---- Main Function----##


##-----Circuit Parameters-----##
Vdd = 1.8
input_slew = ['0.06n', '0.18n', '0.42n', '0.6n', '1.2n' ]
output_capacitance = ['0.025', '0.05', '0.1', '0.3', '0.6' ]
Time_Period = 20 ## ns

##-----Processing Netlist-----##
f = open("/home/akil/Standard-Cell-Library-skywater-130/Characterization/Netlists/xor2_1x.cir", "r")
circuit = f.read()
circuit = circuit.split("\n")
circuit.remove(".end")

##-----Input and Output Nodes-----##
#input_nodes = list()
#still = 'Y'
##while still == 'Y':
##    input_nodes.append(input("Enter the input nodes \n"))
##    still = input("Are there any more input nodes?(Y/N) \n")
input_nodes = ['A','B']

#still = 'Y'
#output_nodes = list()
##while still == 'Y':
##    output_nodes.append(input("Enter the output nodes \n"))
##    still = input("Are there any more output nodes?(Y/N) \n")
output_nodes = ["Y"]

##-----Add Source Voltage-----#
circuit.append("\nV1 Vdd 0 1.8")
source_circuit = circuit
temp_circuit = list()
cir = ''

print("Source Circuit Read")
print("Building Netlists")
for i in range(len(input_nodes)):
    for j in range(len(input_slew)):
        for k in range(len(output_capacitance)):
            cir = Netlist_Build(output_nodes,input_nodes,input_nodes[i],input_slew[j],output_capacitance[k],Time_Period,source_circuit)
            file = open("/home/akil/Standard-Cell-Library-skywater-130/Characterization/"+str(i)+str(j)+str(k)+".cir", "w")
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
file = open("/home/akil/Standard-Cell-Library-skywater-130/Characterization/results.txt", "w")
string = ''
for i in range(len(input_nodes)):
    for j in range(len(input_slew)):
        for k in range(len(output_capacitance)):
            Timing.append(Characterization_run(input_nodes,input_slew[j],output_capacitance[k],input_nodes[i]))
            print(" Case : " + str(m) + "Input Node : " + input_nodes[i] + " Input Slew : " + input_slew[j] + " Output Capacitance : " + output_capacitance[k] + "Complete")
            print(Timing[0])
            print(Timing[m])
            print("\n")
            file.write(str(m) + "Input Node : " + input_nodes[i] + " Input Slew : " + input_slew[j] + " Output Capacitance : " + output_capacitance[k])
            file.write(str(Timing[0]))
            file.write(str(Timing[m]))
            file.write("\n")
            m = m+1
file.close()
    
    