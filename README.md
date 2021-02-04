# Standard-Cell-Library-skywater-130
Custom made Standard cell Library for skywater 130nm PDK

LTSpice --> Ngspice
copy netlist
remove the .anno command at the end
add the .model files (ignore if already present)

Ng Spice
1. cd <directory path>
2. source <filename.cir>
3. run 
4. plot v(input) 
5. plot v(Y) 
verify the plots
6. save <filename.raw> v(Y)
