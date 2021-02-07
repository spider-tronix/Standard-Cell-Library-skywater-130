f = open(r"O:\Standard-Cell-Library-skywater-130\Pre-Layout-Simulation\vY.data", "r")
circuit = f.read()
circuit= circuit.split("\n")
t= circuit[0].split(" ")[1]
v= circuit[0].split(" ")[3]