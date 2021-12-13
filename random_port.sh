#!/bin/bash

function rand_port(){
    min=$1
    max=$(($2-$min+1))
    num=$(($RANDOM+1000000000)) #增加一个10位的数再求余
    echo $(($num%$max+$min))
}

rnd=$(rand_port 10000 50000)

echo $rnd


# https://cdn.jsdelivr.net/gh/8-diagrams/open_shell/random_port.sh
