import os
from time import perf_counter
from os import read
import random
from tokenize import Name, Number
import os
import shutil
import sys
import time

def VerilogLines(nameVerilog):
  VerilogFile = open(nameVerilog,'r')
  Lines = VerilogFile.readlines()
  VerilogFile.close()

  numInf = 0
  # Remove Comments
  for k in range(0,len(Lines)):
    if len(Lines[k].split('//')) > 1:
      Lines[k] = Lines[k].split('//')[0]
      LineInfo = Lines[k].replace('(',' ')
      LineInfo = LineInfo.replace(')',' ')
      LineInfo = LineInfo.replace(';',' ')
      LineInfo = LineInfo.replace(',',' ')
      LineInfo = LineInfo.replace('\n',' ')
      LineInfo = LineInfo.replace('\t',' ')
      numInf = numInf + len(LineInfo.split())
      

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

  SingleLine = SingleLine.split()
  num = len(SingleLine)

  return numInf,num

def percentInfVerilog(VerilogFolder, ResultsFolder):
  filenames = []
  numInfArr = []
  numArr = []
  PercentInfArr = []

  total = 0
  k = 0
  # Loop through Verilog files
  for name in [VerilogFolder+'/Infected/']:
    for nameVerilog in os.listdir(name):
      nameVerilog = os.path.join(name,nameVerilog)

      # print file being processed
      print("\n"+nameVerilog)
      numInf, num = VerilogLines(nameVerilog)

      filenames.append(nameVerilog)
      numInfArr.append(numInf)
      numArr.append(num)
      PercentInfArr.append(numInf/num)
      total += (numInf/num)
      k += 1
  
  # Print Individual File Percentages
  #Print CSV
  #Headers
  print("Writing " + VerilogFolder + " to CSV")
  csvText = "Filename, Number of Infected, Total Number, Infection Percentage\n"
  for files in range(0,len(filenames)):
      csvText = csvText + filenames[files] + ", " + str(numInfArr[files]) + ", " + str(numArr[files]) + ", " + str(PercentInfArr[files]) + "\n"
  File = open(ResultsFolder+"/"+VerilogFolder+"_Percent_Makeup.csv", "w")
  File.write(csvText)
  File.close()

  percentAve = total/k
  percentStr = VerilogFolder + ": " + str(percentAve) + " Infected"
  print(percentStr)
  
  return VerilogFolder,percentAve
  




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
        if len(Lines[k].split("//")) > 0:
          inf = True
          numInf += 1
          print(Lines[k])
          print(Lines[k].split("//"))
          print(len(Lines[k].split("//")) > 0)
          time.sleep(0.5)
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

class GeneralDNAPart:
  use = ""
  
  def __init__(self,name,sequence,converseName = '', converse = ''):
    self.name = name
    self.sequence = sequence
    #Opposite of the current part. For a promotor, this is its terminator and vice versa
    self.converseName = converseName
    self.converse = converse

def readDNALines(filename):
  file = open('DNA_Parts/' + filename, "r")
  lines = file.readlines()
  file.close()

  names = []
  Sequences = []
  for each in lines:
    each = each.replace("\n","")
    array = each.split(" ")
    if len(array) >= 2:
      names.append(array[0])
      Sequences.append(array[1])
  return names, Sequences

cassette = []
cds = []
promoter = []
rbs = []
ribozyme = []
scar = []
terminator = []
def readGeneralDNAParts(filename):
  DNAtype = filename.split(".")[0]
  names, sequences = readDNALines(filename)

  if DNAtype == "terminator":
    converseNames, converseSequences = readDNALines("promoter.txt")
    for k in range(0,len(names)):
      terminator.append(GeneralDNAPart(names[k],sequences[k],converseNames[k],converseSequences[k]))

  elif DNAtype == "promoter":
    converseNames, converseSequences = readDNALines("terminator.txt")
    for k in range(0,len(names)):
      promoter.append(GeneralDNAPart(names[k],sequences[k],converseNames[k],converseSequences[k]))

  elif DNAtype == "cassette":
    for k in range(0,len(names)):
      cassette.append(GeneralDNAPart(names[k],sequences[k]))
  
  elif DNAtype == "cds":
    for k in range(0,len(names)):
      cds.append(GeneralDNAPart(names[k],sequences[k]))
  
  elif DNAtype == "rbs":
    for k in range(0,len(names)):
      rbs.append(GeneralDNAPart(names[k],sequences[k]))

  elif DNAtype == "ribozyme":
    for k in range(0,len(names)):
      ribozyme.append(GeneralDNAPart(names[k],sequences[k]))

  elif DNAtype == "scar":
    for k in range(0,len(names)):
      scar.append(GeneralDNAPart(names[k],sequences[k]))   

def readAllDNAParts():
  readGeneralDNAParts("terminator.txt")
  readGeneralDNAParts("promoter.txt")
  readGeneralDNAParts("cassette.txt")
  readGeneralDNAParts("cds.txt")
  readGeneralDNAParts("rbs.txt")
  readGeneralDNAParts("ribozyme.txt")
  readGeneralDNAParts("scar.txt")

  logicGates = ["not","nor","or","and","nand","xnor","xor"]
  for k in range(0,len(logicGates)):
    cds[k].use = logicGates[k]

def assignDNAParts(Verilog):

  #Clear current assignments
  clearDNAAssignments()

  #assign promoter use
  for a in range(0,len(Verilog.input)):
    promoter[a].use = Verilog.input[a]
  term = 0
  for q in range(150, 150 + len(Verilog.wires)):
    # print(Verilog.wires[term])
    promoter[q].use = Verilog.wires[term]
    term += 1

  #assign terminator use
  for t in range(0,len(Verilog.output)):
    terminator[t].use = Verilog.output[t]
  term = 0
  for w in range(150, 150 + len(Verilog.wires)):
    # print(f"term: {term}")
    terminator[w].use = Verilog.wires[term]
    term += 1

def debugDNA(TypeOrder, PartOrder, SequenceOrder):
  pnum = 0
  tnum = 0
  for t in terminator:
    tnum += 1
    # print(f"t.use: {t.use}")
    if t.use != "":
      print("Terminator use: +"+t.use)
  for p in promoter:
    pnum += 1
    # print(f"p.use: {p.use}")
    if p.use != "":
      print("promoter use: "+p.use)
  
  print("P: "+pnum)
  print("T: "+tnum)

  print("Type Order: "+TypeOrder+"\n")
  print("Part Order: "+PartOrder+"\n")
  print("Sequence Order: "+SequenceOrder+"\n")

def clearDNAAssignments():
  #unassign promoter use
  for a in range(0,len(promoter)):
    promoter[a].use = ""

  #unassign terminator use
  for t in range(0,len(terminator)):
    terminator[t].use = ""
  
  # print("clear printing")
  # debugDNA([],[],[])

def createDNASequence(Verilog):

  TypeOrder = []
  PartOrder = []
  SequenceOrder = []
  scarNum = 0
  ribozymeNum = 0
  rbsNum = 0
  cassetteNum = 0
  numTot = 0
  numInf = 0

  #Assign gates
  for gateNum in range(0,len(Verilog.gates)):
  
    # Add initial Scar
    if Verilog.gates[gateNum].inf == True:
      numInf = numInf + len(scar[scarNum].sequence)
    numTot = numTot +len(scar[scarNum].sequence)
    if scarNum+1 >= len(scar):
      scarNum = 0
    else:
      scarNum += 1

    # Add inputs/promoters
    for inputs in range(0,len(Verilog.gates[gateNum].input)):
      for p in promoter:
        if p.use == Verilog.gates[gateNum].input[inputs]:
          if Verilog.gates[gateNum].inf == True:
            numInf = numInf + len(p.sequence)
          numTot = numTot +len(p.sequence)
        # if p.use != "":
        #   print(f"Verilog: {Verilog.gates[gateNum].input[inputs]}")
        #   print(f"promoter: {p.use}")
        

    # Add ribozyme
    if Verilog.gates[gateNum].inf == True:
      numInf = numInf + len(ribozyme[ribozymeNum].sequence)
    numTot = numTot +len(ribozyme[ribozymeNum].sequence)
    ribozymeNum += 1
    if ribozymeNum+1 >= len(ribozyme):
      ribozymeNum = 0
    else:
      ribozymeNum += 1

    # Add rbs
    if Verilog.gates[gateNum].inf == True:
      numInf = numInf + len(rbs[rbsNum].sequence)
    numTot = numTot +len(rbs[rbsNum].sequence)
    if rbsNum+1 >= len(rbs):
      rbsNum = 0
    else:
      rbsNum += 1
    
    # Add cds/gene/gate
    for g in cds:
      if g.use == Verilog.gates[gateNum].name:
        if Verilog.gates[gateNum].inf == True:
          numInf = numInf + len(g.sequence)
        numTot = numTot +len(g.sequence)
      # if g.use != "":
      #   print(f"Verilog: {Verilog.gates[gateNum].name}")
      #   print(f"gene: {g.use}")

    # Add terminators/outputs
    for t in terminator:
      if t.use == Verilog.gates[gateNum].output:
        if Verilog.gates[gateNum].inf == True:
          numInf = numInf + len(t.sequence)
        numTot = numTot +len(t.sequence)
      # if t.use != "":
      #   print(f"Verilog: {Verilog.gates[gateNum].output}")
      #   print(f"Terminator: {t.use}")
    
  # Add output cassettes
  for outputNum in range(0,len(Verilog.output)):
    Inf = False
    if Verilog.output[outputNum].split('t')[0] != "ou":
      Inf = True

    # Add output scar
    if Inf == True:
      numInf = numInf + len(scar[scarNum].sequence)
    numTot = numTot +len(scar[scarNum].sequence)
    if scarNum+1 >= len(scar):
      scarNum = 0
    else:
      scarNum += 1

    # Add output promoter
    for t in terminator:
      if t.use == Verilog.output[outputNum]:
        TypeOrder.append(Verilog.output[outputNum])
        PartOrder.append(t.converseName)
        SequenceOrder.append(t.converse)
        if Inf == True:
          numInf = numInf + len(t.converse)
        numTot = numTot +len(t.converse)
    
    # Add cassette
    TypeOrder.append("cassette")
    PartOrder.append(cassette[cassetteNum].name)
    SequenceOrder.append(cassette[cassetteNum].sequence)
    if Inf == True:
      numInf = numInf + len(cassette[cassetteNum].sequence)
    numTot = numTot +len(cassette[cassetteNum].sequence)
    cassetteNum += 1
    if cassetteNum+1 >= len(cassette):
      cassetteNum = 0
    else:
      cassetteNum += 1
  
  # Add final output scar
  if Inf == True:
    numInf = numInf + len(scar[scarNum].sequence)
  numTot = numTot +len(scar[scarNum].sequence)
  if scarNum+1 >= len(scar):
    scarNum = 0
  else:
    scarNum += 1
  
  return numInf,numTot

def RegDNASize(InputFolder, DNAFolder, OutputFolder):
  filenames = []
  numInfArr = []
  numArr = []
  PercentInfArr = []

  total = 0
  k = 0
  # Read all DNA parts from files
  readAllDNAParts()
  # Loop through Verilog files
  for name in [InputFolder+'/Infected/']:
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
      #debugVerilogRead(Verilog)
      # end1 = time.time()
      # print("Runtime of the "+"readVerilogGates"+"step is "+str(end1 - start1))
      # start1 = time.time()

      assignDNAParts(Verilog)
      # end1 = time.time()
      # print("Runtime of the "+"assignDNAParts"+"step is "+str(end1 - start1))
      # start1 = time.time()

      numInf, numTot = createDNASequence(Verilog)
      # end1 = time.time()
      # print("Runtime of the "+"createDNASequence"+"step is "+str(end1 - start1))
      # start1 = time.time()
      
      # debugDNA(TypeOrder, PartOrder, SequenceOrder)
      # printDNAFiles(nameVerilog, SequenceOrder)

      clearDNAAssignments()
      # end1 = time.time()
      # print("Runtime of the "+"clearDNAAssignments"+"step is "+str(end1 - start1))
      # start1 = time.time()

      # end = time.time()
      # print("Runtime of the program is "+str(end - start))
      filenames.append(nameVerilog)
      numInfArr.append(numInf)
      numArr.append(numTot)
      PercentInfArr.append(numInf/numTot)
      total += (numInf/numTot)
      k += 1
  
  # Print Individual File Percentages
  #Print CSV
  #Headers
  print("Writing " + DNAFolder + " to CSV")
  csvText = "Filename, Number of Infected, Total Number, Infection Percentage\n"
  for files in range(0,len(filenames)):
      csvText = csvText + filenames[files] + ", " + str(numInfArr[files]) + ", " + str(numArr[files]) + ", " + str(PercentInfArr[files]) + "\n"
  File = open(OutputFolder+"/"+DNAFolder+"_Percent_Makeup.csv", "w")
  File.write(csvText)
  File.close()

  percentAve = total/k
  percentStr = DNAFolder + ": " + str(percentAve) + " Infected"
  print(percentStr)
  
  return DNAFolder,percentAve

def RegGateSize(InputFolder, OutputFolder):
  filenames = []
  numInfArr = []
  numArr = []
  PercentInfArr = []

  total = 0
  k = 0
  # Read all DNA parts from files
  readAllDNAParts()
  # Loop through Verilog files
  for name in [InputFolder+'/Infected/']:
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
      #debugVerilogRead(Verilog)
      # end1 = time.time()
      # print("Runtime of the "+"readVerilogGates"+"step is "+str(end1 - start1))
      # start1 = time.time()

      filenames.append(nameVerilog)
      numInfArr.append(Verilog.infNum)
      numArr.append(Verilog.normNum)
      PercentInfArr.append(Verilog.infNum/Verilog.normNum)
      total += (Verilog.infNum/Verilog.normNum)
      k += 1
  
  # Print Individual File Percentages
  #Print CSV
  #Headers
  print("Writing " + InputFolder + " to CSV")
  csvText = "Filename, Number of Infected, Total Number, Infection Percentage\n"
  for files in range(0,len(filenames)):
      csvText = csvText + filenames[files] + ", " + str(numInfArr[files]) + ", " + str(numArr[files]) + ", " + str(PercentInfArr[files]) + "\n"
  File = open(OutputFolder+"/"+InputFolder+"_Percent_Makeup.csv", "w")
  File.write(csvText)
  File.close()

  percentAve = total/k
  percentStr = InputFolder + ": " + str(percentAve) + " Infected"
  print(percentStr)
  
  return InputFolder,percentAve

# ==============================
# MAIN PROGRAM PROCESSING 
# ==============================
folders = []
percentage = []
ResultsFolder = 'Results/Percent_Infected'

VerilogFolder, percent = RegGateSize('Verilog2',ResultsFolder)
folders.append(VerilogFolder)
percentage.append(percent)

VerilogFolder, percent = RegGateSize('NORVerilog2',ResultsFolder)
folders.append(VerilogFolder)
percentage.append(percent)

VerilogFolder, percent = RegDNASize('Verilog2','K-MersRandomMut_custom2',ResultsFolder)
folders.append(VerilogFolder)
percentage.append(percent)

VerilogFolder, percent = RegDNASize('NORVerilog2','K-MersRandomMut_custom_NOR2',ResultsFolder)
folders.append(VerilogFolder)
percentage.append(percent)

# Print Individual File Percentages
#Print CSV
#Headers
print("Writing " + "Overall Results" + " to CSV")
csvText = "Folder, Infection Percentage\n"
for files in range(0,len(folders)):
    csvText = csvText + folders[files] + ", " + str(percentage[files]) + "\n"
File = open(ResultsFolder+"/"+"Overall_Percent_Makeup.csv", "w")
File.write(csvText)
File.close()






