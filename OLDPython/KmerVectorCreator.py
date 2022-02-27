# Creates a list of all possible vectors to be read

num = 0
VectorList = []

for ones in ['a','c','t','g']:
  for twos in ['a','c','t','g']:
    for threes in ['a','c','t','g']:
      for fours in ['a','c','t','g']:
        for fives in ['a','c','t','g']:
          for sixes in ['a','c','t','g']:
            DNAWord = ones+twos+threes+fours+fives+sixes
            VectorList.append(DNAWord)


file = open('DNA_Parts/' + 'KmerVectorList.txt', 'w')
for l in range(0,len(VectorList)):
  file.write(str(l) + " " + VectorList[l] + '\n')

file.close()
print(f"Printed KmerVectorList.txt\n")