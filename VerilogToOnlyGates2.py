import os
from time import perf_counter
from os import read
import random
from tokenize import Name, Number, Single
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
  def __init__(self,name,output,input):
    self.name = name
    self.input = input[:]
    self.output = output
  # def __init__(self, exist):
  #   self.gate = exist.gate
  #   self.input = exist.input
  #   self.output = exist.output

# This class holds the info from a verilog file
class VerilogInfo:
  def __init__(self,name,output,input,wires,gates):
    self.name = name
    self.output = output[:]
    self.input = input[:]
    self.wires = wires[:]
    self.gates = gates[:]
    
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
          tempGate = VerilogGates(gateParts[0],gateParts[1],tempInputs)
        if len(gateParts) == 3:
          tempGate = VerilogGates(gateParts[0],gateParts[1],[gateParts[2]])
        gates.append(tempGate)
    
  return VerilogInfo(name,outputs,inputs,wires,gates)

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

def VerilogLines(nameVerilog):
  VerilogFile = open(nameVerilog,'r')
  Lines = VerilogFile.readlines()
  VerilogFile.close()

  # Remove Comments
  for k in range(0,len(Lines)):
    if len(Lines[k].split('//')) > 1:
      Lines[k] = Lines[k].split('//')[0]

  SingleLine = ''
  #Make single line
  for k in range(0,len(Lines)):
    SingleLine = SingleLine + Lines[k] + ' '

  # Remove Punctuation
  SingleLine = SingleLine.replace('(',' ')
  SingleLine = SingleLine.replace(')',' ')
  SingleLine = SingleLine.replace(';',' ')
  SingleLine = SingleLine.replace(',',' ')
  SingleLine = SingleLine.replace('\n',' ')
  SingleLine = SingleLine.replace('\t',' ')

  SingleLine = ' '.join(SingleLine.split())

  return SingleLine

def renameVarsVerilog(Verilog, SingleLineVerilog):
  # Rename Verilog Module
  name = Verilog.name
  if name.split('_')[0] == "Inf":
    newName = name.split('_')[1]
    for k in range(2,len(name.split('_'))):
      newName = newName + "_" + name.split('_')[k]
    name = newName

  SingleLineVerilog = SingleLineVerilog.replace(Verilog.name,name)

  # Rename inputs
  for inIndex in range(len(Verilog.input)-1,-1,-1):
    inNameOld = Verilog.input[inIndex]
    inNameNew = "in" + str(inIndex)

    SingleLineVerilog = SingleLineVerilog.replace(inNameOld,inNameNew)

  # Rename outputs
  for outIndex in range(len(Verilog.output)-1,-1,-1):
    outNameOld = Verilog.output[outIndex]
    outNameNew = "out" + str(outIndex)

    SingleLineVerilog = SingleLineVerilog.replace(outNameOld,outNameNew)

  # Rename wires
  for wireIndex in range(len(Verilog.wires)-1,-1,-1):
    wireNameOld = Verilog.wires[wireIndex]
    wireNameNew = "wire" + str(wireIndex)

    SingleLineVerilog = SingleLineVerilog.replace(wireNameOld,wireNameNew)

  return SingleLineVerilog

def emptyDirectories(FilePath):
  print("Emptying Directories")
  # os.mkdir(FilePath)
  
  for test in ["Test","Train","Validation"]:
    # os.mkdir(FilePath + '/' + test)
  # Empty Directories
    folder = os.path.join(sys.path[0], FilePath + '/' + test + '/Uninfected')
    # os.mkdir(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    folder = os.path.join(sys.path[0], FilePath + '/' + test + '/Infected')
    # os.mkdir(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

  print(FilePath+" emptied.")

def printVectors(Folder,nameVerilog, SingleLine):
  type, Filename = getFileValues(nameVerilog)

  rand = random.randint(0, 100)
  if rand < 60:
    test = 'Train'
  elif rand < 75:
    test = 'Validation'
  else:
    test = 'Test'

  name = Folder + "/" + test + "/" + type + "/" + Filename + ".txt"

  # print(name)

  DNAFile = open(name,"w")
  DNAFile.write(SingleLine)
  DNAFile.close()

# ==============================
# MAIN PROGRAM PROCESSING 
# ==============================
InputFolder = 'Verilog3'
OutputFolder = 'Verilog3_Nueral'
#Clear Directory
emptyDirectories(OutputFolder)

# Loop through Verilog files
for name in [InputFolder+'/Infected/']:
# for name in [InputFolder+'/Uninfected/',InputFolder+'/Infected/']:
  for nameVerilog in os.listdir(name):
    # start = start1 = time.time()
    nameVerilog = os.path.join(name,nameVerilog)
    # end1 = time.time()
    # print("Runtime of the "+"os.path.join"+"step is "+str(end1 - start1))
    # start1 = time.time()

    # Create DNA 

    # print file being processed
    print("\n"+nameVerilog)

    # Get file parameters
    type, Filename = getFileValues(nameVerilog)
    # end1 = time.time()
    # print("Runtime of the "+"getFileValues"+"step is "+str(end1 - start1))
    # start1 = time.time()

    Verilog = readVerilogGates(nameVerilog)
    #debugVerilogRead(Verilog)
    # end1 = time.time()
    # print("Runtime of the "+"readVerilogGates"+"step is "+str(end1 - start1))
    # start1 = time.time()

    #Create Single Line
    VerilogLine = VerilogLines(nameVerilog)

    print(VerilogLine)
    VerilogLine = renameVarsVerilog(Verilog, VerilogLine)
    print(VerilogLine)

    # printVectors(OutputFolder,nameVerilog, VerilogLine)
