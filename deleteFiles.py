import os 
import sys
import shutil

def emptyDirectories(FilePath):
  #Empty Directories
  folder = os.path.join(sys.path[0], FilePath)
  for filename in os.listdir(folder):
    folder2 = os.path.join(folder, filename)
    for filename2 in os.listdir(folder2):
      file_path = os.path.join(folder2, filename2)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

  print(f"{FilePath} emptied.")

def emptyDirectories2(FilePath):
  #Empty Directories
  folder = os.path.join(sys.path[0], FilePath)
  for filename in os.listdir(folder):
    folder2 = os.path.join(folder, filename)
    for filename2 in os.listdir(folder2):
      folder3 = os.path.join(folder2, filename2)
      for filename3 in os.listdir(folder3):
        file_path = os.path.join(folder3, filename3)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

  print(f"{FilePath} emptied.")

input = input("Are you sure you want to delete files?(Y/N)")
if input=="Y":
  emptyDirectories('DNA_Custom_OLD2')
  emptyDirectories2('K-MersRandom')
  emptyDirectories2('K-MersRandom_Custom')
  emptyDirectories2('K-MersRandom_Custom_NOR')
  emptyDirectories2('K-MersRandomMut')
  emptyDirectories2('K-MersRandomMut_custom')
  emptyDirectories2('K-MersRandomMut_custom_NOR')


