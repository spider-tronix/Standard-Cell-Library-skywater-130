import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.NgSpice.Shared import NgSpiceShared
ngspice = NgSpiceShared.new_instance()

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
    temp_circuit.append("wrdata "+input_slew + "_" + output_capacitance +  ".data" + " v(Y) " + "v(" +  Pulse_Node + ")")
    temp_circuit.append(".endc")
    ## Add .end command 
    temp_circuit.append(".end")

    ## Concatenate all Values
    result = ''
    for l in range(len(temp_circuit)):
        result = result + "\n" + temp_circuit[l]
    print(result)

    ## Return Result
    return result

def NgSpice_Run(circuit,Pulse_Node):
    ngspice = NgSpiceShared.new_instance()
    ngspice.load_circuit(circuit)
    ngspice.run()
    
    ## Print Vectors
    Vtemp_out = ngspice.exec_command("print v(Y)")
    Vtemp_in = ngspice.exec_command("print v(" + Pulse_Node+")")
    
    ## Obtain Output Vector
    V_out = list();
    for i in range(len(Vtemp_out)):
        if(Vtemp_out[i][0].isnumeric()==True):
            V_out.append(Vtemp_out[i].split("\t")[2])
            
    ## Obtain Time Vector
    t = list();
    for i in range(len(Vtemp_out)):
        if(Vtemp_out[i][0].isnumeric()==True):
            t.append(Vtemp_out[i].split("\t")[3])
            
    ## Obtain Input Vector
    V_in = list();
    for i in range(len(Vtemp_in)):
        if(Vtemp_in[i][0].isnumeric()==True):
            V_in.append(Vtemp_in[i].split("\t")[2])
    
    ## Close Instance
    ngspice.quit()

    ## Return Vectors
    print("Output Voltage Vector \n ")
    print(V_out)
    print("Input Voltage Vector \n ")
    print(V_in)
    print("Time Vector \n")
    print(t)
    
    
    
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
ngspice = NgSpiceShared.new_instance()
for i in range(len(input_nodes)):
    for j in range(len(input_slew)):
        for k in range(len(output_capacitance)):
            cir = Netlist_Build(output_nodes,input_nodes,input_nodes[i],input_slew[j],output_capacitance[k],Time_Period,source_circuit)
            file = open("/home/akil/Standard-Cell-Library-skywater-130/Characterization/"+str(i)+str(j)+str(k)+".cir", "w")
            file.write(cir)
            file.close()
            #NgSpice_Run(cir,input_nodes[i])


