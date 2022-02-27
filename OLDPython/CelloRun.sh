#!/bin/bash
# set the STRING variable
date > failed.txt
date > logInf.txt
STRING="Running Cello for all Files"
# print the contents of the variable on screen
echo $STRING
# 9/3/21 3:43 pm

let "NumRun = 0"
let "NumRunSuccess = 0"
let "n = 0"

for filesSucceed in Eugene/Infected/*.eug; do
  let "NumRunSuccess += 1"
done

for files in Verilog/Infected/*.v; do
  fileRun=false
  # docker run --rm -i -v /C/Users/haehn/OneDrive/Documents/University_of_Cincinnati/Protege_-_MIND_Lab/Projects/TensorFlow/Verilog:/root/input -v /C/Users/haehn/OneDrive/Documents/University_of_Cincinnati/Protege_-_MIND_Lab/Projects/TensorFlow/Bash_Outputs/Uninfected/Out$n:/root/output -t cidarlab/cello-dnacompiler:latest java -classpath /root/app.jar org.cellocad.v2.DNACompiler.runtime.Main -inputNetlist /root/input/"$files" -options root/input/options.csv -userConstraintsFile /root/input/Eco1C1G1T1_3.UCF.json -inputSensorFile /root/input/Eco1C1G1T1.input2.json -outputDeviceFile /root/input/Eco1C1G1T1.output2.json -pythonEnv python -outputDir root/output  
  # docker run --rm -i -v /C/Users/haehn/OneDrive/Documents/University_of_Cincinnati/Protege_-_MIND_Lab/Projects/TensorFlow/Verilog:/root/input -v /C/Users/haehn/OneDrive/Documents/University_of_Cincinnati/Protege_-_MIND_Lab/Projects/TensorFlow/Bash_Outputs/Uninfected:/root/output -t cidarlab/cello-dnacompiler:latest java -classpath /root/app.jar org.cellocad.v2.DNACompiler.runtime.Main -inputNetlist /root/input/Uninfected/comb_logic4.v -options /root/input/options.csv -userConstraintsFile /root/input/Eco1C1G1T1_2.UCF.json -inputSensorFile /root/input/Eco1C1G1T1.input2.json -outputDeviceFile /root/input/Eco1C1G1T1.output2.json -pythonEnv python -outputDir /root/output
  echo "$files" >> logInf.txt
  echo "Running file: $files"
  
  fileRunFile="filesRunInf.txt"
  while read lineRun; do
    #  reading each line
    if [ $lineRun = $files ] ;
    then
      fileRun=true
    fi
  done < $fileRunFile

  if [ "$fileRun" = false ] ;
  then
    runFile="$files"
    echo "$runFile" >> filesRunInf.txt
    IFS='/' read -a fileArray <<< "$files"
    IFS='.' read -a fileBase <<< "${fileArray[2]}"

    docker run --ulimit cpu=600 --rm -i -v ~/Cello/Cello_Hardware_Trojans2:/root/input -v ~/Cello/Bash_Outputs:/root/output -t cidarlab/cello-dnacompiler:latest java -classpath /root/app.jar org.cellocad.v2.DNACompiler.runtime.Main -inputNetlist root/input/"$files" -options /root/input/Verilog/options.csv -userConstraintsFile /root/input/Verilog/Eco1C1G1T1_2.UCF.json -inputSensorFile /root/input/Verilog/Eco1C1G1T1.input2.json -outputDeviceFile /root/input/Verilog/Eco1C1G1T1.output2.json -pythonEnv python -outputDir /root/output/"${fileArray[1]}"/"${fileBase[0]}" > internlogInf.txt
    filename="internlogInf.txt"

    failed=true
    while read line; do
      #  reading each line
      IFS=' '
      echo "$line" >> logInf.txt

      read -a strarr <<< "$line"
      len=${#strarr[@]}
      lenmax=5
      if [ $len -gt $lenmax ];
      then
        if [[ ${strarr[3]} == *"Eugene"* ]] && [[ ${strarr[5]} == *"running"* ]] && [[ ${strarr[6]} == *"Eugene"* ]] ;
        then
          failed=false
        fi
      fi
    done < "$filename"

    if [ "$failed" = true ];
    then
      STRING="Failed on first Run. Quitting."
      echo $STRING
      # docker run --ulimit cpu=600 --rm -i -v ~/Cello/Cello_Hardware_Trojans:/root/input -v ~/Cello/Cello_Hardware_Trojans/Bash_Outputs:/root/output -t cidarlab/cello-dnacompiler:latest java -classpath /root/app.jar org.cellocad.v2.DNACompiler.runtime.Main -inputNetlist root/input/"$files" -options /root/input/Verilog/options.csv -userConstraintsFile /root/input/Verilog/Eco1C1G1T1_2.UCF.json -inputSensorFile /root/input/Verilog/Eco1C1G1T1.input2.json -outputDeviceFile /root/input/Verilog/Eco1C1G1T1.output2.json -pythonEnv python -outputDir /root/output/"${fileArray[1]}"/"${fileBase[0]}" > internlog.txt
      # filename="internlog.txt"
      # while read line; do
      #   IFS=' '
      #   echo "$line" >> log.txt
      #   read -a strarr <<< "$line"
      #   len=${#strarr[@]}
      #   lenmax=5
      #   if [ $len -gt $lenmax ];
      #   then
      #     if [[ ${strarr[3]} == *"Eugene"* ]] && [[ ${strarr[5]} == *"running"* ]] && [[ ${strarr[6]} == *"Eugene"* ]] ;
      #     then
      #       failed=false
      #     fi
      #   fi
      # done < "$filename"

      
      failedFile="$files"
      echo "$failedFile" >> failed.txt
      #   echo "Failed Second Time. Quitting this file."
      # else
      #   cp ~/Cello/Cello_Hardware_Trojans/Bash_Outputs/"${fileArray[1]}"/"${fileBase[0]}"/"${fileBase[0]}_eugeneScript.eug" ~/Cello/Cello_Hardware_Trojans/Eugene/"${fileArray[1]}"
      # fi
    else
      cp ~/Cello/Bash_Outputs/"${fileArray[1]}"/"${fileBase[0]}"/"${fileBase[0]}_eugeneScript.eug" ~/Cello/Cello_Hardware_Trojans2/Eugene/"${fileArray[1]}"
      STRING2="Success!"
      echo $STRING2
      let "NumRunSuccess += 1"
    
    fi
  else
    STRING3="File Already Run"
    echo $STRING3
  fi
  let "NumRun += 1"

  echo "$NumRun files completed"
  echo "$NumRunSuccess files succeeded"
  echo ""
  let "n+=1"
done



# docker run --rm -i -v /C/Cello-v2-develop/input:/root/input -v /C/Cello-v2-develop/output/Network/Network13:/root/output -t cidarlab/cello-dnacompiler:latest java -classpath /root/app.jar org.cellocad.v2.DNACompiler.runtime.Main -inputNetlist /root/input/uninfected_verilog_files/comb_logic4.v -options /root/input/options.csv -userConstraintsFile /root/input/Eco1C1G1T1_3.UCF.json -inputSensorFile /root/input/Eco1C1G1T1.input2.json -outputDeviceFile /root/input/Eco1C1G1T1.output2.json -pythonEnv python -outputDir /root/output
