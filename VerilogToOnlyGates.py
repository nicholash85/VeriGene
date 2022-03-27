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

def VerilogLines(nameVerilog):
  VerilogFile = open(nameVerilog,'r')
  Lines = VerilogFile.readlines()
  VerilogFile.close()
  
  print(Lines)

  # Remove Comments
  for k in range(0,len(Lines)):
    if len(Lines[k].split('//')) > 1:
      Lines[k] = Lines[k].split('//')[0]

  print(Lines) 

  SingleLine = ''
  #Make single line
  for k in range(0,len(Lines)):
    SingleLine + Lines[k] + ' '
  
  print(SingleLine)

  # Remove Punctuation
  SingleLine.replace('(',' ')
  SingleLine.replace(')',' ')
  SingleLine.replace(';',' ')
  SingleLine.replace(',',' ')
  SingleLine.replace('\n',' ')
  SingleLine.replace('\t',' ')

  print(SingleLine)

  return SingleLine

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

def emptyDirectories(FilePath):
  print("Emptying Directories")
  for test in ["Test","Train","Validation"]:
  # Empty Directories
    folder = os.path.join(sys.path[0], FilePath + '/' + test + '/Uninfected')
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

# ==============================
# MAIN PROGRAM PROCESSING 
# ==============================
InputFolder = 'Verilog2'
OutputFolder = 'Verilog2_Nueral'
#Clear Directory
emptyDirectories(OutputFolder)

# Loop through Verilog files
for name in (InputFolder+'/Uninfected/',InputFolder+'/Infected/'):
  for nameVerilog in os.listdir(name):
    # start = start1 = time.time()
    nameVerilog = os.path.join(name,nameVerilog)
    # end1 = time.time()
    # print("Runtime of the "+"os.path.join"+"step is "+str(end1 - start1))
    # start1 = time.time()

    # Create DNA 

    # print file being processed
    print("\n"+nameVerilog)

    #Create Single Line
    VerilogLine = VerilogLines(nameVerilog)

    printVectors(OutputFolder,nameVerilog, VerilogLine)
    # end1 = time.time()
    # print("Runtime of the "+"printVectors"+"step is "+str(end1 - start1))
    # start1 = time.time()

    

    





    







