import os
import glob
import random
import re

# os.chdir('./Cello_Hardware_Trojans2')

for name in glob.glob('DNA_custom/**/'):
  for nameEug in glob.glob(name + '/*.txt'):
    print(f"\n{nameEug}")
    rand = random.randint(0, 100)
    if rand < 60:
      test = 'Train'
    elif rand < 75:
      test = 'Validation'
    else:
      test = 'Test'
    # test = nameEug.split('\\')[1]
    type = nameEug.split('\\')[1]
    Filename = nameEug.split('\\')[2]

    DNAFile = open(nameEug,'r')
    DNA = DNAFile.readlines()[0]
    DNAFile.close()

    Kmer = ''
    for k in range(len(DNA)-5):
      Kmer = Kmer + DNA[k:k+6] + ' '

    # #Check for repeated files
    repeated = False
    # for fileRepeat in glob.glob('DNA_custom/**/*.txt'):
    #   repeatDNAName = fileRepeat.split('\\')[2]
    #   # print(f"1: {repeatDNAName} 2:{nameEug}")
    #   if repeatDNAName == nameEug.split('\\')[2]:
    #     continue
    #   elif repeated == True:
    #     break
    #   fileRepeatCheck = open(fileRepeat,'r')
    #   DNACheck = fileRepeatCheck.readlines()[0]
    #   fileRepeatCheck.close()
    #   if (len(DNA) == len(DNACheck)):
    #     if ((DNACheck in DNA) or (DNA in DNACheck)):
    #       print(f"Sequence Matches {repeatDNAName}. Checking if at least 1 file run.")
    #       #Let one repeated file through
    #       for fileRepeatRun in glob.glob('K-MersRandom_Custom/**/**/*.txt'):
    #         fileRepeatRunName = fileRepeatRun.split('\\')[3]
    #         # print(f"1: {fileRepeatRunName} 2:{repeatDNAName}")
    #         if fileRepeatRunName == repeatDNAName:
    #           repeated = True
    #           print(f"{nameEug} has a duplicate that has already run. Skipping")
    #           break
    #       if repeated == False:
    #         print(f"{repeatDNAName} has not run yet. Continuing.")
  
    if repeated == False:
      KmerName = 'K-MersRandom_Custom/'+test+'/'+type+'/'+Filename
      KmerFile = open('K-MersRandom_Custom/'+test+'/'+type+'/'+Filename, 'w')       
          
      KmerFile.write(Kmer)
      KmerFile.close()
      print(f"Printed {KmerName}")