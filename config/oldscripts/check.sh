#!/bin/env bash
for i in $(cat old.txt); do
    find -name "*$i*"
    printf "\n"
    find -name "*$i*" -ipath "*20old*" -delete
    printf "\n"
    printf "\n"
done
