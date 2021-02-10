import xlsxwriter
    
workbook = xlsxwriter.Workbook('Characterisation Results.xlsx')
def Excel_writer(name,workbook,input_nodes,output_capacitance,input_slew):
    bold = workbook.add_format({'bold': 1})
    column = 'B'
    row = 1
    for k in range(len(input_nodes)):
        worksheet = workbook.add_worksheet(name +" Input Node : " + input_nodes[i]) 
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
                worksheet.write(index, str(t_rise[m+i*table_size]) + " ns")
                m=m+1

