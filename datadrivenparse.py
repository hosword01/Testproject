import csv
import os
import matplotlib.pyplot as plt
import numpy as np
__version__ = "ver:0.0002"
x_ax = np.linspace(0,1000,6)
cap_ax = np.linspace(0.875,1.075,9)
IR_ax =np.linspace(0.0150 , 0.0190 , 9)

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
        if x[ head['Step_Index'] ].replace('.','').isdigit() and temp != x[ head['Step_Index'] ]:
            step_index.append(i-1)
            temp = x[ head['Step_Index'] ]

    DataPack = {}
    j = 0
    for i,row in enumerate(rows[1::]):
        if i == step_index[j]:
            try:
                DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ]
            except:
                DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ]={}
            DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ][ int(row[head['Step_Index']].replace('.0','')) ] = {}
            for para in para_L:
                DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ][ int(row[head['Step_Index']].replace('.0','')) ][para] = []
            if j < len(step_index)-1:    
                j+= 1

        for para in para_L:
            if row[head[para]].replace("-","",2).replace("+","",1).replace(".","",1).replace("E","",1).isdigit():    #specific ex:3.13E-6 
                DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ][ int(row[head['Step_Index']].replace('.0','')) ][para].\
                          append(float(row[head[para]]))
            else:
                DataPack[ int(row[head['Cycle_Index']].replace('.0','')) ][ int(row[head['Step_Index']].replace('.0','')) ][para].\
                          append(row[head[para]])
    return DataPack

def DataDrainQ(path1):
    with open (path1) as file:
        datarow = csv.reader(file)
        rows = [row for row in datarow]

    head = {}
    for i,h in enumerate(rows[0]):
        head[h] = i

    step_index = []
    temp = 0
    fFeed = True

    DataPack = {}
    DataPack['Cycle'] = []
    DataPack['Cap'] = []
    DataPack['IR'] = []
    for i,x in enumerate(rows[1::]):
        if x[ head['Cycle_Index'] ].replace('.','').isdigit() and temp != float(x[ head['Cycle_Index'] ]):
            DataPack['Cycle'].append( float(rows[i][head['Cycle_Index']]) )
            DataPack['Cap'].append( float(rows[i][head['Discharge_Capacity']]) )
            DataPack['IR'].append( float(rows[i][head['Internal_Resistance']]) )
            temp = float(x[ head['Cycle_Index'] ])

        if fFeed  and float(x[ head['Step_Index'] ]) == 2:
            fFeed = False
            feed = float(x[ head['Discharge_Capacity'] ])

        #print(i)

    DataPack['Cap'][0] -=  feed

            
    return DataPack

#DataPack[ Cycle ][ Step ][...]=[p1,p2,p3,....]
#[...] = one of  [ "Step_Time" , "Current" , "Voltage" , "Charge_Capacity" , "Discharge_Capacity" , "Charge_Energy" , "Discharge_Energy" ,"dV/dt","Internal_Resistance","Temperature"]
"""
Path = "DataDriven//"
FList = [ f for f in os.listdir(Path) if os.path.splitext(f)[-1]=='.csv' ]
fig = plt.figure()
L = len(FList)
for i,rdata in enumerate(FList):
    

    path1 =Path + rdata
    #if not os.path.isfile(path1.replace('.csv','.png')): 
    pack1 = DataDrainQ(path1)
    
    ax1 = fig.add_subplot(111)
    ax1.plot(pack1['Cycle'],pack1['Cap'],'m')
    ax1.set_ylabel('Cap(AH)')
    ax1.set_xlabel('Cycle')
    ax2 = ax1.twinx()
    ax2.plot(pack1['Cycle'],pack1['IR'],'g')
    ax2.set_ylabel('IR(Ohm)')
    ax1.set_xlim(0,1000)
    ax1.set_ylim(0.875,1.075)
    ax2.set_ylim(0.013,0.019)
    
    fig.savefig(Path + rdata.split('.')[0])
    plt.clf()
    del(pack1)
    del(ax1)
    del(ax2)
    print( str(i+1) + "//" +str(L) )

"""
