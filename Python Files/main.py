import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
logger = Logging.setup_logging()
from PySpice.Spice.NgSpice.Shared import NgSpiceShared
ngspice = NgSpiceShared.new_instance()

f = open("/home/akil/NAND.cir", "r")
circuit = f.read()
ngspice.load_circuit(circuit)
ngspice.run()
V_y = ngspice.exec_command("print v(Y)")
V_y = V_y.split("\n")
j = 0
Vnode_y = list();
for i in range(len(V_y)):
    if(V_y[i][0].isnumeric()==True):
        Vnode_y.append(V_y[i].split("\t")[2])
print(Vnode_y)
t = list(range(5066))
plt.plot(Vnode_y,t)
