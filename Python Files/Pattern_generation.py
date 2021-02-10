def Test_Pattern_Gen(logic_string,input_nodes,pulse_node):
    pulse_high = logic_string[:].replace(pulse_node,'1')
    pulse_low = logic_string[:].replace(pulse_node,'0')
    pattern_list = list()
    for i in range(2**(len(input_nodes)-1)):
        a = bin(i).replace('0b','')
        while(len(a)<(len(input_nodes)-1)):
            a = '0'+a
        pattern_list.append(a)
    pulse_low_list = list()
    pulse_high_list = list()
    input_nodes_floating = input_nodes[:]
    input_nodes_floating.remove(pulse_node)


    for i in range(len(pattern_list)):
        low = pulse_low[:]
        high = pulse_high[:]
        for j in range(len(input_nodes_floating)):
            low = low.replace(input_nodes_floating[j],pattern_list[i][j])
            high = high.replace(input_nodes_floating[j],pattern_list[i][j])
        pulse_low_list.append(low)
        pulse_high_list.append(high)
    
logic_string = '( A1 | A2 ) & ( B1 & B2 )'
input_nodes = ['A1','A2','B1','B2']
pulse_node = 'A1'
j = Test_Pattern_Gen(logic_string,input_nodes,pulse_node)
