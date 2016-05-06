#!/bin/bash -xe

gsutil -m rsync -rd scripts gs://recommender/scripts
gsutil -m rsync -rd config/hadoop gs://recommender/config/hadoop 
