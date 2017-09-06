#!/bin/bash
dias=$(cat dias.txt)
for i in $dias
do
  grep $i "cei_pblh.cca" | awk '-F'$i' ' '{print $2}' > $i".dat"
  echo $i "done"
done
echo "**DONE**"
