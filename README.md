# Standard-Cell-Library-skywater-130
Custom made Standard cell Library for skywater 130nm PDK

## Requirements 
1. Run the following command to clone the skywater130 MOS models in your local machine 
    ```
    git clone https://foss-eda-tools.googlesource.com/skywater-pdk/libs/sky130_fd_pr
    ```
2. Copy the file path of sky130_fd_pr and include the file path in the SPICE file using the following command
    ```
    .include "<filepath>/sky130_fd_pr/models/r+c/res_typical__cap_typical__lin.spice"
    .include "<filepath>/sky130_fd_pr/models/r+c/res_typical__cap_typical.spice"
    .include "<filepath>/sky130_fd_pr/models/corners/tt.spice"
    ```
    Ex : 
    ```
    .include "O:/sky130_fd_pr/models/r+c/res_typical__cap_typical__lin.spice"
    .include "O:/sky130_fd_pr/models/r+c/res_typical__cap_typical.spice"
    .include "O:/sky130_fd_pr/models/corners/tt.spice"
    ```
## Pre-Layout Simulation 
Nmos model : sky130_fd_pr__nfet_01v8
Pmos model : sky130_fd_pr__pfet_01v8

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

## Layout

## Post-Layout Simulation

## Characterization
.lib format - liberty file format
Reference : Liberty User Guides and Reference Manual Suite Version 2017.06 ; 
            http://www.cs.utah.edu/~elb/cadbook/color-figs/Chapter8-Char.pdf
Variable Parameters : input transition time ; output load capacitance

input_net_transition : 0.06, 0.18, 0.42, 0.6, 1.2 ns

total_output_net_capacitance : 0.025, 0.05, 0.1, 0.3, 0.6 pf