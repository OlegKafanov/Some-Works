#!/bin/bash
while read line
do
#  echo "$line"
python ./search.py "$line"
done < "${1:-/dev/stdin}"

#IFS=$'\n'

