import glob
from os import read
import random
import re
from tokenize import Number
from typing import Sequence
import os
import shutil
import sys


# Given an entire file string, this function gets the type (folder before) and filename
def getFileValues(nameVerilog):
  type = nameVerilog.split('\\')[1]
  Filename = nameVerilog.split('\\')[2]
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
  print(f"\nVerilog File Name: {Verilog.name}")
  print(f"Verilog Input List: {Verilog.input}")
  print(f"Verilog Output List: {Verilog.output}")
  print(f"Verilog Wire List: {Verilog.wires}\n")
    
  for k in range(0,len(Verilog.gates)):
    print(f"\t Verilog gate {k}: {Verilog.gates[k].name}")
    print(f"\t Gate {k} inputs: {Verilog.gates[k].input}")
    print(f"\t Gate {k} outputs: {Verilog.gates[k].output}\n")

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
      print(f"Terminator use: {t.use}")
  for p in promoter:
    pnum += 1
    # print(f"p.use: {p.use}")
    if p.use != "":
      print(f"promoter use: {p.use}")
  
  print(f"P: {pnum}")
  print(f"T: {tnum}")

  print(f"Type Order: {TypeOrder}\n")
  print(f"Part Order: {PartOrder}\n")
  print(f"Sequence Order: {SequenceOrder}\n")

  

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

  #Assign gates
  for gateNum in range(0,len(Verilog.gates)):

    # Add initial Scar
    TypeOrder.append("Scar")
    PartOrder.append(scar[scarNum].name)
    SequenceOrder.append(scar[scarNum].sequence)
    if scarNum+1 >= len(scar):
      scarNum = 0
    else:
      scarNum += 1

    # Add inputs/promoters
    for inputs in range(0,len(Verilog.gates[gateNum].input)):
      for p in promoter:
        if p.use == Verilog.gates[gateNum].input[inputs]:
          TypeOrder.append(Verilog.gates[gateNum].input[inputs])
          PartOrder.append(p.name)
          SequenceOrder.append(p.sequence)
        # if p.use != "":
        #   print(f"Verilog: {Verilog.gates[gateNum].input[inputs]}")
        #   print(f"promoter: {p.use}")
        

    # Add ribozyme
    TypeOrder.append("Ribozyme")
    PartOrder.append(ribozyme[ribozymeNum].name)
    SequenceOrder.append(ribozyme[ribozymeNum].sequence)
    ribozymeNum += 1
    if ribozymeNum+1 >= len(ribozyme):
      ribozymeNum = 0
    else:
      ribozymeNum += 1

    # Add rbs
    TypeOrder.append("rbs")
    PartOrder.append(rbs[rbsNum].name)
    SequenceOrder.append(rbs[rbsNum].sequence)
    if rbsNum+1 >= len(rbs):
      rbsNum = 0
    else:
      rbsNum += 1
    
    # Add cds/gene/gate
    for g in cds:
      if g.use == Verilog.gates[gateNum].name:
        TypeOrder.append(Verilog.gates[gateNum].name)
        PartOrder.append(g.name)
        SequenceOrder.append(g.sequence)
      # if g.use != "":
      #   print(f"Verilog: {Verilog.gates[gateNum].name}")
      #   print(f"gene: {g.use}")

    # Add terminators/outputs
    for t in terminator:
      if t.use == Verilog.gates[gateNum].output:
        TypeOrder.append(Verilog.gates[gateNum].output)
        PartOrder.append(t.name)
        SequenceOrder.append(t.sequence)
      # if t.use != "":
      #   print(f"Verilog: {Verilog.gates[gateNum].output}")
      #   print(f"Terminator: {t.use}")
    
  # Add output cassettes
  for outputNum in range(0,len(Verilog.output)):
    
    # Add output scar
    TypeOrder.append("Scar")
    PartOrder.append(scar[scarNum].name)
    SequenceOrder.append(scar[scarNum].sequence)
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
    
    # Add cassette
    TypeOrder.append("cassette")
    PartOrder.append(cassette[cassetteNum].name)
    SequenceOrder.append(cassette[cassetteNum].sequence)
    cassetteNum += 1
    if cassetteNum+1 >= len(cassette):
      cassetteNum = 0
    else:
      cassetteNum += 1
  
  # Add final output scar
  TypeOrder.append("Scar")
  PartOrder.append(scar[scarNum].name)
  SequenceOrder.append(scar[scarNum].sequence)
  if scarNum+1 >= len(scar):
    scarNum = 0
  else:
    scarNum += 1
  
  return TypeOrder, PartOrder, SequenceOrder

def printDNAFiles(nameVerilog, SequenceOrder):
  DNA = ""
  for w in range(0,len(SequenceOrder)):
    DNA += SequenceOrder[w]
  
  # print(f"DNA: {DNA}")

  type, Filename = getFileValues(nameVerilog)

  name = "DNA_Custom\\" + type + "\\" + Filename + ".txt"

  # print(name)

  DNAFile = open(name,"w")
  DNAFile.write(DNA)
  DNAFile.close()

def printKmerFile(Folder, nameVerilog, ModKmer):
  type, Filename = getFileValues(nameVerilog)

  name = Folder + "\\" + type + "\\" + Filename + ".txt"

  # print(name)

  DNAFile = open(name,"w")
  DNAFile.write(ModKmer)
  DNAFile.close()

def ModifyKmer(Kmer):
  Ks = list(Kmer)
  #Add mutations
  for index in range(0, len(Kmer)):
    base = ["a","c","t","g"]
    if random.randint(0, 100) == 1 and Kmer[index] != " ":
      Ks[index] = base[random.randint(0, 3)]
  
  ModKmer = "".join(Ks)
  return ModKmer

def KmerCreator(SequenceOrder):
  DNA = ""
  for w in range(0,len(SequenceOrder)):
    DNA += SequenceOrder[w]

  # print(f"\nDNA: {DNA}\n")
  Kmer = ''
  for k in range(len(DNA)-5):
    Kmer = Kmer + DNA[k:k+6] + ' '
  # print(f"\nKmer: {Kmer}\n")

  ModKmer = ModifyKmer(Kmer)
  # print(f"\nModKmer: {ModKmer}\n")
  return ModKmer

# Convert DNA (a,c,t,g) to Hexadecimal
def VectorizeKmer(ModKmer):
  KmerArray = ModKmer.split(" ")
  VectorArray = []
  for CurrentKmer in KmerArray:
    NumberizedChars = []

    # Base 4 DNA sequences
    for char in CurrentKmer:
      if char == "a" or char == 'A':
        NumberizedChars.append('0')
      elif char == "c" or char == 'C':
        NumberizedChars.append('1')
      elif char == "t" or char == 'T':
        NumberizedChars.append('2')
      elif char == "g" or char == 'G':
        NumberizedChars.append('3')
      else:
        NumberizedChars.append("9")
  
    HexChars = []
    # Base 16 DNA sequences
    for i in range(1,len(NumberizedChars),2):
      BaseHex = int(NumberizedChars[i])*4+int(NumberizedChars[i-1])

      # Convert to Hex notation
      if BaseHex < 10:
        HexChars.append(str(BaseHex))
      elif BaseHex == 10:
        HexChars.append("A")
      elif BaseHex == 11:
        HexChars.append("B")
      elif BaseHex == 12:
        HexChars.append("C")
      elif BaseHex == 13:
        HexChars.append("D")
      elif BaseHex == 14:
        HexChars.append("E")
      elif BaseHex == 15:
        HexChars.append("F")

    # print(CurrentKmer)
    # print("".join(NumberizedChars))
    # print("".join(HexChars))

    VectorArray.append("".join(HexChars))

  VectorString = " ".join(VectorArray)
  # print(VectorString)
  return VectorString 

def printVectors(Folder,nameVerilog, VectorizedKmer):
  type, Filename = getFileValues(nameVerilog)

  rand = random.randint(0, 100)
  if rand < 60:
    test = 'Train'
  elif rand < 75:
    test = 'Validation'
  else:
    test = 'Test'

  name = Folder + "\\" + test + "\\" + type + "\\" + Filename + ".txt"

  # print(name)

  DNAFile = open(name,"w")
  DNAFile.write(VectorizedKmer)
  DNAFile.close()

def emptyDirectories(FilePath):
  print("Emptying Directories")
  for test in ["Test","Train","Validation"]:
  # Empty Directories
    # folder = os.path.join(sys.path[0], FilePath + '/' + test + '/Uninfected')
    # for filename in os.listdir(folder):
    #     file_path = os.path.join(folder, filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))

    folder = os.path.join(sys.path[0], FilePath + '/' + test + '/Infected')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

  print(f"{FilePath} emptied.")

# ==============================
# MAIN PROGRAM PROCESSING 
# ==============================

#Clear Directory
emptyDirectories('K-MersRandomMut_custom')

# Read all DNA parts from files
readAllDNAParts()

# Loop through Verilog files
for name in ('Verilog\\Infected\\',''):
  for nameVerilog in glob.glob(name + '/*.v'):

    # Create DNA 

    # print file being processed
    #print(f"\n{nameVerilog}")

    # Get file parameters
    type, Filename = getFileValues(nameVerilog)

    Verilog = readVerilogGates(nameVerilog)
    #debugVerilogRead(Verilog)

    assignDNAParts(Verilog)

    TypeOrder, PartOrder, SequenceOrder = createDNASequence(Verilog)
    
    # debugDNA(TypeOrder, PartOrder, SequenceOrder)
    # printDNAFiles(nameVerilog, SequenceOrder)

    # Create Kmer
    ModKmer = KmerCreator(SequenceOrder)

    # printKmerFile("DNA_Custom",nameVerilog, ModKmer)

    # Vectorize Data
    VectorizedKmer = VectorizeKmer(ModKmer)

    printVectors("K-MersRandomMut_custom",nameVerilog, VectorizedKmer)

    clearDNAAssignments()

    

    





    







