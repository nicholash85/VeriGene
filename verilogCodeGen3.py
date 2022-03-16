"""
#######################################
Generates gate-level for given number of inputs/outputs
Generates infected version of code with fault injection and info leaking

modified by Nicholas Haehn
"""
import random
import os
import sys
import shutil

NumFiles = int(input("Enter the max number of files you want: ")) # 10 #65536 max
fileCount = 0

numInputsMax = int(input("Enter the max number of inputs (18 available, suggested 8 or less): "))#8
numOutputsMax = int(input("Enter the max number of outputs (7 available, suggested 3. Save at least one for info leaking trojan): "))#3
numGatesMax = int(input("Enter the number of internal gates (suggested 8 max, must be larger than number of outputs): ")) #8
numRepeats = int(input("Enter the number of repeats: ")) #4

# alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# wires = ['wire1','wire2','wire3','wire4','wire5','wire6','wire7','wire8']
possibleGates = ['and', 'or', 'nor', 'nand', 'xor', 'xnor']
# if numFiles > (2 ^ (2 ^ ))

print("Deleting Files")
#Empty Directories
folder = os.path.join(sys.path[0],'Verilog2/Uninfected')
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

print("Deleted Uninfected Files")
folder = os.path.join(sys.path[0],'Verilog2/Infected')
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    #print(f"{file_path}")
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

print("Deleted Infected Files")


#Generate Files
for inNum in range(2, numInputsMax + 1): #MaxInputs
    for outNum in range(1, numOutputsMax + 1): #MaxOutputs
        for numGates in range(outNum,numGatesMax):
            for repeat in range(0,numRepeats):

                #Uninfected Version Creation
                usedWires = []
                usedOuts = []
                AssignedGates = []
                inputs = []
                outputs = []
                inputList = ''
                inputListIntern = ''
                outputList = ''
                used = 0
                UnusedInputsWires = []
                AvailableInputsWires = []
                Infected = False
                numInfections = 0
                InfWires = []
                InfOutputs = []
                InfInputs = []
                InfAssignedGates = []
                for k in range(inNum):
                    inputs.append('in' + str(k))
                    if k == inNum - 1:
                        inputList = inputList + 'in' + str(k)
                        inputListIntern = inputListIntern + 'in' + str(k)
                    else:
                        inputList = inputList + 'in' + str(k) + ', '
                        inputListIntern = inputListIntern + 'in' + str(k) + ','
                    used += 1
                for n in range(outNum):
                    outputs.append('out' + str(n))
                    if n == outNum - 1:
                        outputList = outputList + 'out' + str(n)
                    else:
                        outputList = outputList + 'out' + str(n) + ', '
                
                for o in inputs:
                    UnusedInputsWires.append(o)
                    AvailableInputsWires.append(o)

                fileCount += 1
                if fileCount > NumFiles: break
                
                DOSFault = random.randint(0,500)
                DOSWireNum = 0
                DOSType = random.randint(0,3)

                for k in range(0,numGates):

                    #add gate type
                    if len(usedOuts) >= outNum: break
                    tempGate = possibleGates[random.randint(0,len(possibleGates)-1)] + '('   
                    tempInfGate = tempGate          

                    #add gate inputs
                    gateIn1 = ''
                    gateIn2 = ''
                    if (((len(UnusedInputsWires))+1) >= (2*(numGates-k))):
                        In1Index = random.randint(0,len(UnusedInputsWires)-1)
                        gateIn1 = UnusedInputsWires[In1Index]
                        del UnusedInputsWires[In1Index]
                        if len(UnusedInputsWires) == 0:
                            In2Index = random.randint(0,len(AvailableInputsWires)-1)
                            gateIn2 = AvailableInputsWires[In2Index]
                            if gateIn2 in UnusedInputsWires:
                                UnusedInputsWires.remove(gateIn2)
                        else:
                            In2Index = random.randint(0,len(UnusedInputsWires)-1)
                            gateIn2 = UnusedInputsWires[In2Index]
                            del UnusedInputsWires[In2Index]
                    else:
                        In1Index = random.randint(0,len(AvailableInputsWires)-1)
                        gateIn1 = AvailableInputsWires[In1Index]
                        if gateIn1 in UnusedInputsWires:
                            UnusedInputsWires.remove(gateIn1)
                        In2Index = random.randint(0,len(AvailableInputsWires)-1)
                        gateIn2 = AvailableInputsWires[In2Index]
                        if gateIn2 in UnusedInputsWires:
                            UnusedInputsWires.remove(gateIn2)

                    while gateIn2 == gateIn1:
                        In2Index = random.randint(0,len(AvailableInputsWires)-1)
                        gateIn2 = AvailableInputsWires[In2Index]

                    #add gate out name
                    gateOut = ''
                    if ((outNum - len(usedOuts)) >= (numGates-k)): #assign output if there are as many gates as outputs left
                        gateOutIndex = random.randint(0,len(outputs)-1)
                        gateOut = outputs[gateOutIndex]
                        usedOuts.append(outputs[gateOutIndex])
                        del outputs[gateOutIndex]
                    else:
                        outType = random.randint(0,numGates)
                        if outType < (numGates - outNum): #output is a wire
                            gateOut = "wire" + str(len(usedWires))
                            usedWires.append(gateOut)
                            UnusedInputsWires.append(gateOut)
                            AvailableInputsWires.append(gateOut)
                        else: #output is a out
                            if len(outputs) <= 1:
                                gateOut = "wire" + str(len(usedWires))
                                usedWires.append(gateOut)
                                UnusedInputsWires.append(gateOut)
                                AvailableInputsWires.append(gateOut)
                            else:
                                gateOutIndex = random.randint(0,len(outputs)-1)
                                gateOut = outputs[gateOutIndex]
                                usedOuts.append(outputs[gateOutIndex])
                                del outputs[gateOutIndex]
                        
                    tempGate = tempGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + ');'
                    AssignedGates.append(tempGate)

                    #Infected Verions

                    # Fault Injecting 
                    #  and(randOut,rand1,rand2) //Pick random from 2 to total number of inputs
                    #  xor(out1, randOut, wireFault)

                    # Information Leaking 
                    #  not(leakOut, infoToLeak)
                    #  OR
                    #  and(leakOut, infoToLeak, Trigger)

                    # Adds fault to a second circuit 20% of the time or at the last gate
                    if (Infected == False and k == numGates-1) or (random.randint(0,100) < 20) or (DOSFault == 1):
                        
                        #Complete denial of service module
                        if DOSFault == 1:
                            #Denial of Service externally triggered on true
                            if DOSType == 0:
                                if k == 0:
                                    DOSTrigger = 'DOSTrigger'
                                    InfInputs.append(DOSTrigger)
                                DOSWire = 'DOSWire' + str(numInfections)
                                InfWires.append(DOSWire)
                                DOSNotWire = 'DOSNotWire' + str(numInfections)
                                InfWires.append(DOSNotWire)
                                tempInfGate = tempInfGate + DOSWire + ',' + gateIn1 + ',' + gateIn2 + '); // DENIAL OF SERVICE EXTERNALLY TRIGGERED ON TRUE \n'
                                tempInfGate = tempInfGate + '\tnot(' + DOSNotWire + ',' + DOSTrigger + '); // DENIAL OF SERVICE EXTERNALLY TRIGGERED ON TRUE \n'
                                tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + DOSWire + ',' + DOSNotWire + '); // DENIAL OF SERVICE EXTERNALLY TRIGGERED ON TRUE'

                            #Denial of Service interally triggered on true
                            elif DOSType == 2:
                                DOSWire = 'DOSWire' + str(numInfections)
                                InfWires.append(DOSWire)
                                DOSNotWire = 'DOSNotWire' + str(numInfections)
                                InfWires.append(DOSNotWire)
                                InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                DOSTrigger = AvailableInputsWires[InfIn1Index]
                                if DOSTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(DOSTrigger)
                                tempInfGate = tempInfGate + DOSWire + ',' + gateIn1 + ',' + gateIn2 + '); // DENIAL OF SERVICE INTERNALLY TRIGGERED ON TRUE \n'
                                tempInfGate = tempInfGate + '\tnot(' + DOSNotWire + ',' + DOSTrigger + '); // DENIAL OF SERVICE INTERNALLY TRIGGERED ON TRUE \n'
                                tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + DOSWire + ',' + DOSNotWire + '); // DENIAL OF SERVICE INTERNALLY TRIGGERED ON TRUE'

                            #Denial of Service externally triggered on false
                            elif DOSType == 2:
                                if k == 0:
                                    DOSTrigger = 'DOSTrigger'
                                    InfInputs.append(DOSTrigger)
                                DOSWire = 'DOSWire' + str(numInfections)
                                InfWires.append(DOSWire)
                                tempInfGate = tempInfGate + DOSWire + ',' + gateIn1 + ',' + gateIn2 + '); // DENIAL OF SERVICE EXTERNALLY TRIGGERED ON FALSE \n'
                                tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + DOSWire + ',' + DOSTrigger + '); // DENIAL OF SERVICE EXTERNALLY TRIGGERED ON FALSE'

                            #Denial of Service internally triggered on false
                            else:
                                InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                DOSTrigger = AvailableInputsWires[InfIn1Index]
                                if DOSTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(DOSTrigger)
                                DOSWire = 'DOSWire' + str(numInfections)
                                InfWires.append(DOSWire)
                                tempInfGate = tempInfGate + DOSWire + ',' + gateIn1 + ',' + gateIn2 + '); // DENIAL OF SERVICE INTERNALLY TRIGGERED ON FALSE \n'
                                tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + DOSWire + ',' + DOSTrigger + '); // DENIAL OF SERVICE INTERNALLY TRIGGERED ON FALSE'

                        
                        else:
                            TrojanType = random.randint(0,2)

                            #info leaking
                            if gateOut.split('e')[0] == 'wir' and TrojanType == 0:
                                LeakType = random.randint(0,4)

                                #Leak triggered on external on true
                                if LeakType == 0:
                                    leakTrigger = 'leakTrigger' + str(numInfections)
                                    InfInputs.append(leakTrigger)
                                    leakOut = 'leakOut' + str(numInfections)
                                    InfOutputs.append(leakOut)
                                    tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + '); //LEAK EXTERNALLY TRIGGERED ON TRUE\n'
                                    tempInfGate = tempInfGate + '\tand(' + leakOut + ',' + gateOut + ',' + leakTrigger + '); //LEAK EXTERNALLY TRIGGERED ON TRUE'
                                #Leak triggered on external false
                                elif LeakType == 1:
                                    leakTrigger = 'leakTrigger' + str(numInfections)
                                    InfInputs.append(leakTrigger)
                                    leakOut = 'leakOut' + str(numInfections)
                                    InfOutputs.append(leakOut)
                                    leakWire = 'DOSWire' + str(numInfections)
                                    InfWires.append(leakWire)
                                    tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + '); //FLIPPED LEAK EXTERNALLY TRIGGERED ON FALSE\n'
                                    tempInfGate = tempInfGate + '\tnot(' + leakWire + ',' + leakTrigger + '); //FLIPPED LEAK EXTERNALLY TRIGGERED ON FALSE\n'
                                    tempInfGate = tempInfGate + '\tnand(' + leakOut + ',' + gateOut + ',' + leakWire + '); //LEAK EXTERNALLY TRIGGERED ON FALSE'
                                #Leak triggered on internal on true
                                elif LeakType == 2:
                                    InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                    leakTrigger = AvailableInputsWires[InfIn1Index]
                                    if leakTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(leakTrigger)
                                    leakOut = 'leakOut' + str(numInfections)
                                    InfOutputs.append(leakOut)
                                    tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + '); //LEAK INTERNALLY TRIGGERED ON TRUE\n'
                                    tempInfGate = tempInfGate + '\tand(' + leakOut + ',' + gateOut + ',' + leakTrigger + '); //LEAK INTERNALLY TRIGGERED ON TRUE'
                                #Leak triggered on internal false
                                elif LeakType == 3:
                                    InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                    leakTrigger = AvailableInputsWires[InfIn1Index]
                                    if leakTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(leakTrigger)
                                    leakOut = 'leakOut' + str(numInfections)
                                    InfOutputs.append(leakOut)
                                    leakWire = 'DOSWire' + str(numInfections)
                                    InfWires.append(leakWire)
                                    tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + '); //FLIPPED LEAK INTERNALLY TRIGGERED ON FALSE\n'
                                    tempInfGate = tempInfGate + '\tnot(' + leakWire + ',' + leakTrigger + '); //FLIPPED LEAK INTERNALLY TRIGGERED ON FALSE\n'
                                    tempInfGate = tempInfGate + '\tnand(' + leakOut + ',' + gateOut + ',' + leakWire + '); //FLIPPED LEAK INTERNALLY TRIGGERED ON FALSE'
                                #Always on leak
                                else: #LeakType == 4
                                    leakOut = 'leakOut' + str(numInfections)
                                    InfOutputs.append(leakOut)
                                    leakWire = 'DOSWire' + str(numInfections)
                                    InfWires.append(leakWire)
                                    tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + '); //LEAK ALWAYS ON\n'
                                    tempInfGate = tempInfGate + '\tnot(' + leakOut + ',' + gateOut + '); //LEAK ALWAYS ON'
                            
                            #fault injecting
                            elif TrojanType == 1: 
                                FaultType = random.randint(0,1)

                                #Fault injecting internally triggered
                                if FaultType == 0:
                                    faultWire = 'faultWire' + str(numInfections)
                                    randOut = 'randOut' + str(numInfections)
                                    InfWires.append(faultWire)
                                    InfWires.append(randOut)
                                    InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                    InfgateIn1 = AvailableInputsWires[InfIn1Index]
                                    if InfgateIn1 in UnusedInputsWires:
                                        UnusedInputsWires.remove(InfgateIn1)
                                    InfIn2Index = random.randint(0,len(AvailableInputsWires)-1)
                                    InfgateIn2 = AvailableInputsWires[InfIn2Index]
                                    if InfgateIn2 in UnusedInputsWires:
                                        UnusedInputsWires.remove(InfgateIn2)
                                    while InfgateIn2 == InfgateIn1:
                                        InfIn2Index = random.randint(0,len(AvailableInputsWires)-1)
                                        InfgateIn2 = AvailableInputsWires[InfIn2Index]

                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT INTERNALLY TRIGGERED\n'
                                    tempInfGate = tempInfGate + '\tand(' + randOut + ',' + InfgateIn1 + ',' + InfgateIn2 + ');   //FAULT INTERNALLY TRIGGERED\n'
                                    tempInfGate = tempInfGate + '\txor(' + gateOut + ',' + randOut + ',' + faultWire + ');   //FAULT INTERNALLY TRIGGERED'

                                #Fault injecting externally triggered
                                else: #FaultType == 1
                                    faultWire = 'faultWire' + str(numInfections)
                                    randOut = 'randOut' + str(numInfections)
                                    InfWires.append(faultWire)
                                    InfWires.append(randOut)
                                    
                                    FirstFaultTrigger = 'FirstFaultTrigger' + str(numInfections)
                                    InfInputs.append(FirstFaultTrigger) 
                                    SecondFaultTrigger = 'SecondFaultTrigger' + str(numInfections)
                                    InfInputs.append(SecondFaultTrigger) 
                                    

                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT EXTERNALLY TRIGGERED\n'
                                    tempInfGate = tempInfGate + '\tand(' + randOut + ',' + SecondFaultTrigger + ',' + FirstFaultTrigger + ');   //FAULT EXTERNALLY TRIGGERED\n'
                                    tempInfGate = tempInfGate + '\txor(' + gateOut + ',' + randOut + ',' + faultWire + ');   //FAULT EXTERNALLY TRIGGERED'
                            
                            #Gate Deletion
                            else: #TrojanType == 2
                                DeletionType = random.randint(0,3)

                                #Gate 'deletion'/ small-scale DOS externally triggered on false
                                if DeletionType == 0:
                                    faultWire = 'faultWire' + str(numInfections)
                                    InfWires.append(faultWire)
                                    DeletionTrigger = 'DeletionTrigger' + str(numInfections)
                                    InfInputs.append(DeletionTrigger) 

                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT GATE DOS EXTERNALLY TRIGGERED ON FLASE\n'
                                    tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + faultWire + ',' + DeletionTrigger + ');   //FAULT GATE DOS EXTERNALLY TRIGGERED ON FALSE'
                                
                                #Gate 'deletion'/ small-scale DOS Interally triggered on false
                                elif DeletionType == 1:
                                    faultWire = 'faultWire' + str(numInfections)
                                    InfWires.append(faultWire)
                                    InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                    DeletionTrigger = AvailableInputsWires[InfIn1Index]
                                    if DeletionTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(DeletionTrigger)

                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT GATE DOS INTERNALLY TRIGGERED ON FALSE\n'                                  
                                    tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + faultWire + ',' + DeletionTrigger + ');   //FAULT GATE DOS INTERNALLY TRIGGERED ON FALSE'

                                #Gate 'deletion'/ small-scale DOS externally triggered on true
                                elif DeletionType == 2:
                                    faultWire = 'faultWire' + str(numInfections)
                                    InfWires.append(faultWire)
                                    DeletionTrigger = 'DeletionTrigger' + str(numInfections)
                                    InfInputs.append(DeletionTrigger)
                                    DOSNotWire = 'DOSNotWire' + str(numInfections)
                                    InfWires.append(DOSNotWire)

                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE\n'
                                    tempInfGate = tempInfGate + '\tnot(' + DOSNotWire + ',' + DeletionTrigger + '); //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE \n'
                                    tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + faultWire + ',' + DOSNotWire + ');   //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE'
                                
                                #Gate 'deletion'/ small-scale DOS Interally triggered on true
                                else: #DeletionType == 3
                                    faultWire = 'faultWire' + str(numInfections)
                                    InfWires.append(faultWire)
                                    InfIn1Index = random.randint(0,len(AvailableInputsWires)-1)
                                    DeletionTrigger = AvailableInputsWires[InfIn1Index]
                                    if DeletionTrigger in UnusedInputsWires:
                                        UnusedInputsWires.remove(DeletionTrigger)
                                    DOSNotWire = 'DOSNotWire' + str(numInfections)
                                    InfWires.append(DOSNotWire)
                                    
                                    tempInfGate = tempInfGate + faultWire + ',' + gateIn1 + ',' + gateIn2 + ');  //FAULT GATE DOS INTERNALLY TRIGGERED ON TRUE\n'
                                    tempInfGate = tempInfGate + '\tnot(' + DOSNotWire + ',' + DeletionTrigger + '); //FAULT GATE DOS INTERNALLY TRIGGERED ON TRUE \n'
                                    tempInfGate = tempInfGate + '\tand(' + gateOut + ',' + faultWire + ',' + DOSNotWire + ');   //FAULT GATE DOS INTERNALLY TRIGGERED ON TRUE'

                        numInfections += 1
                        Infected = True
                
                    else:
                        tempInfGate = tempInfGate + gateOut + ',' + gateIn1 + ',' + gateIn2 + ');'

                    InfAssignedGates.append(tempInfGate)

                #Create uninfected verilog text
                temp =  "module gate_level_"+str(fileCount)+ "(output "+outputList+", input "+inputList+");\n"
                if len(usedWires) > 0:
                    temp += "\twire "
                    for k in range(0,len(usedWires)):
                        if (k == len(usedWires) - 1):
                            temp += usedWires[k]+";\n\n"
                        else:
                            temp += usedWires[k]+", "
                
                for l in range(0, len(AssignedGates)):
                    temp += "\t"+AssignedGates[l]+"\n"

                temp += "endmodule"
                #print("Uninfected Verilog:")
                #print('{0}\n'.format(temp))

                #Create infected Verilog Text
                Inftemp =  "module Inf_gate_level_"+str(fileCount)+"(output "+outputList+","
                for infOut in InfOutputs:
                    Inftemp += " "+infOut+","
                Inftemp += " input "+inputList
                for infIn in InfInputs:
                    Inftemp += ", "+infIn
                Inftemp += ");\n"
                if len(usedWires) > 0 or len(InfWires) > 0:
                    Inftemp += "\twire "
                    for e in range(0,len(InfWires)):
                        if len(usedWires) > 0:
                            Inftemp += InfWires[e]+", "
                        elif e == len(InfWires) - 1:
                            Inftemp += InfWires[e]+";\n\n"
                        else:
                            Inftemp += InfWires[e]+", "
                    for k in range(0,len(usedWires)):
                        if (k == len(usedWires) - 1):
                            Inftemp += usedWires[k]+";\n\n"
                        else:
                            Inftemp += usedWires[k]+", "
                
                for l in range(0, len(InfAssignedGates)):
                    Inftemp += "\t"+InfAssignedGates[l]+"\n"

                Inftemp += "endmodule"
                #print("Infected Verilog:")
                #print('{0}\n'.format(Inftemp))

                filenameUninf = "Verilog2/Uninfected/gate_level_"+str(fileCount)+"_in"+str(inNum)+"_out"+str(outNum)+"_gates"+str(numGates)+".v"
                filenameInf = "Verilog2/Infected/Inf_gate_level_"+str(fileCount)+"_in"+str(inNum)+"_out"+str(outNum)+"_gates"+str(numGates)+".v"    

                #Write Uninfected Verilog
                print("Writing Uninfected file to {0}.".format(filenameUninf))
                with open(os.path.join(sys.path[0],filenameUninf),"w+") as f:
                    f.write(temp)
                    f.close()
                
                #Write infected verilog
                print("Writing Infected file to {0}.\n".format(filenameInf))
                with open(os.path.join(sys.path[0],filenameInf),"w+") as k:
                    k.write(Inftemp)
                    k.close()

            

# for num in range(100): #65536
#     filename = f"C:/Cello-v2-develop/input/uninfected_verilog_files/temp/temp/comb_logic_in4_out1_{str(num)}.v"
#     res = [int(i) for i in list('{0:016b}'.format(num))]
#     #print(res)
#     with open(filename,"w+") as f:
#         temp =  f"module comb_logic_{str(num)}(input a, b, c, d, output e, f);\n\n"
#         temp += f"always@(a,b,c,d)\n"
#         temp += f"\tbegin\n"
#         temp += f"\tcase({{a,b,c,d}})\n"
#         temp += f"\t\t4'b0000:  e = 1'b{res[0]};\n"
#         temp += f"\t\t4'b0001:  e = 1'b{res[1]};\n"
#         temp += f"\t\t4'b0010:  e = 1'b{res[2]};\n"
#         temp += f"\t\t4'b0011:  e = 1'b{res[3]};\n"
#         temp += f"\t\t4'b0100:  e = 1'b{res[4]};\n"
#         temp += f"\t\t4'b0101:  e = 1'b{res[5]};\n"
#         temp += f"\t\t4'b0110:  e = 1'b{res[6]};\n"
#         temp += f"\t\t4'b0111:  e = 1'b{res[7]};\n"
#         temp += f"\t\t4'b1000:  e = 1'b{res[8]};\n"
#         temp += f"\t\t4'b1001:  e = 1'b{res[9]};\n"
#         temp += f"\t\t4'b1010:  e = 1'b{res[10]};\n"
#         temp += f"\t\t4'b1011:  e = 1'b{res[11]};\n"
#         temp += f"\t\t4'b1100:  e = 1'b{res[12]};\n"
#         temp += f"\t\t4'b1101:  e = 1'b{res[13]};\n"
#         temp += f"\t\t4'b1110:  e = 1'b{res[14]};\n"
#         temp += f"\t\t4'b1111:  e = 1'b{res[15]};\n"
#         temp += f"\tendcase\n"
#         temp += f"\tend\n"
#         temp += f"endmodule"

#         f.write(temp)