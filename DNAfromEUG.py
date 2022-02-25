# Author: Nicholas Haehn
# Date 7/1/2021
# Program to read .eug file and create resulting DNA sequence

import os
import glob
from datetime import datetime
import numpy
import os.path

class part:
  name = ''
  sequence = ''
  type = ''
  def __init__(self, name = '',type = '', sequence = ''):
    self.name = name
    self.sequence = sequence
    self.type = type

class device:
  name = ''
  partOrder = []

  # def __init__(self, otherClass):
  #   self.name = otherClass.name
  #   self.partOrder = otherClass.partOrder
  def __init__(self, name = '', partOrder = []):
    self.name = name
    self.partOrder = partOrder

def readParts(EugFileP):
  EugFile = open(EugFileP, 'r')
  partsAvailable = []
  partsListFound = 0
  #print("\nReading Eugene Parts\n")
  #print("Parts Possible: ")
  for lines in EugFile.readlines():  
    if lines == '\n':
      partsListFound = partsListFound + 1

    if partsListFound == 1 and lines != '\n':
      temp = part()
      temp.type, partInfo = lines.split()
      D = partInfo.split('(')
      temp.name = D[0]
      partSeq = D[2].split('"')
      temp.sequence = partSeq[1]
      partsAvailable.append(part(temp.name, temp.type, temp.sequence))
      # print('{0}\t{1}\t{2}\n'.format(temp.name, temp.type, temp.sequence))   
      #print('{0}'.format(temp.name).ljust(15) + '{0}'.format(temp.type).ljust(15) + '{0}\n'.format(temp.sequence).ljust(15))
  EugFile.close()
  return partsAvailable

def readDevices(EugFileD, partsAvailable):
  EugFile = open(EugFileD, 'r')
  devices = []
  partsListFound = 0
  cont = False
  usedParts = []
  #print("Devices:")
  temp = device()
  for lines in EugFile.readlines(): 
    if lines == '\n':
      partsListFound = partsListFound + 1

    if lines == ');\n':
      cont = False
    
    if cont:
      partLine = lines.split(',')
      cass = False
      for words in lines.split('_'):
        if words == 'cassette\n':
          cass = True
      if lines == ('    YFP_cassette\n') or lines == ('    RFP_cassette\n') or lines == ('    BFP_cassette\n') or lines == ('    sigmaK1FR_cassette\n') or lines == ('    sigmaT3_cassette\n') or lines == ('    sigmaT7_cassette\n') or lines == ('    sigmaCGG_cassette\n'):
        cass = False
      if cass:
        ribozyme = ''
        rbs = ''
        cds = lines.split('_')[1]
        terminator = ''
        for parts in partsAvailable:
          usedP = False
          for used in usedParts:
            if parts.name == used:
              usedP = True
          if usedP:
            continue
          elif parts.type == 'ribozyme' and ribozyme == '':
            ribozyme = parts.name
            usedParts.append(parts.name)
          elif parts.type == 'rbs' and rbs == '':
            rbs = parts.name
            usedParts.append(parts.name)
          elif parts.type == 'terminator' and terminator == '':
            terminator = parts.name
            usedParts.append(parts.name)
        temp.partOrder.append(ribozyme)
        temp.partOrder.append(rbs)
        temp.partOrder.append(cds)
        temp.partOrder.append(terminator)
        #print('\t{0}\n\t{1}\n\t{2}\n\t{3}\n'.format(ribozyme,rbs,cds,terminator))
      else:
        partLine = partLine[0].split()
        if len(partLine) != 0:
          temp.partOrder.append(partLine[0])
          #print('\t{0}'.format(partLine[0]))

    if (partsListFound >= 3 and lines != '\n'):
      lists = lines.split()
      if lists[0] == 'Device':
        devName = lists[1].split('(')
        temp.name = devName[0]
        #print(temp.name)
        cont = True
      elif lists[0] == 'Rule':
        partsListFound = -1000
    if(partsListFound >= 3 and lines == '\n'):
      # print('\nName: {0} Order: {1}'.format(temp.name, temp.partOrder))
      devices.append(device(temp.name, temp.partOrder))
      temp.name = ''
      temp.partOrder = []
  devices.pop()
  del devices[0]
  EugFile.close()
  return devices
      
def readOrder(EugFileR):
  EugFile = open(EugFileR, 'r')
  cont = False
  Circuit = device()
  Circuit.name = 'Circuit'
  CircuitContains = []
  Before = []
  for lines in EugFile.readlines(): 
    if len(lines.split()) > 1 and lines.split()[1] == 'CircuitRule0(':
      cont = True
    elif lines == ');\n':
      cont = False
    elif len(lines.split()) > 1 and cont == True:
      if lines.split()[0] == 'CONTAINS':
        CircuitContains.append(lines.split()[1])
      elif lines.split()[1] == 'BEFORE':
        brr = []
        brr.append(lines.split()[0])
        brr.append(lines.split()[2])
        Before.append(brr)
      elif lines.split()[1] == 'AFTER':
        arr = []
        arr.append(lines.split()[2])
        arr.append(lines.split()[0])
        Before.append(arr)
  EugFile.close()
  Circuit.partOrder = CircuitContains
  ordered = False
  while ordered == False:
    if len(Before) > 0:
      for array in Before:
        if Circuit.partOrder.count(array[0]) == 0:
          Circuit.partOrder.append(array[0])
        if Circuit.partOrder.count(array[1]) == 0:
          Circuit.partOrder.append(array[1])
        if Circuit.partOrder.index(array[0]) > Circuit.partOrder.index(array[1]):
          ordered = False
          del Circuit.partOrder[Circuit.partOrder.index(array[0])]
          Circuit.partOrder.insert(Circuit.partOrder.index(array[1]), array[0])
        else:
          ordered = True
    else:
      for k in range(len(Circuit.partOrder)):
        if Circuit.partOrder[k].split('_')[1] == 'reporterDevice':
          temp = Circuit.partOrder[k]
          del Circuit.partOrder[k]
          Circuit.partOrder.append(temp)
        else:
          ordered = True
  
  #print('\nOrdered Devices:')
  #for parts in range(0,len(Circuit.partOrder)):
  #  print('\t{0}'.format(Circuit.partOrder[parts]))

  return Circuit
        
def simplifyOrder(Circuit, devices):
  for largeDevs in Circuit.partOrder:
    for smallDev in devices:
      if largeDevs == (smallDev.name + 'Device'):
        index = Circuit.partOrder.index(largeDevs)
        for k in range(0,len(smallDev.partOrder)):
          Circuit.partOrder.insert(index+k, smallDev.partOrder[k])
        del Circuit.partOrder[Circuit.partOrder.index(largeDevs)]

  #print("\nSimplified Ordered Devices:")
  #for k in Circuit.partOrder: print('\t{0}'.format(k))
  return Circuit

def splitCircuit(Circuit):
  partCircuit = device()
  partOutput = device()
  CircuitParts = []
  OutputParts = []

  partCircuit.name = 'Circuit'
  partOutput.name = 'Output'
  output = False
  for parts in Circuit.partOrder:
    if (parts == 'L1') or (parts == 'L2'):
      continue
    elif (Circuit.partOrder.index(parts)+1) < len(Circuit.partOrder):
      if len(Circuit.partOrder[(Circuit.partOrder.index(parts)+1)].split('_')) > 1:
        if Circuit.partOrder[(Circuit.partOrder.index(parts)+1)].split('_')[1] == 'cassette':
          output = True
    if output == False:
      CircuitParts.append(parts)
    elif output == True:
      OutputParts.append(parts)

  partCircuit.partOrder = CircuitParts
  partOutput.partOrder = OutputParts
  #print('\nCircuit Ordered Devices:')
  #for k in partCircuit.partOrder: print('\t{0}'.format(k))
  #print('\nOutput Ordered Devices:')
  #for k in partOutput.partOrder: print('\t{0}'.format(k))

  return partCircuit, partOutput

def writeDNA(deviceList, partsAvailable):
  DNA = ''
  for parts in deviceList.partOrder:
    for avail in partsAvailable:
      if parts == avail.name:
        DNA = DNA + avail.sequence

  #print('\n{0} DNA: \n{1}'.format(deviceList.name, DNA))
  return DNA

def writeFullDNA(deviceList, DNA, baseDNA, loc):
  FullDNA = baseDNA[:loc - 1] + DNA + baseDNA[loc - 1:]
  #print('\n{0} DNA Full: \n{1}'.format(deviceList.name, FullDNA))
  return FullDNA

def writeDNAtxtFile(EugFile, curFile, numFiles, TrainSplit, DNA, type):
  # preprocess DNA name
  EugFileSplit = EugFile.split('\\')[len(EugFile.split('\\'))-1]
  EugFileSplit = EugFileSplit.split('_')
  DNAName = EugFileSplit[0]
  for k in range(1, len(EugFileSplit)-1):
    DNAName = DNAName + '_' + EugFileSplit[k]
  
  if curFile/numFiles <= TrainSplit:
    UseCase = 'Train'
  else:
    UseCase = 'Test'
  circuitStat = os.path.relpath(EugFile).split('\\')[1]
  # DNAFile = open('DNA/' + UseCase + '/' + circuitStat + '/' + DNAName + '_' + type + '_DNA.txt', 'w')
  if os.path.exists('DNA/' + circuitStat + '/' + DNAName + '_' + type + '_DNA.txt') == False:
    DNAFile = open('DNA/' + circuitStat + '/' + DNAName + '_' + type + '_DNA.txt', 'w')
    DNAFile.write(DNA)
    # print("\nWriting to DNA to File: {0}".format('DNA/' + UseCase + '/' + circuitStat + '/' + DNAName + '_' + type + '_DNA.txt'))
    print("\nWriting to DNA to File: {0}".format('DNA/' + circuitStat + '/' + DNAName + '_' + type + '_DNA.txt'))
    DNAFile.close()
  else:
    print("\nFile already exists in DNA")

def processEug(EugFile, curFile, numFiles, TrainSplit, CircuitDNARaw, CircuitLoc, OutputDNARaw, OutputLoc):
  #print('-----------------------------------------------------')
  #print("Processing {0}".format(EugFile))
  partsAvailable = readParts(EugFile)
  devices = readDevices(EugFile, partsAvailable)
  # for dev in devices:
  #   print('Device: {0}, Order: {1}'.format(dev.name, dev.partOrder))
  # for parts in partsAvailable:
  #   print('Part: {0}, Type: {1}, Seq: {2}'.format(parts.name, parts.type, parts.sequence))
  Circuit = readOrder(EugFile)
  Circuit = simplifyOrder(Circuit, devices)
  Circuit, Output = splitCircuit(Circuit)
  CircuitDNA = writeDNA(Circuit, partsAvailable)
  OutputDNA = writeDNA(Output, partsAvailable)
  CircuitFullDNA = writeFullDNA(Circuit, CircuitDNA, CircuitDNARaw, CircuitLoc)
  OutputFullDNA = writeFullDNA(Output, OutputDNA, OutputDNARaw, OutputLoc)
  writeDNAtxtFile(EugFile, curFile, numFiles, TrainSplit, CircuitFullDNA + OutputFullDNA, 'Circuit') #only need Circuit DNA. Most outputs will be the same, or have differences covered by circuit
  #writeDNAtxtFile(EugFile, curFile, numFiles, TrainSplit, CircuitFullDNA, 'Circuit') #only need Circuit DNA. Most outputs will be the same, or have differences covered by circuit

circuitDNARaw =  'CCAATTATTGAAGGCCTCCCTAACGGGGGGCCTTTTTTTGTTTCTGGTCTCCCgcttctg' + \
  'tcttctgcaccatatgcggtgtgaaataccgcacagatgcgtaaggagaaaataccgcat' + \
  'caggcgccattcgccattcaggctgcgcaactgttgggaagggcgatcggtgcgggcctc' + \
  'ttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaac' + \
  'gccagggttttcccagtcacgacgttgtaaaacgacggccagtgaattcgagctcggtac' + \
  'ccggggatcctctagagtcgacctgcaggcatgcaagcttggcgtaatcatggtcatagc' + \
  'tgtttcctgtgtgaaattgttatccgctcacaattccacacaacatacgagccggaagca' + \
  'taaagtgtaaagcctggggtgcctaatgagtgagctaactcacattaattgcgttgcgct' + \
  'cactgcccgctttccagtcgggaaacctgtcgtgccagctgcattaatgaatcggccaac' + \
  'gcgcggggaagacagaatgAGGTGCTTCCTCGCTCACTGACTCGCTGCACGAGGCAGACC' + \
  'TCAGCGCTAGCGGAGTGTATACTGGCTTACTATGTTGGCACTGATGAGGGTGTCAGTGAA' + \
  'GTGCTTCATGTGGCAGGAGAAAAAAGGCTGCACCGGTGCGTCAGCAGAATATGTGATACA' + \
  'GGATATATTCCGCTTCCTCGCTCACTGACTCGCTACGCTCGGTCGTTCGACTGCGGCGAG' + \
  'CGGAAATGGCTTACGAACGGGGCGGAGATTTCCTGGAAGATGCCAGGAAGATACTTAACA' + \
  'GGGAAGTGAGAGGGCCGCGGCAAAGCCGTTTTTCCATAGGCTCCGCCCCCCTGACAAGCA' + \
  'TCACGAAATCTGACGCTCAAATCAGTGGTGGCGAAACCCGACAGGACTATAAAGATACCA' + \
  'GGCGTTTCCCCTGGCGGCTCCCTCGTGCGCTCTCCTGTTCCTGCCTTTCGGTTTACCGGT' + \
  'GTCATTCCGCTGTTATGGCCGCGTTTGTCTCATTCCACGCCTGACACTCAGTTCCGGGTA' + \
  'GGCAGTTCGCTCCAAGCTGGACTGTATGCACGAACCCCCCGTTCAGTCCGACCGCTGCGC' + \
  'CTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGAAAGACATGCAAAAGCACCACTGGC' + \
  'AGCAGCCACTGGTAATTGATTTAGAGGAGTTAGTCTTGAAGTCATGCGCCGGTTAAGGCT' + \
  'AAACTGAAAGGACAAGTTTTGGTGACTGCGCTCCTCCAAGCCAGTTACCTCGGTTCAAAG' + \
  'AGTTGGTAGCTCAGAGAACCTTCGAAAAACCGCCCTGCAAGGCGGTTTTTTCGTTTTCAG' + \
  'AGCAAGAGATTACGCGCAGACCAAAACGATCTCAAGAAGATCATCTTATTAAGGGGTCTG' + \
  'ACGCTCAGTGGAACGAAAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAGTT' + \
  'ACCTTAGAAAAACTCATCGAGCATCAAATGAAACTGCAATTTATTCATATCAGGATTATC' + \
  'AATACCATATTTTTGAAAAAGCCGTTTCTGTAATGAAGGAGAAAACTCACCGAGGCAGTT' + \
  'CCATAGGATGGCAAGATCCTGGTATCGGTCTGCGATTCCGACTCGTCCAACATCAATACA' + \
  'ACCTATTAATTTCCCCTCGTCAAAAATAAGGTTATCAAGTGAGAAATCACCATGAGTGAC' + \
  'GACTGAATCCGGTGAGAATGGCAAAAGCTTATGCATTTCTTTCCAGACTTGTTCAACAGG' + \
  'CCAGCCATTACGCTCGTCATCAAAATCACTCGCATCAACCAAACCGTTATTCATTCGTGA' + \
  'TTGCGCCTGAGCGAGACGAAATACGCGATCGCTGTTAAAAGGACAATTACAAACAGGAAT' + \
  'CGAATGCAACCGGCGCAGGAACACTGCCAGCGCATCAACAATATTTTCACCTGAATCAGG' + \
  'ATATTCTTCTAATACCTGGAATGCTGTTTTCCCGGGGATCGCAGTGGTGAGTAACCATGC' + \
  'ATCATCAGGAGTACGGATAAAATGCTTGATGGTCGGAAGAGGCATAAATTCCGTCAGCCA' + \
  'GTTTAGTCTGACCATCTCATCTGTAACATCATTGGCAACGCTACCTTTGCCATGTTTCAG' + \
  'AAACAACTCTGGCGCATCGGGCTTCCCATACAATCGATAGATTGTCGCACCTGATTGCCC' + \
  'GACATTATCGCGAGCCCATTTATACCCATATAAATCAGCATCCATGTTGGAATTTAATCG' + \
  'CGGCCTCGAGCAAGACGTTTCCCGTTGAATATGGCTCATAACACCCCTTGTATTACTGTT' + \
  'TATGTAAGCAGACAGTTTTATTGTTCATGATGATATATTTTTATCTTGTGCAATGTACAT' + \
  'CAGAGATTTTGAGACACAA' #pCello_circuit #Logic gates location #CircuitLoc     

outputDNARaw = 'atgagggaagcggtgatcgccgaagtatcgactcaactatcagaggtagttggcgtcatc' + \
  'gagcgccatctcgaaccgacgttgctggccgtacatttgtacggctccgcagtggatggc' + \
  'ggcctgaagccacacagtgatattgatttgctggttacggtgaccgtaaggcttgatgaa' + \
  'acaacgcggcgagctttgatcaacgaccttttggaaacttcggcttcccctggagagagc' + \
  'gagattctccgcgctgtagaagtcaccattgttgtgcacgacgacatcattccgtggcgt' + \
  'tatccagctaagcgcgaactgcaatttggagaatggcagcgcaatgacattcttgcaggt' + \
  'atcttcgagccagccacgatcgacattgatctggctatcttgctgacaaaagcaagagaa' + \
  'catagcgttgccttggtaggtccagcggcggaggaactctttgatccggttcctgaacag' + \
  'gatctatttgaggcgctaaatgaaaccttaacgctatggaactcgccgcccgactgggct' + \
  'ggcgatgagcgaaatgtagtgcttacgttgtcccgcatttggtacagcgcagtaaccggc' + \
  'aaaatcgcgccgaaggatgtcgctgccgactgggcaatggagcgcctgccggcccagtat' + \
  'cagcccgtcatacttgaagctagacaggcttatcttggacaagaagaagatcgcttggcc' + \
  'tcgcgcgcagatcagttggaagaatttgtccactacgtgaaaggcgagatcaccaaggta' + \
  'gtcggcaaataatactagctccggcaaaaaaacgggcaaggtgtcaccaccctgcccttt' + \
  'ttctttaaaaccgaaaagattacttcgcgtttgccacctgacgtctaagaaCTCGGTACC' + \
  'AAACCAATTATTGAAGACGCTGAAAAGCGTCTTTTTTTGTTTCGGTCCGCTTAATGgctc' + \
  'actcaaaggcggtaatacggttatccacagaatcaggggataacgcaggaaagaacatgt' + \
  'gagcaaaaggccagcaaaaggccaggaaccgtaaaaactgtcagaccaagtttacgagct' + \
  'cgcttggactcctgttgatagatccagtaatgacctcagaactccatctggatttgttca' + \
  'gaacgctcggttgccgccgggcgttttttattggtgagaatccaagcactagggacagta' + \
  'agacgggtaagcctgttgatgataccgctgccttactgggtgcattagccagtctgaatg' + \
  'acctgtcacgggataatccgaagtggtcagactggaaaatcagagggcaggaactgctga' + \
  'acagcaaaaagtcagatagcaccacatagcagacccgccataaaacgccctgagaagccc' + \
  'gtgacgggcttttcttgtattatgggtagtttccttgcatgaatccataaaaggcgcctg' + \
  'tagtgccatttacccccattcactgccagagccgtgagcgcagcgaactgaatgtcacga' + \
  'aaaagacagcgactcaggtgcctgatggtcggagacaaaaggaatattcagcgatttgcc' + \
  'cgagcttgcgagggtgctacttaagcctttagggttttaaggtctgttttgtagaggagc' + \
  'aaacagcgtttgcgacatccttttgtaatactgcggaactgactaaagtagtgagttata' + \
  'cacagggctgggatctattctttttatctttttttattctttctttattctataaattat' + \
  'aaccacttgaatataaacaaaaaaaacacacaaaggtctagcggaatttacagagggtct' + \
  'agcagaatttacaagttttccagcaaaggtctagcagaatttacagatacccacaactca' + \
  'aaggaaaaggacatgtaattatcattgactagcccatctcaattggtatagtgattaaaa' + \
  'tcacctagaccaattgagatgtatgtctgaattagttgttttcaaagcaaatgaactagc' + \
  'gattagtcgctatgacttaacggagcatgaaaccaagctaattttatgctgtgtggcact' + \
  'actcaaccccacgattgaaaaccctacaaggaaagaacggacggtatcgttcacttataa' + \
  'ccaatacgctcagatgatgaacatcagtagggaaaatgcttatggtgtattagctaaagc' + \
  'aaccagagagctgatgacgagaactgtggaaatcaggaatcctttggttaaaggctttga' + \
  'gattttccagtggacaaactatgccaagttctcaagcgaaaaattagaattagtttttag' + \
  'tgaagagatattgccttatcttttccagttaaaaaaattcataaaatataatctggaaca' + \
  'tgttaagtcttttgaaaacaaatactctatgaggatttatgagtggttattaaaagaact' + \
  'aacacaaaagaaaactcacaaggcaaatatagagattagccttgatgaatttaagttcat' + \
  'gttaatgcttgaaaataactaccatgagtttaaaaggcttaaccaatgggttttgaaacc' + \
  'aataagtaaagatttaaacacttacagcaatatgaaattggtggttgataagcgaggccg' + \
  'cccgactgatacgttgattttccaagttgaactagatagacaaatggatctcgtaaccga' + \
  'acttgagaacaaccagataaaaatgaatggtgacaaaataccaacaaccattacatcaga' + \
  'ttcctacctacgtaacggactaagaaaaacactacacgatgctttaactgcaaaaattca' + \
  'gctcaccagttttgaggcaaaatttttgagtgacatgcaaagtaagcatgatctcaatgg' + \
  'ttcgttctcatggctcacgcaaaaacaacgaaccacactagagaacatactggctaaata' + \
  'cggaaggatctgaggttcttatggctcttgtatctatcagtgaagcatcaagactaacaa' + \
  'acaaaagtagaacaactgttcaccgttagatatcaaagggaaaactgtccatatgcacag' + \
  'atgaaaacggtgtaaaaaagatagatacatcagagcttttacgagtttttggtgcattta' + \
  'aagctgttcaccatgaacagatcgacaatgtaacgattatcaaaaaggatcttcacctag' + \
  'atccttttaaattaaaaatgaagcttcgttgtgtctcaaaatctctgatgttacattgca' + \
  'caagataaaaatatatcatcatgaacaataaaactgtctgcttacataaacagtaataca' + \
  'aggggtgtttactagaggttgatcgggcacgtaagaggttccaactttcaccataatgaa' + \
  'ataagatcactaccgggcgtattttttgagttatcgagattttcaggagctaaggaagct' + \
  'aaa' #pAN1201 #OutputLoc

circuitInsertLoc = 54
outputInsertLoc = 953

NumFiles = 0
TrainSplit = 0.8
Files = []
# os.chdir('./Cello_Hardware_Trojans')
for name in glob.glob('Eugene/**/'):
  for nameEug in glob.glob(name + '/*.eug'):
    NumFiles = NumFiles + 1
    Files.insert(numpy.random.random_integers(0, len(Files)), nameEug)
curFile = 0
for EugFile in Files:
  curFile = curFile + 1
  # processEug(EugFile, curFile, NumFiles, TrainSplit, circuitDNARaw, circuitInsertLoc, outputDNARaw, outputInsertLoc)
  processEug(EugFile, curFile, NumFiles, TrainSplit, "", 0, "", 0)

#Test only one file
# NumFiles = 1
# TrainSplit = 0.8
# Files = ["Eugene/Uninfected/gate_level_1_in2_out1_gates1_eugeneScript.eug"]
# curFile = 0
# for EugFile in Files:
#   curFile = curFile + 1
#   processEug(EugFile, curFile, NumFiles, TrainSplit, circuitDNARaw, circuitInsertLoc, outputDNARaw, outputInsertLoc)
 




