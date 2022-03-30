import os
from time import perf_counter
from os import read
import random
from tokenize import Name, Number
import os
import shutil
import sys
import time

# Given an entire file string, this function gets the type (folder before) and filename
def getFileValues(nameVerilog):
  type = nameVerilog.split('/')[1]
  Filename = nameVerilog.split('/')[2]
  return type, Filename

# This class holds the gates of the verilog file
class VerilogGates:
  def __init__(self,name,output,input,inf):
    self.name = name
    self.input = input[:]
    self.output = output
    self.inf = inf
  # def __init__(self, exist):
  #   self.gate = exist.gate
  #   self.input = exist.input
  #   self.output = exist.output

# This class holds the info from a verilog file
class VerilogInfo:
  def __init__(self,name,output,input,wires,gates,infNum,normNum):
    self.name = name
    self.output = output[:]
    self.input = input[:]
    self.wires = wires[:]
    self.gates = gates[:]
    self.infNum = infNum
    self.normNum = normNum
    
# Reads logic gates from Verilog
def readVerilogGates(nameVerilog):
  VerilogFile = open(nameVerilog,'r')
  Lines = VerilogFile.readlines()
  VerilogFile.close()

  transcode = False
  name = ""
  mode = ''
  inputs = []
  outputs = []
  wires = []
  gates = []
  numInf = 0
  normNum = 0
  for k in range(0,len(Lines)):

    #Start of Verilog File
    if Lines[k].split(" ")[0] == "module":
      transcode = True
      line = Lines[k].split("(")
      name = line[0].split(" ")[1]
      line = line[1].split(")")[0]
      line = line.replace(", ", " ")
      for parameter in line.split(" "):
        if parameter == "output":
          mode = "output"
        elif parameter == "input":
          mode = "input"
        else:
          if mode == "output":
            outputs.append(parameter)
          elif mode == "input":
            inputs.append(parameter)


    #End of verilog file
    elif Lines[k].split(" ")[0] == "endmodule":
      transcode = False
      break

    #Verilog code
    elif transcode == True:
      line = Lines[k].split("//")[0]
      line = line.replace("\t", "")
      line = line.replace("\n","")

      # Get wires
      if line.split(" ")[0] == "wire":
        line = line.replace(", ", " ")
        line = line.replace(";", "")
        for parameter in line.split(" "):
          if parameter != "wire":
            wires.append(parameter)

      #Get gates
      elif len(line)>1:
        inf = False
        if len(Lines[k].split("//")) > 1:
          inf = True
          numInf += 1
          # print(Lines[k])
          # print(Lines[k].split("//"))
          # time.sleep(0.5)
        normNum += 1
        line = line.split(")")[0]
        line = line.replace("(",",")
        gateParts = line.split(",")
        if len(gateParts) > 3:
          tempInputs = [gateParts[2],gateParts[3]]
          tempGate = VerilogGates(gateParts[0],gateParts[1],tempInputs,inf)
        if len(gateParts) == 3:
          tempGate = VerilogGates(gateParts[0],gateParts[1],[gateParts[2]],inf)
        gates.append(tempGate)
    
  return VerilogInfo(name,outputs,inputs,wires,gates,numInf,normNum)

#Prints all Verilog values
def debugVerilogRead(Verilog):
  print("\nVerilog File Name: "+ str(Verilog.name))
  print("Verilog Input List: "+ str(Verilog.input))
  print("Verilog Output List: "+str(Verilog.output))
  print("Verilog Wire List: "+str(Verilog.wires)+"\n")
    
  for k in range(0,len(Verilog.gates)):
    print("\t Verilog gate "+str(k)+": "+str(Verilog.gates[k].name))
    print("\t Gate "+str(k)+" inputs: "+str(Verilog.gates[k].input))
    print("\t Gate "+str(k)+" outputs: "+str(Verilog.gates[k].output)+"\n")


def ConvertVerilogToLine(InputFolder, OutputFolder):
  # Loop through Verilog files
  for name in [InputFolder+'/Infected/',InputFolder+'/Uninfected/']:
    for nameVerilog in os.listdir(name):
      # start = start1 = time.time()
      nameVerilog = os.path.join(name,nameVerilog)
      # end1 = time.time()
      # print("Runtime of the "+"os.path.join"+"step is "+str(end1 - start1))
      # start1 = time.time()

      # Create DNA 

      # print file being processed
      print("\n"+nameVerilog)

      Verilog = readVerilogGates(nameVerilog)
      debugVerilogRead(Verilog)
      # end1 = time.time()
      # print("Runtime of the "+"readVerilogGates"+"step is "+str(end1 - start1))
      # start1 = time.time()
  
  


# ==============================
# MAIN PROGRAM PROCESSING 
# ==============================
ResultsFolder = 'Results/Percent_Infected'

ConvertVerilogToLine('Verilog2',ResultsFolder)

ConvertVerilogToLine('NORVerilog2',ResultsFolder)






