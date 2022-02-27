import glob
from os import read
import sys
import os
import shutil


# Given an entire file string, this function gets the type (folder before) and filename
def getFileValues(nameVerilog):
  print(nameVerilog)
  type = nameVerilog.split('/')[1]
  Filename = nameVerilog.split('/')[2]
  return type, Filename

# This class holds the gates of the verilog file
class VerilogGates:
  def __init__(self,name,output,input,comment):
    self.name = name
    self.input = input[:]
    self.output = output
    self.comment = comment
  # def __init__(self, exist):
  #   self.gate = exist.gate
  #   self.input = exist.input
  #   self.output = exist.output

# This class holds the info from a verilog file
class VerilogInfo:
  def __init__(self,name,output,input,wires,gates):
    self.name = name
    self.output = output[:]
    self.input = input[:]
    self.wires = wires[:]
    self.gates = gates[:]
    
# Reads logic gates from Verilog
def readVerilogGates(nameVerilog):
  VerilogFile = open(nameVerilog,'r')
  Lines = VerilogFile.readlines()
  VerilogFile.close()

  transcode = False
  name = ""
  mode = ''
  inputs = []
  outputs = []
  wires = []
  gates = []
  for k in range(0,len(Lines)):

    #Start of Verilog File
    if Lines[k].split(" ")[0] == "module":
      transcode = True
      line = Lines[k].split("(")
      name = line[0].split(" ")[1]
      line = line[1].split(")")[0]
      line = line.replace(", ", " ")
      for parameter in line.split(" "):
        if parameter == "output":
          mode = "output"
        elif parameter == "input":
          mode = "input"
        else:
          if mode == "output":
            outputs.append(parameter)
          elif mode == "input":
            inputs.append(parameter)


    #End of verilog file
    elif Lines[k].split(" ")[0] == "endmodule":
      transcode = False
      break

    #Verilog code
    elif transcode == True:
      line = Lines[k].split("//")[0]
      if len(Lines[k].split("//")) > 1:
        Comment = "//" + Lines[k].split("//")[1]
        Comment = Comment.split("\n")[0]
      else:
        Comment = ''
      line = line.replace("\t", "")
      line = line.replace("\n","")

      # Get wires
      if line.split(" ")[0] == "wire":
        line = line.replace(", ", " ")
        line = line.replace(";", "")
        for parameter in line.split(" "):
          if parameter != "wire":
            wires.append(parameter)

      #Get gates
      elif len(line)>1:
        line = line.split(")")[0]
        line = line.replace("(",",")
        gateParts = line.split(",")
        if len(gateParts) > 3:
          tempInputs = [gateParts[2],gateParts[3]]
          tempGate = VerilogGates(gateParts[0],gateParts[1],tempInputs, Comment)
        if len(gateParts) == 3:
          tempGate = VerilogGates(gateParts[0],gateParts[1],[gateParts[2]], Comment)
        gates.append(tempGate)
    
  return VerilogInfo(name,outputs,inputs,wires,gates)

#Prints all Verilog values
def debugVerilogRead(Verilog):
  print("\nVerilog File Name: "+Verilog.name)
  print("Verilog Input List: "+Verilog.input)
  print("Verilog Output List: "+Verilog.output)
  print("Verilog Wire List: "+Verilog.wires+"\n")
    
  for k in range(0,len(Verilog.gates)):
    print("\t Verilog gate "+str(k)+": "+Verilog.gates[k].name)
    print("\t Gate "+str(k)+" inputs: "+Verilog.gates[k].input)
    print("\t Gate "+str(k)+" outputs: "+Verilog.gates[k].output)
    print("\t Gate "+str(k)+" comment: "+Verilog.gates[k].comment+"\n")

#Modify Verilog to NOR/NOR Logic
def ConvertNORLogic(Verilog):
  name = Verilog.name + '_NOR'
  input = []
  for i in Verilog.input:
    input.append(i)
  output = []
  for o in Verilog.output:
    output.append(o)
  wires = []
  for w in Verilog.wires:
    wires.append(w)
  gates = []

  for k in range(0,len(Verilog.gates)):

    if Verilog.gates[k].name == "not":
      #Q = NOT( A )	= A NOR A

      # nor(Output,A,A)
      GateName = "nor"
      GateInputs = []
      for GI in Verilog.gates[k].input:
        GateInputs.append(GI)
        GateInputs.append(GI)
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

    elif Verilog.gates[k].name == "nor":
      # Q = A NOR B	= A NOR B 
    
      # nor(Output,A,B)
      GateName = "nor"
      GateInputs = []
      for GI in Verilog.gates[k].input:
        GateInputs.append(GI)
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)
      
    elif Verilog.gates[k].name == "or":
      # Q = A OR B	= ( A NOR B ) NOR ( A NOR B )

      # nor(Wire,A,B)
      GateName = "nor"
      GateInputs = []
      for GI in Verilog.gates[k].input:
        GateInputs.append(GI)
      GateOutputs = []
      norWire = 'NORWire' + str(k)
      GateOutputs.append(norWire)
      wires.append(norWire)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      #nor(Output,Wire,Wire)
      GateName = "nor"
      GateInputs = [norWire, norWire]
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

    elif Verilog.gates[k].name == "and":
      #Q = A AND B	= ( A NOR A ) NOR ( B NOR B )

      # nor(wire1,A,A)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[0],Verilog.gates[k].input[0]]
      norWire1 = 'NORWire' + str(k) + "_1"
      GateOutputs = []
      GateOutputs.append(norWire1)
      wires.append(norWire1)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire2,B,B)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[1],Verilog.gates[k].input[1]]
      norWire2 = 'NORWire' + str(k) + "_2"
      GateOutputs = []
      GateOutputs.append(norWire2)
      wires.append(norWire2)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(output,wire1,wire2)
      GateName = "nor"
      GateInputs = [norWire1, norWire2]
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

    elif Verilog.gates[k].name == "nand":
      # Q = A NAND B	= [ ( A NOR A ) NOR ( B NOR B ) ] NOR [ ( A NOR A ) NOR ( B NOR B ) ]

      # nor(wire1,A,A)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[0],Verilog.gates[k].input[0]]
      norWire1 = 'NORWire' + str(k) + "_1"
      GateOutputs = []
      GateOutputs.append(norWire1)
      wires.append(norWire1)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire2,B,B)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[1],Verilog.gates[k].input[1]]
      norWire2 = 'NORWire' + str(k) + "_2"
      GateOutputs = []
      GateOutputs.append(norWire2)
      wires.append(norWire2)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire3,wire1,wire2)
      GateName = "nor"
      GateInputs = [norWire1, norWire2]
      norWire3 = 'NORWire' + str(k) + "_3"
      GateOutputs = [norWire3]
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(output,wire3,wire3)
      GateName = "nor"
      GateInputs = [norWire3, norWire3]
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

    elif Verilog.gates[k].name == "xnor":
      # Q = A XNOR B	= [ A NOR ( A NOR B ) ] NOR [ B NOR ( A NOR B ) ]

      # nor(wire1,A,B)
      GateName = "nor"
      GateInputs = []
      for GI in Verilog.gates[k].input:
        GateInputs.append(GI)
      GateOutputs = []
      norWire1 = 'NORWire' + str(k) + "_1"
      GateOutputs.append(norWire1)
      wires.append(norWire1)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire2,A,wire1)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[0],norWire1]
      GateOutputs = []
      norWire2 = 'NORWire' + str(k) +"_2"
      GateOutputs.append(norWire2)
      wires.append(norWire2)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire3,B,wire1)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[1],norWire1]
      GateOutputs = []
      norWire3 = 'NORWire' + str(k) +"_3"
      GateOutputs.append(norWire3)
      wires.append(norWire3)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(output,wire2,wire3)
      GateName = "nor"
      GateInputs = [norWire2, norWire3]
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

    elif Verilog.gates[k].name == "xor":
      # Q = A XOR B	= { [ A NOR ( A NOR B ) ] NOR [ B NOR ( A NOR B ) ] } NOR { [ A NOR ( A NOR B ) ] NOR [ B NOR ( A NOR B ) ] }

      # nor(wire1,A,B)
      GateName = "nor"
      GateInputs = []
      for GI in Verilog.gates[k].input:
        GateInputs.append(GI)
      GateOutputs = []
      norWire1 = 'NORWire' + str(k) + "_1"
      GateOutputs.append(norWire1)
      wires.append(norWire1)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire2,A,wire1)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[0],norWire1]
      GateOutputs = []
      norWire2 = 'NORWire' + str(k) +"_2"
      GateOutputs.append(norWire2)
      wires.append(norWire2)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire3,B,wire1)
      GateName = "nor"
      GateInputs = [Verilog.gates[k].input[1],norWire1]
      GateOutputs = []
      norWire3 = 'NORWire' + str(k) +"_3"
      GateOutputs.append(norWire3)
      wires.append(norWire3)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(wire4,wire2,wire3)
      GateName = "nor"
      GateInputs = [norWire2,norWire3]
      GateOutputs = []
      norWire4 = 'NORWire' + str(k) +"_4"
      GateOutputs.append(norWire4)
      wires.append(norWire4)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

      # nor(output,wire4,wire4)
      GateName = "nor"
      GateInputs = [norWire4,norWire4]
      GateOutputs = []
      GateOutputs.append(Verilog.gates[k].output)
      GateComment = Verilog.gates[k].comment
      tempGate = VerilogGates(GateName,GateOutputs,GateInputs,GateComment)
      gates.append(tempGate)

  return VerilogInfo(name,output,input,wires,gates)

def SetNORVerilog(Verilog):

  #Module Line
  temp =  "module "+Verilog.name+"(output "
  for k in range(0,len(Verilog.output)):
    temp += Verilog.output[k]+", "
  temp += "input "
  for k in range(0,len(Verilog.input)):
    if k != len(Verilog.input)-1:
      temp += Verilog.input[k]+", "
    else:
      temp += Verilog.input[k]+");\n"
  
  #wire Line
  temp+= "\twire "
  for k in range(0,len(Verilog.wires)):
    if k != len(Verilog.wires)-1:
      temp += Verilog.wires[k]+", "
    else:
      temp += Verilog.wires[k]+";\n\n"

  #Gates
  for g in range(0,len(Verilog.gates)):
    temp += "\t"+Verilog.gates[g].name+"("+Verilog.gates[g].output[0]+","
    for i in range(0,len(Verilog.gates[g].input)):
      if i != len(Verilog.gates[g].input)-1:
        temp += Verilog.gates[g].input[i]+","
      else:
        temp += Verilog.gates[g].input[i]+"); "+Verilog.gates[g].comment+"\n"

  temp += "endmodule"
  return temp

def WriteVerilog(WrittenVerilog, type, filename, path):
  FullFileName = os.path.join(path, type, filename)
  # print("Writing Uninfected file to {0}.".format(FullFileName))
  with open(os.path.join(sys.path[0],FullFileName),"w+") as f:
    f.write(WrittenVerilog)
    f.close()

def emptyDirectories(FilePath):
  #Empty Directories
  folder = os.path.join(sys.path[0], FilePath + '/Uninfected')
  for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

  # folder = os.path.join(sys.path[0], FilePath + '/Infected')
  # for filename in os.listdir(folder):
  #     file_path = os.path.join(folder, filename)
  #     try:
  #         if os.path.isfile(file_path) or os.path.islink(file_path):
  #             os.unlink(file_path)
  #         elif os.path.isdir(file_path):
  #             shutil.rmtree(file_path)
  #     except Exception as e:
  #         print('Failed to delete %s. Reason: %s' % (file_path, e))

  print(FilePath+" emptied.")




#Empty Directories
emptyDirectories('NORVerilog')
# Loop through Verilog files
print("Working")
for name in ('Verilog/Uninfected/',''):  
  for nameVerilog in os.listdir(name):
    # print file being processed
    print("\n"+nameVerilog)

    # Get file parameters
    type, Filename = getFileValues(nameVerilog)

    Verilog = readVerilogGates(nameVerilog)
    #debugVerilogRead(Verilog)

    VerilogNOR = ConvertNORLogic(Verilog)
    #debugVerilogRead(VerilogNOR)
    WholeVerilog = SetNORVerilog(VerilogNOR)
    #print(WholeVerilog)
    WriteVerilog(WholeVerilog,type,VerilogNOR.name + '.v','NORVerilog')    

    

    

    





    







