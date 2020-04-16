#!/bin/env bash
for i in {1..10}
do
    wsk -i action invoke mypython/couchdb_init_hail -p url http://admin:iam123@192.168.66.90:5984 -p _id $i
done
