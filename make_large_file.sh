#!/bin/bash
cp moby-dic.txt large_file.txt

for i in {1..9}
do
    echo "Duplication #$i"
    cat large_file.txt large_file.txt > tmp
    mv tmp large_file.txt
done

