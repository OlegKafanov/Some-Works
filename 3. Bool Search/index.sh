#!/bin/sh
python ./coding.py $1
#param="varbyte"
#if [ "$1" = "$param" ]
#then 
shift
python ./index.py $*
#echo "1" $*
#else
#shift
#python ./index_sim9.py 
#echo "2" $*
#fi
