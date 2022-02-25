import os
import glob
import random
import re

# os.chdir('./Cello_Hardware_Trojans2')

for name in glob.glob('K-MersRandom/**/**/'):
  for nameEug in glob.glob(name + '/*.txt'):
    print(f"\n{nameEug}")
    test = nameEug.split('\\')[1]
    type = nameEug.split('\\')[2]
    Filename = nameEug.split('\\')[3]
    

    DNAFile = open(nameEug,'r')
    Kmer = DNAFile.readlines()[0]
    DNAFile.close()

    Ks = list(Kmer)

    KmerName = 'K-MersRandomMut/'+test+'/'+type+'/'+Filename
    KmerFile = open('K-MersRandomMut/'+test+'/'+type+'/'+Filename, 'w')

    #Add mutations
    for index in range(0, len(Kmer)):
      base = ["a","c","t","g"]
      if random.randint(0, 100) == 1 and Kmer[index] != " ":
        Ks[index] = base[random.randint(0, 3)]

    #flip order
    # if random.randint(0, 100) == 1:
    #   KsFlip = Ks
    #   for k in range(0,len(Ks)):
    #     Ks[k] = KsFlip[len(Ks)-k-1]
          
    KmerFile.write("".join(Ks))
    KmerFile.close()
    print(f"Printed {KmerName}")