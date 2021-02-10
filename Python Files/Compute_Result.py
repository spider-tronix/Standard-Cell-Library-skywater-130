def Infix_PostFix(logic_string):
    Operator_Stack = list()
    output = ''
    logic_string = logic_string.replace(' ','')
    for i in range(len(logic_string)):
        print("Incoming Character")
        print(logic_string[i])
        if logic_string[i].isnumeric() == True:
            output = output + logic_string[i]
            print("Operand Appended")
            print("output")
            print(output)
        elif logic_string[i] == '(':
            Operator_Stack.append(logic_string[i])
            print("Stack Push")
            print(Operator_Stack)
        elif logic_string[i] == ')':
            while(Operator_Stack[len(Operator_Stack)-1] != '('):
                output = output + Operator_Stack.pop()
            Operator_Stack.pop()
            print("output")
            print(output)
        elif len(Operator_Stack) == 0 :
            Operator_Stack.append(logic_string[i])
        elif Operator_Stack[len(Operator_Stack)-1] == '(':
            Operator_Stack.append(logic_string[i])
        else : 
            output = output + Operator_Stack.pop()
            Operator_Stack.append(logic_string[i])
    while(len(Operator_Stack) != 0):
        output = output + Operator_Stack.pop()
    return output

def Evaluate_Postfix(string):
    Stack = list()
    result = 0 
    for i in range(len(string)):
        if string[i].isnumeric() == True:
            Stack.append(string[i])
        else:
            if string[i] == '&':
                result = int(Stack.pop()) & int(Stack.pop())
            elif string[i] == '|':
                result = int(Stack.pop()) | int(Stack.pop())
            elif string[i] == '!':
                result = int(Stack.pop()) ^ 1
            Stack.append(result)
    print("Result : ")
    print(Stack.pop())
logic_string = '(0 & 1)|(1 & 1)'
string = Infix_PostFix(logic_string)
Evaluate_Postfix(string)

