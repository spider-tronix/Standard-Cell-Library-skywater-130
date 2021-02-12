# Standard-Cell-Library-skywater-130
Custom made Standard cell Library for skywater 130nm PDK

## Standard Cells List:
1. xnor2_1x
2. xnor3_1x
3. xor2_1x
4. xor3_1x
5. maj3
6. a41oi
7. o311ai
8. o31ai
9. o32ai
10. o41ai

## Schematic Diagram

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/xor2_1x.PNG" 
alt="xnor2_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/xnor3_1x.PNG" 
alt="xnor3_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/xor2_1x.PNG" 
alt="xor2_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/xor3_1x.PNG" 
alt="xor3_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/maj3.PNG" 
alt="maj3" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/a41oi.PNG" 
alt="a41oi" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/o311ai.PNG" 
alt="o311ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/o31ai.PNG" 
alt="o31ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/o32ai.PNG" 
alt="o32ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/o41ai.PNG" 
alt="o41ai" >

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

Characterization Results:
1) Timing characteristics : rise_delay, fall_delay, rise_transition, fall_transition related to input pin
2) Power characteristics : rise_power, fall_power related to input pin and leakage power .
