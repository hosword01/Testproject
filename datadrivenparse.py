import csv
import os
__version__ = "beta_v0.001"
para_L = [ "Step_Time" , "Current" , "Voltage" , "Charge_Capacity" , "Discharge_Capacity" , "Charge_Energy" , "Discharge_Energy" ,"dV/dt","Internal_Resistance","Temperature"]
#modify para_L to add or remove parameter in datapack

def DataDrain(path1):
    with open (path1) as file:
        datarow = csv.reader(file)
        rows = [row for row in datarow]

    head = {}
    for i,h in enumerate(rows[0]):
        head[h] = i

    step_index = []
    temp = ""

    for i,x in enumerate(rows):
        if x[ head['Step_Index'] ].isdigit() and temp != x[ head['Step_Index'] ]:
            step_index.append(i-1)
            temp = x[ head['Step_Index'] ]

    DataPack = {}
    j = 0
    for i,row in enumerate(rows[1::]):
        if i == step_index[j]:
            try:
                DataPack[ int(row[head['Cycle_Index']]) ]
            except:
                DataPack[ int(row[head['Cycle_Index']]) ]={}
            DataPack[ int(row[head['Cycle_Index']]) ][ int(row[head['Step_Index']]) ] = {}
            for para in para_L:
                DataPack[ int(row[head['Cycle_Index']]) ][ int(row[head['Step_Index']]) ][para] = []
            if j < len(step_index)-1:    
                j+= 1

        for para in para_L:
            if row[head[para]].replace("-","",2).replace("+","",1).replace(".","",1).replace("E","",1).isdigit():    #specific ex:3.13E-6 
                DataPack[ int(row[head['Cycle_Index']]) ][ int(row[head['Step_Index']]) ][para].\
                          append(float(row[head[para]]))
            else:
                DataPack[ int(row[head['Cycle_Index']]) ][ int(row[head['Step_Index']]) ][para].\
                          append(row[head[para]])
    return DataPack

#DataPack[ Cycle ][ Step ][...]=[p1,p2,p3,....]
#[...] = one of  [ "Step_Time" , "Current" , "Voltage" , "Charge_Capacity" , "Discharge_Capacity" , "Charge_Energy" , "Discharge_Energy" ,"dV/dt","Internal_Resistance","Temperature"]
