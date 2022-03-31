import shutil
import os
import random
import sys

from pip import main

def mkdir(Folder):
  if not os.path.exists(Folder):
    os.makedirs(Folder)

def mkSplitDirs(Foldername):
  mkdir(Foldername)
  mkdir(Foldername+'/Test')
  mkdir(Foldername+'/Train')
  mkdir(Foldername+'/Validation')
  mkdir(Foldername+'/Test/Uninfected')
  mkdir(Foldername+'/Train/Uninfected')
  mkdir(Foldername+'/Validation/Uninfected')
  mkdir(Foldername+'/Test/Infected')
  mkdir(Foldername+'/Train/Infected')
  mkdir(Foldername+'/Validation/Infected')

def mkdirsInfUninf(Foldername):
  mkdir(Foldername)
  mkdir(Foldername+'/Uninfected')
  mkdir(Foldername+'/Infected')

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

def ResplitData(InputFolder,OutputFolder,TrainSplit,ValSplit,TestSplit):
  mkSplitDirs(OutputFolder)
  emptyDirectories(OutputFolder)

  if TrainSplit+ValSplit+TestSplit != 100:
    raise

  for name in [InputFolder+'/Test/',InputFolder+'/Train/',InputFolder+'/Validation/']:
    for name2 in ['Uninfected/','Infected/']:
      for nameVerilog1 in os.listdir(name+name2):
        nameVerilog = os.path.join(name+name2,nameVerilog1)

        rand = random.randint(0, 100)
        if rand < TrainSplit:
          test = 'Train'
        elif rand < TrainSplit+ValSplit:
          test = 'Validation'
        else:
          test = 'Test'
        
        outputLocation = OutputFolder+'/'+test+'/'+name2
        shutil.copy(nameVerilog,outputLocation)

        print("Moved "+nameVerilog+ " to "+ outputLocation+nameVerilog1+"\n")


##########
# MAIN
##########

ResplitData('K-MersRandomMut_custom3','K-MersRandomMut_custom3_Shuffle',60,20,20)
ResplitData('K-MersRandomMut_custom_NOR3','K-MersRandomMut_custom_NOR3_Shuffle',60,20,20)
ResplitData('Verilog3_Nueral','Verilog3_Neural_Shuffle',60,20,20)
ResplitData('NORVerilog3_Nueral','NORVerilog3_Neural_Shuffle',60,20,20)

