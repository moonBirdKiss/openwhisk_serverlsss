#!/bin/env bash
for i in {1..10}
do
    curl -X PUT http://admin:iam123@192.168.66.90:5984/hail_num/{$i} -d '{"_id":"{$i}", "data":1048576}'
done
