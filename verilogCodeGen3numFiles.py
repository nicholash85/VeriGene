"""
#######################################
Generates gate-level for given number of inputs/outputs
Generates infected version of code with fault injection and info leaking

modified by Nicholas Haehn
"""
import random
import os
import sys
import shutil

NumFiles = int(input("Enter the max number of files you want: ")) # 10 #65536 max
fileCount = 0
numInputsMin = int(input("Enter the min number of inputs (18 available, suggested 8 or less): "))#8
numInputsMax = int(input("Enter the max number of inputs (18 available, suggested 8 or less): "))#8
numOutputsMax = int(input("Enter the max number of outputs (7 available, suggested 3. Save at least one for info leaking trojan): "))#3
numGatesMax = int(input("Enter the number of internal gates (suggested 8 max, must be larger than number of outputs): ")) #8
numRepeats = int(input("Enter the number of repeats: ")) #4

# alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# wires = ['wire1','wire2','wire3','wire4','wire5','wire6','wire7','wire8']
possibleGates = ['and', 'or', 'nor', 'nand', 'xor', 'xnor']
# if numFiles > (2 ^ (2 ^ ))

# print("Deleting Files")
#Empty Directories
# folder = os.path.join(sys.path[0],'Verilog2/Uninfected')
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))

# print("Deleted Uninfected Files")
# folder = os.path.join(sys.path[0],'Verilog2/Infected')
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     #print(f"{file_path}")
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))

# print("Deleted Infected Files")

num =0 
#Generate Files
# for inNum in range(numInputsMin, numInputsMax + 1): #MaxInputs
for inNum in [2,4,8,16,32,64]: #MaxInputs
    for outNum in range(1, numOutputsMax + 1): #MaxOutputs
        for numGates in range(outNum,numGatesMax):
            for repeat in range(0,numRepeats):
                num +=1

print(f"{num} files will be made with this input combo")

                

            

# for num in range(100): #65536
#     filename = f"C:/Cello-v2-develop/input/uninfected_verilog_files/temp/temp/comb_logic_in4_out1_{str(num)}.v"
#     res = [int(i) for i in list('{0:016b}'.format(num))]
#     #print(res)
#     with open(filename,"w+") as f:
#         temp =  f"module comb_logic_{str(num)}(input a, b, c, d, output e, f);\n\n"
#         temp += f"always@(a,b,c,d)\n"
#         temp += f"\tbegin\n"
#         temp += f"\tcase({{a,b,c,d}})\n"
#         temp += f"\t\t4'b0000:  e = 1'b{res[0]};\n"
#         temp += f"\t\t4'b0001:  e = 1'b{res[1]};\n"
#         temp += f"\t\t4'b0010:  e = 1'b{res[2]};\n"
#         temp += f"\t\t4'b0011:  e = 1'b{res[3]};\n"
#         temp += f"\t\t4'b0100:  e = 1'b{res[4]};\n"
#         temp += f"\t\t4'b0101:  e = 1'b{res[5]};\n"
#         temp += f"\t\t4'b0110:  e = 1'b{res[6]};\n"
#         temp += f"\t\t4'b0111:  e = 1'b{res[7]};\n"
#         temp += f"\t\t4'b1000:  e = 1'b{res[8]};\n"
#         temp += f"\t\t4'b1001:  e = 1'b{res[9]};\n"
#         temp += f"\t\t4'b1010:  e = 1'b{res[10]};\n"
#         temp += f"\t\t4'b1011:  e = 1'b{res[11]};\n"
#         temp += f"\t\t4'b1100:  e = 1'b{res[12]};\n"
#         temp += f"\t\t4'b1101:  e = 1'b{res[13]};\n"
#         temp += f"\t\t4'b1110:  e = 1'b{res[14]};\n"
#         temp += f"\t\t4'b1111:  e = 1'b{res[15]};\n"
#         temp += f"\tendcase\n"
#         temp += f"\tend\n"
#         temp += f"endmodule"

#         f.write(temp)