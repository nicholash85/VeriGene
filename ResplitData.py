import shutil
import os
import random

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

def ResplitData(InputFolder,OutputFolder,TrainSplit,ValSplit,TestSplit):
  mkSplitDirs(OutputFolder)

  if TrainSplit+ValSplit+TestSplit != 100:
    raise

  for name in [InputFolder+'/Test/',InputFolder+'/Train/',InputFolder+'/Validation/']:
    for name2 in ['Uninfected/','Infected/']:
      for nameVerilog in os.listdir(name+name2):
        nameVerilog = os.path.join(name+name2,nameVerilog)

        rand = random.randint(0, 100)
        if rand < TrainSplit:
          test = 'Train'
        elif rand < TrainSplit+ValSplit:
          test = 'Validation'
        else:
          test = 'Test'
        
        shutil.copy(nameVerilog,OutputFolder+'/'+test+'/'+name2)


##########
# MAIN
##########

ResplitData('K-MersRandomMut_custom3','K-MersRandomMut_custom3_Shuffle',60,20,20)
ResplitData('K-MersRandomMut_custom_NOR3','K-MersRandomMut_custom_NOR3_Shuffle',60,20,20)
ResplitData('Verilog3_Nueral','Verilog3_Neural_Shuffle',60,20,20)
ResplitData('NORVerilog3_Nueral','NORVerilog3_Neural_Shuffle',60,20,20)

