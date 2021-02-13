# Standard-Cell-Library-skywater-130
Custom made Standard cell Library for skywater 130nm PDK <br/>
Description of the original Standard Cell library for Skywater 130 can be found [here](http://diychip.org/sky130/sky130_fd_sc_lp/cells/)<br/>
**Note : Work Under Progress**
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

# Schematic Diagram
The following schematic diagrams are obtained using LTSpice. <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/xnor2_1x.PNG" 
alt="xnor2_1x" >


<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/xnor3_1x.PNG" 
alt="xnor3_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/xor2_1x.PNG" 
alt="xor2_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/xor3_1x.PNG" 
alt="xor3_1x" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/maj3.PNG" 
alt="maj3" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/a41oi.PNG" 
alt="a41oi" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/o311ai.PNG" 
alt="o311ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/o31ai.PNG" 
alt="o31ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/o32ai.PNG" 
alt="o32ai" >

<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Schematics/Schematic%20Images/o41ai.PNG" 
alt="o41ai" >

# Pre-Layout Simulation 
Pre-layout simulation is done using NGspice - an open source SPICE tool for circuit simulation and analysis <br/>
**Nmos model** : *sky130_fd_pr__nfet_01v8* <br/>
**Pmos model** : *sky130_fd_pr__pfet_01v8*

## Requirements 

### Skywater 130 Primitives
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
### Ngspice Installation

## Netlists for Pre-layout Simulation
Netlists for the pre-layout simulation of standard cells can be found under the [Pre-layout-Simulation](https://github.com/akilm/Standard-Cell-Library-skywater-130/tree/main/Pre-Layout-Simulation) folder. After cloning, the repository the netlists can be run in ngspice using the following commands

## Running Ngspice from Linux Terminal
1. cd  `<file location>`
2. ngspice 
3. source  `<filename.cir>` 
4. run 
5. plot v(Y) v(<input_nodes>) 

## Output Waveforms
**xnor2_1x** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/xnor2_1x_waveforms.PNG" 
alt="xnor2_1x" >

**xnor3_1x** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/xnor3_1x_waveforms.PNG" 
alt="xnor3_1x" >

**xor2_1x** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/xor2_1x_waveforms.PNG" 
alt="xor2_1x" >

**xor3_1x** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/xor3_1x_waveforms.PNG" 
alt="xor3_1x" >

**maj3** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/maj3_waveforms.PNG" 
alt="maj3" >

**a41oi** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/a41oi_waveforms.PNG" 
alt="a41oi" >

**o311ai** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/o311ai_waveforms.PNG" 
alt="o311ai" >

**o31ai** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/o31ai_waveforms.PNG" 
alt="o31ai" >

**o32ai** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/o32ai_waveforms.PNG" 
alt="o32ai" >

**o41ai** <br/>
<img src="https://github.com/akilm/Standard-Cell-Library-skywater-130/blob/main/Pre-Layout-Simulation/Waveforms/o41ai_waveforms.PNG" 
alt="o41ai" >

# Layout
Later Stages

# Post-Layout Simulation
Later Stages

# Characterization
Characterization is done using this [tool](https://github.com/akilm/Standard-Cell-Characterization). The tool takes in the Netlist and different input parameters like Logic Function, input slew,  output capacitance, Vdd, Time period of operation, input and output nodes through an excel file with the same name as the SPICE netlist. The tool then runs the Timing Characterization algorithm to obtain the different values like rise_delay, fall_delay, rise_transition, fall_transition. The outputs are stored in an excel format. The Cells are being Characterised for the following input values for sample. <br/>
Vdd = 1.8 V <br/>
T = 20 ns  <br/>
Input Slew : 0.06, 0.18, 0.42, 0.6, 1.2 ns  <br/>
Output Capacitance : 0.025, 0.05, 0.1, 0.3, 0.6 pf  <br/>
The complete Description of the tool can be found [here](https://github.com/akilm/Standard-Cell-Characterization)

## Characterization Results:
1. Timing characteristics : rise_delay, fall_delay, rise_transition, fall_transition related to input pin. 
    ``` Status : Complete ``` <br/> <br/>
    **Results for xor2_1x.cir** <br/>
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Characterization%20Results_1.PNG" 
alt="Characterization Results" ><br/>
    <img src="https://github.com/akilm/Standard-Cell-Characterization/blob/main/Image%20Files/Characterization%20Results_2.PNG" 
alt="Characterization Results2" ><br/>
    

2) Power characteristics : rise_power, fall_power related to input pin and leakage power . 
 ``` Status : Work Under Progress ```  
