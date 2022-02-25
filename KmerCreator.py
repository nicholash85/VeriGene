import os
import glob

os.chdir('./Cello_Hardware_Trojans')
for name in glob.glob('DNA/**/**/'):
  for nameEug in glob.glob(name + '/*.txt'):
    print(nameEug)
    test = nameEug.split('\\')[1]
    type = nameEug.split('\\')[2]
    Filename = nameEug.split('\\')[3]
    DNAFile = open(nameEug,'r')
    KmerFile = open('K-Mers/'+test+'/'+type+'/'+Filename, 'w')
    DNA = DNAFile.readlines()[0]
    Kmer = ''
    for k in range(len(DNA)-5):
      Kmer = Kmer + DNA[k:k+6] + ' '

    KmerFile.write(Kmer)
    DNAFile.close()
    KmerFile.close()