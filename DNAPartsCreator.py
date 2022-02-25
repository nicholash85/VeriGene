import random
import glob

#Check for repeated sequences
def checkMatches(DNASequence, currentDNAParts):
  repeated = False
  for files in glob.glob('DNA_Parts/*.txt'):
    fileRepeatCheck = open(files,'r')
    DNACheck = fileRepeatCheck.readlines()
    fileRepeatCheck.close()

    for lines in DNACheck:
      lines.replace('\n', "")
      if DNASequence.lower() == lines.lower(): 
        repeated = True

    for lines in currentDNAParts:
      lines.replace('\n', "")
      if DNASequence.lower() == lines.lower(): 
        repeated = True
    
  return repeated

#Global promoter and terminator arrays
promoterNames = []
terminatorNames = []
AllNames = []
def DNANames(fileName, partnum):
  name = ''
  alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  
  firstChar = alphabet[random.randint(0,len(alphabet)-1)]
  name += firstChar.upper()
  for l in range(1,6):
    name += alphabet[random.randint(0,len(alphabet)-1)]

  for each in AllNames:
    while name == each:
      name = ""
      firstChar = alphabet[random.randint(0,len(alphabet)-1)]
      name += firstChar.upper()
      for l in range(1,6):
        name += alphabet[random.randint(0,len(alphabet)-1)]  

  #promoter and terminator names
  if fileName == "promoter":
    promoterNames.append('p' + name)
    terminatorNames.append(name)
    AllNames.append(name)
    return promoterNames[partnum]
  elif fileName == "terminator":
    if len(terminatorNames)  < partnum:
      print("ERROR: terminator number larger than available promotors")
      return "ERROR"
    else:
      AllNames.append(name)
      return terminatorNames[partnum]
  else:
    AllNames.append(name)
    return name

def createDNAPartSequences(fileName, partNum, minLength, maxLength):
  basePair = ['a','c','t','g']
  Sequences = []
  
  for k in range(0,partNum):
    DNA = ""
    seqLength = random.randint(minLength,maxLength)
    for n in range(0,seqLength):     
      bitNum = random.randint(0,3)
      DNA += basePair[bitNum]

    if k > (4**(maxLength))-1:
      if k == (4**(maxLength)): 
        print("Not possible to produce non-matching sequence for given length")
      break

    a = 0
    while checkMatches(DNA, Sequences) == True:
      print(f"Sequence Matched: {DNA}")
      DNA = ""
      seqLength = random.randint(minLength,maxLength)
      for n in range(0,seqLength):
        bitNum = random.randint(0,3)
        DNA += basePair[bitNum]
      
      a  += 1
      if a > 50:
        print("Can't produce non-matching name")
        break
    
    Sequences.append(DNA)

  file = open('DNA_Parts/' + fileName + '.txt', 'w')
  
  
  for l in range(0,len(Sequences)):
    partName = DNANames(fileName, l)
    file.write(partName + " " + Sequences[l] + '\n')

  file.close()
  print(f"Printed {fileName}.txt\n")

createDNAPartSequences("promoter",2000,70 ,250)
createDNAPartSequences("terminator",2000,50,70)
createDNAPartSequences("scar",500,4,4)
createDNAPartSequences("rbs",500,30,50)
createDNAPartSequences("ribozyme",500,79,79)
createDNAPartSequences("cassette",500,650,1000)
createDNAPartSequences("cds",200,500,700)
