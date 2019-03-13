#!/bin/bash
 
UUID=$(cat /proc/sys/kernel/random/uuid)
UUID=${UUID//-/}
#echo $UUID
t=`date +%s`
t_str=`printf "%X\n" $t`
echo $UUID$t_str

shang="68656c6c6f20e5a4a7e6a392e5aea2e4b8bae6ada6e6b189e58aa0e6b2b9"
lenth=`expr length $shang`
printstr=""
string=$shang
for (( i = 0; i < $lenth/2; i++)); do
    tmp='\x'${string:$(($i*2)):2}
    printstr=$printstr$tmp
done

echo -en "$printstr"
echo "A."
echo "B"
