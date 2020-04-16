#!/bin/env bash
for i in {1...10}
do 
    wsk -i action invoke mypython/redis_hail -p url 192.168.66.90 -p id $i
done
