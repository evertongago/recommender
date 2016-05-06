#!/bin/bash -xe

dsopz login-gce

cat /root/data/recommendation_list.data | awk '{printf "{\"properties\": {\"user_id\": {\"indexed\": true, \"integerValue\": %s}, \"content_id\": {\"indexed\": false, \"stringValue\": %s}, \"rate\": {\"indexed\": true, \"doubleValue\": %s}}, \"key\": { \"path\": [{\"kind\": \"RecommendationContent\", \"name\": \"%s\"}]}}\n", $2, $3, $4, $1}' | dsopz import -d gadsense-1218 -o upsert
